"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CreditCard, Check, Zap } from "lucide-react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { api } from "@/lib/api";
import { getStoredAuth, AuthUser } from "@/lib/auth";

export default function BillingPage() {
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [subscribing, setSubscribing] = useState(false);

  useEffect(() => {
    const { token, user: storedUser } = getStoredAuth();
    if (!token || !storedUser) {
      router.push("/auth/login");
      return;
    }

    // Refresh user data
    api
      .getMe(token)
      .then((data) => setUser(data))
      .catch(() => router.push("/auth/login"))
      .finally(() => setLoading(false));
  }, [router]);

  async function handleSubscribe() {
    const { token } = getStoredAuth();
    if (!token) return;

    setSubscribing(true);
    try {
      const result = await api.createSubscription(token);
      window.location.href = result.checkout_url;
    } catch {
      setSubscribing(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading...</div>
      </div>
    );
  }

  const isActive = user?.subscription_status === "active";

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">
      <Link
        href="/console"
        className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </Link>

      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-violet-100 rounded-2xl flex items-center justify-center">
          <CreditCard className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Billing</h1>
          <p className="text-sm text-gray-500">
            Manage your consultant subscription
          </p>
        </div>
      </div>

      {/* Current Plan */}
      <Card className="mb-6" padding="lg">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-gray-900">Current Plan</h2>
          <Badge variant={isActive ? "success" : "warning"}>
            {user?.subscription_status || "inactive"}
          </Badge>
        </div>

        {isActive ? (
          <div>
            <div className="flex items-baseline gap-1 mb-2">
              <span className="text-3xl font-extrabold text-gray-900">
                $149
              </span>
              <span className="text-gray-500">/month</span>
            </div>
            <p className="text-sm text-gray-600">
              Your whitelabel portal is active. Clients see your branding.
            </p>
          </div>
        ) : (
          <div>
            <p className="text-gray-600 mb-6">
              Activate your subscription to enable your branded portal.
            </p>

            <div className="bg-gradient-to-br from-blue-50 to-violet-50 rounded-xl p-6 mb-6">
              <div className="flex items-baseline gap-1 mb-4">
                <span className="text-4xl font-extrabold text-gray-900">
                  $149
                </span>
                <span className="text-gray-500">/month</span>
              </div>

              <ul className="space-y-2 mb-6">
                {[
                  "Your own branded subdomain (company.auditiq.com)",
                  "Custom logo, colors, and CTA on all reports",
                  "Dashboard to track client assessments",
                  "Downloadable PDF reports for clients",
                  "Unlimited client assessments",
                ].map((feature) => (
                  <li
                    key={feature}
                    className="flex items-start gap-2 text-sm text-gray-700"
                  >
                    <Check className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>

              <Button
                onClick={handleSubscribe}
                loading={subscribing}
                size="lg"
                className="w-full group"
              >
                <Zap className="w-5 h-5 mr-2" />
                Activate Subscription
              </Button>
            </div>

            <div className="text-center">
              <p className="text-xs text-gray-400">
                Annual plan available: $1,199/year (save $589)
              </p>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
