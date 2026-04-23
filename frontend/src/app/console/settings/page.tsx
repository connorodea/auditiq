"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Check, Palette } from "lucide-react";
import Link from "next/link";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { api } from "@/lib/api";
import { getStoredAuth } from "@/lib/auth";

interface TenantConfig {
  slug: string;
  name: string;
  logo_url: string | null;
  primary_color: string;
  accent_color: string;
  cta_text: string;
  cta_url: string | null;
}

export default function BrandingSettings() {
  const router = useRouter();
  const [tenant, setTenant] = useState<TenantConfig | null>(null);
  const [form, setForm] = useState({
    name: "",
    logo_url: "",
    primary_color: "#2563EB",
    accent_color: "#7C3AED",
    cta_text: "",
    cta_url: "",
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const { token } = getStoredAuth();
    if (!token) {
      router.push("/auth/login");
      return;
    }

    api
      .getMyTenant(token)
      .then((data) => {
        setTenant(data);
        setForm({
          name: data.name || "",
          logo_url: data.logo_url || "",
          primary_color: data.primary_color || "#2563EB",
          accent_color: data.accent_color || "#7C3AED",
          cta_text: data.cta_text || "",
          cta_url: data.cta_url || "",
        });
      })
      .catch(() => router.push("/auth/login"))
      .finally(() => setLoading(false));
  }, [router]);

  async function handleSave() {
    const { token } = getStoredAuth();
    if (!token) return;

    setSaving(true);
    setError("");

    try {
      const updated = await api.updateMyTenant(token, {
        name: form.name || undefined,
        logo_url: form.logo_url || null,
        primary_color: form.primary_color,
        accent_color: form.accent_color,
        cta_text: form.cta_text || undefined,
        cta_url: form.cta_url || null,
      });
      setTenant(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading...</div>
      </div>
    );
  }

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
          <Palette className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Branding Settings
          </h1>
          <p className="text-sm text-gray-500">
            Customize how your audit portal looks to clients
          </p>
        </div>
      </div>

      <Card padding="lg">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              Brand Name
            </label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            <p className="text-xs text-gray-400 mt-1">
              Displayed in the header and report footer
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              Logo URL
            </label>
            <input
              type="url"
              value={form.logo_url}
              onChange={(e) => setForm({ ...form, logo_url: e.target.value })}
              placeholder="https://example.com/logo.png"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">
                Primary Color
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="color"
                  value={form.primary_color}
                  onChange={(e) =>
                    setForm({ ...form, primary_color: e.target.value })
                  }
                  className="w-12 h-12 rounded-xl border border-gray-200 cursor-pointer"
                />
                <input
                  type="text"
                  value={form.primary_color}
                  onChange={(e) =>
                    setForm({ ...form, primary_color: e.target.value })
                  }
                  className="flex-1 px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">
                Accent Color
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="color"
                  value={form.accent_color}
                  onChange={(e) =>
                    setForm({ ...form, accent_color: e.target.value })
                  }
                  className="w-12 h-12 rounded-xl border border-gray-200 cursor-pointer"
                />
                <input
                  type="text"
                  value={form.accent_color}
                  onChange={(e) =>
                    setForm({ ...form, accent_color: e.target.value })
                  }
                  className="flex-1 px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              CTA Text
            </label>
            <input
              type="text"
              value={form.cta_text}
              onChange={(e) => setForm({ ...form, cta_text: e.target.value })}
              placeholder="Get Your AI Readiness Report"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            <p className="text-xs text-gray-400 mt-1">
              Shown on the report as the bottom CTA
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              CTA Link
            </label>
            <input
              type="url"
              value={form.cta_url}
              onChange={(e) => setForm({ ...form, cta_url: e.target.value })}
              placeholder="https://yoursite.com/contact"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>

          {/* Preview */}
          <div className="border border-gray-100 rounded-xl p-6 bg-gray-50">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Preview
            </h3>
            <div className="flex items-center gap-3 mb-4">
              {form.logo_url ? (
                <img
                  src={form.logo_url}
                  alt="Logo"
                  className="w-9 h-9 rounded-lg object-contain"
                />
              ) : (
                <div
                  className="w-9 h-9 rounded-lg"
                  style={{
                    background: `linear-gradient(135deg, ${form.primary_color}, ${form.accent_color})`,
                  }}
                />
              )}
              <span className="text-lg font-bold text-gray-900">
                {form.name || "Your Brand"}
              </span>
            </div>
            <div
              className="text-sm font-medium text-white px-4 py-2 rounded-lg inline-block"
              style={{ backgroundColor: form.primary_color }}
            >
              {form.cta_text || "Call to Action"}
            </div>
          </div>

          {error && (
            <p className="text-sm text-red-600 bg-red-50 px-4 py-2 rounded-lg">
              {error}
            </p>
          )}

          <Button onClick={handleSave} loading={saving} className="w-full">
            {saved ? (
              <>
                <Check className="w-4 h-4 mr-1.5" />
                Saved!
              </>
            ) : (
              "Save Branding"
            )}
          </Button>
        </div>
      </Card>
    </div>
  );
}
