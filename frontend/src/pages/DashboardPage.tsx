import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Flame,
  Zap,
  CheckCircle2,
  XCircle,
  ArrowRight,
  TrendingUp,
  Award,
  BookOpen,
  Code2,
  Clock,
  Sparkles,
  Play,
  AlertTriangle,
  Compass,
  Filter,
  Layers,
  Link2,
  GitFork,
  Calculator,
  ArrowDownUp,
  ShieldCheck,
  Crown,
  Target,
  BarChart2,
  Check,
  RefreshCw,
} from 'lucide-react';
import { progressService, ProgressSummary, BadgeInfo } from '../services/progressService';
import { Badge } from '../components/common/Badge';

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<ProgressSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'levels' | 'topics' | 'badges'>('levels');

  const loadProgress = () => {
    setIsLoading(true);
    progressService.getSummary()
      .then((data) => setSummary(data))
      .catch((err) => console.error('Failed to load dashboard progress:', err))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    loadProgress();
  }, []);

  const getBadgeIcon = (iconName: string) => {
    switch (iconName) {
      case 'Flame': return <Flame className="w-5 h-5 text-amber-400" />;
      case 'Crown': return <Crown className="w-5 h-5 text-amber-300" />;
      case 'Compass': return <Compass className="w-5 h-5 text-emerald-400" />;
      case 'Filter': return <Filter className="w-5 h-5 text-blue-400" />;
      case 'Layers': return <Layers className="w-5 h-5 text-purple-400" />;
      case 'Link2': return <Link2 className="w-5 h-5 text-cyan-400" />;
      case 'GitFork': return <GitFork className="w-5 h-5 text-teal-400" />;
      case 'Calculator': return <Calculator className="w-5 h-5 text-indigo-400" />;
      case 'ArrowDownUp': return <ArrowDownUp className="w-5 h-5 text-orange-400" />;
      case 'BarChart3': return <BarChart2 className="w-5 h-5 text-sky-400" />;
      case 'ShieldCheck': return <ShieldCheck className="w-5 h-5 text-rose-400" />;
      case 'Sparkles': return <Sparkles className="w-5 h-5 text-yellow-400" />;
      default: return <Award className="w-5 h-5 text-brand-400" />;
    }
  };

  if (isLoading || !summary) {
    return (
      <div className="min-h-screen bg-dark-950 flex items-center justify-center text-dark-300">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm font-medium">Loading learner progress & performance metrics...</p>
        </div>
      </div>
    );
  }

  const { user } = summary;

  return (
    <div className="min-h-screen bg-dark-950 text-dark-100 py-10">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* 1. Welcome & Rank Banner */}
        <div className="relative overflow-hidden rounded-2xl border border-dark-800 bg-gradient-to-r from-dark-900 via-dark-900/90 to-dark-950 p-6 sm:p-8">
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-center gap-5">
              <div className="relative">
                <img
                  src={user.avatar_url}
                  alt={user.name}
                  className="w-16 h-16 rounded-full object-cover ring-4 ring-brand-500/20"
                />
                <div className="absolute -bottom-1 -right-1 p-1 rounded-full bg-dark-900 border border-dark-700">
                  <Flame className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                </div>
              </div>
              <div className="space-y-1">
                <div className="flex flex-wrap items-center gap-2">
                  <h1 className="text-2xl font-extrabold text-white tracking-tight">
                    {user.name}
                  </h1>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-mono font-semibold">
                    {user.level_title}
                  </span>
                </div>
                <p className="text-xs text-dark-400">
                  Current Rank: <span className="text-dark-200 font-semibold">Tier {user.rank_level}</span> • Progress to Next Rank: <span className="text-brand-400 font-mono">{user.xp} / {user.next_rank_xp} XP</span> ({user.rank_progress_percentage}%)
                </p>

                {/* Rank Progress Bar */}
                <div className="w-64 max-w-full bg-dark-800 rounded-full h-1.5 overflow-hidden mt-2">
                  <div
                    className="bg-gradient-to-r from-brand-500 to-emerald-400 h-1.5 rounded-full transition-all duration-500"
                    style={{ width: `${Math.max(user.rank_progress_percentage, 5)}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex items-center gap-3">
              {summary.recommended_topic && (
                <Link
                  to={summary.recommended_topic.lesson_url}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-brand-500 hover:bg-brand-400 text-dark-950 font-bold text-xs shadow-lg shadow-brand-500/20 transition-all"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Resume Curriculum</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              )}
            </div>
          </div>

          <div className="absolute top-0 right-0 w-96 h-96 bg-brand-500/5 rounded-full blur-3xl pointer-events-none" />
        </div>

        {/* 2. Top-Level Motivation & Analytics KPI Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          {/* Card 1: Daily Streak & Activity */}
          <div className="p-5 rounded-xl border border-dark-800 bg-dark-900/60 space-y-3">
            <div className="flex items-center justify-between text-xs text-dark-400">
              <span className="font-semibold uppercase tracking-wider">Active Streak</span>
              <Flame className="w-4 h-4 text-amber-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white font-mono">{user.streak_days}</span>
              <span className="text-xs text-dark-400">days streak</span>
            </div>
            
            {/* 7-Day Activity Strip */}
            <div className="pt-1 border-t border-dark-800/80">
              <div className="flex items-center justify-between text-[10px] text-dark-400 mb-1">
                <span>Past 7 Days</span>
                <span className="font-mono text-dark-300">Best: {user.longest_streak}d</span>
              </div>
              <div className="flex items-center justify-between gap-1">
                {summary.weekly_activity.map((day, idx) => (
                  <div key={idx} className="flex flex-col items-center gap-1">
                    <div
                      className={`w-6 h-6 rounded flex items-center justify-center text-[10px] font-mono transition-all ${
                        day.active
                          ? 'bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold'
                          : 'bg-dark-800/50 border border-dark-800 text-dark-500'
                      }`}
                      title={`${day.date}: ${day.submissions_count} queries executed`}
                    >
                      {day.day_name[0]}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Card 2: Questions Solved & Attempted */}
          <div className="p-5 rounded-xl border border-dark-800 bg-dark-900/60 space-y-3">
            <div className="flex items-center justify-between text-xs text-dark-400">
              <span className="font-semibold uppercase tracking-wider">Questions Solved</span>
              <Code2 className="w-4 h-4 text-brand-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white font-mono">{summary.solved_questions_count}</span>
              <span className="text-xs text-dark-400">/ {summary.total_questions} total ({summary.attempted_questions_count} tried)</span>
            </div>
            
            {/* Difficulty Breakdown */}
            <div className="pt-1 border-t border-dark-800/80 flex items-center justify-between text-[11px] font-mono">
              <span className="text-emerald-400">{summary.easy_solved}/{summary.easy_total} Easy</span>
              <span className="text-dark-600">•</span>
              <span className="text-amber-400">{summary.medium_solved}/{summary.medium_total} Med</span>
              <span className="text-dark-600">•</span>
              <span className="text-rose-400">{summary.hard_solved}/{summary.hard_total} Hard</span>
            </div>
          </div>

          {/* Card 3: Accuracy & Submissions */}
          <div className="p-5 rounded-xl border border-dark-800 bg-dark-900/60 space-y-3">
            <div className="flex items-center justify-between text-xs text-dark-400">
              <span className="font-semibold uppercase tracking-wider">Query Accuracy</span>
              <Target className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white font-mono">{summary.submission_accuracy_percentage}%</span>
              <span className="text-xs text-dark-400">pass rate</span>
            </div>
            <div className="pt-1 border-t border-dark-800/80 text-[11px] text-dark-400 flex items-center justify-between">
              <span>{summary.accepted_submissions} passed / {summary.total_submissions} submissions</span>
            </div>
          </div>

          {/* Card 4: Curriculum Progress & XP */}
          <div className="p-5 rounded-xl border border-dark-800 bg-dark-900/60 space-y-3">
            <div className="flex items-center justify-between text-xs text-dark-400">
              <span className="font-semibold uppercase tracking-wider">Curriculum Mastery</span>
              <Zap className="w-4 h-4 text-yellow-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white font-mono">{summary.overall_progress_percentage}%</span>
              <span className="text-xs text-dark-400">overall</span>
            </div>
            <div className="pt-1 border-t border-dark-800/80 text-[11px] text-dark-400 flex items-center justify-between">
              <span className="text-brand-400 font-mono font-semibold">{user.xp} Total XP</span>
              <span className="text-dark-400">{summary.completed_topics_count}/{summary.total_topics_count} Topics</span>
            </div>
          </div>

        </div>

        {/* 3. Recommended Next Topic & Weak Topics Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          
          {/* Smart Recommendation Card */}
          {summary.recommended_topic && (
            <div className="p-5 rounded-xl border border-brand-500/30 bg-gradient-to-br from-brand-500/5 via-dark-900/70 to-dark-950 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-semibold uppercase tracking-wider text-[10px]">
                  <Sparkles className="w-3 h-3" />
                  Recommended Next Step
                </span>
                <span className="text-dark-400 font-mono text-[11px]">{summary.recommended_topic.level_title}</span>
              </div>

              <div>
                <h3 className="text-base font-bold text-white">
                  {summary.recommended_topic.title}
                </h3>
                <p className="text-xs text-dark-300 mt-1 leading-relaxed">
                  {summary.recommended_topic.reason}
                </p>
              </div>

              <div className="pt-2 flex items-center gap-3">
                <Link
                  to={summary.recommended_topic.lesson_url}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-400 text-dark-950 font-bold text-xs transition-colors"
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Study Concept</span>
                </Link>
                <Link
                  to={summary.recommended_topic.practice_url}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-dark-800 hover:bg-dark-700 text-white font-medium text-xs border border-dark-700 transition-colors"
                >
                  <Code2 className="w-3.5 h-3.5 text-brand-400" />
                  <span>Practice Questions</span>
                </Link>
              </div>
            </div>
          )}

          {/* Weak Topics Identification Alert */}
          <div className="p-5 rounded-xl border border-dark-800 bg-dark-900/60 space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="inline-flex items-center gap-1.5 font-semibold uppercase tracking-wider text-dark-400 text-[10px]">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                Targeted Weak Areas & Reinforcement
              </span>
              <span className="text-[11px] text-dark-500 font-mono">
                {summary.weak_topics.length} Areas Flagged
              </span>
            </div>

            {summary.weak_topics.length === 0 ? (
              <div className="py-6 text-center space-y-1.5">
                <CheckCircle2 className="w-8 h-8 text-emerald-400/80 mx-auto" />
                <p className="text-xs font-semibold text-white">Strong Concept Retention</p>
                <p className="text-[11px] text-dark-400 max-w-sm mx-auto">
                  No recurring query failures or syntax bottlenecks detected. Continue challenging harder levels!
                </p>
              </div>
            ) : (
              <div className="space-y-2.5">
                {summary.weak_topics.slice(0, 2).map((wt) => (
                  <div
                    key={wt.topic_slug}
                    className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/20 flex items-center justify-between gap-3 text-xs"
                  >
                    <div className="space-y-0.5">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-amber-300">{wt.title}</span>
                        <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-500/10 text-amber-400 font-mono">
                          {wt.failed_attempts_count} failed queries
                        </span>
                      </div>
                      <p className="text-[11px] text-dark-400">
                        {wt.reason}
                      </p>
                    </div>

                    <Link
                      to={wt.lesson_url}
                      className="shrink-0 px-3 py-1.5 rounded bg-dark-800 hover:bg-dark-700 text-white font-medium text-[11px] border border-dark-700 transition-colors"
                    >
                      Review
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        {/* 4. Tab Navigation: Curriculum Levels, Topic Progress, Badges Showcase */}
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b border-dark-800 pb-3">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('levels')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  activeTab === 'levels'
                    ? 'bg-brand-500 text-dark-950'
                    : 'text-dark-400 hover:text-white bg-dark-900 border border-dark-800'
                }`}
              >
                Curriculum Levels ({summary.level_progress.length})
              </button>
              <button
                onClick={() => setActiveTab('topics')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  activeTab === 'topics'
                    ? 'bg-brand-500 text-dark-950'
                    : 'text-dark-400 hover:text-white bg-dark-900 border border-dark-800'
                }`}
              >
                All Topics ({summary.topic_progress.length})
              </button>
              <button
                onClick={() => setActiveTab('badges')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 ${
                  activeTab === 'badges'
                    ? 'bg-brand-500 text-dark-950'
                    : 'text-dark-400 hover:text-white bg-dark-900 border border-dark-800'
                }`}
              >
                <Award className="w-3.5 h-3.5" />
                <span>Earned Badges ({summary.badges.length})</span>
              </button>
            </div>

            <Link to="/curriculum" className="text-xs text-brand-400 hover:text-brand-300 font-medium flex items-center gap-1">
              <span>View Full Roadmap</span>
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* TAB 1: Curriculum Levels */}
          {activeTab === 'levels' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {summary.level_progress.map((lvl) => (
                <div
                  key={lvl.level_number}
                  className="p-4 rounded-xl border border-dark-800 bg-dark-900/40 space-y-3"
                >
                  <div className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded bg-dark-800 text-brand-400 font-mono font-bold flex items-center justify-center text-[11px]">
                        L{lvl.level_number}
                      </span>
                      <span className="font-bold text-white text-sm">{lvl.title}</span>
                    </div>
                    {lvl.is_completed ? (
                      <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        <CheckCircle2 className="w-3 h-3" /> Mastered
                      </span>
                    ) : (
                      <span className="text-[11px] font-mono text-dark-400">
                        {lvl.completed_topics} / {lvl.total_topics} Topics ({lvl.completion_percentage}%)
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-dark-400 leading-relaxed line-clamp-2">
                    {lvl.description}
                  </p>

                  <div className="w-full bg-dark-800 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full transition-all duration-500 ${
                        lvl.is_completed ? 'bg-emerald-400' : 'bg-brand-500'
                      }`}
                      style={{ width: `${Math.max(lvl.completion_percentage, 5)}%` }}
                    />
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-dark-400 pt-1">
                    <span>{lvl.solved_questions} / {lvl.total_questions} Questions Solved</span>
                    {lvl.milestone_badge ? (
                      <span className="text-amber-400 font-medium flex items-center gap-1">
                        <Award className="w-3 h-3" /> Milestone Earned
                      </span>
                    ) : (
                      <span className="text-dark-500">+250 XP Milestone on Completion</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB 2: All Topics Progression */}
          {activeTab === 'topics' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {summary.topic_progress.map((t) => (
                <div
                  key={t.topic_slug}
                  className="p-3.5 rounded-lg border border-dark-800 bg-dark-900/40 space-y-2 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-brand-400 uppercase">
                      Level {t.level_number}
                    </span>
                    {t.is_completed && (
                      <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-400">
                        <Check className="w-3 h-3" /> Completed
                      </span>
                    )}
                  </div>

                  <h4 className="font-bold text-white text-xs truncate">
                    {t.title}
                  </h4>

                  <div className="flex items-center justify-between text-[11px] text-dark-400">
                    <span>{t.solved_questions} / {t.total_questions} Solved</span>
                    <span>{t.completion_rate}% Done</span>
                  </div>

                  <div className="pt-2 flex items-center gap-2 border-t border-dark-800">
                    <Link
                      to={`/lesson/${t.topic_slug}`}
                      className="text-[11px] text-dark-300 hover:text-white font-medium"
                    >
                      Lesson
                    </Link>
                    <span className="text-dark-600">•</span>
                    <Link
                      to={`/practice/${t.topic_slug}`}
                      className="text-[11px] text-brand-400 hover:text-brand-300 font-medium"
                    >
                      Practice &rarr;
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB 3: Badges Showcase */}
          {activeTab === 'badges' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {summary.badges.map((b) => (
                <div
                  key={b.key}
                  className="p-4 rounded-xl border border-dark-800 bg-dark-900/50 flex items-start gap-3.5"
                >
                  <div className="p-2.5 rounded-lg bg-dark-800 border border-dark-700 shrink-0">
                    {getBadgeIcon(b.icon)}
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h4 className="text-xs font-bold text-white">{b.title}</h4>
                      <span className="text-[9px] px-1.5 py-0.2 rounded bg-brand-500/10 text-brand-400 font-mono uppercase">
                        {b.badge_type}
                      </span>
                    </div>
                    <p className="text-[11px] text-dark-400 leading-relaxed">
                      {b.description}
                    </p>
                    <p className="text-[10px] text-dark-500 font-mono">
                      Earned {new Date(b.earned_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 5. Live Recent Submissions Audit Table */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-cyan-400" />
              Recent Execution Submissions
            </h2>
            <span className="text-xs text-dark-400 font-mono">
              Persistently Recorded in DB
            </span>
          </div>

          <div className="rounded-xl border border-dark-800 bg-dark-900/40 overflow-hidden">
            {summary.recent_submissions.length === 0 ? (
              <p className="text-xs text-dark-400 py-8 text-center">No recent submissions recorded.</p>
            ) : (
              <div className="divide-y divide-dark-800/60">
                {summary.recent_submissions.map((sub) => (
                  <div
                    key={sub.id}
                    className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-dark-900/60 transition-colors"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <Link
                          to={`/practice/${sub.question_id}`}
                          className="text-xs font-bold text-white hover:text-brand-400 transition-colors"
                        >
                          {sub.question_title}
                        </Link>
                        <span className="text-[10px] px-1.5 py-0.2 rounded bg-dark-800 text-dark-400 font-mono">
                          {sub.database_id}
                        </span>
                      </div>
                      <div className="text-[11px] font-mono text-dark-400 flex items-center gap-2">
                        <span>{sub.passed_test_cases} / {sub.total_test_cases} Tests</span>
                        <span>•</span>
                        <span>{sub.execution_time_ms.toFixed(1)} ms</span>
                        <span>•</span>
                        <span>{new Date(sub.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      {sub.xp_awarded > 0 && (
                        <span className="text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                          +{sub.xp_awarded} XP
                        </span>
                      )}

                      {sub.status === 'ACCEPTED' ? (
                        <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Accepted
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-[11px] font-bold text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded border border-rose-500/20">
                          <XCircle className="w-3.5 h-3.5" /> {sub.status}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};
