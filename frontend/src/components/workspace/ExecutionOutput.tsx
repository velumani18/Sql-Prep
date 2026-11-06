import React, { useState } from 'react';
import {
  CheckCircle,
  XCircle,
  AlertTriangle,
  Clock,
  Table as TableIcon,
  Check,
  ShieldCheck,
  Layers,
  HelpCircle,
  Lock
} from 'lucide-react';
import { QueryExecutionResult, QuestionDetail } from '../../types';

interface ExecutionOutputProps {
  result: QueryExecutionResult | null;
  question: QuestionDetail;
  isRunning: boolean;
  isSubmitting: boolean;
}

export const ExecutionOutput: React.FC<ExecutionOutputProps> = ({
  result,
  question,
  isRunning,
  isSubmitting,
}) => {
  const [activeTab, setActiveTab] = useState<'output' | 'expected' | 'diff' | 'testcases'>('output');
  const [selectedTestCaseIdx, setSelectedTestCaseIdx] = useState(0);

  if (isRunning || isSubmitting) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center bg-dark-950">
        <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
        <span className="text-xs font-semibold text-white">
          {isSubmitting ? 'Evaluating query against synthetic test datasets...' : 'Executing query in isolated SQLite sandbox...'}
        </span>
        <span className="text-[11px] text-dark-400 mt-1">
          Spinning up ephemeral in-memory database & verifying AST bounds
        </span>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8 text-center bg-dark-950 text-dark-400">
        <TableIcon className="w-8 h-8 text-dark-700 mb-2" />
        <p className="text-xs font-medium text-dark-300">No Query Results Yet</p>
        <p className="text-[11px] text-dark-500 mt-1">
          Click <span className="text-white font-semibold">Run Query</span> to test in scratchpad, or <span className="text-brand-400 font-semibold">Submit</span> to evaluate all test cases.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-dark-950 border-t border-dark-800 text-xs">

      {/* Status Bar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-dark-800 bg-dark-900/60">
        <div className="flex items-center gap-3">
          {result.status === 'ACCEPTED' && (
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-bold">
                <CheckCircle className="w-4 h-4" />
                <span>Accepted</span>
              </div>
              {result.gamificationMessage && (
                <span className={`text-[11px] font-mono px-2 py-0.5 rounded border ${result.isFirstSolve
                    ? 'bg-brand-500/15 text-brand-400 border-brand-500/30 font-bold'
                    : 'bg-dark-800/80 text-dark-300 border-dark-700'
                  }`}>
                  {result.gamificationMessage}
                </span>
              )}
            </div>
          )}

          {result.status === 'WRONG_ANSWER' && (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-rose-500/15 border border-rose-500/30 text-rose-400 font-bold">
              <XCircle className="w-4 h-4" />
              <span>Wrong Answer</span>
            </div>
          )}

          {result.status === 'SYNTAX_ERROR' && (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-500/15 border border-amber-500/30 text-amber-400 font-bold">
              <AlertTriangle className="w-4 h-4" />
              <span>Runtime / Syntax Error</span>
            </div>
          )}

          {result.status === 'IDLE' && (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-dark-800 text-dark-300 font-medium">
              <Check className="w-4 h-4 text-brand-400" />
              <span>Query Executed</span>
            </div>
          )}

          {/* Stats */}
          <div className="flex items-center gap-3 text-[11px] text-dark-400 font-mono">
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3 text-dark-500" />
              Runtime: <strong className="text-dark-200">{result.executionTimeMs} ms</strong>
            </span>
            <span>
              Rows: <strong className="text-dark-200">{result.rowCount}</strong>
            </span>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center gap-1 bg-dark-950 p-0.5 rounded-lg border border-dark-800 text-[11px]">
          <button
            onClick={() => setActiveTab('output')}
            className={`px-2.5 py-1 rounded font-medium transition-colors ${activeTab === 'output' ? 'bg-dark-800 text-white shadow-sm' : 'text-dark-400 hover:text-dark-200'
              }`}
          >
            Output Data
          </button>
          <button
            onClick={() => setActiveTab('expected')}
            className={`px-2.5 py-1 rounded font-medium transition-colors ${activeTab === 'expected' ? 'bg-dark-800 text-white shadow-sm' : 'text-dark-400 hover:text-dark-200'
              }`}
          >
            Expected Data
          </button>
          <button
            onClick={() => setActiveTab('diff')}
            className={`px-2.5 py-1 rounded font-medium transition-colors ${activeTab === 'diff' ? 'bg-dark-800 text-white shadow-sm' : 'text-dark-400 hover:text-dark-200'
              }`}
          >
            Diff View
          </button>
          {result.testCaseResults && (
            <button
              onClick={() => setActiveTab('testcases')}
              className={`px-2.5 py-1 rounded font-medium transition-colors flex items-center gap-1 ${activeTab === 'testcases' ? 'bg-dark-800 text-white shadow-sm' : 'text-dark-400 hover:text-dark-200'
                }`}
            >
              <ShieldCheck className="w-3 h-3 text-brand-400" />
              <span>Test Cases ({result.testCaseResults.filter(t => t.passed).length}/{result.testCaseResults.length})</span>
            </button>
          )}
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-auto p-4">

        {/* Error View */}
        {result.errorMessage && (
          <div className="p-4 rounded-lg bg-rose-950/20 border border-rose-800/40 text-rose-300 font-mono text-xs space-y-1">
            <div className="flex items-center gap-2 font-bold text-rose-400">
              <AlertTriangle className="w-4 h-4" />
              <span>Execution Terminated with Error:</span>
            </div>
            <p className="pl-6 text-rose-200">{result.errorMessage}</p>
          </div>
        )}

        {/* Tab 1: User Output Table */}
        {activeTab === 'output' && !result.errorMessage && (
          <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-900/50">
            {result.rows.length === 0 ? (
              <div className="p-6 text-center text-dark-500 italic">
                Query returned 0 rows.
              </div>
            ) : (
              <table className="w-full text-left font-mono text-xs">
                <thead className="bg-dark-900 text-dark-400 text-[10px] uppercase border-b border-dark-800">
                  <tr>
                    <th className="py-2 px-3 text-dark-500 w-10">#</th>
                    {result.columns.map((col) => (
                      <th key={col} className="py-2 px-3 text-brand-400 font-semibold">{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-dark-800 text-dark-200">
                  {result.rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-dark-800/30">
                      <td className="py-2 px-3 text-dark-500">{rIdx + 1}</td>
                      {row.map((val, cIdx) => (
                        <td key={cIdx} className="py-2 px-3 whitespace-nowrap">
                          {val !== null ? String(val) : <span className="text-dark-500 italic">NULL</span>}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {/* Tab 2: Expected Output Table */}
        {activeTab === 'expected' && (
          <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-900/50">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-dark-900 text-dark-400 text-[10px] uppercase border-b border-dark-800">
                <tr>
                  <th className="py-2 px-3 text-dark-500 w-10">#</th>
                  {question.sampleExpectedOutput.columns.map((col) => (
                    <th key={col} className="py-2 px-3 text-cyan-400 font-semibold">{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-800 text-dark-200">
                {question.sampleExpectedOutput.rows.map((row, rIdx) => (
                  <tr key={rIdx} className="hover:bg-dark-800/30">
                    <td className="py-2 px-3 text-dark-500">{rIdx + 1}</td>
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
        )}

        {/* Tab 3: Visual Diff View */}
        {activeTab === 'diff' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <span className="text-[11px] font-semibold uppercase text-dark-400 tracking-wider">
                Your Output ({result.rows.length} rows)
              </span>
              <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-900/40">
                <table className="w-full text-left font-mono text-xs">
                  <thead className="bg-dark-900 text-[10px] text-dark-400 uppercase border-b border-dark-800">
                    <tr>
                      {result.columns.map((c) => (
                        <th key={c} className="py-2 px-3">{c}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-dark-800">
                    {result.rows.map((r, i) => (
                      <tr key={i}>
                        {r.map((v, ci) => (
                          <td key={ci} className="py-2 px-3 whitespace-nowrap text-dark-200">{String(v)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="space-y-1.5">
              <span className="text-[11px] font-semibold uppercase text-dark-400 tracking-wider">
                Expected Output ({question.sampleExpectedOutput.rows.length} rows)
              </span>
              <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-900/40">
                <table className="w-full text-left font-mono text-xs">
                  <thead className="bg-dark-900 text-[10px] text-dark-400 uppercase border-b border-dark-800">
                    <tr>
                      {question.sampleExpectedOutput.columns.map((c) => (
                        <th key={c} className="py-2 px-3">{c}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-dark-800">
                    {question.sampleExpectedOutput.rows.map((r, i) => (
                      <tr key={i}>
                        {r.map((v, ci) => (
                          <td key={ci} className="py-2 px-3 whitespace-nowrap text-dark-200">{String(v)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Tab 4: Test Cases breakdown */}
        {activeTab === 'testcases' && result.testCaseResults && (
          <div className="space-y-4">
            {/* Test Case Selectors */}
            <div className="flex items-center gap-2">
              {result.testCaseResults.map((tc, idx) => (
                <button
                  key={tc.testCaseId}
                  onClick={() => setSelectedTestCaseIdx(idx)}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors ${selectedTestCaseIdx === idx
                      ? 'border-brand-500 bg-brand-500/10 text-white'
                      : 'border-dark-800 bg-dark-900/60 text-dark-400 hover:text-dark-200'
                    }`}
                >
                  {tc.passed ? (
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <XCircle className="w-3.5 h-3.5 text-rose-400" />
                  )}
                  <span>Case {idx + 1}</span>
                  {tc.isHidden && (
                    <span title="Hidden Evaluation Test Case" className="text-dark-500">
                      <Lock className="w-3 h-3" />
                    </span>
                  )}
                </button>
              ))}
            </div>

            {/* Selected Test Case Details */}
            {(() => {
              const currentTc = result.testCaseResults[selectedTestCaseIdx];
              if (!currentTc) return null;
              return (
                <div className="p-4 rounded-xl border border-dark-800 bg-dark-900/50 space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-semibold text-white text-xs">{currentTc.name}</h4>
                      <p className="text-[11px] text-dark-400 mt-0.5">
                        {currentTc.isHidden ? 'Protected hidden evaluation dataset' : 'Standard public sample database state'}
                      </p>
                    </div>
                    <span
                      className={`px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider ${currentTc.passed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                        }`}
                    >
                      {currentTc.passed ? 'Passed' : 'Failed'}
                    </span>
                  </div>

                  {currentTc.mismatchReason && (
                    <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-800/40 text-rose-300 text-xs">
                      {currentTc.mismatchReason}
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
        )}

      </div>
    </div>
  );
};

