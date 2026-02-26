'use client';

import { useRouter, usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { LayoutDashboard, Dumbbell, Utensils, LogOut } from 'lucide-react';
import { authAPI } from '@/lib/api';

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();

  const handleLogout = () => {
    authAPI.logout();
    router.push('/');
  };

  const navLinks = [
    { path: '/dashboard',   label: 'Dashboard', icon: LayoutDashboard },
    { path: '/select-age',  label: 'Workouts',  icon: Dumbbell },   // ← redirects to age first
    { path: '/nutrition',   label: 'Nutrition',  icon: Utensils },
  ];

  // Mark Workouts as active when user is on either /select-age or /workouts
  const isWorkoutsActive =
    pathname === '/select-age' || pathname === '/workouts';

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

        {/* Logo */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          onClick={() => router.push('/dashboard')}
          className="flex items-center gap-3 cursor-pointer"
        >
          <div className="w-9 h-9 rounded-lg bg-[#1F2937] flex items-center justify-center text-white font-bold shadow-sm">
            F
          </div>
          <h1 className="text-xl font-bold text-[#1F2937] tracking-tight hidden sm:block">
            FitMood
          </h1>
        </motion.div>

        {/* Nav Links */}
        <div className="flex items-center gap-1">
          {navLinks.map((link) => {
            const Icon = link.icon;

            // Special active check for workouts flow
            const isActive =
              link.path === '/select-age'
                ? isWorkoutsActive
                : pathname === link.path;

            return (
              <button
                key={link.path}
                onClick={() => router.push(link.path)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-[11px] font-bold uppercase tracking-wider transition-all duration-200 ${
                  isActive
                    ? 'bg-[#FB923C] text-white shadow-md'
                    : 'text-[#6B7280] hover:bg-gray-50'
                }`}
              >
                <Icon size={14} />
                <span className="hidden md:inline">{link.label}</span>
              </button>
            );
          })}

          <div className="h-6 w-[1px] bg-gray-100 mx-2 hidden sm:block" />

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 text-[#6B7280] hover:text-red-500 transition-colors text-[11px] font-bold uppercase tracking-widest"
          >
            <LogOut size={14} />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>

      </div>
    </nav>
  );
}