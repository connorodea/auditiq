"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

export default function FullReportRedirect() {
  const params = useParams();
  const router = useRouter();
  const reportId = params.reportId as string;

  useEffect(() => {
    // After Stripe success, redirect back to the main report page
    // which will now show the full unlocked content
    router.replace(`/report/${reportId}`);
  }, [reportId, router]);

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <p className="text-gray-500">Unlocking your report...</p>
    </div>
  );
}
