"use client";

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from "recharts";

interface ScoreRadarProps {
  scores: {
    data_readiness: number | null;
    process_maturity: number | null;
    tech_infrastructure: number | null;
    team_capability: number | null;
    strategic_alignment: number | null;
  };
}

export default function ScoreRadar({ scores }: ScoreRadarProps) {
  const data = [
    { dimension: "Data", score: scores.data_readiness ?? 0, fullMark: 100 },
    { dimension: "Process", score: scores.process_maturity ?? 0, fullMark: 100 },
    { dimension: "Technology", score: scores.tech_infrastructure ?? 0, fullMark: 100 },
    { dimension: "Team", score: scores.team_capability ?? 0, fullMark: 100 },
    { dimension: "Strategy", score: scores.strategic_alignment ?? 0, fullMark: 100 },
  ];

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="75%">
          <PolarGrid stroke="#e5e7eb" />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fontSize: 12, fill: "#6b7280", fontWeight: 500 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fontSize: 10, fill: "#9ca3af" }}
          />
          <Radar
            name="Score"
            dataKey="score"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.15}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
