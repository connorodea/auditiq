"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, Building2 } from "lucide-react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { api } from "@/lib/api";

const INDUSTRIES = [
  { value: "healthcare", label: "Healthcare" },
  { value: "finance", label: "Finance & Banking" },
  { value: "retail", label: "Retail" },
  { value: "ecommerce", label: "E-Commerce" },
  { value: "manufacturing", label: "Manufacturing" },
  { value: "professional_services", label: "Professional Services" },
  { value: "technology", label: "Technology" },
  { value: "education", label: "Education" },
  { value: "real_estate", label: "Real Estate" },
  { value: "construction", label: "Construction" },
  { value: "logistics", label: "Logistics & Supply Chain" },
  { value: "hospitality", label: "Hospitality" },
  { value: "legal", label: "Legal" },
  { value: "other", label: "Other" },
];

const COMPANY_SIZES = [
  { value: "1-10", label: "1-10 employees" },
  { value: "11-50", label: "11-50 employees" },
  { value: "51-200", label: "51-200 employees" },
  { value: "201-1000", label: "201-1,000 employees" },
  { value: "1000+", label: "1,000+ employees" },
];

export default function AssessPage() {
  const router = useRouter();
  const [industry, setIndustry] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [companySize, setCompanySize] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleStart() {
    if (!industry) {
      setError("Please select your industry");
      return;
    }
    setLoading(true);
    setError("");

    try {
      const result = await api.createAssessment({
        industry,
        company_name: companyName || undefined,
        company_size: companySize || undefined,
      });
      router.push(`/assess/${result.session_token}`);
    } catch (err: any) {
      setError(err.message || "Failed to start assessment");
      setLoading(false);
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-6">
      <Card className="w-full max-w-lg" padding="lg">
        <div className="text-center mb-8">
          <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-violet-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Building2 className="w-7 h-7 text-blue-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Let&apos;s Get Started
          </h1>
          <p className="text-gray-600">
            Tell us a bit about your business to personalize your assessment.
          </p>
        </div>

        <div className="space-y-5">
          {/* Industry */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Industry <span className="text-red-500">*</span>
            </label>
            <select
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            >
              <option value="">Select your industry</option>
              {INDUSTRIES.map((ind) => (
                <option key={ind.value} value={ind.value}>
                  {ind.label}
                </option>
              ))}
            </select>
          </div>

          {/* Company Name */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Company Name <span className="text-gray-400">(optional)</span>
            </label>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="Acme Corp"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            />
          </div>

          {/* Company Size */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Company Size <span className="text-gray-400">(optional)</span>
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {COMPANY_SIZES.map((size) => (
                <button
                  key={size.value}
                  onClick={() => setCompanySize(size.value)}
                  className={`px-3 py-2.5 rounded-xl text-sm font-medium border transition-all ${
                    companySize === size.value
                      ? "border-blue-500 bg-blue-50 text-blue-700"
                      : "border-gray-200 bg-white text-gray-700 hover:border-gray-300"
                  }`}
                >
                  {size.label}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <p className="text-sm text-red-600 bg-red-50 px-4 py-2 rounded-lg">
              {error}
            </p>
          )}

          <Button
            onClick={handleStart}
            loading={loading}
            className="w-full"
            size="lg"
          >
            Begin Assessment
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>

          <p className="text-xs text-gray-400 text-center">
            Takes approximately 4 minutes &middot; No account required
          </p>
        </div>
      </Card>
    </div>
  );
}
