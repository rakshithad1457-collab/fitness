'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Navbar from '../components/Navbar';
import { authAPI } from '@/lib/api'; // FIXED PATH

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const currentUser = authAPI.getCurrentUser();
    if (!currentUser) {
      router.push('/login');
    } else {
      setUser(currentUser);
      setLoading(false);
    }
  }, [router]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
       <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
    </div>
  );

  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-6 py-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-4xl font-bold mb-4">
            Welcome back, <span className="text-orange-600">{user?.email?.split('@')[0]}</span>! 👋
          </h1>
          <p className="text-gray-600 text-lg mb-8">Choose your path to fitness today.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div 
              className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 hover:shadow-lg transition-all cursor-pointer" 
              onClick={() => router.push('/workouts')}
            >
               <div className="text-3xl mb-4">💪</div>
               <h3 className="font-bold text-xl">Get Workout</h3>
               <p className="text-gray-500 text-sm">Exercises based on your mood</p>
            </div>
          </div>
        </motion.div>
      </div>
    </main>
  );
}