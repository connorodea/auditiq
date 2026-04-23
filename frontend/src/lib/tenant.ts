"use client";

import { createContext, useContext } from "react";

export interface TenantConfig {
  slug: string;
  name: string;
  logo_url: string | null;
  primary_color: string;
  accent_color: string;
  cta_text: string;
  cta_url: string | null;
}

export const DEFAULT_TENANT: TenantConfig = {
  slug: "app",
  name: "AuditIQ",
  logo_url: null,
  primary_color: "#2563EB",
  accent_color: "#7C3AED",
  cta_text: "Get Your AI Readiness Report",
  cta_url: null,
};

export const TenantContext = createContext<TenantConfig>(DEFAULT_TENANT);

export function useTenant() {
  return useContext(TenantContext);
}
