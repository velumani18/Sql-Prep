import React, { useState } from 'react';
import {
  HelpCircle,
  CheckCircle2,
  Lock,
  Unlock,
  ChevronDown,
  ChevronUp,
  Database,
  Lightbulb,
  Sparkles,
  Check,
  Copy
} from 'lucide-react';
import { QuestionDetail } from '../../types';
import { Badge } from '../common/Badge';

interface ProblemDescriptionProps {
  question: QuestionDetail;
  activeTab: 'description' | 'solution' | 'submissions';
  setActiveTab: (tab: 'description' | 'solution' | 'submissions') => void;
}

export const ProblemDescription: React.FC<ProblemDescriptionProps> = ({
  question,
  activeTab,
  setActiveTab,
}) => {
  const [unlockedHints, setUnlockedHints] = useState<number[]>([]);
  const [isSolutionUnlocked, setIsSolutionUnlocked] = useState(false);
  const [copiedSolution, setCopiedSolution] = useState(false);

  const toggleHint = (index: number) => {
    if (unlockedHints.includes(index)) {
      setUnlockedHints(unlockedHints.filter((i) => i !== index));
    } else {
      setUnlockedHints([...unlockedHints, index]);
    }
  };

  const handleCopySolution = () => {
    navigator.clipboard.writeText(question.officialSolution.sql);
    setCopiedSolution(true);
    setTimeout(() => setCopiedSolution(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-dark-950 border-r border-dark-800 text-dark-200">
      
      {/* Tab Navigation */}
      <div className="flex items-center border-b border-dark-800 bg-dark-900/60 px-4">
        <button
          onClick={() => setActiveTab('description')}
          className={`py-3 px-3 text-xs font-medium border-b-2 transition-colors ${
            activeTab === 'description'
              ? 'border-brand-500 text-white font-semibold'
              : 'border-transparent text-dark-400 hover:text-dark-200'
          }`}
        >
          Problem Description
        </button>
        <button
          onClick={() => setActiveTab('solution')}
          className={`py-3 px-3 text-xs font-medium border-b-2 transition-colors flex items-center gap-1.5 ${
            activeTab === 'solution'
              ? 'border-brand-500 text-white font-semibold'
              : 'border-transparent text-dark-400 hover:text-dark-200'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          Official Solution
        </button>
      </div>

      {/* Panel Content */}
      <div className="flex-1 overflow-y-auto p-5 space-y-6">
        
        {activeTab === 'description' && (
          <>
            {/* Header info */}
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs text-dark-400 font-mono">#{question.id}</span>
                <Badge variant={question.difficulty}>{question.difficulty}</Badge>
                <span className="text-xs text-dark-400">
                  Acceptance: <span className="text-dark-300 font-semibold">{question.acceptanceRate}</span>
                </span>
                <span className="text-xs text-dark-400 flex items-center gap-1">
                  <Database className="w-3 h-3 text-brand-400" />
                  <span className="font-mono text-dark-300">{question.databaseName}</span>
                </span>
              </div>
              <h1 className="text-xl font-bold text-white tracking-tight">{question.title}</h1>
              <p className="text-xs text-brand-400 font-medium mt-1">Topic: {question.topic}</p>
            </div>

            {/* Prompt */}
            <div className="prose prose-invert max-w-none text-xs text-dark-300 leading-relaxed space-y-3">
              <p className="whitespace-pre-line">{question.prompt}</p>
            </div>

            {/* Explicit Constraints & Requirements */}
            <div className="space-y-2">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-300 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-brand-400" />
                Problem Requirements & Output Specifications
              </h4>
              <ul className="space-y-1.5 text-xs text-dark-300 bg-dark-900/80 border border-dark-800 rounded-lg p-3">
                {question.requirements.map((req, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-brand-400 font-bold">•</span>
                    <span>{req}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Sample Expected Output Table */}
            <div className="space-y-2">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-300">
                Sample Test Case Output Example
              </h4>
              <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-900/60">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-dark-900 text-dark-400 text-[10px] uppercase border-b border-dark-800">
                    <tr>
                      {question.sampleExpectedOutput.columns.map((col) => (
                        <th key={col} className="py-2 px-3">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-dark-800 text-dark-200">
                    {question.sampleExpectedOutput.rows.map((row, idx) => (
                      <tr key={idx} className="hover:bg-dark-800/40">
                        {row.map((val, cIdx) => (
                          <td key={cIdx} className="py-2 px-3 whitespace-nowrap">
                            {val !== null ? String(val) : <span className="text-dark-500 italic">NULL</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Progressive Hints */}
            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-300 flex items-center gap-1.5">
                  <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                  Hints & Conceptual Clues ({question.hints.length})
                </h4>
                <span className="text-[11px] text-dark-500">Reveal only if stuck</span>
              </div>

              <div className="space-y-2">
                {question.hints.map((hint, index) => {
                  const isRevealed = unlockedHints.includes(index);
                  return (
                    <div
                      key={index}
                      className="border border-dark-800 rounded-lg bg-dark-900/50 overflow-hidden"
                    >
                      <button
                        onClick={() => toggleHint(index)}
                        className="w-full flex items-center justify-between p-3 text-xs text-left font-medium text-dark-200 hover:text-white transition-colors"
                      >
                        <span className="flex items-center gap-2">
                          <HelpCircle className="w-3.5 h-3.5 text-brand-400" />
                          Hint {index + 1}
                        </span>
                        {isRevealed ? (
                          <ChevronUp className="w-4 h-4 text-dark-400" />
                        ) : (
                          <ChevronDown className="w-4 h-4 text-dark-400" />
                        )}
                      </button>
                      {isRevealed && (
                        <div className="px-3 pb-3 text-xs text-dark-300 border-t border-dark-800/60 pt-2 leading-relaxed bg-dark-950/40">
                          {hint}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </>
        )}

        {activeTab === 'solution' && (
          <div className="space-y-5">
            {!isSolutionUnlocked ? (
              <div className="border border-dark-800 bg-dark-900/60 rounded-xl p-6 text-center space-y-4">
                <div className="w-12 h-12 rounded-full bg-amber-500/10 text-amber-400 flex items-center justify-center mx-auto border border-amber-500/20">
                  <Lock className="w-6 h-6" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-sm font-bold text-white">Solution Locked</h3>
                  <p className="text-xs text-dark-400 max-w-sm mx-auto">
                    Try solving this problem first! Viewing the official solution will unlock the SQL query and comprehensive architectural explanation.
                  </p>
                </div>
                <button
                  onClick={() => setIsSolutionUnlocked(true)}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-dark-800 hover:bg-dark-700 text-xs font-semibold text-white transition-colors border border-dark-700"
                >
                  <Unlock className="w-3.5 h-3.5 text-brand-400" />
                  Reveal Official Solution
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-white">Reference SQL Implementation</h3>
                    <p className="text-xs text-brand-400">Time Complexity: {question.officialSolution.timeComplexity}</p>
                  </div>
                  <button
                    onClick={handleCopySolution}
                    className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-dark-800 hover:bg-dark-700 text-xs text-dark-300 hover:text-white transition-colors"
                  >
                    {copiedSolution ? <Check className="w-3.5 h-3.5 text-brand-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copiedSolution ? 'Copied' : 'Copy SQL'}</span>
                  </button>
                </div>

                <div className="p-3 rounded-lg bg-dark-900 border border-dark-800 font-mono text-xs text-brand-300 overflow-x-auto whitespace-pre">
                  {question.officialSolution.sql}
                </div>

                <div className="space-y-2 pt-2">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-300">
                    Architectural Breakdown & Strategy
                  </h4>
                  <div className="p-4 rounded-lg bg-dark-900/60 border border-dark-800 text-xs text-dark-300 leading-relaxed whitespace-pre-line">
                    {question.officialSolution.explanation}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
};

