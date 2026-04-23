export interface ReportData {
  id: string;
  assessment_id: string;
  score_overall: number | null;
  score_data_readiness: number | null;
  score_process_maturity: number | null;
  score_tech_infrastructure: number | null;
  score_team_capability: number | null;
  score_strategic_alignment: number | null;
  is_unlocked: boolean;
  status: string;
  report_content: ReportContent | TeaserContent | null;
  created_at: string;
}

export interface ReportContent {
  executive_summary: {
    headline: string;
    summary: string;
    overall_assessment: string;
    key_finding: string;
  };
  dimension_analysis: DimensionAnalysis[];
  opportunity_zones: OpportunityZone[];
  implementation_roadmap: {
    phase_1_quick_wins: RoadmapPhase;
    phase_2_foundation: RoadmapPhase;
    phase_3_scale: RoadmapPhase;
  };
  roi_analysis: {
    estimated_annual_savings_range: string;
    productivity_gain_estimate: string;
    payback_period: string;
    key_assumptions: string[];
  };
  risk_factors: RiskFactor[];
  next_steps: string[];
}

export interface TeaserContent {
  executive_summary: ReportContent["executive_summary"];
  dimension_analysis: DimensionAnalysis[];
  opportunity_zones_count: number;
  opportunity_zones_preview: { title: string; impact: string; effort: string }[];
  has_roadmap: boolean;
  has_roi_analysis: boolean;
  next_steps_count: number;
}

export interface DimensionAnalysis {
  dimension: string;
  title: string;
  score: number;
  level: string;
  analysis: string;
  strengths: string[];
  gaps: string[];
  priority: string;
}

export interface OpportunityZone {
  title: string;
  description: string;
  dimension_addressed: string;
  effort: string;
  impact: string;
  timeline: string;
  estimated_roi: string;
  prerequisites: string[];
  recommended_tools: string[];
}

export interface RoadmapPhase {
  timeline: string;
  initiatives: string[];
  expected_outcomes: string[];
  estimated_investment: string;
}

export interface RiskFactor {
  risk: string;
  severity: string;
  mitigation: string;
}

export interface ReportStatusResponse {
  status: string;
  is_unlocked: boolean;
  score_overall: number | null;
}
