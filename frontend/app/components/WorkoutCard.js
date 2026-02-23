/**
 * WorkoutCard.jsx
 * ---------------
 * Displays a mood-based workout plan and opens the matched
 * YouTube workout video when the button is pressed.
 *
 * Props:
 *   workout  - object returned by POST /api/workouts/mood-based
 *   onRetry  - optional callback to go back and re-generate
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Linking,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';

// ── Mood colour/emoji config ────────────────────────────────────────────────

const MOOD_META = {
  happy:     { emoji: '😊', bg: '#FFF3CD', accent: '#F59E0B' },
  stressed:  { emoji: '😤', bg: '#E8F5E9', accent: '#22C55E' },
  tired:     { emoji: '😴', bg: '#EDE9FE', accent: '#7C3AED' },
  energetic: { emoji: '⚡', bg: '#FEE2E2', accent: '#EF4444' },
  anxious:   { emoji: '😰', bg: '#E0F2FE', accent: '#0EA5E9' },
  sad:       { emoji: '😢', bg: '#FDF4FF', accent: '#A855F7' },
  neutral:   { emoji: '😐', bg: '#F1F5F9', accent: '#64748B' },
  motivated: { emoji: '💪', bg: '#FFF1F2', accent: '#F43F5E' },
};

const INTENSITY_COLOURS = {
  low:      { bg: '#DCFCE7', text: '#166534' },
  moderate: { bg: '#FEF9C3', text: '#713F12' },
  high:     { bg: '#FEE2E2', text: '#991B1B' },
};

// ── Component ───────────────────────────────────────────────────────────────

export default function WorkoutCard({ workout, onRetry }) {
  const [launching, setLaunching] = useState(false);

  if (!workout) return null;

  const meta = MOOD_META[workout.mood] ?? MOOD_META.neutral;
  const intensityKey = workout.intensity ?? 'moderate';
  const intensityStyle = INTENSITY_COLOURS[intensityKey] ?? INTENSITY_COLOURS.moderate;

  const handleYouTubePress = async () => {
    setLaunching(true);
    try {
      const canOpen = await Linking.canOpenURL(workout.youtube_url);
      if (canOpen) {
        await Linking.openURL(workout.youtube_url);
      } else {
        Alert.alert('Error', 'Unable to open YouTube. Please check your settings.');
      }
    } catch {
      Alert.alert('Error', 'Something went wrong opening YouTube.');
    } finally {
      setLaunching(false);
    }
  };

  return (
    <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>

      {/* ── Header ── */}
      <View style={[styles.headerCard, { backgroundColor: meta.bg }]}>
        <Text style={styles.emoji}>{meta.emoji}</Text>
        <Text style={[styles.title, { color: meta.accent }]}>{workout.title}</Text>
        <Text style={styles.description}>{workout.description}</Text>

        <View style={styles.pillsRow}>
          <View style={[styles.pill, { backgroundColor: meta.accent }]}>
            <Text style={styles.pillText}>🕐 {workout.duration_minutes} min</Text>
          </View>
          <View style={[styles.pill, { backgroundColor: intensityStyle.bg }]}>
            <Text style={[styles.pillText, { color: intensityStyle.text }]}>
              {intensityKey.charAt(0).toUpperCase() + intensityKey.slice(1)} intensity
            </Text>
          </View>
        </View>
      </View>

      {/* ── Exercises ── */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Your Exercises</Text>
        {workout.exercises.map((ex, idx) => (
          <View key={idx} style={styles.exerciseRow}>
            <View style={[styles.indexBadge, { backgroundColor: meta.accent }]}>
              <Text style={styles.indexText}>{idx + 1}</Text>
            </View>
            <View style={styles.exerciseInfo}>
              <Text style={styles.exerciseName}>{ex.name}</Text>
              <Text style={styles.exerciseMeta}>
                {ex.sets} {ex.sets === 1 ? 'set' : 'sets'} · {ex.reps_or_duration}
              </Text>
            </View>
          </View>
        ))}
      </View>

      {/* ── YouTube CTA ── */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Follow Along on YouTube</Text>
        <Text style={styles.ytHint}>
          Searching for:{' '}
          <Text style={styles.ytQuery}>"{workout.youtube_query}"</Text>
        </Text>

        <TouchableOpacity
          style={styles.ytButton}
          onPress={handleYouTubePress}
          activeOpacity={0.85}
          disabled={launching}
        >
          {launching ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <>
              <Text style={styles.ytIcon}>▶</Text>
              <Text style={styles.ytButtonText}>Open YouTube Workout</Text>
            </>
          )}
        </TouchableOpacity>
      </View>

      {/* ── Retry ── */}
      {onRetry && (
        <TouchableOpacity style={styles.retryButton} onPress={onRetry}>
          <Text style={styles.retryText}>↺  Try a Different Workout</Text>
        </TouchableOpacity>
      )}

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

// ── Styles ──────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  scroll: {
    flex: 1,
    paddingHorizontal: 16,
  },
  headerCard: {
    borderRadius: 20,
    padding: 24,
    marginTop: 16,
    marginBottom: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
    elevation: 4,
  },
  emoji: {
    fontSize: 52,
    marginBottom: 8,
  },
  title: {
    fontSize: 22,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 6,
  },
  description: {
    fontSize: 14,
    color: '#555',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 14,
  },
  pillsRow: {
    flexDirection: 'row',
    gap: 8,
  },
  pill: {
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 20,
  },
  pillText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: 12,
  },
  exerciseRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f1f5f9',
  },
  indexBadge: {
    width: 30,
    height: 30,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  indexText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 13,
  },
  exerciseInfo: {
    flex: 1,
  },
  exerciseName: {
    fontSize: 15,
    fontWeight: '600',
    color: '#1e293b',
  },
  exerciseMeta: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 2,
  },
  ytHint: {
    fontSize: 13,
    color: '#64748b',
    marginBottom: 12,
  },
  ytQuery: {
    fontStyle: 'italic',
    color: '#334155',
  },
  ytButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FF0000',
    paddingVertical: 14,
    borderRadius: 12,
    gap: 8,
  },
  ytIcon: {
    color: '#fff',
    fontSize: 16,
  },
  ytButtonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 16,
  },
  retryButton: {
    alignItems: 'center',
    paddingVertical: 14,
  },
  retryText: {
    color: '#64748b',
    fontSize: 14,
    fontWeight: '600',
  },
});