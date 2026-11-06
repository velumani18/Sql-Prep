import React from 'react';
import { Link } from 'react-router-dom';
import {
  Terminal,
  Code2,
  Database,
  CheckCircle2,
  Zap,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  Play,
  Briefcase,
  Layers,
  BookOpen,
  Table as TableIcon
} from 'lucide-react';
import { mockCurriculumModules } from '../services/mockData';
import { Badge } from '../components/common/Badge';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-dark-950 text-dark-100 overflow-hidden">
      
      {/* 1. HERO SECTION */}
      <section className="relative pt-20 pb-24 lg:pt-28 lg:pb-32 overflow-hidden">
        {/* Ambient background glows */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[350px] bg-brand-500/10 rounded-full blur-[140px] pointer-events-none" />
        <div className="absolute top-1/3 left-1/4 w-[300px] h-[300px] bg-blue-500/10 rounded-full blur-[120px] pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center space-y-8">
          
          {/* Top Pill */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-dark-900 border border-dark-700/80 text-dark-300 text-xs font-medium shadow-md shadow-black/40">
            <span className="flex h-2 w-2 rounded-full bg-brand-400 animate-pulse" />
            <span className="text-white font-semibold">SQLForge 2.0 Released</span>
            <span className="text-dark-500">•</span>
            <span className="text-dark-300">The LeetCode for Database Engineers</span>
            <ArrowRight className="w-3.5 h-3.5 text-brand-400 ml-0.5" />
          </div>

          {/* Headline */}
          <div className="space-y-4 max-w-4xl mx-auto">
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.1]">
              Master SQL from First Query <br className="hidden sm:inline" />
              to <span className="bg-gradient-to-r from-brand-400 via-emerald-300 to-cyan-400 bg-clip-text text-transparent">Database Architect</span>
            </h1>
            <p className="text-base sm:text-lg text-dark-300 max-w-2xl mx-auto leading-relaxed">
              Learn SQL through structured conceptual lessons and immediately solve hands-on coding challenges in an interactive Monaco editor powered by isolated relational execution sandboxes.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <Link
              to="/curriculum"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-xl bg-brand-500 hover:bg-brand-400 text-dark-950 font-bold text-sm shadow-xl shadow-brand-500/25 transition-all hover:scale-105"
            >
              <Zap className="w-4 h-4 fill-dark-950" />
              <span>Start Learning Free</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              to="/practice/customers-with-zero-orders"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-xl bg-dark-900 hover:bg-dark-800 text-white font-semibold text-sm border border-dark-700 transition-all"
            >
              <Terminal className="w-4 h-4 text-brand-400" />
              <span>Launch Practice Workspace</span>
            </Link>
          </div>

          {/* Live Code Preview Mockup */}
          <div className="pt-10 max-w-5xl mx-auto">
            <div className="rounded-2xl border border-dark-800 bg-dark-900/90 shadow-2xl shadow-black/80 overflow-hidden text-left">
              {/* Window Bar */}
              <div className="px-4 py-3 border-b border-dark-800 bg-dark-950 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block" />
                  <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block" />
                  <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block" />
                  <span className="ml-3 text-xs font-mono text-dark-400">workspace.sql — ecommerce_db</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-mono text-[10px] font-bold">
                    ACCEPTED (18ms)
                  </span>
                </div>
              </div>

              {/* Code + Output Split */}
              <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-dark-800 font-mono text-xs">
                {/* Code Editor Preview */}
                <div className="p-5 bg-dark-950/80 text-dark-300 space-y-1 overflow-x-auto">
                  <div className="text-dark-500 italic">-- LeetCode #183: Customers who never order</div>
                  <div><span className="text-brand-400 font-bold">SELECT</span></div>
                  <div className="pl-4">c.id <span className="text-brand-400 font-bold">AS</span> customer_id,</div>
                  <div className="pl-4">c.name <span className="text-brand-400 font-bold">AS</span> customer_name,</div>
                  <div className="pl-4">c.email</div>
                  <div><span className="text-brand-400 font-bold">FROM</span> customers c</div>
                  <div><span className="text-brand-400 font-bold">LEFT JOIN</span> orders o</div>
                  <div className="pl-4"><span className="text-brand-400 font-bold">ON</span> c.id = o.customer_id</div>
                  <div><span className="text-brand-400 font-bold">WHERE</span> o.id <span className="text-brand-400 font-bold">IS NULL</span>;</div>
                </div>

                {/* Output Table Preview */}
                <div className="p-5 bg-dark-900/60 space-y-3">
                  <div className="flex items-center justify-between text-[11px] text-dark-400">
                    <span className="font-semibold text-white">Execution Result Table</span>
                    <span className="text-emerald-400 font-bold">3 of 3 Test Cases Passed</span>
                  </div>
                  <div className="border border-dark-800 rounded-lg overflow-hidden bg-dark-950">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-dark-900 text-dark-400 text-[10px] uppercase border-b border-dark-800">
                        <tr>
                          <th className="py-2 px-3">customer_id</th>
                          <th className="py-2 px-3">customer_name</th>
                          <th className="py-2 px-3">email</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-dark-800 text-dark-200">
                        <tr>
                          <td className="py-2 px-3">105</td>
                          <td className="py-2 px-3 font-semibold text-brand-300">Mateo Morales</td>
                          <td className="py-2 px-3 text-dark-400">mateo.m@example.es</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* 2. PLATFORM STATISTICS */}
      <section className="border-y border-dark-800 bg-dark-900/40 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-1">
              <span className="text-3xl sm:text-4xl font-extrabold text-white font-mono">150+</span>
              <p className="text-xs text-dark-400 uppercase tracking-wider font-semibold">Interactive SQL Problems</p>
            </div>
            <div className="space-y-1">
              <span className="text-3xl sm:text-4xl font-extrabold text-brand-400 font-mono">4</span>
              <p className="text-xs text-dark-400 uppercase tracking-wider font-semibold">Synthetic Relational DBs</p>
            </div>
            <div className="space-y-1">
              <span className="text-3xl sm:text-4xl font-extrabold text-white font-mono">99.8%</span>
              <p className="text-xs text-dark-400 uppercase tracking-wider font-semibold">Evaluation Accuracy</p>
            </div>
            <div className="space-y-1">
              <span className="text-3xl sm:text-4xl font-extrabold text-cyan-400 font-mono">25,000+</span>
              <p className="text-xs text-dark-400 uppercase tracking-wider font-semibold">Queries Evaluated</p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. PLATFORM CORE FEATURES */}
      <section id="features" className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <h2 className="text-xs font-semibold text-brand-400 uppercase tracking-wider">
            Engineered for Precision
          </h2>
          <p className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Everything You Need to Master Relational Thinking
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Feature 1 */}
          <div className="p-6 rounded-2xl border border-dark-800 bg-dark-900/60 space-y-4 hover:border-brand-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center">
              <Code2 className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Monaco SQL Editor</h3>
            <p className="text-xs text-dark-400 leading-relaxed">
              Built on the same core as VS Code. Includes intelligent SQL keywords, syntax coloring, line numbers, and keyboard shortcuts (`Ctrl+Enter` to run).
            </p>
          </div>

          {/* Feature 2 */}
          <div className="p-6 rounded-2xl border border-dark-800 bg-dark-900/60 space-y-4 hover:border-brand-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Semantic Result Evaluator</h3>
            <p className="text-xs text-dark-400 leading-relaxed">
              We never compare brittle SQL string matches. Your query results are validated semantically across both public and hidden edge case datasets.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="p-6 rounded-2xl border border-dark-800 bg-dark-900/60 space-y-4 hover:border-brand-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center">
              <Database className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Synthetic Relational DBs</h3>
            <p className="text-xs text-dark-400 leading-relaxed">
              Practice against real-world schemas: Multi-table E-Commerce marketplaces, corporate HR payrolls, and logistics tracking databases.
            </p>
          </div>

        </div>
      </section>

      {/* 4. CURRICULUM ROADMAP PREVIEW */}
      <section className="py-20 border-t border-dark-800 bg-dark-900/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h2 className="text-xs font-semibold text-brand-400 uppercase tracking-wider mb-2">
                Structured Learning Flow
              </h2>
              <p className="text-3xl font-extrabold text-white tracking-tight">
                Curriculum Designed for Real Mastery
              </p>
            </div>
            <Link
              to="/curriculum"
              className="inline-flex items-center gap-2 text-xs font-semibold text-brand-400 hover:text-brand-300"
            >
              <span>Explore Complete Roadmap</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {mockCurriculumModules.slice(0, 3).map((mod, idx) => (
              <div
                key={mod.id}
                className="p-6 rounded-2xl border border-dark-800 bg-dark-900/70 space-y-4 flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-dark-500">Track 0{idx + 1}</span>
                    <Badge variant={mod.level} size="sm">{mod.level}</Badge>
                  </div>
                  <h3 className="text-base font-bold text-white">{mod.title}</h3>
                  <p className="text-xs text-dark-400 leading-relaxed">{mod.description}</p>
                </div>

                <div className="pt-4 border-t border-dark-800 flex items-center justify-between text-xs">
                  <span className="text-dark-500">{mod.totalTopics} topics</span>
                  <Link
                    to={`/topic/${mod.lessons[0].slug}`}
                    className="text-brand-400 hover:underline flex items-center gap-1 font-semibold"
                  >
                    <span>View Lessons</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* 5. CALL TO ACTION */}
      <section className="py-24 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <div className="p-10 sm:p-14 rounded-3xl border border-brand-500/30 bg-gradient-to-b from-brand-950/40 via-dark-900 to-dark-950 space-y-6 relative overflow-hidden">
          <div className="space-y-3">
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Ready to Write Real SQL?
            </h2>
            <p className="text-xs sm:text-sm text-dark-300 max-w-xl mx-auto leading-relaxed">
              No complicated database installation required. Jump straight into the Monaco editor, query synthetic schemas, and master SQL today.
            </p>
          </div>

          <div className="flex items-center justify-center gap-4">
            <Link
              to="/curriculum"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-brand-500 hover:bg-brand-400 text-dark-950 font-bold text-sm shadow-xl shadow-brand-500/25 transition-all"
            >
              <span>Get Started Now</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
};

