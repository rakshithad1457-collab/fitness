'use client';

import { useRouter, usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { authAPI } from '@/lib/api'; // FIXED PATH

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();

  const handleLogout = () => {
    authAPI.logout();
    router.push('/');
  };

  const navLinks = [
    { path: '/dashboard', label: 'Dashboard', icon: '🏠' },
    { path: '/workouts', label: 'Workouts', icon: '💪' },
    { path: '/nutrition', label: 'Nutrition', icon: '🥗' },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <motion.div 
          whileHover={{ scale: 1.05 }}
          onClick={() => router.push('/dashboard')}
          className="flex items-center gap-3 cursor-pointer"
        >
          <div className="w-10 h-10 rounded-full bg-orange-500 flex items-center justify-center text-white font-bold shadow-lg">F</div>
          <h1 className="text-2xl font-bold text-orange-600 hidden sm:block">FitMood</h1>
        </motion.div>

        <div className="flex gap-2">
          {navLinks.map((link) => (
            <button
              key={link.path}
              onClick={() => router.push(link.path)}
              className={`px-4 py-2 rounded-xl font-semibold transition-all ${
                pathname === link.path ? 'bg-orange-500 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <span className="mr-2">{link.icon}</span>
              <span className="hidden sm:inline">{link.label}</span>
            </button>
          ))}
          <button onClick={handleLogout} className="px-4 py-2 text-red-600 font-semibold hover:bg-red-50 rounded-xl transition-all">Logout</button>
        </div>
      </div>
    </nav>
  );
}