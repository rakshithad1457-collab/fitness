// app/admin/login/page.js
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Lock, Eye, EyeOff, ShieldCheck } from 'lucide-react';

export default function AdminLoginPage() {
  const router = useRouter();
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/admin/login', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ password }),
      });

      if (res.ok) {
        router.push('/admin');
      } else {
        setError('Wrong password. Try again.');
      }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#1F2937] flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md"
      >
        <div className="bg-[#111827] rounded-[2rem] p-10 shadow-[0_20px_60px_rgba(0,0,0,0.5)]">

          {/* Icon */}
          <div className="w-16 h-16 rounded-2xl bg-[#FB923C]/10 border border-[#FB923C]/20 flex items-center justify-center mb-8 mx-auto">
            <ShieldCheck size={28} className="text-[#FB923C]" />
          </div>

          <h1 className="text-2xl font-bold text-white text-center tracking-tight mb-1">
            Admin Access
          </h1>
          <p className="text-[#6B7280] text-sm text-center mb-8">
            FitMood Control Panel
          </p>

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="relative">
              <Lock size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#6B7280]" />
              <input
                type={showPass ? 'text' : 'password'}
                placeholder="Enter admin password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-[#1F2937] text-white placeholder-[#4B5563] border border-[#374151] rounded-xl pl-11 pr-11 py-3.5 text-sm focus:outline-none focus:border-[#FB923C] transition-colors"
              />
              <button
                type="button"
                onClick={() => setShowPass(!showPass)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#6B7280] hover:text-white transition-colors"
              >
                {showPass ? <EyeOff size={15} /> : <Eye size={15} />}
              </button>
            </div>

            {error && (
              <p className="text-red-400 text-xs text-center font-medium">{error}</p>
            )}

            <motion.button
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading || !password}
              className="w-full bg-gradient-to-r from-[#FB923C] to-[#F97316] text-white py-3.5 rounded-xl font-bold uppercase tracking-[0.15em] text-sm disabled:opacity-50 mt-2"
            >
              {loading ? 'Verifying...' : 'Enter Panel'}
            </motion.button>
          </form>

          <p className="text-[#4B5563] text-[10px] text-center mt-6 uppercase tracking-widest">
            Unauthorized access is prohibited
          </p>
        </div>
      </motion.div>
    </main>
  );
}