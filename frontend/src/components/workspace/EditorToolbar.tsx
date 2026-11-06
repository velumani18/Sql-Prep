import React from 'react';
import {
  Play,
  Send,
  RotateCcw,
  Sparkles,
  Database,
  Code2,
  Loader2
} from 'lucide-react';

interface EditorToolbarProps {
  databaseName: string;
  isRunning: boolean;
  isSubmitting: boolean;
  onRunQuery: () => void;
  onSubmitQuery: () => void;
  onResetCode: () => void;
  onFormatCode: () => void;
}

export const EditorToolbar: React.FC<EditorToolbarProps> = ({
  databaseName,
  isRunning,
  isSubmitting,
  onRunQuery,
  onSubmitQuery,
  onResetCode,
  onFormatCode,
}) => {
  return (
    <div className="flex items-center justify-between px-4 py-2 border-b border-dark-800 bg-dark-900/90 text-xs">
      
      {/* Left controls */}
      <div className="flex items-center gap-3">
        {/* Database indicator */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-dark-950 border border-dark-800 text-dark-300 font-mono">
          <Database className="w-3.5 h-3.5 text-brand-400" />
          <span className="font-semibold text-white">{databaseName}</span>
        </div>

        {/* Dialect */}
        <div className="hidden sm:flex items-center gap-1.5 text-dark-400 font-mono">
          <Code2 className="w-3.5 h-3.5 text-dark-500" />
          <span>SQLite 3.x</span>
        </div>

        <div className="h-4 w-px bg-dark-800 hidden sm:block" />

        {/* Action icons */}
        <button
          onClick={onFormatCode}
          title="Auto-format SQL"
          className="p-1.5 rounded text-dark-400 hover:text-white hover:bg-dark-800 transition-colors flex items-center gap-1"
        >
          <Sparkles className="w-3.5 h-3.5 text-brand-400" />
          <span className="hidden md:inline">Format</span>
        </button>

        <button
          onClick={onResetCode}
          title="Reset to starter code"
          className="p-1.5 rounded text-dark-400 hover:text-white hover:bg-dark-800 transition-colors flex items-center gap-1"
        >
          <RotateCcw className="w-3.5 h-3.5 text-amber-400" />
          <span className="hidden md:inline">Reset</span>
        </button>
      </div>

      {/* Right controls: Run & Submit */}
      <div className="flex items-center gap-2">
        <span className="hidden lg:inline text-[11px] text-dark-500 font-mono mr-1">
          Ctrl + Enter
        </span>

        {/* Run Query Button */}
        <button
          onClick={onRunQuery}
          disabled={isRunning || isSubmitting}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-white font-medium border border-dark-700 transition-colors disabled:opacity-50"
        >
          {isRunning ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin text-brand-400" />
          ) : (
            <Play className="w-3.5 h-3.5 text-brand-400 fill-brand-400" />
          )}
          <span>Run Query</span>
        </button>

        {/* Submit Solution Button */}
        <button
          onClick={onSubmitQuery}
          disabled={isRunning || isSubmitting}
          className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-brand-500 hover:bg-brand-400 text-dark-950 font-semibold shadow-md shadow-brand-500/20 transition-all disabled:opacity-50"
        >
          {isSubmitting ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin text-dark-950" />
          ) : (
            <Send className="w-3.5 h-3.5" />
          )}
          <span>Submit</span>
        </button>
      </div>

    </div>
  );
};

