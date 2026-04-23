import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  Brain,
  Clock,
  FileText,
  Shield,
  Zap,
} from "lucide-react";
import Button from "@/components/ui/Button";

export default function Home() {
  return (
    <div className="bg-white">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-violet-50" />
        <div className="relative max-w-6xl mx-auto px-6 pt-20 pb-24">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-full text-sm font-medium text-blue-700 mb-8">
              <Zap className="w-4 h-4" />
              Free AI Readiness Score
            </div>
            <h1 className="text-5xl sm:text-6xl font-extrabold text-gray-900 tracking-tight leading-[1.1] mb-6">
              Is Your Business{" "}
              <span className="bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent">
                Ready for AI?
              </span>
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed mb-10 max-w-2xl mx-auto">
              4 minutes. 15 questions. Get a personalized AI readiness report
              with your score across 5 critical dimensions, opportunity zones,
              and an implementation roadmap.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/assess">
                <Button size="lg" className="group">
                  Start Free Assessment
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-0.5 transition-transform" />
                </Button>
              </Link>
              <p className="text-sm text-gray-500">
                No signup required &middot; Results in 4 minutes
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
            How It Works
          </h2>
          <p className="text-gray-600 text-center mb-16 max-w-2xl mx-auto">
            A structured assessment designed by AI strategy experts to evaluate
            your organization across five critical dimensions.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: FileText,
                title: "Answer 15 Questions",
                desc: "Quick, multiple-choice questions about your data, processes, technology, team, and strategy.",
              },
              {
                icon: Brain,
                title: "AI Analyzes Your Responses",
                desc: "Our AI engine scores you across 5 dimensions and benchmarks against your industry peers.",
              },
              {
                icon: BarChart3,
                title: "Get Your Report",
                desc: "Receive a detailed report with scores, opportunity zones, ROI estimates, and an action plan.",
              },
            ].map((step, i) => (
              <div
                key={i}
                className="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm text-center"
              >
                <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-violet-100 rounded-2xl flex items-center justify-center mx-auto mb-5">
                  <step.icon className="w-7 h-7 text-blue-600" />
                </div>
                <div className="text-sm font-semibold text-blue-600 mb-2">
                  Step {i + 1}
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {step.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5 Dimensions */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
            5 Dimensions of AI Readiness
          </h2>
          <p className="text-gray-600 text-center mb-16 max-w-2xl mx-auto">
            Each dimension is scored 0-100 and categorized into maturity levels.
          </p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {[
              { name: "Data Readiness", color: "from-blue-500 to-blue-600" },
              { name: "Process Maturity", color: "from-violet-500 to-violet-600" },
              { name: "Tech Infrastructure", color: "from-cyan-500 to-cyan-600" },
              { name: "Team Capability", color: "from-emerald-500 to-emerald-600" },
              { name: "Strategic Alignment", color: "from-amber-500 to-amber-600" },
            ].map((dim) => (
              <div
                key={dim.name}
                className="bg-gray-50 rounded-xl p-5 text-center border border-gray-100"
              >
                <div
                  className={`w-3 h-3 rounded-full bg-gradient-to-r ${dim.color} mx-auto mb-3`}
                />
                <span className="text-sm font-semibold text-gray-800">
                  {dim.name}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-8 text-gray-400">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5" />
              <span className="text-sm font-medium">256-bit Encryption</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              <span className="text-sm font-medium">4 Minute Assessment</span>
            </div>
            <div className="flex items-center gap-2">
              <Brain className="w-5 h-5" />
              <span className="text-sm font-medium">AI-Powered Analysis</span>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-br from-blue-600 to-violet-600">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Discover Your AI Potential?
          </h2>
          <p className="text-blue-100 text-lg mb-8">
            Join hundreds of businesses that have used AuditIQ to chart their AI
            journey.
          </p>
          <Link href="/assess">
            <Button
              size="lg"
              className="bg-white text-blue-600 hover:bg-gray-50 shadow-xl group"
            >
              Start Your Free Assessment
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-0.5 transition-transform" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
