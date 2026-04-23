"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Brain,
  Download,
  Loader2,
  TrendingUp,
} from "lucide-react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import ScoreRadar from "@/components/report/ScoreRadar";
import DimensionCard from "@/components/report/DimensionCard";
import PaywallOverlay from "@/components/report/PaywallOverlay";
import { api } from "@/lib/api";
import { getLevelColor } from "@/lib/utils";
import type { ReportData, TeaserContent, ReportContent } from "@/types/report";

export default function ReportPage() {
  const params = useParams();
  const router = useRouter();
  const reportId = params.reportId as string;

  const [report, setReport] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [error, setError] = useState("");

  const loadReport = useCallback(async () => {
    try {
      const data = await api.getReport(reportId);
      setReport(data);

      // If still generating, poll
      if (data.status === "generating" || data.status === "pending") {
        setTimeout(() => loadReport(), 3000);
      } else {
        setLoading(false);
      }
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  }, [reportId]);

  useEffect(() => {
    loadReport();
  }, [loadReport]);

  async function handleUnlock() {
    setCheckoutLoading(true);
    try {
      const result = await api.createCheckout(reportId, "");
      window.location.href = result.checkout_url;
    } catch (err: any) {
      setError(err.message);
      setCheckoutLoading(false);
    }
  }

  if (loading || !report) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            Generating Your Report
          </h2>
          <p className="text-gray-500">
            Our AI is analyzing your responses. This takes about 15 seconds...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center px-6">
        <Card className="max-w-md text-center" padding="lg">
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            Something went wrong
          </h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </Card>
      </div>
    );
  }

  const content = report.report_content as TeaserContent | ReportContent | null;
  const isUnlocked = report.is_unlocked;
  const overallLevel =
    content && "executive_summary" in content
      ? content.executive_summary.overall_assessment
      : "Emerging";

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      {/* Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-full text-sm font-medium text-blue-700 mb-4">
          <Brain className="w-4 h-4" />
          AI Readiness Assessment Report
        </div>
        <h1 className="text-3xl font-extrabold text-gray-900 mb-3">
          Your AI Readiness Score
        </h1>
        <div className="flex items-center justify-center gap-3">
          <span
            className={`text-6xl font-extrabold ${getLevelColor(overallLevel)}`}
          >
            {report.score_overall}
          </span>
          <span className="text-2xl text-gray-400 font-light">/100</span>
        </div>
        <Badge
          variant={
            overallLevel === "Advanced"
              ? "success"
              : overallLevel === "Established"
              ? "info"
              : overallLevel === "Emerging"
              ? "warning"
              : "danger"
          }
          className="mt-2"
        >
          {overallLevel}
        </Badge>
      </div>

      {/* Executive Summary */}
      {content && "executive_summary" in content && (
        <Card className="mb-8" padding="lg">
          <h2 className="text-lg font-bold text-gray-900 mb-1">
            {content.executive_summary.headline}
          </h2>
          <p className="text-gray-600 leading-relaxed whitespace-pre-line">
            {content.executive_summary.summary}
          </p>
          <div className="mt-4 p-4 bg-blue-50 rounded-xl">
            <p className="text-sm font-semibold text-blue-800">
              <TrendingUp className="w-4 h-4 inline mr-1" />
              Key Finding:
            </p>
            <p className="text-sm text-blue-700 mt-1">
              {content.executive_summary.key_finding}
            </p>
          </div>
        </Card>
      )}

      {/* Radar Chart */}
      <Card className="mb-8" padding="lg">
        <h2 className="text-lg font-bold text-gray-900 mb-4 text-center">
          Score Breakdown
        </h2>
        <ScoreRadar
          scores={{
            data_readiness: report.score_data_readiness,
            process_maturity: report.score_process_maturity,
            tech_infrastructure: report.score_tech_infrastructure,
            team_capability: report.score_team_capability,
            strategic_alignment: report.score_strategic_alignment,
          }}
        />
      </Card>

      {/* Dimension Cards */}
      {content && "dimension_analysis" in content && (
        <div className="space-y-4 mb-8">
          <h2 className="text-lg font-bold text-gray-900">
            Dimension Analysis
          </h2>
          <div className="grid gap-4">
            {content.dimension_analysis.map((dim) => (
              <DimensionCard
                key={dim.dimension}
                dimension={dim}
                showDetails={isUnlocked}
              />
            ))}
          </div>
        </div>
      )}

      {/* Paywall or Full Content */}
      {!isUnlocked ? (
        <div className="mb-8">
          <PaywallOverlay onUnlock={handleUnlock} loading={checkoutLoading} />
        </div>
      ) : (
        <>
          {/* Opportunity Zones */}
          {content && "opportunity_zones" in content && (
            <Card className="mb-8" padding="lg">
              <h2 className="text-lg font-bold text-gray-900 mb-4">
                Opportunity Zones
              </h2>
              <div className="space-y-4">
                {(content as ReportContent).opportunity_zones.map((oz, i) => (
                  <div
                    key={i}
                    className="border border-gray-100 rounded-xl p-5"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-bold text-gray-900">{oz.title}</h3>
                      <div className="flex gap-1.5">
                        <Badge
                          variant={
                            oz.impact === "high" ? "success" : oz.impact === "medium" ? "info" : "default"
                          }
                        >
                          {oz.impact} impact
                        </Badge>
                        <Badge
                          variant={
                            oz.effort === "low" ? "success" : oz.effort === "medium" ? "warning" : "danger"
                          }
                        >
                          {oz.effort} effort
                        </Badge>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">
                      {oz.description}
                    </p>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Timeline:</span>{" "}
                        <span className="font-medium">{oz.timeline}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Est. ROI:</span>{" "}
                        <span className="font-medium">{oz.estimated_roi}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Implementation Roadmap */}
          {content && "implementation_roadmap" in content && (
            <Card className="mb-8" padding="lg">
              <h2 className="text-lg font-bold text-gray-900 mb-4">
                Implementation Roadmap
              </h2>
              {[
                { key: "phase_1_quick_wins", label: "Phase 1: Quick Wins", color: "emerald" },
                { key: "phase_2_foundation", label: "Phase 2: Foundation", color: "blue" },
                { key: "phase_3_scale", label: "Phase 3: Scale", color: "violet" },
              ].map(({ key, label, color }) => {
                const phase = (content as ReportContent).implementation_roadmap[
                  key as keyof ReportContent["implementation_roadmap"]
                ];
                return (
                  <div key={key} className="mb-6 last:mb-0">
                    <div className="flex items-center gap-2 mb-2">
                      <div className={`w-2.5 h-2.5 rounded-full bg-${color}-500`} />
                      <h3 className="font-bold text-gray-900">{label}</h3>
                      <span className="text-xs text-gray-500">
                        ({phase.timeline})
                      </span>
                    </div>
                    <ul className="ml-5 space-y-1">
                      {phase.initiatives.map((item, i) => (
                        <li key={i} className="text-sm text-gray-700">
                          {item}
                        </li>
                      ))}
                    </ul>
                    <p className="text-xs text-gray-500 mt-1 ml-5">
                      Investment: {phase.estimated_investment}
                    </p>
                  </div>
                );
              })}
            </Card>
          )}

          {/* Next Steps */}
          {content && "next_steps" in content && (
            <Card className="mb-8" padding="lg">
              <h2 className="text-lg font-bold text-gray-900 mb-4">
                Your Next Steps
              </h2>
              <ol className="space-y-3">
                {(content as ReportContent).next_steps.map((step, i) => (
                  <li key={i} className="flex gap-3">
                    <span className="w-7 h-7 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                      {i + 1}
                    </span>
                    <span className="text-gray-700 text-sm pt-1">{step}</span>
                  </li>
                ))}
              </ol>
            </Card>
          )}

          {/* Download */}
          <div className="text-center">
            <Button variant="secondary" size="lg">
              <Download className="mr-2 w-5 h-5" />
              Download PDF Report
            </Button>
          </div>
        </>
      )}

      {/* Teaser opportunity preview for non-unlocked */}
      {!isUnlocked && content && "opportunity_zones_preview" in content && (
        <Card className="mb-8" padding="lg">
          <h2 className="text-lg font-bold text-gray-900 mb-2">
            Opportunity Zones Preview
          </h2>
          <p className="text-sm text-gray-500 mb-4">
            {(content as TeaserContent).opportunity_zones_count} opportunities
            identified. Showing 2 of{" "}
            {(content as TeaserContent).opportunity_zones_count}.
          </p>
          <div className="space-y-3">
            {(content as TeaserContent).opportunity_zones_preview.map(
              (oz, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between p-4 border border-gray-100 rounded-xl"
                >
                  <span className="font-medium text-gray-900">{oz.title}</span>
                  <div className="flex gap-1.5">
                    <Badge
                      variant={oz.impact === "high" ? "success" : "info"}
                    >
                      {oz.impact} impact
                    </Badge>
                    <Badge
                      variant={oz.effort === "low" ? "success" : "warning"}
                    >
                      {oz.effort} effort
                    </Badge>
                  </div>
                </div>
              )
            )}
          </div>
        </Card>
      )}
    </div>
  );
}
