import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(amount);
}

export function getDimensionLabel(dimension: string): string {
  const labels: Record<string, string> = {
    data_readiness: "Data Readiness",
    process_maturity: "Process Maturity",
    tech_infrastructure: "Technology Infrastructure",
    team_capability: "Team Capability",
    strategic_alignment: "Strategic Alignment",
  };
  return labels[dimension] || dimension;
}

export function getLevelColor(level: string): string {
  switch (level) {
    case "Advanced":
      return "text-emerald-600";
    case "Established":
      return "text-blue-600";
    case "Emerging":
      return "text-amber-600";
    case "Nascent":
      return "text-red-600";
    default:
      return "text-gray-600";
  }
}

export function getLevelBg(level: string): string {
  switch (level) {
    case "Advanced":
      return "bg-emerald-50 border-emerald-200";
    case "Established":
      return "bg-blue-50 border-blue-200";
    case "Emerging":
      return "bg-amber-50 border-amber-200";
    case "Nascent":
      return "bg-red-50 border-red-200";
    default:
      return "bg-gray-50 border-gray-200";
  }
}

export function getScoreColor(score: number): string {
  if (score >= 80) return "#10b981";
  if (score >= 55) return "#3b82f6";
  if (score >= 30) return "#f59e0b";
  return "#ef4444";
}
