"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/context", label: "Context" },
];

export default function NavBar() {
  const pathname = usePathname();
  return (
    <nav className="bg-white dark:bg-gray-800 shadow mb-8">
      <div className="max-w-4xl mx-auto px-4 py-3 flex gap-6">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`text-base font-medium px-2 py-1 rounded transition-colors ${
              pathname === item.href
                ? "text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900"
                : "text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  );
} 