import { Brain } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-gray-50 mt-auto">
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-gradient-to-br from-blue-600 to-violet-600 rounded-lg flex items-center justify-center">
              <Brain className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm font-semibold text-gray-600">AuditIQ</span>
          </div>
          <p className="text-xs text-gray-400">
            &copy; {new Date().getFullYear()} UPSCALED Inc. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
