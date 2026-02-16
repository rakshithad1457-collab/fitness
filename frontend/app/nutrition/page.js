'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
// FIXED: Updated paths for components moved into the app folder
import Navbar from '@/components/Navbar';
import RecipeCard from '@/components/RecipeCard';
import MealPlanCard from '@/components/MealPlanCard';
import { nutritionAPI, authAPI } from '@/lib/api';

function NutritionContent() {
  const [activeTab, setActiveTab] = useState('recipes');
  const [goal, setGoal] = useState('');
  const [dietaryRestrictions, setDietaryRestrictions] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);

  const toggleRestriction = (r) => {
    setDietaryRestrictions(prev => 
      prev.includes(r) ? prev.filter(item => item !== r) : [...prev, r]
    );
  };

  const handleFetchRecipes = async () => {
    if (!goal) return alert("Please select a goal");
    setLoading(true);
    try {
      const data = await nutritionAPI.getRecipes(goal, dietaryRestrictions);
      setRecipes(data.recipes || []);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold mb-6">Smart Nutrition</h1>
        
        {/* Category Tabs */}
        <div className="flex gap-4 mb-8">
          {['recipes', 'meal-plan', 'swaps'].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)} 
              className={`px-6 py-2 rounded-full font-bold ${activeTab === tab ? 'bg-orange-500 text-white' : 'bg-white border'}`}>
              {tab.replace('-', ' ').toUpperCase()}
            </button>
          ))}
        </div>

        {/* Goal & Restriction Selection */}
        <div className="bg-white p-6 rounded-2xl shadow-sm mb-10">
          <h2 className="font-bold mb-4">Select Goal & Restrictions</h2>
          <div className="flex flex-wrap gap-4 mb-6">
            {['weight_loss', 'muscle_gain', 'maintenance'].map(g => (
              <button key={g} onClick={() => setGoal(g)} 
                className={`px-4 py-2 rounded-lg border ${goal === g ? 'border-orange-500 bg-orange-50' : ''}`}>
                {g.replace('_', ' ')}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            {['vegan', 'vegetarian', 'keto', 'gluten_free'].map(r => (
              <button key={r} onClick={() => toggleRestriction(r)}
                className={`px-3 py-1 rounded-full text-sm border ${dietaryRestrictions.includes(r) ? 'bg-green-500 text-white' : ''}`}>
                {r}
              </button>
            ))}
          </div>
          <button onClick={handleFetchRecipes} className="mt-6 w-full bg-orange-600 text-white py-3 rounded-xl font-bold">
            {loading ? 'Loading...' : 'Get Personalized Results'}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map((r, i) => <RecipeCard key={i} recipe={r} index={i} />)}
        </div>
      </div>
    </main>
  );
}

export default function NutritionPage() {
  return <Suspense fallback={<div>Loading...</div>}><NutritionContent /></Suspense>;
}