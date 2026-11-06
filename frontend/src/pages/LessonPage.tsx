import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  BookOpen,
  Code2,
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  Clock,
  Sparkles,
  Terminal,
  HelpCircle,
  Play,
  Copy,
  Check,
  CheckCircle,
} from 'lucide-react';
import { getTopicLessonBySlug, markTopicCompleted } from '../services/curriculumService';
import { TopicLesson } from '../types';
import { Badge } from '../components/common/Badge';

export const LessonPage: React.FC = () => {
  const { topicSlug } = useParams<{ topicSlug?: string }>();
  const [lesson, setLesson] = useState<TopicLesson | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCompleted, setIsCompleted] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    setIsLoading(true);

    const slug = topicSlug || 'sql-relational-tables-select';
    getTopicLessonBySlug(slug)
      .then((data) => {
        setLesson(data);
      })
      .catch((err) => {
        console.error('Failed to load topic lesson:', err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [topicSlug]);

  const handleCopyCode = (code: string, idx: number) => {
    navigator.clipboard.writeText(code);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleMarkComplete = async () => {
    if (!lesson) return;
    try {
      const res = await markTopicCompleted(lesson.slug);
      if (res.success) {
        setIsCompleted(true);
      }
    } catch (err) {
      console.error('Failed to mark topic complete:', err);
    }
  };

  if (isLoading || !lesson) {
    return (
      <div className="min-h-screen bg-dark-950 flex items-center justify-center text-dark-300">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm font-medium">Loading lesson curriculum...</p>
        </div>
      </div>
    );
  }

  const firstQuestionSlug = lesson.practiceQuestions[0]?.slug || lesson.practiceQuestions[0]?.id || 'q-001';

  return (
    <div className="min-h-screen bg-dark-950 text-dark-100 py-10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between text-xs text-dark-400">
          <Link
            to="/curriculum"
            className="flex items-center gap-1.5 hover:text-brand-400 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Curriculum / {lesson.moduleName}</span>
          </Link>
          <div className="flex items-center gap-2">
            <Badge variant={lesson.level}>{lesson.level}</Badge>
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-dark-500" />
              {lesson.readTimeMinutes} min read
            </span>
          </div>
        </div>

        {/* Lesson Header */}
        <div className="space-y-4 border-b border-dark-800 pb-8">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            {lesson.title}
          </h1>
          <p className="text-base text-dark-300 leading-relaxed max-w-3xl">
            {lesson.conceptSummary}
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4">
            <Link
              to={`/practice/${firstQuestionSlug}`}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-brand-500 hover:bg-brand-400 text-dark-950 font-bold text-sm shadow-lg shadow-brand-500/20 transition-all"
            >
              <Code2 className="w-4 h-4" />
              <span>Start Practicing ({lesson.practiceQuestions.length} Questions)</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <button
              onClick={handleMarkComplete}
              disabled={isCompleted}
              className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-lg border text-sm font-semibold transition-all ${
                isCompleted
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 cursor-default'
                  : 'bg-dark-900 hover:bg-dark-800 text-white border-dark-700'
              }`}
            >
              <CheckCircle className="w-4 h-4 text-emerald-400" />
              <span>{isCompleted ? 'Topic Completed (+100 XP)' : 'Mark Topic as Completed'}</span>
            </button>
          </div>
        </div>

        {/* 1. CONCEPT EXPLANATION */}
        <section className="space-y-4">
          <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
            <BookOpen className="w-4 h-4" />
            <span>1. Concept Explanation & Theory</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Relational Architecture & Mechanics
          </h2>
          <div className="space-y-4 text-dark-300 text-sm leading-relaxed">
            {lesson.conceptContent.map((paragraph, idx) => (
              <p key={idx} className="bg-dark-900/40 border border-dark-800/80 p-5 rounded-xl whitespace-pre-line">
                {paragraph}
              </p>
            ))}
          </div>
        </section>

        {/* 2. SQL SYNTAX & VARIATIONS */}
        <section className="space-y-6">
          <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
            <Terminal className="w-4 h-4" />
            <span>2. SQL Syntax & Standard Variations</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Anatomy of the Syntax
          </h2>

          <div className="grid grid-cols-1 gap-6">
            {lesson.syntaxBlocks.map((block, idx) => (
              <div
                key={idx}
                className="border border-dark-800 rounded-xl bg-dark-900/60 overflow-hidden"
              >
                <div className="p-4 border-b border-dark-800 bg-dark-900 flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-white">{block.title}</h3>
                    <p className="text-xs text-dark-400">{block.description}</p>
                  </div>
                  <button
                    onClick={() => handleCopyCode(block.syntax, idx + 10)}
                    className="p-1.5 rounded text-dark-400 hover:text-white hover:bg-dark-800 transition-colors"
                  >
                    {copiedIndex === idx + 10 ? <Check className="w-4 h-4 text-brand-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>

                <div className="p-4 bg-dark-950 font-mono text-xs text-brand-300 overflow-x-auto whitespace-pre">
                  {block.syntax}
                </div>

                {block.notes && (
                  <div className="p-4 bg-dark-950/40 border-t border-dark-800/60 text-xs text-dark-400 space-y-1">
                    <span className="font-semibold text-dark-300 block mb-1">Clause Breakdown:</span>
                    {block.notes.map((note, nIdx) => (
                      <div key={nIdx} className="flex items-start gap-2">
                        <span className="text-brand-400">•</span>
                        <span>{note}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* 3. WORKED EXAMPLES */}
        <section className="space-y-6">
          <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-4 h-4" />
            <span>3. Practical Worked Examples</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Interactive Example Queries & Expected Result Tables
          </h2>

          <div className="space-y-6">
            {lesson.examples.map((ex, idx) => (
              <div
                key={idx}
                className="border border-dark-800 rounded-xl bg-dark-900/60 overflow-hidden space-y-4 p-5"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-bold text-white flex items-center gap-2">
                      <span className="w-6 h-6 rounded-full bg-dark-800 text-brand-400 text-xs flex items-center justify-center font-mono">
                        {idx + 1}
                      </span>
                      {ex.title}
                    </h3>
                    <p className="text-xs text-dark-400 mt-1">{ex.description}</p>
                  </div>

                  <Link
                    to={`/practice/${firstQuestionSlug}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-xs text-white font-medium transition-colors"
                  >
                    <Play className="w-3 h-3 text-brand-400" />
                    <span>Try in Sandbox</span>
                  </Link>
                </div>

                {/* SQL Code Block */}
                <div className="rounded-lg bg-dark-950 border border-dark-800 p-4 font-mono text-xs text-cyan-300 overflow-x-auto whitespace-pre">
                  {ex.sql}
                </div>

                {/* Expected Output Table Preview */}
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-dark-400 uppercase tracking-wider block">
                    Expected Output Table
                  </span>
                  <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-950">
                    <table className="w-full text-left text-xs font-mono">
                      <thead className="bg-dark-900 text-dark-400 uppercase text-[10px] border-b border-dark-800">
                        <tr>
                          {ex.columns.map((col, cIdx) => (
                            <th key={cIdx} className="py-2 px-3 whitespace-nowrap">
                              {col}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-dark-800">
                        {ex.rows.map((row, rIdx) => (
                          <tr key={rIdx} className="hover:bg-dark-900/40">
                            {row.map((val, vIdx) => (
                              <td key={vIdx} className="py-2 px-3 text-dark-200 whitespace-nowrap">
                                {val !== null ? String(val) : <span className="text-dark-500 italic">NULL</span>}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 4. PRACTICE QUESTIONS LIST */}
        <section className="space-y-6 pt-4 border-t border-dark-800">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
                <HelpCircle className="w-4 h-4" />
                <span>4. Hands-on Practice Questions</span>
              </div>
              <h2 className="text-2xl font-bold text-white tracking-tight mt-1">
                Apply What You Learned
              </h2>
            </div>
            <span className="text-xs px-2.5 py-1 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-bold">
              {lesson.practiceQuestions.length} Questions Available
            </span>
          </div>

          <div className="grid grid-cols-1 gap-3">
            {lesson.practiceQuestions.map((q, idx) => (
              <Link
                key={q.id}
                to={`/practice/${q.slug || q.id}`}
                className="group flex items-center justify-between p-4 rounded-xl border border-dark-800 bg-dark-900/60 hover:bg-dark-800/80 hover:border-brand-500/40 transition-all shadow-sm"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-dark-800 text-dark-300 font-mono text-xs flex items-center justify-center font-bold group-hover:bg-brand-500 group-hover:text-dark-950 transition-colors">
                    {idx + 1}
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white group-hover:text-brand-300 transition-colors">
                      {q.title}
                    </h3>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className={`text-[10px] font-bold uppercase tracking-wider ${
                        q.difficulty === 'easy'
                          ? 'text-emerald-400'
                          : q.difficulty === 'medium'
                          ? 'text-amber-400'
                          : 'text-rose-400'
                      }`}>
                        {q.difficulty}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {q.isSolved && (
                    <span className="flex items-center gap-1 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                    </span>
                  )}
                  <span className="text-xs text-dark-400 group-hover:text-brand-400 group-hover:translate-x-0.5 transition-all flex items-center gap-1">
                    Solve <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </section>

      </div>
    </div>
  );
};
