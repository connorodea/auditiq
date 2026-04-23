import Link from "next/link";
import { Brain } from "lucide-react";

export default function Header() {
  return (
    <header className="border-b border-gray-100 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-9 h-9 bg-gradient-to-br from-blue-600 to-violet-600 rounded-xl flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900">AuditIQ</span>
        </Link>
        <nav className="flex items-center gap-6">
          <Link
            href="/assess"
            className="text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
          >
            Take Assessment
          </Link>
        </nav>
      </div>
    </header>
  );
}
