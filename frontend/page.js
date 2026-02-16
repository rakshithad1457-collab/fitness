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

  const features = [
    {
      icon: '🎯',
      title: 'Mood-Based Training',
      description: 'Workouts that adapt to your energy levels and emotional state',
      gradient: 'from-orange-400 to-pink-500',
    },
    {
      icon: '🍎',
      title: 'Smart Nutrition',
      description: 'Personalized meal plans aligned with your fitness goals',
      gradient: 'from-green-400 to-cyan-500',
    },
    {
      icon: '📊',
      title: 'Progress Tracking',
      description: 'Watch your transformation with detailed insights',
      gradient: 'from-purple-400 to-indigo-500',
    },
    {
      icon: '🔄',
      title: 'Healthy Swaps',
      description: 'Better alternatives for your favorite indulgences',
      gradient: 'from-blue-400 to-teal-500',
    },
  ];

  const stats = [
    { value: '50K+', label: 'Active Users' },
    { value: '500+', label: 'Workouts' },
    { value: '1000+', label: 'Recipes' },
    { value: '4.9⭐', label: 'Rating' },
  ];

  return (
    <main className="relative min-h-screen overflow-hidden bg-white">
      {/* Floating Orbs Background */}
      <div className="floating-orb orb-1"></div>
      <div className="floating-orb orb-2"></div>
      <div className="floating-orb orb-3"></div>

      {/* Navigation */}
      <nav className="relative z-50">
        <div className="container-custom">
          <div className="flex items-center justify-between py-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="flex items-center gap-3"
            >
              <div className="relative">
                <div className="w-12 h-12 rounded-2xl bg-gradient-energy flex items-center justify-center text-white text-2xl font-bold shadow-glow-orange">
                  F
                </div>
                <div className="absolute inset-0 rounded-2xl bg-gradient-energy blur-xl opacity-50"></div>
              </div>
              <h1 className="text-3xl font-display font-bold gradient-text-hero">
                FitMood
              </h1>
            </motion.div>

            <motion.button
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push('/login')}
              className="btn-secondary"
            >
              Sign In
            </motion.button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 py-20 md:py-32">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Content */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-effect mb-6"
              >
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                </span>
                <span className="text-sm font-semibold">Your Personal AI Fitness Coach</span>
              </motion.div>

              <h2 className="text-5xl md:text-6xl lg:text-7xl font-display font-extrabold mb-6 leading-tight">
                Fitness That
                <br />
                <span className="gradient-text-hero">Fits Your Mood</span>
              </h2>
              
              <p className="text-xl text-gray-600 mb-8 leading-relaxed max-w-xl">
                Get personalized workouts and nutrition plans designed around how you feel, 
                what you need, and where you want to go. Transform your body and mind.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-12">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: '0 20px 60px rgba(255, 107, 53, 0.4)' }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => router.push('/login')}
                  className="btn-primary text-lg px-8 py-4"
                >
                  Start Free Today →
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-secondary text-lg px-8 py-4"
                  onClick={() => {
                    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
                  }}
                >
                  Explore Features
                </motion.button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-4 gap-4">
                {stats.map((stat, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 + i * 0.1 }}
                    className="text-center"
                  >
                    <div className="text-2xl font-display font-bold gradient-text mb-1">
                      {stat.value}
                    </div>
                    <div className="text-xs text-gray-600">{stat.label}</div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Right Column - Visual */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="relative"
            >
              <div className="relative">
                {/* Main Card */}
                <div className="card-elevated p-8 relative z-10">
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    {['🏃', '🧘', '🏋️', '🥗'].map((emoji, i) => (
                      <motion.div
                        key={i}
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{ 
                          delay: 0.5 + i * 0.1,
                          type: 'spring',
                          stiffness: 200 
                        }}
                        whileHover={{ scale: 1.1, rotate: 10 }}
                        className="aspect-square rounded-2xl bg-gradient-to-br from-orange-100 to-purple-100 flex items-center justify-center text-5xl cursor-pointer"
                      >
                        {emoji}
                      </motion.div>
                    ))}
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-green-50 to-cyan-50">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center text-white font-bold">
                          ✓
                        </div>
                        <div>
                          <div className="font-semibold text-sm">Today's Workout</div>
                          <div className="text-xs text-gray-600">20 min HIIT</div>
                        </div>
                      </div>
                      <div className="text-2xl">💪</div>
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-purple-50 to-pink-50">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold">
                          7
                        </div>
                        <div>
                          <div className="font-semibold text-sm">Meal Plan Ready</div>
                          <div className="text-xs text-gray-600">Balanced nutrition</div>
                        </div>
                      </div>
                      <div className="text-2xl">🥗</div>
                    </div>
                  </div>
                </div>

                {/* Floating Elements */}
                <motion.div
                  animate={{ y: [-10, 10, -10] }}
                  transition={{ duration: 4, repeat: Infinity }}
                  className="absolute -top-6 -right-6 w-24 h-24 rounded-3xl bg-gradient-energy flex items-center justify-center text-4xl shadow-glow-orange"
                >
                  🔥
                </motion.div>

                <motion.div
                  animate={{ y: [10, -10, 10] }}
                  transition={{ duration: 5, repeat: Infinity }}
                  className="absolute -bottom-6 -left-6 w-20 h-20 rounded-2xl bg-gradient-cosmic flex items-center justify-center text-3xl shadow-glow-purple"
                >
                  ⭐
                </motion.div>

                {/* Glow Effect */}
                <div className="absolute inset-0 bg-gradient-hero opacity-20 blur-3xl -z-10"></div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 py-20 bg-gradient-to-b from-transparent to-gray-50">
        <div className="container-custom">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h3 className="text-4xl md:text-5xl font-display font-bold mb-4">
              Everything You Need,
              <br />
              <span className="gradient-text-cosmic">All in One Place</span>
            </h3>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful features designed to help you achieve your fitness goals faster
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -8, boxShadow: '0 20px 60px rgba(0, 0, 0, 0.1)' }}
                className="card-elevated p-6 group cursor-pointer"
              >
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform`}>
                  {feature.icon}
                </div>
                <h4 className="text-xl font-display font-bold mb-3">{feature.title}</h4>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="relative z-10 py-20">
        <div className="container-custom">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h3 className="text-4xl md:text-5xl font-display font-bold mb-4">
              <span className="gradient-text-cool">Three Simple Steps</span> to Success
            </h3>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              { 
                step: '01', 
                title: 'Tell Us How You Feel', 
                desc: 'Share your mood, energy level, and available time',
                icon: '🎯'
              },
              { 
                step: '02', 
                title: 'Get Your Plan', 
                desc: 'Receive personalized workouts and nutrition guidance',
                icon: '📋'
              },
              { 
                step: '03', 
                title: 'Achieve Your Goals', 
                desc: 'Follow along with videos, recipes, and support',
                icon: '🏆'
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                viewport={{ once: true }}
                className="relative text-center"
              >
                <div className="text-7xl font-display font-black text-transparent bg-clip-text bg-gradient-energy mb-4 opacity-20">
                  {item.step}
                </div>
                <div className="text-6xl mb-4">{item.icon}</div>
                <h4 className="text-xl font-display font-bold mb-2">{item.title}</h4>
                <p className="text-gray-600">{item.desc}</p>
                
                {index < 2 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <div className="text-4xl text-gray-300">→</div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-20">
        <div className="container-custom">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="relative overflow-hidden rounded-3xl bg-gradient-hero p-12 md:p-16 text-center"
          >
            <div className="absolute inset-0 bg-black opacity-5"></div>
            <div className="relative z-10 text-white">
              <h3 className="text-4xl md:text-5xl font-display font-bold mb-6">
                Ready to Transform
                <br />
                Your Fitness Journey?
              </h3>
              <p className="text-lg md:text-xl mb-8 max-w-2xl mx-auto opacity-90">
                Join thousands who are already achieving their goals with FitMood
              </p>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => router.push('/login')}
                className="bg-white text-primary font-display font-bold text-xl px-12 py-5 rounded-2xl shadow-2xl hover:shadow-glow-orange transition-all"
              >
                Start Your Journey Now
              </motion.button>
            </div>

            {/* Decorative Elements */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-gray-200 py-8">
        <div className="container-custom">
          <div className="text-center text-gray-600">
            <p>© 2024 FitMood. Built with passion for your wellness.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}