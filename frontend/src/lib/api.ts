const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `API error: ${res.status}`);
  }
  return res.json();
}

// Assessment endpoints
export const api = {
  getIndustries: () => request<string[]>("/assessments/industries"),

  createAssessment: (data: {
    industry: string;
    company_name?: string;
    company_size?: string;
  }) =>
    request<{
      assessment_id: string;
      session_token: string;
      total_questions: number;
      first_question: any;
    }>("/assessments", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getAssessment: (sessionToken: string) =>
    request<any>(`/assessments/${sessionToken}`),

  getNextQuestion: (sessionToken: string) =>
    request<any>(`/assessments/${sessionToken}/questions/next`),

  submitResponse: (
    sessionToken: string,
    data: { question_id: string; answer_value: string; answer_text?: string }
  ) =>
    request<any>(`/assessments/${sessionToken}/responses`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  completeAssessment: (sessionToken: string, email: string) =>
    request<any>(`/assessments/${sessionToken}/complete`, {
      method: "POST",
      body: JSON.stringify({ email }),
    }),

  // Report endpoints
  getReport: (reportId: string) => request<any>(`/reports/${reportId}`),

  getReportStatus: (reportId: string) =>
    request<any>(`/reports/${reportId}/status`),

  triggerGeneration: (reportId: string) =>
    request<any>(`/reports/${reportId}/generate`, { method: "POST" }),

  // Payment endpoints
  createCheckout: (reportId: string, email: string) =>
    request<{ checkout_url: string; checkout_session_id: string }>(
      "/payments/checkout",
      {
        method: "POST",
        body: JSON.stringify({ report_id: reportId, email }),
      }
    ),
};
