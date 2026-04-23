"use client";

import { Lock, Sparkles } from "lucide-react";
import Button from "@/components/ui/Button";

interface PaywallOverlayProps {
  onUnlock: () => void;
  loading?: boolean;
}

export default function PaywallOverlay({ onUnlock, loading }: PaywallOverlayProps) {
  return (
    <div className="relative">
      {/* Blurred content preview */}
      <div className="blur-sm opacity-40 pointer-events-none select-none">
        <div className="space-y-4 p-6">
          <div className="h-6 bg-gray-200 rounded w-3/4" />
          <div className="h-4 bg-gray-200 rounded w-full" />
          <div className="h-4 bg-gray-200 rounded w-5/6" />
          <div className="h-4 bg-gray-200 rounded w-4/6" />
          <div className="grid grid-cols-2 gap-4 mt-6">
            <div className="h-24 bg-gray-200 rounded-xl" />
            <div className="h-24 bg-gray-200 rounded-xl" />
            <div className="h-24 bg-gray-200 rounded-xl" />
            <div className="h-24 bg-gray-200 rounded-xl" />
          </div>
          <div className="h-4 bg-gray-200 rounded w-full mt-4" />
          <div className="h-4 bg-gray-200 rounded w-2/3" />
        </div>
      </div>

      {/* Overlay CTA */}
      <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-b from-white/60 via-white/90 to-white">
        <div className="text-center max-w-sm px-6">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-violet-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Lock className="w-8 h-8 text-blue-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Unlock Your Full Report
          </h3>
          <p className="text-gray-600 text-sm mb-6">
            Get the complete analysis with detailed opportunity zones,
            implementation roadmap, ROI estimates, and actionable next steps.
          </p>
          <Button onClick={onUnlock} loading={loading} size="lg" className="w-full group">
            <Sparkles className="mr-2 w-5 h-5" />
            Unlock Full Report — $47
          </Button>
          <p className="text-xs text-gray-400 mt-3">
            One-time payment &middot; Instant access &middot; PDF download included
          </p>
        </div>
      </div>
    </div>
  );
}
