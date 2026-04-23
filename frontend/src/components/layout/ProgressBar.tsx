"use client";

import { cn } from "@/lib/utils";

interface ProgressBarProps {
  percent: number;
  answered: number;
  total: number;
}

export default function ProgressBar({ percent, answered, total }: ProgressBarProps) {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-600">
          Question {Math.min(answered + 1, total)} of {total}
        </span>
        <span className="text-sm font-semibold text-blue-600">{percent}%</span>
      </div>
      <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-500 ease-out",
            percent >= 80
              ? "bg-gradient-to-r from-emerald-500 to-emerald-400"
              : percent >= 50
              ? "bg-gradient-to-r from-blue-600 to-blue-400"
              : "bg-gradient-to-r from-blue-600 to-violet-500"
          )}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
