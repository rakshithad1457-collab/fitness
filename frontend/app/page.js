'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  Dumbbell, 
  Utensils, 
  Calendar, 
  Target, 
  Zap, 
  Activity,
  ArrowRight
} from 'lucide-react';

export default function Home() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <main className="relative min-h-screen bg-[#F8F9FC] text-[#1F2937]">
      
      {/* Premium Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#1F2937] flex items-center justify-center text-white text-xl font-bold shadow-sm">
              F
            </div>
            <h1 className="text-xl font-bold tracking-tight text-[#1F2937]">FitMood</h1>
          </div>

          <button
            onClick={() => router.push('/login')}
            className="text-[11px] font-bold uppercase tracking-widest text-[#6B7280] hover:text-[#1F2937] transition-all"
          >
            Sign In
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 py-24 md:py-40">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-100 shadow-sm mb-10">
              <span className="flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-[#FB923C] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-[#FB923C]"></span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-widest text-[#6B7280]">
                Elite Fitness Companion
              </span>
            </div>

            <h2 className="text-5xl md:text-7xl font-semibold tracking-[-0.04em] text-[#1F2937] mb-8 leading-[1.1]">
              Fitness That
              <br />
              <span className="text-[#FB923C] italic font-medium">Fits Your Mood</span>
            </h2>
            
            <p className="text-lg text-[#6B7280] mb-12 max-w-2xl mx-auto font-medium leading-relaxed">
              Experience performance-driven workouts and nutrition strategies tailored 
              precisely to your current energy and long-term objectives.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => router.push('/login')}
                className="bg-gradient-to-r from-[#FB923C] to-[#F97316] text-white text-[11px] font-bold uppercase tracking-[0.2em] px-12 py-5 rounded-2xl shadow-[0_8px_20px_rgba(249,115,22,0.3)] flex items-center justify-center gap-2"
              >
                Get Started Free <ArrowRight size={16} />
              </motion.button>
              
              <button
                onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
                className="bg-white text-[#1F2937] text-[11px] font-bold uppercase tracking-[0.2em] px-12 py-5 rounded-2xl border border-gray-100 shadow-[0_4px_12px_rgba(0,0,0,0.05)] hover:bg-gray-50 transition-all"
              >
                Learn More
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature Ecosystem */}
      <section id="features" className="relative z-10 py-24 bg-white border-y border-gray-100">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-20">
            <h3 className="text-3xl md:text-5xl font-semibold tracking-[-0.02em] text-[#1F2937] mb-4">
              Everything You Need,
              <br />
              <span className="text-[#FB923C]">All in One Place</span>
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { icon: Dumbbell, title: 'Mood-Based Workouts', desc: 'Adapt training to your energy.' },
              { icon: Utensils, title: 'Smart Nutrition', desc: 'Fueling based on objectives.' },
              { icon: Calendar, title: '7-Day Meal Plans', desc: 'Weekly nutrition consistency.' },
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-white p-8 rounded-[2.5rem] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border-2 border-transparent hover:border-[#FB923C]/20 transition-all group cursor-pointer"
              >
                <div className="w-12 h-12 rounded-xl bg-[#F8F9FC] text-[#FB923C] flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <feature.icon size={22} />
                </div>
                <h4 className="text-sm font-bold uppercase tracking-wider text-[#1F2937] mb-3">{feature.title}</h4>
                <p className="text-[#6B7280] text-sm font-medium leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Anchor */}
      <section className="relative z-10 py-24">
        <div className="max-w-7xl mx-auto px-6">
          <div className="rounded-[3rem] bg-[#1F2937] p-12 md:p-20 text-center text-white shadow-2xl overflow-hidden relative">
            <div className="relative z-10">
                <h3 className="text-4xl md:text-6xl font-semibold tracking-[-0.03em] mb-6 uppercase">
                Ready to <span className="text-[#FB923C]">Start?</span>
                </h3>
                <p className="text-lg mb-10 max-w-xl mx-auto text-slate-400 font-medium">
                Join thousands achieving their fitness goals with precision mood-based training.
                </p>
                <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => router.push('/login')}
                className="bg-[#FB923C] text-white font-bold text-[11px] uppercase tracking-[0.3em] px-12 py-5 rounded-2xl shadow-xl shadow-orange-900/20"
                >
                Begin Your Journey
                </motion.button>
            </div>
            <div className="absolute top-0 right-0 w-64 h-64 bg-[#FB923C] blur-[120px] opacity-10"></div>
          </div>
        </div>
      </section>

      {/* Footer Branding */}
      <footer className="relative z-10 border-t border-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-[10px] font-bold uppercase tracking-[0.4em] text-[#6B7280]">
            © 2026 FitMood. Engineered for Elite Performance.
          </p>
        </div>
      </footer>
    </main>
  );
}