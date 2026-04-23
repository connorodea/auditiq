import { NextRequest, NextResponse } from "next/server";

const PUBLIC_DOMAINS = ["localhost", "auditiq.com", "www.auditiq.com"];

export function middleware(request: NextRequest) {
  const hostname = request.headers.get("host") || "";
  const domain = hostname.split(":")[0]; // strip port

  // Check if this is a subdomain (e.g., acme.auditiq.com)
  let tenantSlug: string | null = null;

  if (!PUBLIC_DOMAINS.includes(domain)) {
    // Extract subdomain: "acme.auditiq.com" -> "acme"
    const parts = domain.split(".");
    if (parts.length >= 3) {
      tenantSlug = parts[0];
    } else if (parts.length === 1 && domain !== "localhost") {
      // Local dev: "acme.localhost" -> "acme"
      tenantSlug = parts[0];
    }
  }

  // For "app" subdomain or no subdomain, use default tenant
  if (tenantSlug === "app" || tenantSlug === "www") {
    tenantSlug = null;
  }

  // Pass tenant slug via header for server components / API calls
  const response = NextResponse.next();
  if (tenantSlug) {
    response.headers.set("x-tenant-slug", tenantSlug);
    // Also set as a cookie so client components can read it
    response.cookies.set("tenant_slug", tenantSlug, {
      path: "/",
      httpOnly: false,
      sameSite: "lax",
    });
  }

  return response;
}

export const config = {
  matcher: [
    // Match all paths except static files and API routes
    "/((?!_next/static|_next/image|favicon.ico|api/).*)",
  ],
};
