"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  BarChart3,
  Copy,
  ExternalLink,
  FileText,
  Settings,
  Users,
  CreditCard,
  TrendingUp,
  Unlock,
} from "lucide-react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { api } from "@/lib/api";
import { getStoredAuth } from "@/lib/auth";

interface DashboardData {
  stats: {
    total_assessments: number;
    completed_assessments: number;
    reports_generated: number;
    reports_unlocked: number;
    avg_score: number | null;
  };
  clients: Array<{
    assessment_id: string;
    email: string | null;
    company_name: string | null;
    industry: string;
    status: string;
    score_overall: number | null;
    report_id: string | null;
    report_status: string | null;
    is_unlocked: boolean;
    started_at: string;
  }>;
}

interface TenantData {
  slug: string;
  name: string;
  logo_url: string | null;
  primary_color: string;
}

export default function ConsolePage() {
  const router = useRouter();
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [tenant, setTenant] = useState<TenantData | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const { token } = getStoredAuth();
    if (!token) {
      router.push("/auth/login");
      return;
    }

    Promise.all([api.getDashboard(token), api.getMyTenant(token)])
      .then(([dashData, tenantData]) => {
        setDashboard(dashData);
        setTenant(tenantData);
      })
      .catch(() => {
        router.push("/auth/login");
      })
      .finally(() => setLoading(false));
  }, [router]);

  function copyLink() {
    if (!tenant) return;
    const url = `https://${tenant.slug}.auditiq.com/assess`;
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  if (loading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="animate-pulse text-gray-400">
          Loading dashboard...
        </div>
      </div>
    );
  }

  if (!dashboard || !tenant) return null;

  const auditLink = `https://${tenant.slug}.auditiq.com/assess`;

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {tenant.name} Dashboard
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Manage your whitelabel AI audit portal
          </p>
        </div>
        <div className="flex gap-3">
          <Link href="/console/settings">
            <Button variant="secondary" size="sm">
              <Settings className="w-4 h-4 mr-1.5" />
              Branding
            </Button>
          </Link>
          <Link href="/console/billing">
            <Button variant="secondary" size="sm">
              <CreditCard className="w-4 h-4 mr-1.5" />
              Billing
            </Button>
          </Link>
        </div>
      </div>

      {/* Audit Link */}
      <Card className="mb-8 bg-gradient-to-r from-blue-50 to-violet-50 border-blue-100">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-gray-900 mb-1">
              Your Branded Audit Link
            </h3>
            <p className="text-sm text-gray-600">
              Share this with your clients to start their AI readiness
              assessment
            </p>
            <code className="text-sm font-mono text-blue-700 mt-2 block">
              {auditLink}
            </code>
          </div>
          <div className="flex gap-2">
            <Button onClick={copyLink} variant="secondary" size="sm">
              <Copy className="w-4 h-4 mr-1" />
              {copied ? "Copied!" : "Copy"}
            </Button>
            <a href={auditLink} target="_blank" rel="noopener noreferrer">
              <Button variant="ghost" size="sm">
                <ExternalLink className="w-4 h-4" />
              </Button>
            </a>
          </div>
        </div>
      </Card>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        {[
          {
            label: "Total Assessments",
            value: dashboard.stats.total_assessments,
            icon: FileText,
          },
          {
            label: "Completed",
            value: dashboard.stats.completed_assessments,
            icon: Users,
          },
          {
            label: "Reports Generated",
            value: dashboard.stats.reports_generated,
            icon: BarChart3,
          },
          {
            label: "Reports Unlocked",
            value: dashboard.stats.reports_unlocked,
            icon: Unlock,
          },
          {
            label: "Avg Score",
            value: dashboard.stats.avg_score
              ? `${dashboard.stats.avg_score}`
              : "—",
            icon: TrendingUp,
          },
        ].map((stat) => (
          <Card key={stat.label} padding="sm">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gray-100 rounded-xl flex items-center justify-center">
                <stat.icon className="w-5 h-5 text-gray-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {stat.value}
                </div>
                <div className="text-xs text-gray-500">{stat.label}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Client Table */}
      <Card>
        <h2 className="text-lg font-bold text-gray-900 mb-4">
          Client Assessments
        </h2>
        {dashboard.clients.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            <Users className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p className="font-medium">No assessments yet</p>
            <p className="text-sm mt-1">
              Share your branded link to start collecting assessments
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wide py-3 px-2">
                    Client
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wide py-3 px-2">
                    Industry
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wide py-3 px-2">
                    Status
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wide py-3 px-2">
                    Score
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wide py-3 px-2">
                    Date
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wide py-3 px-2">
                    Report
                  </th>
                </tr>
              </thead>
              <tbody>
                {dashboard.clients.map((client) => (
                  <tr
                    key={client.assessment_id}
                    className="border-b border-gray-50 hover:bg-gray-50"
                  >
                    <td className="py-3 px-2">
                      <div className="font-medium text-gray-900 text-sm">
                        {client.company_name || "—"}
                      </div>
                      <div className="text-xs text-gray-500">
                        {client.email || "No email yet"}
                      </div>
                    </td>
                    <td className="py-3 px-2 text-sm text-gray-600 capitalize">
                      {client.industry.replace("_", " ")}
                    </td>
                    <td className="py-3 px-2">
                      <Badge
                        variant={
                          client.status === "completed"
                            ? "success"
                            : "warning"
                        }
                      >
                        {client.status}
                      </Badge>
                    </td>
                    <td className="py-3 px-2 text-sm font-semibold text-gray-900">
                      {client.score_overall ?? "—"}
                    </td>
                    <td className="py-3 px-2 text-xs text-gray-500">
                      {new Date(client.started_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-2">
                      {client.report_id ? (
                        <Link
                          href={`/report/${client.report_id}`}
                          className="text-blue-600 text-sm hover:underline"
                        >
                          View
                        </Link>
                      ) : (
                        <span className="text-xs text-gray-400">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
