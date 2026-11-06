import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Terminal,
  Flame,
  Zap,
  BookOpen,
  Code2,
  Briefcase,
  LayoutDashboard,
  Menu,
  X,
  Database,
} from 'lucide-react';
import { authService, User } from '../../services/authService';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [user, setUser] = useState<User>({
    id: 'usr-demo',
    name: 'Alex Developer',
    email: 'alex.dev@sqlforge.dev',
    avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces',
    streak_days: 5,
    xp: 850,
    level_title: 'SQL Practitioner',
  });

  useEffect(() => {
    authService.getCurrentUser().then(setUser).catch(() => {});
  }, [location.pathname]);

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Curriculum', path: '/curriculum', icon: BookOpen },
    { name: 'Practice Workspace', path: '/practice/q-001', icon: Code2 },
    { name: 'Interview Prep', path: '/interview', icon: Briefcase },
  ];

  const isActive = (path: string) => {
    if (path.startsWith('/practice') && location.pathname.startsWith('/practice')) return true;
    return location.pathname === path;
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-dark-800 bg-dark-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-brand-500/20 group-hover:shadow-brand-500/30 transition-all">
              <Terminal className="w-5 h-5 text-dark-950 font-bold" />
            </div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-xl font-bold tracking-tight text-white font-mono">
                SQL<span className="text-brand-400">Forge</span>
              </span>
              <span className="text-[10px] uppercase font-semibold tracking-wider px-1.5 py-0.5 rounded bg-brand-500/10 text-brand-400 border border-brand-500/20">
                PRO
              </span>
            </div>
          </Link>

          {/* Desktop Nav Items */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const active = isActive(link.path);
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    active
                      ? 'bg-dark-800 text-brand-400 shadow-sm'
                      : 'text-dark-300 hover:text-white hover:bg-dark-900'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${active ? 'text-brand-400' : 'text-dark-400'}`} />
                  {link.name}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Right Action Icons & User Profile */}
        <div className="hidden sm:flex items-center gap-4">
          {/* Active Engine Badge */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-dark-900 border border-dark-800 text-xs text-dark-300 font-mono">
            <Database className="w-3.5 h-3.5 text-brand-400" />
            <span>SQLite 3.49 Sandbox</span>
          </div>

          {/* User Streak */}
          <div 
            title={`${user.streak_days} day learning streak!`}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/20 text-xs font-semibold text-amber-400"
          >
            <Flame className="w-4 h-4 text-amber-400 fill-amber-400/20" />
            <span>{user.streak_days}d Streak</span>
          </div>

          {/* XP Points */}
          <div 
            title="Total Earned Experience Points"
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-brand-500/10 border border-brand-500/20 text-xs font-semibold text-brand-400"
          >
            <Zap className="w-3.5 h-3.5 text-brand-400 fill-brand-400/20" />
            <span>{user.xp} XP</span>
          </div>

          {/* User Avatar */}
          <Link
            to="/dashboard"
            className="flex items-center gap-2 pl-2 border-l border-dark-800 hover:opacity-90 transition-opacity"
          >
            <div className="relative">
              <img
                src={user.avatar_url}
                alt={user.name}
                className="w-8 h-8 rounded-full object-cover ring-2 ring-brand-500/30"
              />
              <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-2 ring-dark-950" />
            </div>
            <span className="text-sm font-medium text-dark-200 hidden lg:inline-block">
              {user.name.split(' ')[0]}
            </span>
          </Link>
        </div>

        {/* Mobile menu trigger */}
        <div className="flex md:hidden items-center gap-3">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg text-dark-400 hover:text-white hover:bg-dark-900 transition-colors"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-dark-800 bg-dark-950 px-4 pt-2 pb-6 space-y-3">
          <nav className="flex flex-col gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const active = isActive(link.path);
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium ${
                    active
                      ? 'bg-dark-800 text-brand-400'
                      : 'text-dark-300 hover:bg-dark-900 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {link.name}
                </Link>
              );
            })}
          </nav>
        </div>
      )}
    </header>
  );
};
