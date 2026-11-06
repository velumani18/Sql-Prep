import React from 'react';
import { Link } from 'react-router-dom';
import { Terminal, Code, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-dark-800 bg-dark-950 text-dark-400 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          
          {/* Brand Column */}
          <div className="md:col-span-1 space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded bg-brand-600 flex items-center justify-center">
                <Terminal className="w-4 h-4 text-dark-950" />
              </div>
              <span className="text-lg font-bold text-white font-mono">
                SQL<span className="text-brand-400">Forge</span>
              </span>
            </div>
            <p className="text-xs text-dark-400 leading-relaxed">
              The professional interactive platform for mastering relational query architecture, query optimization, and technical SQL interviews.
            </p>
          </div>

          {/* Curriculum Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-200">Curriculum</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/curriculum" className="hover:text-brand-400 transition-colors">SQL Fundamentals</Link></li>
              <li><Link to="/curriculum" className="hover:text-brand-400 transition-colors">Relational JOINs & Anti-Joins</Link></li>
              <li><Link to="/curriculum" className="hover:text-brand-400 transition-colors">Aggregations & Grouping</Link></li>
              <li><Link to="/curriculum" className="hover:text-brand-400 transition-colors">Window Functions & Analytics</Link></li>
              <li><Link to="/curriculum" className="hover:text-brand-400 transition-colors">Execution Plans & Indexing</Link></li>
            </ul>
          </div>

          {/* Practice & Tools */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-200">Practice & Prep</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/practice/customers-with-zero-orders" className="hover:text-brand-400 transition-colors">SQL Practice Workspace</Link></li>
              <li><Link to="/interview" className="hover:text-brand-400 transition-colors">LeetCode-Style Interview Bank</Link></li>
              <li><Link to="/dashboard" className="hover:text-brand-400 transition-colors">Progress Dashboard</Link></li>
              <li><a href="#features" className="hover:text-brand-400 transition-colors">Synthetic Relational DBs</a></li>
            </ul>
          </div>

          {/* Engine & Tech */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-200">Architecture</h4>
            <p className="text-xs text-dark-400 leading-relaxed">
              Powered by isolated ephemeral execution sandboxes, Monaco Editor IntelliSense, and AST semantic result evaluators.
            </p>
            <div className="flex items-center gap-2 pt-2 text-xs text-dark-400">
              <Code className="w-4 h-4 text-brand-400" />
              <span>React 19 • Vite • FastAPI • SQLite</span>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-dark-900 flex flex-col sm:flex-row items-center justify-between text-xs text-dark-500 gap-4">
          <p>© {new Date().getFullYear()} SQLForge. Designed for high-performance SQL engineering.</p>
          <div className="flex items-center gap-1">
            <span>Built with precision for database practitioners</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
          </div>
        </div>
      </div>
    </footer>
  );
};
