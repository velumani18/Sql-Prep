import React from 'react';

interface BadgeProps {
  variant?: 'easy' | 'medium' | 'hard' | 'beginner' | 'intermediate' | 'advanced' | 'neutral' | 'success' | 'warning' | 'danger';
  size?: 'sm' | 'md';
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'neutral',
  size = 'md',
  children,
  className = '',
}) => {
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-xs font-medium';

  const variantClasses = {
    easy: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    beginner: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    medium: 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
    intermediate: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    hard: 'bg-rose-500/10 text-rose-400 border border-rose-500/20',
    advanced: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
    neutral: 'bg-dark-800 text-dark-300 border border-dark-700',
    success: 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30',
    warning: 'bg-amber-500/15 text-amber-300 border border-amber-500/30',
    danger: 'bg-rose-500/15 text-rose-300 border border-rose-500/30',
  }[variant];

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full capitalize font-medium ${sizeClasses} ${variantClasses} ${className}`}
    >
      {children}
    </span>
  );
};

