import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Database,
  FileText,
  Sparkles,
  History,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Code2,
} from 'lucide-react';
import {
  getQuestionBySlug,
  getDatabaseSchema,
  previewTableData,
  getQuestionSolution,
  getQuestionList,
} from '../services/questionService';
import { executeQueryMock, getSubmissionHistory, SubmissionRecord } from '../services/executionService';
import {
  QuestionDetail,
  SyntheticDatabase,
  TableDefinition,
  QueryExecutionResult,
} from '../types';
import { ProblemDescription } from '../components/workspace/ProblemDescription';
import { SchemaExplorer } from '../components/workspace/SchemaExplorer';
import { TablePreviewModal } from '../components/workspace/TablePreviewModal';
import { MonacoSQLEditor } from '../components/workspace/MonacoSQLEditor';
import { EditorToolbar } from '../components/workspace/EditorToolbar';
import { ExecutionOutput } from '../components/workspace/ExecutionOutput';

export const WorkspacePage: React.FC = () => {
  const { questionSlug } = useParams<{ questionSlug?: string }>();
  const navigate = useNavigate();

  const [question, setQuestion] = useState<QuestionDetail | null>(null);
  const [activeDatabase, setActiveDatabase] = useState<SyntheticDatabase | null>(null);
  const [editorSql, setEditorSql] = useState<string>('');
  const [previewTable, setPreviewTable] = useState<TableDefinition | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Left panel view mode
  const [leftNavMode, setLeftNavMode] = useState<'description' | 'schema' | 'hints' | 'solution' | 'submissions'>('description');
  
  // Official solution state
  const [solutionData, setSolutionData] = useState<{ solution_sql: string; alternative_solution?: string; detailed_explanation: string } | null>(null);
  const [loadingSolution, setLoadingSolution] = useState(false);

  // Submissions history state
  const [submissionsList, setSubmissionsList] = useState<SubmissionRecord[]>([]);
  const [loadingSubmissions, setLoadingSubmissions] = useState(false);

  // Execution status
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [executionResult, setExecutionResult] = useState<QueryExecutionResult | null>(null);

  // Questions index for prev/next navigation
  const [allQuestionsList, setAllQuestionsList] = useState<any[]>([]);

  // Load question and database on slug change
  useEffect(() => {
    let isMounted = true;
    async function loadWorkspaceData() {
      setIsLoading(true);
      setExecutionResult(null);
      setSolutionData(null);

      try {
        const targetSlug = questionSlug || 'q-001';
        const qDetail = await getQuestionBySlug(targetSlug);
        if (!isMounted) return;

        setQuestion(qDetail);
        setEditorSql(qDetail.starterCode || '-- Write your query below\nSELECT \n');

        // Fetch database schema
        const dbSchema = await getDatabaseSchema(qDetail.databaseId);
        if (!isMounted) return;
        setActiveDatabase(dbSchema);

        // Fetch question list for navigation
        const list = await getQuestionList();
        if (!isMounted) return;
        setAllQuestionsList(list);
      } catch (err) {
        console.error('Error loading workspace:', err);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }

    loadWorkspaceData();
    return () => {
      isMounted = false;
    };
  }, [questionSlug]);

  // Load solutions when solution tab is selected
  useEffect(() => {
    if (leftNavMode === 'solution' && question && !solutionData) {
      setLoadingSolution(true);
      getQuestionSolution(question.id)
        .then((data) => setSolutionData(data))
        .catch((err) => console.error('Failed to load solution:', err))
        .finally(() => setLoadingSolution(false));
    } else if (leftNavMode === 'submissions') {
      setLoadingSubmissions(true);
      getSubmissionHistory()
        .then((records) => setSubmissionsList(records))
        .catch((err) => console.error('Failed to load submissions:', err))
        .finally(() => setLoadingSubmissions(false));
    }
  }, [leftNavMode, question, solutionData]);

  // Handle table preview click
  const handleTablePreview = async (table: TableDefinition) => {
    if (!activeDatabase) return;
    try {
      const preview = await previewTableData(activeDatabase.id, table.name, 10);
      const formattedSample = preview.rows.map((row) => {
        const obj: Record<string, any> = {};
        preview.columns.forEach((colName, idx) => {
          obj[colName] = row[idx];
        });
        return obj;
      });

      setPreviewTable({
        ...table,
        sampleData: formattedSample,
      });
    } catch {
      setPreviewTable(table);
    }
  };

  const handleRunQuery = async () => {
    if (!question) return;
    setIsRunning(true);
    try {
      const res = await executeQueryMock(editorSql, question, false);
      setExecutionResult(res);
    } finally {
      setIsRunning(false);
    }
  };

  const handleSubmitQuery = async () => {
    if (!question) return;
    setIsSubmitting(true);
    try {
      const res = await executeQueryMock(editorSql, question, true);
      setExecutionResult(res);

      // If accepted, refresh submissions list if viewing submissions
      if (res.status === 'ACCEPTED') {
        getSubmissionHistory().then(setSubmissionsList).catch(() => {});
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResetCode = () => {
    if (question) {
      setEditorSql(question.starterCode);
    }
  };

  const handleFormatCode = () => {
    const formatted = editorSql
      .replace(/\s+/g, ' ')
      .replace(/SELECT /gi, 'SELECT\n    ')
      .replace(/FROM /gi, '\nFROM\n    ')
      .replace(/LEFT JOIN /gi, '\nLEFT JOIN\n    ')
      .replace(/INNER JOIN /gi, '\nINNER JOIN\n    ')
      .replace(/WHERE /gi, '\nWHERE\n    ')
      .replace(/GROUP BY /gi, '\nGROUP BY\n    ')
      .replace(/HAVING /gi, '\nHAVING\n    ')
      .replace(/ORDER BY /gi, '\nORDER BY\n    ')
      .replace(/LIMIT /gi, '\nLIMIT ')
      .replace(/;/g, ';\n');
    setEditorSql(formatted);
  };

  // Prev / Next Question Navigation
  const currentIndex = allQuestionsList.findIndex((q) => q.id === question?.id || q.slug === question?.slug);
  const prevQuestion = currentIndex > 0 ? allQuestionsList[currentIndex - 1] : null;
  const nextQuestion = currentIndex >= 0 && currentIndex < allQuestionsList.length - 1 ? allQuestionsList[currentIndex + 1] : null;

  if (isLoading || !question || !activeDatabase) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-4rem)] bg-dark-950 text-dark-300">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm font-medium text-dark-300">Connecting to SQL sandbox engine...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-dark-950 overflow-hidden">
      
      {/* Workspace Top Sub-Header */}
      <div className="h-10 border-b border-dark-800 bg-dark-900/90 px-4 flex items-center justify-between text-xs text-dark-300 shrink-0">
        
        {/* Left Breadcrumb & Prev/Next */}
        <div className="flex items-center gap-3">
          <Link
            to={`/topic/${question.topicSlug}`}
            className="flex items-center gap-1.5 text-dark-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Back to Lesson</span>
          </Link>

          <span className="text-dark-700">|</span>

          <div className="flex items-center gap-2">
            <span className="font-semibold text-white truncate max-w-xs sm:max-w-md">
              {question.title}
            </span>
            <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
              question.difficulty === 'easy'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : question.difficulty === 'medium'
                ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
            }`}>
              {question.difficulty}
            </span>
          </div>
        </div>

        {/* Right Pager */}
        <div className="flex items-center gap-2">
          <button
            title={prevQuestion ? `Previous: ${prevQuestion.title}` : 'No previous problem'}
            disabled={!prevQuestion}
            onClick={() => prevQuestion && navigate(`/practice/${prevQuestion.slug || prevQuestion.id}`)}
            className="p-1 rounded text-dark-400 hover:text-white hover:bg-dark-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-dark-400 text-[11px] font-mono">
            {currentIndex >= 0 ? `${currentIndex + 1} / ${allQuestionsList.length}` : 'Exercise'}
          </span>
          <button
            title={nextQuestion ? `Next: ${nextQuestion.title}` : 'No next problem'}
            disabled={!nextQuestion}
            onClick={() => nextQuestion && navigate(`/practice/${nextQuestion.slug || nextQuestion.id}`)}
            className="p-1 rounded text-dark-400 hover:text-white hover:bg-dark-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Split-Screen Workspace Content */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        
        {/* Left Side: Navigation Tabs & Problem / Schema / Solution Panels */}
        <div className="w-full lg:w-[45%] xl:w-[40%] flex flex-col border-b lg:border-b-0 lg:border-r border-dark-800 bg-dark-900/40 overflow-hidden">
          
          {/* Navigation Bar for Left Side */}
          <div className="h-10 border-b border-dark-800 bg-dark-900 flex items-center px-2 gap-1 shrink-0">
            <button
              onClick={() => setLeftNavMode('description')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                leftNavMode === 'description'
                  ? 'bg-dark-800 text-white shadow-sm'
                  : 'text-dark-400 hover:text-dark-200 hover:bg-dark-800/40'
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-brand-400" />
              Description
            </button>

            <button
              onClick={() => setLeftNavMode('schema')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                leftNavMode === 'schema'
                  ? 'bg-dark-800 text-white shadow-sm'
                  : 'text-dark-400 hover:text-dark-200 hover:bg-dark-800/40'
              }`}
            >
              <Database className="w-3.5 h-3.5 text-blue-400" />
              Schema ({activeDatabase.tables.length})
            </button>

            <button
              onClick={() => setLeftNavMode('hints')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                leftNavMode === 'hints'
                  ? 'bg-dark-800 text-white shadow-sm'
                  : 'text-dark-400 hover:text-dark-200 hover:bg-dark-800/40'
              }`}
            >
              <HelpCircle className="w-3.5 h-3.5 text-amber-400" />
              Hints ({question.hints.length})
            </button>

            <button
              onClick={() => setLeftNavMode('solution')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                leftNavMode === 'solution'
                  ? 'bg-dark-800 text-white shadow-sm'
                  : 'text-dark-400 hover:text-dark-200 hover:bg-dark-800/40'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              Solution
            </button>

            <button
              onClick={() => setLeftNavMode('submissions')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                leftNavMode === 'submissions'
                  ? 'bg-dark-800 text-white shadow-sm'
                  : 'text-dark-400 hover:text-dark-200 hover:bg-dark-800/40'
              }`}
            >
              <History className="w-3.5 h-3.5 text-cyan-400" />
              Submissions
            </button>
          </div>

          {/* Left Panel Body */}
          <div className="flex-1 overflow-y-auto">
            {leftNavMode === 'description' && (
              <ProblemDescription
                question={question}
                activeTab="description"
                setActiveTab={(tab) => setLeftNavMode(tab)}
              />
            )}

            {leftNavMode === 'schema' && (
              <div className="p-4">
                <SchemaExplorer
                  database={activeDatabase}
                  onPreviewTable={(table: TableDefinition) => handleTablePreview(table)}
                />
              </div>
            )}

            {leftNavMode === 'hints' && (
              <div className="p-6 space-y-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <HelpCircle className="w-4 h-4 text-amber-400" />
                  Progressive Problem Hints
                </h3>
                <div className="space-y-3">
                  {question.hints.map((hint, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl border border-dark-800 bg-dark-900/60 space-y-1.5"
                    >
                      <span className="text-[11px] font-bold text-amber-400 uppercase tracking-wider">
                        Hint {idx + 1}
                      </span>
                      <p className="text-xs text-dark-300 leading-relaxed">{hint}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {leftNavMode === 'solution' && (
              <div className="p-6 space-y-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-purple-400" />
                    Verified Reference Solution
                  </h3>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    Engine Verified
                  </span>
                </div>

                {loadingSolution ? (
                  <div className="p-8 text-center text-xs text-dark-400">Loading verified solution...</div>
                ) : solutionData ? (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <span className="text-xs font-semibold text-dark-300">Primary SQL Solution</span>
                      <pre className="p-4 rounded-xl bg-dark-950 border border-dark-800 text-xs font-mono text-emerald-300 overflow-x-auto whitespace-pre-wrap">
                        {solutionData.solution_sql}
                      </pre>
                    </div>

                    {solutionData.alternative_solution && (
                      <div className="space-y-2">
                        <span className="text-xs font-semibold text-dark-300">Alternative Approach</span>
                        <pre className="p-4 rounded-xl bg-dark-950 border border-dark-800 text-xs font-mono text-cyan-300 overflow-x-auto whitespace-pre-wrap">
                          {solutionData.alternative_solution}
                        </pre>
                      </div>
                    )}

                    <div className="p-4 rounded-xl bg-dark-900/80 border border-dark-800 text-xs text-dark-300 leading-relaxed space-y-1.5">
                      <span className="font-semibold text-white block">Algorithmic Explanation</span>
                      <p>{solutionData.detailed_explanation}</p>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-dark-400">Unable to load solution.</p>
                )}
              </div>
            )}

            {leftNavMode === 'submissions' && (
              <div className="p-6 space-y-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <History className="w-4 h-4 text-cyan-400" />
                  Your Submission History
                </h3>
                {loadingSubmissions ? (
                  <div className="p-8 text-center text-xs text-dark-400">Loading submissions...</div>
                ) : submissionsList.length === 0 ? (
                  <div className="p-8 text-center text-xs text-dark-400 border border-dashed border-dark-800 rounded-xl">
                    No submissions recorded yet. Click Submit to evaluate your query!
                  </div>
                ) : (
                  <div className="space-y-3">
                    {submissionsList.map((sub) => (
                      <div
                        key={sub.id}
                        className={`p-3.5 rounded-xl border transition-all ${
                          sub.status === 'ACCEPTED'
                            ? 'bg-emerald-500/5 border-emerald-500/20'
                            : 'bg-rose-500/5 border-rose-500/20'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1.5">
                          <div className="flex items-center gap-2">
                            {sub.status === 'ACCEPTED' ? (
                              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                            ) : (
                              <XCircle className="w-4 h-4 text-rose-400" />
                            )}
                            <span className={`text-xs font-bold ${
                              sub.status === 'ACCEPTED' ? 'text-emerald-400' : 'text-rose-400'
                            }`}>
                              {sub.status === 'ACCEPTED' ? 'Accepted' : 'Wrong Answer'}
                            </span>
                          </div>
                          <span className="text-[10px] font-mono text-dark-400">
                            {new Date(sub.created_at).toLocaleTimeString()}
                          </span>
                        </div>
                        <div className="text-[11px] text-dark-300 font-mono flex items-center justify-between">
                          <span>{sub.passed_test_cases} / {sub.total_test_cases} test cases passed</span>
                          <span className="text-dark-500">{sub.execution_time_ms.toFixed(2)} ms</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Side: Monaco SQL Editor & Execution Results Panel */}
        <div className="w-full lg:w-[55%] xl:w-[60%] flex flex-col h-full overflow-hidden bg-dark-950">
          
          {/* Top Half: Editor with Toolbar */}
          <div className="h-[55%] flex flex-col border-b border-dark-800">
            <EditorToolbar
              databaseName={question.databaseName}
              isRunning={isRunning}
              isSubmitting={isSubmitting}
              onRunQuery={handleRunQuery}
              onSubmitQuery={handleSubmitQuery}
              onResetCode={handleResetCode}
              onFormatCode={handleFormatCode}
            />

            <div className="flex-1 relative overflow-hidden">
              <MonacoSQLEditor
                value={editorSql}
                onChange={(newVal) => setEditorSql(newVal)}
                onRunQuery={handleRunQuery}
              />
            </div>
          </div>

          {/* Bottom Half: Execution Output, Results, Diff, Test Cases */}
          <div className="h-[45%] flex flex-col bg-dark-950 overflow-hidden">
            <ExecutionOutput
              result={executionResult}
              question={question}
              isRunning={isRunning}
              isSubmitting={isSubmitting}
            />
          </div>

        </div>

      </div>

      {/* Dynamic Table Preview Modal */}
      {previewTable && (
        <TablePreviewModal
          table={previewTable}
          databaseName={activeDatabase.displayName}
          onClose={() => setPreviewTable(null)}
        />
      )}

    </div>
  );
};
