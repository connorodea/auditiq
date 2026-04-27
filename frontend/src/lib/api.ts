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

function authRequest<T>(path: string, token: string, options?: RequestInit): Promise<T> {
  return request<T>(path, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...options?.headers,
    },
  });
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

  // Auth endpoints
  register: (data: {
    email: string;
    password: string;
    full_name: string;
    company_name: string;
  }) =>
    request<any>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  login: (email: string, password: string) =>
    request<any>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  getMe: (token: string) => authRequest<any>("/auth/me", token),

  // Tenant endpoints
  getMyTenant: (token: string) => authRequest<any>("/tenants/me", token),

  updateMyTenant: (token: string, data: Record<string, any>) =>
    authRequest<any>("/tenants/me", token, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  lookupTenant: (slug: string) => request<any>(`/tenants/lookup/${slug}`),

  // Dashboard endpoints
  getDashboard: (token: string) => authRequest<any>("/dashboard", token),

  // Subscription
  createSubscription: (token: string) =>
    authRequest<any>("/payments/subscribe", token, { method: "POST" }),
};
