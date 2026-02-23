'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, Flame, ChevronDown, ChevronUp, Users } from 'lucide-react';

// ── Recipe Card ──────────────────────────────────────────────────────────────

export function RecipeCard({ recipe }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-[0_4px_12px_rgba(0,0,0,0.06)] overflow-hidden"
    >
      <div className="p-6">
        <div className="flex items-start gap-4 mb-4">
          <span className="text-4xl">{recipe.icon}</span>
          <div className="flex-1">
            <h3 className="font-bold text-sm uppercase tracking-tight text-[#1F2937] mb-1">
              {recipe.name}
            </h3>
            <p className="text-[#6B7280] text-xs leading-relaxed">{recipe.description}</p>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {(recipe.dietary_tags || []).map((tag, i) => (
            <span key={i} className="px-2 py-0.5 bg-[#F0FDF4] text-[#16A34A] text-[10px] font-bold uppercase tracking-wider rounded-md">
              {tag}
            </span>
          ))}
        </div>

        {/* Stats */}
        <div className="flex gap-5">
          <div className="flex items-center gap-1 text-[11px] font-bold text-[#6B7280] uppercase">
            <Flame size={11} className="text-[#FB923C]" /> {recipe.calories} kcal
          </div>
          <div className="flex items-center gap-1 text-[11px] font-bold text-[#6B7280] uppercase">
            <Clock size={11} /> {recipe.prep_time} min
          </div>
          <div className="flex items-center gap-1 text-[11px] font-bold text-[#6B7280] uppercase">
            <Users size={11} /> {recipe.servings} {recipe.servings === 1 ? 'serving' : 'servings'}
          </div>
        </div>
      </div>

      {/* Expand toggle */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-6 py-3 bg-[#F8F9FC] text-[11px] font-bold uppercase tracking-widest text-[#6B7280] hover:bg-gray-100 transition-colors"
      >
        {expanded ? 'Hide Recipe' : 'View Full Recipe'}
        {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="p-6 grid md:grid-cols-2 gap-6 border-t border-gray-100">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-widest text-[#1F2937] mb-3">Ingredients</h4>
                <ul className="space-y-1.5">
                  {(recipe.ingredients || []).map((ing, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-[#374151]">
                      <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[#FB923C] shrink-0" />
                      {ing}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-xs font-bold uppercase tracking-widest text-[#1F2937] mb-3">Instructions</h4>
                <ol className="space-y-2">
                  {(recipe.instructions || []).map((step, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-[#374151]">
                      <span className="w-5 h-5 rounded-full bg-[#1F2937] text-white text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                        {i + 1}
                      </span>
                      {step}
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}


// ── Meal Plan Day Card ────────────────────────────────────────────────────────

export function MealPlanCard({ day }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-[0_4px_12px_rgba(0,0,0,0.06)] overflow-hidden"
    >
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-6 text-left hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-[#1F2937] text-white flex items-center justify-center font-bold text-sm shrink-0">
            {day.day}
          </div>
          <div>
            <h3 className="font-bold text-sm uppercase tracking-tight text-[#1F2937]">{day.day_name}</h3>
            <p className="text-[11px] text-[#6B7280] font-bold uppercase tracking-wider mt-0.5">
              {day.total_calories} kcal total
            </p>
          </div>
        </div>
        {expanded ? <ChevronUp size={16} className="text-[#6B7280]" /> : <ChevronDown size={16} className="text-[#6B7280]" />}
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-5 space-y-3 border-t border-gray-100 pt-4">
              {(day.meals || []).map((meal, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-[#F8F9FC] rounded-xl">
                  <div className="flex items-center gap-3">
                    <span className="text-xl">{meal.icon}</span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-bold uppercase tracking-widest text-[#FB923C]">{meal.meal_type}</span>
                        <span className="text-[10px] text-[#9CA3AF]">{meal.time}</span>
                      </div>
                      <p className="font-semibold text-sm text-[#1F2937]">{meal.name}</p>
                      <p className="text-[11px] text-[#6B7280] mt-0.5">{meal.quick_recipe}</p>
                      <div className="flex gap-3 mt-1">
                        <span className="text-[10px] text-[#9CA3AF]">P: {meal.protein}g</span>
                        <span className="text-[10px] text-[#9CA3AF]">C: {meal.carbs}g</span>
                        <span className="text-[10px] text-[#9CA3AF]">F: {meal.fats}g</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right shrink-0 ml-4">
                    <p className="font-bold text-sm text-[#1F2937]">{meal.calories}</p>
                    <p className="text-[10px] text-[#6B7280] uppercase">kcal</p>
                  </div>
                </div>
              ))}

              {/* Tip */}
              <div className="flex items-start gap-2 p-3 bg-[#FFF7ED] rounded-xl">
                <span className="text-base">💡</span>
                <p className="text-xs text-[#92400E] font-medium">{day.tips}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}


// ── Healthy Swap Card ─────────────────────────────────────────────────────────

export function SwapCard({ swap }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white p-5 rounded-2xl shadow-[0_4px_12px_rgba(0,0,0,0.06)] flex items-start gap-4"
    >
      <span className="text-3xl shrink-0">{swap.icon}</span>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-1">
          <h3 className="font-bold text-sm text-[#1F2937]">{swap.name}</h3>
          <span className="text-[10px] font-bold text-[#FB923C] uppercase">{swap.calories} kcal</span>
        </div>
        <p className="text-xs text-[#6B7280] mb-2">{swap.description}</p>
        <div className="flex flex-wrap gap-1">
          {(swap.benefits || []).map((b, i) => (
            <span key={i} className="px-2 py-0.5 bg-[#F0FDF4] text-[#16A34A] text-[10px] font-bold rounded-md">{b}</span>
          ))}
        </div>
      </div>
    </motion.div>
  );
}