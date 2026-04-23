import Badge from "@/components/ui/Badge";
import { getLevelColor, getLevelBg } from "@/lib/utils";
import type { DimensionAnalysis } from "@/types/report";

interface DimensionCardProps {
  dimension: DimensionAnalysis;
  showDetails: boolean;
}

export default function DimensionCard({
  dimension,
  showDetails,
}: DimensionCardProps) {
  const levelVariant =
    dimension.level === "Advanced"
      ? "success"
      : dimension.level === "Established"
      ? "info"
      : dimension.level === "Emerging"
      ? "warning"
      : "danger";

  return (
    <div className={`rounded-xl border p-6 ${getLevelBg(dimension.level)}`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-bold text-gray-900">{dimension.title}</h3>
          <Badge variant={levelVariant} className="mt-1">
            {dimension.level}
          </Badge>
        </div>
        <div className="text-right">
          <div className={`text-3xl font-extrabold ${getLevelColor(dimension.level)}`}>
            {dimension.score}
          </div>
          <div className="text-xs text-gray-500">/100</div>
        </div>
      </div>

      {/* Score bar */}
      <div className="w-full h-2 bg-white/60 rounded-full overflow-hidden mb-4">
        <div
          className="h-full rounded-full bg-current transition-all duration-700"
          style={{
            width: `${dimension.score}%`,
            color:
              dimension.level === "Advanced"
                ? "#10b981"
                : dimension.level === "Established"
                ? "#3b82f6"
                : dimension.level === "Emerging"
                ? "#f59e0b"
                : "#ef4444",
          }}
        />
      </div>

      {showDetails && (
        <>
          <p className="text-sm text-gray-700 leading-relaxed mb-4">
            {dimension.analysis}
          </p>

          {dimension.strengths.length > 0 && (
            <div className="mb-3">
              <h4 className="text-xs font-semibold text-emerald-700 uppercase tracking-wide mb-1">
                Strengths
              </h4>
              <ul className="space-y-1">
                {dimension.strengths.map((s, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-emerald-500 mt-1">+</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {dimension.gaps.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-red-700 uppercase tracking-wide mb-1">
                Gaps
              </h4>
              <ul className="space-y-1">
                {dimension.gaps.map((g, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-red-500 mt-1">-</span>
                    {g}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}
