import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Briefcase,
  Search,
  CheckCircle2,
  Circle,
  Database,
  ArrowRight,
  Filter,
  Sparkles,
  Building2,
  Code2
} from 'lucide-react';
import { getInterviewQuestions } from '../services/questionService';
import { mockInterviewQuestions, InterviewQuestionItem } from '../services/mockData';
import { Badge } from '../components/common/Badge';

export const InterviewPage: React.FC = () => {
  const [questions, setQuestions] = useState<InterviewQuestionItem[]>(mockInterviewQuestions);
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<'all' | 'easy' | 'medium' | 'hard'>('all');
  const [topicFilter, setTopicFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<'all' | 'solved' | 'unsolved'>('all');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    getInterviewQuestions()
      .then((data) => setQuestions(data))
      .catch((err) => console.error('Failed to load interview questions:', err))
      .finally(() => setIsLoading(false));
  }, []);

  const topicsList = ['all', 'SELECT & Column Aliasing', 'WHERE & Comparison Operators', 'Logical Operators & Pattern Matching', 'ORDER BY, LIMIT, and Pagination', 'Aggregate Functions', 'GROUP BY & HAVING', 'CASE Expressions, COALESCE & Conditional Logic', 'INNER JOIN & Relational Navigation', 'LEFT JOIN & Handling Missing Data', 'Multi-Table Joins & Self Joins'];

  const filteredQuestions = questions.filter((q) => {
    // Search
    if (searchQuery.trim()) {
      const qLower = searchQuery.toLowerCase();
      const matchesTitle = q.title.toLowerCase().includes(qLower);
      const matchesCompany = q.companies.some((c) => c.toLowerCase().includes(qLower));
      if (!matchesTitle && !matchesCompany) return false;
    }
    // Difficulty
    if (difficultyFilter !== 'all' && q.difficulty !== difficultyFilter) {
      return false;
    }
    // Topic
    if (topicFilter !== 'all' && q.topic !== topicFilter) {
      return false;
    }
    // Status
    if (statusFilter === 'solved' && !q.isSolved) return false;
    if (statusFilter === 'unsolved' && q.isSolved) return false;

    return true;
  });

  return (
    <div className="min-h-screen bg-dark-950 text-dark-100 py-10">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-dark-800 pb-8">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 text-xs font-semibold mb-3">
              <Briefcase className="w-3.5 h-3.5" />
              Interview Arena
            </div>
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              Curated SQL Interview Questions
            </h1>
            <p className="text-xs text-dark-400 mt-1 max-w-xl">
              Real technical interview challenges from top companies: Amazon, Google, Meta, and Stripe. Practice anti-joins, running totals, and multi-tier CTE queries.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-dark-400 font-mono">
              Showing <strong className="text-white">{filteredQuestions.length}</strong> problems
            </span>
          </div>
        </div>

        {/* Filters and Search Bar */}
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            
            {/* Search Input */}
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-dark-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search problem title or company..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-dark-900 border border-dark-800 rounded-xl text-xs text-white placeholder-dark-500 focus:outline-none focus:border-brand-500 transition-colors"
              />
            </div>

            {/* Quick Status Buttons */}
            <div className="flex items-center gap-2 w-full sm:w-auto">
              {(['all', 'solved', 'unsolved'] as const).map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                    statusFilter === st
                      ? 'bg-dark-800 text-white border border-dark-700'
                      : 'text-dark-400 hover:text-white'
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>
          </div>

          {/* Difficulty and Topic Chips */}
          <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
            <span className="text-dark-500 flex items-center gap-1 mr-1">
              <Filter className="w-3.5 h-3.5" />
              Filters:
            </span>

            {/* Difficulty Chips */}
            {(['all', 'easy', 'medium', 'hard'] as const).map((diff) => (
              <button
                key={diff}
                onClick={() => setDifficultyFilter(diff)}
                className={`px-2.5 py-1 rounded-md capitalize transition-colors ${
                  difficultyFilter === diff
                    ? 'bg-brand-500/20 text-brand-300 border border-brand-500/30 font-semibold'
                    : 'bg-dark-900 text-dark-400 hover:text-white border border-dark-800'
                }`}
              >
                {diff}
              </button>
            ))}

            <div className="h-4 w-px bg-dark-800 mx-1" />

            {/* Topic dropdown/chips */}
            {topicsList.map((top) => (
              <button
                key={top}
                onClick={() => setTopicFilter(top)}
                className={`px-2.5 py-1 rounded-md transition-colors ${
                  topicFilter === top
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30 font-semibold'
                    : 'bg-dark-900 text-dark-400 hover:text-white border border-dark-800'
                }`}
              >
                {top === 'all' ? 'All Topics' : top}
              </button>
            ))}
          </div>
        </div>

        {/* Problems List Table */}
        <div className="border border-dark-800 rounded-2xl overflow-hidden bg-dark-900/60 shadow-xl">
          <table className="w-full text-left text-xs">
            <thead className="bg-dark-900 text-dark-400 uppercase text-[10px] border-b border-dark-800 font-mono tracking-wider">
              <tr>
                <th className="py-3 px-4 w-12 text-center">Status</th>
                <th className="py-3 px-4">Problem Title & Companies</th>
                <th className="py-3 px-4">Topic Area</th>
                <th className="py-3 px-4">Database</th>
                <th className="py-3 px-4">Difficulty</th>
                <th className="py-3 px-4">Acceptance</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-800/80">
              {filteredQuestions.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-dark-500">
                    No interview questions match your filter criteria.
                  </td>
                </tr>
              ) : (
                filteredQuestions.map((q) => (
                  <tr
                    key={q.id}
                    className="hover:bg-dark-800/40 transition-colors group"
                  >
                    {/* Status */}
                    <td className="py-3 px-4 text-center">
                      {q.isSolved ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 mx-auto" />
                      ) : (
                        <Circle className="w-4 h-4 text-dark-600 mx-auto" />
                      )}
                    </td>

                    {/* Title & Companies */}
                    <td className="py-3 px-4">
                      <Link
                        to={`/practice/${q.slug}`}
                        className="font-semibold text-white group-hover:text-brand-300 transition-colors block text-sm"
                      >
                        {q.title}
                      </Link>
                      <div className="flex flex-wrap items-center gap-1.5 mt-1">
                        {q.companies.map((comp) => (
                          <span
                            key={comp}
                            className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-dark-800 text-dark-400 font-medium"
                          >
                            <Building2 className="w-2.5 h-2.5 text-dark-500" />
                            {comp}
                          </span>
                        ))}
                      </div>
                    </td>

                    {/* Topic */}
                    <td className="py-3 px-4 text-dark-300 font-medium">
                      {q.topic}
                    </td>

                    {/* Database */}
                    <td className="py-3 px-4 font-mono text-[11px] text-dark-400">
                      <div className="flex items-center gap-1">
                        <Database className="w-3 h-3 text-brand-400" />
                        <span>{q.databaseName}</span>
                      </div>
                    </td>

                    {/* Difficulty */}
                    <td className="py-3 px-4">
                      <Badge variant={q.difficulty} size="sm">{q.difficulty}</Badge>
                    </td>

                    {/* Acceptance */}
                    <td className="py-3 px-4 font-mono text-dark-300">
                      {q.acceptanceRate}
                    </td>

                    {/* Action */}
                    <td className="py-3 px-4 text-right">
                      <Link
                        to={`/practice/${q.slug}`}
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-brand-500 hover:text-dark-950 text-xs font-semibold text-white transition-all shadow-sm"
                      >
                        <Code2 className="w-3 h-3" />
                        <span>Solve</span>
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
};

