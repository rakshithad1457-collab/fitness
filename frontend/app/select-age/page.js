'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Baby, User, Users, Crown } from 'lucide-react';
import Navbar from '../components/Navbar';

const AGE_CATEGORIES = [
  {
    id: 'teen',
    label: 'Teen',
    range: '13 – 17',
    icon: Baby,
    tagline: 'Build habits early',
    accent: '#34D399',
    bg: '#ECFDF5',
    description: 'Fun, energizing routines designed for developing bodies.',
  },
  {
    id: 'young_adult',
    label: 'Young Adult',
    range: '18 – 35',
    icon: User,
    tagline: 'Peak performance',
    accent: '#FB923C',
    bg: '#FFF7ED',
    description: 'High-intensity sessions to maximize strength and endurance.',
  },
  {
    id: 'adult',
    label: 'Adult',
    range: '36 – 55',
    icon: Users,
    tagline: 'Stay strong & balanced',
    accent: '#60A5FA',
    bg: '#EFF6FF',
    description: 'Smart training that balances effort with recovery.',
  },
  {
    id: 'senior',
    label: 'Senior',
    range: '56 +',
    icon: Crown,
    tagline: 'Move well, live well',
    accent: '#A78BFA',
    bg: '#F5F3FF',
    description: 'Low-impact, joint-friendly movement for lifelong vitality.',
  },
];

export default function AgePage() {
  const router = useRouter();
  const [selected, setSelected] = useState(null);
  const [hovering, setHovering] = useState(null);

  const handleContinue = () => {
    if (!selected) return;
    router.push(`/workouts?age=${selected}`);
  };

  return (
    <main className="min-h-screen bg-[#F8F9FC] text-[#1F2937] flex flex-col">
      <Navbar />

      <div className="flex-1 max-w-5xl mx-auto w-full px-6 py-16">

        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-14"
        >
          <p className="text-[10px] font-bold uppercase tracking-[0.3em] text-[#FB923C] mb-3">
            Step 1 of 2
          </p>
          <h1 className="text-4xl font-semibold tracking-[0.04em] text-[#1F2937] mb-3">
            SELECT YOUR <span className="text-[#FB923C]">AGE GROUP</span>
          </h1>
          <p className="text-[#6B7280] text-sm font-medium tracking-wide">
            Workouts are calibrated to your life stage for optimal results.
          </p>
        </motion.header>

        {/* Age Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-12">
          {AGE_CATEGORIES.map((cat, i) => {
            const Icon = cat.icon;
            const isActive = selected === cat.id;
            const isHover = hovering === cat.id;

            return (
              <motion.button
                key={cat.id}
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08, duration: 0.4 }}
                whileHover={{ translateY: -6 }}
                whileTap={{ scale: 0.97 }}
                onClick={() => setSelected(cat.id)}
                onHoverStart={() => setHovering(cat.id)}
                onHoverEnd={() => setHovering(null)}
                className={`relative flex flex-col items-start p-7 rounded-[2rem] bg-white text-left transition-all duration-200 cursor-pointer overflow-hidden ${
                  isActive
                    ? 'border-2 shadow-lg scale-[1.02]'
                    : 'border-2 border-transparent shadow-[0_4px_16px_rgba(0,0,0,0.06)]'
                }`}
                style={isActive ? { borderColor: cat.accent } : {}}
              >
                {/* Background glow blob */}
                <div
                  className="absolute top-0 right-0 w-24 h-24 rounded-full -translate-y-6 translate-x-6 transition-all duration-300"
                  style={{
                    background: cat.accent,
                    filter: 'blur(24px)',
                    opacity: isActive || isHover ? 0.35 : 0.15,
                  }}
                />

                {/* Icon */}
                <div
                  className="w-12 h-12 rounded-2xl flex items-center justify-center mb-5"
                  style={{ background: cat.bg }}
                >
                  <Icon size={22} style={{ color: cat.accent }} />
                </div>

                {/* Text */}
                <span
                  className="text-[10px] font-bold uppercase tracking-widest mb-1"
                  style={{ color: cat.accent }}
                >
                  {cat.range} yrs
                </span>
                <h2 className="text-lg font-bold text-[#1F2937] mb-1">{cat.label}</h2>
                <p className="text-xs text-[#6B7280] font-medium italic mb-3">{cat.tagline}</p>
                <p className="text-[11px] text-[#9CA3AF] leading-relaxed">{cat.description}</p>

                {/* Checkmark when selected */}
                <AnimatePresence>
                  {isActive && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      exit={{ scale: 0 }}
                      className="absolute top-5 right-5 w-6 h-6 rounded-full flex items-center justify-center"
                      style={{ background: cat.accent }}
                    >
                      <svg width="11" height="8" viewBox="0 0 11 8" fill="none">
                        <path
                          d="M1 3.5L4 6.5L10 1"
                          stroke="white"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.button>
            );
          })}
        </div>

        {/* Continue Button */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="flex justify-center"
        >
          <motion.button
            whileHover={{ scale: selected ? 1.02 : 1 }}
            whileTap={{ scale: selected ? 0.98 : 1 }}
            onClick={handleContinue}
            disabled={!selected}
            className={`flex items-center gap-3 px-14 py-5 rounded-2xl font-bold uppercase tracking-[0.2em] text-sm transition-all duration-300 ${
              selected
                ? 'bg-gradient-to-r from-[#FB923C] to-[#F97316] text-white shadow-[0_8px_20px_rgba(249,115,22,0.3)] hover:shadow-[0_12px_28px_rgba(249,115,22,0.4)]'
                : 'bg-[#E5E7EB] text-[#9CA3AF] cursor-not-allowed'
            }`}
          >
            Continue to Mood
            <ArrowRight size={16} />
          </motion.button>
        </motion.div>

        {/* Step dots */}
        <div className="flex justify-center gap-2 mt-10">
          <span className="w-8 h-1.5 rounded-full bg-[#FB923C]" />
          <span className="w-8 h-1.5 rounded-full bg-[#E5E7EB]" />
        </div>

      </div>
    </main>
  );
}