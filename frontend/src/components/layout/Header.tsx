"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Brain, LayoutDashboard, LogOut } from "lucide-react";
import { getStoredAuth, clearAuth, AuthUser } from "@/lib/auth";

export default function Header() {
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    const { user: stored } = getStoredAuth();
    setUser(stored);
  }, []);

  function handleLogout() {
    clearAuth();
    setUser(null);
    window.location.href = "/";
  }

  return (
    <header className="border-b border-gray-100 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-9 h-9 bg-gradient-to-br from-blue-600 to-violet-600 rounded-xl flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900">AuditIQ</span>
        </Link>
        <nav className="flex items-center gap-4">
          <Link
            href="/assess"
            className="text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
          >
            Take Assessment
          </Link>
          {user ? (
            <>
              <Link
                href="/console"
                className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors flex items-center gap-1"
              >
                <LayoutDashboard className="w-4 h-4" />
                Console
              </Link>
              <button
                onClick={handleLogout}
                className="text-sm font-medium text-gray-400 hover:text-gray-600 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </>
          ) : (
            <Link
              href="/auth/login"
              className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              Consultant Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
