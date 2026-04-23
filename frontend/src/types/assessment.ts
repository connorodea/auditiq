export interface QuestionOption {
  value: string;
  label: string;
  score: number;
}

export interface Question {
  id: string;
  sequence: number;
  dimension: string;
  question_text: string;
  question_type: string;
  options: QuestionOption[] | null;
  help_text: string | null;
}

export interface ProgressInfo {
  answered: number;
  total: number;
  percent: number;
}

export interface AssessmentResponse {
  assessment_id: string;
  session_token: string;
  total_questions: number;
  first_question: Question | null;
}

export interface SubmitResponseResult {
  saved: boolean;
  progress: ProgressInfo;
  next_question: Question | null;
}

export interface CompleteAssessmentResult {
  report_id: string;
  status: string;
  scores_preview: Record<string, number | string>;
  estimated_time_seconds: number;
}

export interface AssessmentStatus {
  assessment_id: string;
  status: string;
  industry: string;
  company_name: string | null;
  company_size: string | null;
  progress: ProgressInfo;
  started_at: string;
}
