import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Compass,
  CheckCircle2,
  Lock,
  Unlock,
  ArrowRight,
  BookOpen,
  Code2,
  Clock,
  Layers,
  Sparkles,
  Database,
  BarChart3,
  GitFork,
  Cpu
} from 'lucide-react';
import { getCurriculumModules } from '../services/curriculumService';
import { mockCurriculumModules } from '../services/mockData';
import { CurriculumModule } from '../types';
import { Badge } from '../components/common/Badge';

export const RoadmapPage: React.FC = () => {
  const [modules, setModules] = useState<CurriculumModule[]>(mockCurriculumModules);
  const [selectedLevel, setSelectedLevel] = useState<'all' | 'beginner' | 'intermediate' | 'advanced'>('all');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    getCurriculumModules()
      .then((data) => setModules(data))
      .catch((err) => console.error('Failed to load modules:', err))
      .finally(() => setIsLoading(false));
  }, []);

  const filteredModules = modules.filter((mod) => {
    if (selectedLevel === 'all') return true;
    return mod.level === selectedLevel;
  });

  const getModuleIcon = (iconName: string) => {
    switch (iconName) {
      case 'Database': return <Database className="w-5 h-5 text-emerald-400" />;
      case 'BarChart3': return <BarChart3 className="w-5 h-5 text-blue-400" />;
      case 'GitFork': return <GitFork className="w-5 h-5 text-cyan-400" />;
      case 'Layers': return <Layers className="w-5 h-5 text-purple-400" />;
      case 'Sparkles': return <Sparkles className="w-5 h-5 text-amber-400" />;
      case 'Cpu': return <Cpu className="w-5 h-5 text-rose-400" />;
      default: return <Database className="w-5 h-5 text-brand-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-dark-950 text-dark-100 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-semibold uppercase tracking-wider">
            <Compass className="w-3.5 h-3.5" />
            Curriculum Blueprint
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            SQL Mastery Roadmap
          </h1>
          <p className="text-sm text-dark-400 leading-relaxed">
            From basic single-table queries to advanced window frames and indexing architectures. Each module features concept lessons and interactive practice challenges.
          </p>
        </div>

        {/* Level Filter Tabs */}
        <div className="flex justify-center">
          <div className="inline-flex items-center gap-1.5 p-1 rounded-xl bg-dark-900 border border-dark-800 text-xs font-medium">
            <button
              onClick={() => setSelectedLevel('all')}
              className={`px-4 py-1.5 rounded-lg transition-colors ${
                selectedLevel === 'all' ? 'bg-brand-500 text-dark-950 font-bold' : 'text-dark-400 hover:text-white'
              }`}
            >
              All Tracks
            </button>
            <button
              onClick={() => setSelectedLevel('beginner')}
              className={`px-4 py-1.5 rounded-lg transition-colors ${
                selectedLevel === 'beginner' ? 'bg-brand-500 text-dark-950 font-bold' : 'text-dark-400 hover:text-white'
              }`}
            >
              Beginner
            </button>
            <button
              onClick={() => setSelectedLevel('intermediate')}
              className={`px-4 py-1.5 rounded-lg transition-colors ${
                selectedLevel === 'intermediate' ? 'bg-brand-500 text-dark-950 font-bold' : 'text-dark-400 hover:text-white'
              }`}
            >
              Intermediate
            </button>
            <button
              onClick={() => setSelectedLevel('advanced')}
              className={`px-4 py-1.5 rounded-lg transition-colors ${
                selectedLevel === 'advanced' ? 'bg-brand-500 text-dark-950 font-bold' : 'text-dark-400 hover:text-white'
              }`}
            >
              Advanced
            </button>
          </div>
        </div>

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredModules.map((mod, idx) => {
            const completionPercent = Math.round((mod.completedTopics / mod.totalTopics) * 100);
            return (
              <div
                key={mod.id}
                className={`relative rounded-2xl border transition-all duration-200 overflow-hidden flex flex-col ${
                  mod.isLocked
                    ? 'border-dark-800 bg-dark-950/40 opacity-70'
                    : 'border-dark-800 bg-dark-900/60 hover:border-brand-500/40 hover:shadow-xl hover:shadow-brand-500/5'
                }`}
              >
                {/* Card Top */}
                <div className="p-6 flex-1 space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 rounded-xl bg-dark-800 border border-dark-700/60">
                        {getModuleIcon(mod.icon)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono text-dark-400">Track #{idx + 1}</span>
                          <Badge variant={mod.level} size="sm">{mod.level}</Badge>
                        </div>
                        <h3 className="text-lg font-bold text-white tracking-tight mt-0.5">
                          {mod.title}
                        </h3>
                      </div>
                    </div>

                    {mod.isLocked ? (
                      <span className="p-1.5 rounded-lg bg-dark-800 text-dark-500" title="Locked: Complete prerequisites first">
                        <Lock className="w-4 h-4" />
                      </span>
                    ) : (
                      <span className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400" title="Unlocked & Ready">
                        <Unlock className="w-4 h-4" />
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-dark-300 leading-relaxed">
                    {mod.description}
                  </p>

                  {/* Prerequisites */}
                  {mod.prerequisites && mod.prerequisites.length > 0 && (
                    <div className="text-[11px] text-dark-400 bg-dark-950/60 border border-dark-800/80 p-2.5 rounded-lg">
                      <span className="font-semibold text-dark-300">Prerequisites: </span>
                      {mod.prerequisites.join(' • ')}
                    </div>
                  )}

                  {/* Progress Bar */}
                  <div className="space-y-1.5 pt-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-dark-400 font-medium">Progress</span>
                      <span className="font-mono text-dark-200">
                        {mod.completedTopics} / {mod.totalTopics} Topics ({completionPercent}%)
                      </span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-dark-800 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-brand-600 to-brand-400 transition-all duration-500"
                        style={{ width: `${completionPercent}%` }}
                      />
                    </div>
                  </div>

                  {/* Lessons List Preview */}
                  <div className="pt-2 space-y-1.5">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-dark-400">
                      Curriculum Topics:
                    </span>
                    <div className="space-y-1">
                      {mod.lessons.map((lesson, lIdx) => (
                        <div
                          key={lesson.id}
                          className="flex items-center justify-between py-1.5 px-2.5 rounded-lg bg-dark-950/40 text-xs"
                        >
                          <div className="flex items-center gap-2 truncate">
                            {lesson.isCompleted ? (
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                            ) : (
                              <span className="w-3.5 h-3.5 rounded-full border border-dark-600 flex-shrink-0" />
                            )}
                            <span className={`truncate ${lesson.isCompleted ? 'text-dark-400 line-through' : 'text-dark-200'}`}>
                              {lesson.title}
                            </span>
                          </div>
                          <span className="text-[10px] text-dark-500 font-mono ml-2">
                            {lesson.questionsCount} problems
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Card Footer Actions */}
                <div className="px-6 py-4 border-t border-dark-800/80 bg-dark-950/60 flex items-center justify-between">
                  <span className="flex items-center gap-1.5 text-xs text-dark-400">
                    <Clock className="w-3.5 h-3.5 text-dark-500" />
                    ~{mod.estimatedHours} hours total
                  </span>

                  {mod.isLocked ? (
                    <button
                      disabled
                      className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-dark-800 text-dark-500 text-xs font-semibold cursor-not-allowed"
                    >
                      <Lock className="w-3.5 h-3.5" />
                      <span>Locked</span>
                    </button>
                  ) : (
                    <Link
                      to={`/topic/${mod.lessons[0].slug}`}
                      className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-dark-800 hover:bg-brand-500 hover:text-dark-950 text-xs font-semibold text-white transition-all shadow-sm"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>Open Module</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  )}
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
};

