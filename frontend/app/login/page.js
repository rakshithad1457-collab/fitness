'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Mail, Lock, ArrowRight, ShieldCheck, Zap } from 'lucide-react';
import { authAPI } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await authAPI.login(formData.email, formData.password);
      } else {
        // Assuming your authAPI has a register method
        await authAPI.register(formData.email, formData.password);
      }
      router.push('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#F8F9FC] flex flex-col items-center justify-center px-6 relative overflow-hidden">
      {/* Brand Header */}
      <motion.div 
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-3 mb-10 cursor-pointer" 
        onClick={() => router.push('/')}
      >
        <div className="w-10 h-10 rounded-xl bg-[#1F2937] flex items-center justify-center text-white text-xl font-bold shadow-sm">
          F
        </div>
        <h1 className="text-xl font-bold tracking-tight text-[#1F2937]">FitMood</h1>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md z-10 bg-white rounded-[2.5rem] p-10 md:p-12 shadow-[0_4px_20px_rgba(0,0,0,0.05)] border border-gray-50"
      >
        <header className="text-center mb-10">
          <h2 className="text-3xl font-semibold text-[#1F2937] tracking-[-0.02em] mb-2 uppercase">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h2>
          <p className="text-[10px] font-bold uppercase tracking-[0.3em] text-[#6B7280]">
            {isLogin ? 'Ready for your mood-based workout?' : 'Initialize your fitness journey'}
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-[10px] font-bold uppercase tracking-widest text-[#6B7280] ml-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300" size={18} />
              <input
                type="email"
                required
                value={formData.email}
                className="w-full bg-[#F8F9FC] border-2 border-transparent focus:border-[#FB923C]/30 focus:bg-white rounded-2xl py-4 pl-12 pr-4 text-sm font-medium text-[#1F2937] transition-all outline-none"
                placeholder="name@example.com"
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-bold uppercase tracking-widest text-[#6B7280] ml-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300" size={18} />
              <input
                type="password"
                required
                value={formData.password}
                className="w-full bg-[#F8F9FC] border-2 border-transparent focus:border-[#FB923C]/30 focus:bg-white rounded-2xl py-4 pl-12 pr-4 text-sm font-medium text-[#1F2937] transition-all outline-none"
                placeholder="••••••••"
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              />
            </div>
          </div>

          {error && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-4 rounded-xl bg-red-50 border border-red-100 text-red-600 text-[11px] font-bold uppercase tracking-wider text-center"
            >
              {error}
            </motion.div>
          )}

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-[#FB923C] to-[#F97316] text-white py-5 rounded-2xl font-bold uppercase tracking-[0.2em] text-xs shadow-[0_8px_20px_rgba(249,115,22,0.3)] hover:shadow-[0_12px_24px_rgba(249,115,22,0.4)] transition-all flex items-center justify-center gap-2"
          >
            {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
            <ArrowRight size={16} />
          </motion.button>
        </form>

        <footer className="mt-10 text-center border-t border-gray-50 pt-8">
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className="text-[10px] font-bold uppercase tracking-widest text-[#6B7280] hover:text-[#FB923C] transition-colors"
          >
            {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Sign In"}
          </button>
        </footer>
      </motion.div>

      {/* Trust Badges */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.4 }}
        transition={{ delay: 0.5 }}
        className="mt-12 flex gap-8"
      >
        <div className="flex items-center gap-2">
          <ShieldCheck size={14} />
          <span className="text-[10px] font-bold uppercase tracking-widest">Secure Access</span>
        </div>
        <div className="flex items-center gap-2">
          <Zap size={14} />
          <span className="text-[10px] font-bold uppercase tracking-widest">Instant Sync</span>
        </div>
      </motion.div>
    </main>
  );
}