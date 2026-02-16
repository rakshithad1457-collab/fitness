'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function Home() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <main className="relative min-h-screen overflow-hidden bg-white">
      {/* Background Orbs */}
      <div className="floating-orb orb-1"></div>
      <div className="floating-orb orb-2"></div>
      <div className="floating-orb orb-3"></div>

      {/* Navigation */}
      <nav className="relative z-50 py-6">
        <div className="container-custom">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                F
              </div>
              <h1 className="text-2xl font-bold gradient-text-hero">FitMood</h1>
            </div>

            <button
              onClick={() => router.push('/login')}
              className="btn-secondary px-6 py-2.5"
            >
              Sign In
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 py-16 md:py-24">
        <div className="container-custom">
          <div className="text-center max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-50 border border-green-200 mb-8">
                <span className="flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                <span className="text-sm font-semibold text-green-700">Your Personal Fitness Companion</span>
              </div>

              <h2 className="text-5xl md:text-6xl lg:text-7xl font-extrabold mb-6 leading-tight">
                Fitness That
                <br />
                <span className="gradient-text-hero">Fits Your Mood</span>
              </h2>
              
              <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
                Get personalized workouts and nutrition plans designed around how you feel, 
                what you need, and where you want to go.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
                <button
                  onClick={() => router.push('/login')}
                  className="btn-primary text-lg px-8 py-4"
                >
                  Get Started Free →
                </button>
                
                <button
                  className="btn-secondary text-lg px-8 py-4"
                  onClick={() => {
                    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
                  }}
                >
                  Learn More
                </button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto">
                {[
                  { value: '10K+', label: 'Active Users' },
                  { value: '500+', label: 'Workouts' },
                  { value: '1000+', label: 'Recipes' },
                  { value: '4.9★', label: 'Rating' },
                ].map((stat, i) => (
                  <div key={i} className="text-center">
                    <div className="text-3xl font-bold gradient-text mb-1">{stat.value}</div>
                    <div className="text-sm text-gray-600">{stat.label}</div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="relative z-10 py-20 bg-gray-50">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h3 className="text-4xl md:text-5xl font-bold mb-4">
              Everything You Need,
              <br />
              <span className="gradient-text-cosmic">All in One Place</span>
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: '🎯',
                title: 'Mood-Based Workouts',
                desc: 'Exercises that match your energy',
                color: 'from-orange-400 to-pink-500',
              },
              {
                icon: '🍎',
                title: 'Smart Nutrition',
                desc: 'Personalized meal plans for your goals',
                color: 'from-green-400 to-cyan-500',
              },
              {
                icon: '📅',
                title: '7-Day Meal Plans',
                desc: 'Complete weekly nutrition guidance',
                color: 'from-purple-400 to-indigo-500',
              },
              {
                icon: '🔄',
                title: 'Healthy Swaps',
                desc: 'Better alternatives for cravings',
                color: 'from-blue-400 to-teal-500',
              },
            ].map((feature, index) => (
              <div
                key={index}
                className="card-elevated p-6 cursor-pointer group"
              >
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform`}>
                  {feature.icon}
                </div>
                <h4 className="text-lg font-bold mb-2">{feature.title}</h4>
                <p className="text-gray-600 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="relative z-10 py-20">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h3 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="gradient-text-cool">Simple Steps</span> to Success
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              { icon: '🎯', title: 'Tell Us How You Feel', desc: 'Share your mood and energy level' },
              { icon: '📋', title: 'Get Your Plan', desc: 'Receive personalized recommendations' },
              { icon: '🏆', title: 'Achieve Goals', desc: 'Follow along and see results' },
            ].map((step, i) => (
              <div key={i} className="text-center">
                <div className="text-6xl mb-4">{step.icon}</div>
                <h4 className="text-xl font-bold mb-2">{step.title}</h4>
                <p className="text-gray-600">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 py-20">
        <div className="container-custom">
          <div className="rounded-3xl bg-gradient-to-r from-orange-500 to-purple-600 p-12 md:p-16 text-center text-white">
            <h3 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Start?
            </h3>
            <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
              Join thousands achieving their fitness goals
            </p>
            <button
              onClick={() => router.push('/login')}
              className="bg-white text-orange-600 font-bold text-xl px-10 py-4 rounded-xl hover:scale-105 transition-transform"
            >
              Get Started Now
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t py-8">
        <div className="container-custom text-center text-gray-600">
          <p>© 2024 FitMood. Built with passion for your wellness.</p>
        </div>
      </footer>
    </main>
  );
}
