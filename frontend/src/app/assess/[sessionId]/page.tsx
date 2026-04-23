"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ArrowRight, Mail, Send } from "lucide-react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import ProgressBar from "@/components/layout/ProgressBar";
import { api } from "@/lib/api";
import { getDimensionLabel } from "@/lib/utils";
import type { Question, ProgressInfo } from "@/types/assessment";

type Phase = "questions" | "email" | "generating";

export default function QuestionnairePage() {
  const params = useParams();
  const router = useRouter();
  const sessionToken = params.sessionId as string;

  const [phase, setPhase] = useState<Phase>("questions");
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string>("");
  const [progress, setProgress] = useState<ProgressInfo>({
    answered: 0,
    total: 15,
    percent: 0,
  });
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState("");

  const loadQuestion = useCallback(async () => {
    try {
      const question = await api.getNextQuestion(sessionToken);
      if (!question) {
        setPhase("email");
      } else {
        setCurrentQuestion(question);
        setSelectedAnswer("");
      }
    } catch (err: any) {
      setError(err.message);
    }
  }, [sessionToken]);

  useEffect(() => {
    async function init() {
      try {
        const status = await api.getAssessment(sessionToken);
        setProgress(status.progress);
        if (status.status === "completed") {
          setPhase("email");
          return;
        }
        await loadQuestion();
      } catch (err: any) {
        setError(err.message);
      } finally {
        setInitialLoading(false);
      }
    }
    init();
  }, [sessionToken, loadQuestion]);

  async function handleSubmitAnswer() {
    if (!currentQuestion || !selectedAnswer) return;
    setLoading(true);
    setError("");

    try {
      const result = await api.submitResponse(sessionToken, {
        question_id: currentQuestion.id,
        answer_value: selectedAnswer,
      });

      setProgress(result.progress);

      if (result.next_question) {
        setCurrentQuestion(result.next_question);
        setSelectedAnswer("");
      } else {
        setPhase("email");
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleComplete() {
    if (!email) {
      setError("Please enter your email to receive your report");
      return;
    }
    setLoading(true);
    setError("");

    try {
      const result = await api.completeAssessment(sessionToken, email);

      // Trigger report generation
      await api.triggerGeneration(result.report_id);

      // Redirect to report page
      router.push(`/report/${result.report_id}`);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  }

  if (initialLoading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading assessment...</div>
      </div>
    );
  }

  return (
    <div className="min-h-[80vh] flex flex-col items-center py-8 px-6">
      <div className="w-full max-w-2xl">
        {/* Progress */}
        <div className="mb-8">
          <ProgressBar
            percent={progress.percent}
            answered={progress.answered}
            total={progress.total}
          />
        </div>

        {/* Question Phase */}
        {phase === "questions" && currentQuestion && (
          <Card padding="lg" className="animate-in fade-in duration-300">
            <div className="mb-6">
              <span className="inline-block text-xs font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full mb-4">
                {getDimensionLabel(currentQuestion.dimension)}
              </span>
              <h2 className="text-xl font-bold text-gray-900 leading-relaxed">
                {currentQuestion.question_text}
              </h2>
              {currentQuestion.help_text && (
                <p className="text-sm text-gray-500 mt-2">
                  {currentQuestion.help_text}
                </p>
              )}
            </div>

            <div className="space-y-3 mb-8">
              {currentQuestion.options?.map((option) => (
                <button
                  key={option.value}
                  onClick={() => setSelectedAnswer(option.value)}
                  className={`w-full text-left px-5 py-4 rounded-xl border-2 transition-all duration-200 ${
                    selectedAnswer === option.value
                      ? "border-blue-500 bg-blue-50 shadow-sm"
                      : "border-gray-100 bg-white hover:border-gray-200 hover:bg-gray-50"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-5 h-5 rounded-full border-2 mt-0.5 flex-shrink-0 flex items-center justify-center transition-all ${
                        selectedAnswer === option.value
                          ? "border-blue-500 bg-blue-500"
                          : "border-gray-300"
                      }`}
                    >
                      {selectedAnswer === option.value && (
                        <div className="w-2 h-2 rounded-full bg-white" />
                      )}
                    </div>
                    <span
                      className={`text-sm leading-relaxed ${
                        selectedAnswer === option.value
                          ? "text-blue-900 font-medium"
                          : "text-gray-700"
                      }`}
                    >
                      {option.label}
                    </span>
                  </div>
                </button>
              ))}
            </div>

            {error && (
              <p className="text-sm text-red-600 bg-red-50 px-4 py-2 rounded-lg mb-4">
                {error}
              </p>
            )}

            <div className="flex justify-end">
              <Button
                onClick={handleSubmitAnswer}
                disabled={!selectedAnswer}
                loading={loading}
                className="group"
              >
                Next
                <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Button>
            </div>
          </Card>
        )}

        {/* Email Capture Phase */}
        {phase === "email" && (
          <Card padding="lg" className="animate-in fade-in duration-300">
            <div className="text-center mb-8">
              <div className="w-14 h-14 bg-gradient-to-br from-emerald-100 to-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Mail className="w-7 h-7 text-emerald-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Almost There!
              </h2>
              <p className="text-gray-600">
                Enter your email to receive your personalized AI Readiness Report.
              </p>
            </div>

            <div className="space-y-4">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                onKeyDown={(e) => e.key === "Enter" && handleComplete()}
              />

              {error && (
                <p className="text-sm text-red-600 bg-red-50 px-4 py-2 rounded-lg">
                  {error}
                </p>
              )}

              <Button
                onClick={handleComplete}
                loading={loading}
                className="w-full group"
                size="lg"
              >
                Generate My Report
                <Send className="ml-2 w-5 h-5 group-hover:translate-x-0.5 transition-transform" />
              </Button>

              <p className="text-xs text-gray-400 text-center">
                We&apos;ll email your report. No spam, ever.
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
