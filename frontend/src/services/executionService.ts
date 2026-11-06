import { QueryExecutionResult, QuestionDetail } from '../types';
import { apiRequest } from './apiClient';

export interface SubmissionRecord {
  id: string;
  user_id: string;
  question_id: string;
  question_title: string;
  database_id: string;
  status: string;
  submitted_sql: string;
  execution_time_ms: number;
  passed_test_cases: number;
  total_test_cases: number;
  error_message?: string;
  created_at: string;
}

/**
 * Executes a user SQL query or submits it for semantic multi-dataset test case evaluation.
 * Communicates directly with the FastAPI backend engine at http://localhost:8000.
 */
export async function executeQueryMock(
  sql: string,
  question: QuestionDetail,
  isSubmit: boolean = false
): Promise<QueryExecutionResult> {
  const endpoint = isSubmit ? '/sql/submit' : '/sql/execute';
  const body = isSubmit
    ? { question_id: question.id, sql, mode: 'READ_ONLY' }
    : { database_id: question.databaseId, sql, mode: 'READ_ONLY' };

  try {
    const data = await apiRequest<any>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });

    if (isSubmit) {
      // Map backend SubmissionResult to frontend QueryExecutionResult
      const firstTestCase = data.test_case_results?.[0];
      const actualColumns = firstTestCase?.actual_output?.columns || question.sampleExpectedOutput.columns;
      const actualRows = firstTestCase?.actual_output?.rows || (data.status === 'ACCEPTED' ? question.sampleExpectedOutput.rows : []);

      return {
        status: data.status,
        executionTimeMs: data.execution_time_ms,
        columns: actualColumns,
        rows: actualRows,
        rowCount: actualRows.length,
        errorMessage: data.error_message,
        xpAwarded: data.xp_awarded,
        isFirstSolve: data.is_first_solve,
        gamificationMessage: data.gamification_message,
        testCaseResults: data.test_case_results?.map((tc: any) => ({
          testCaseId: tc.test_case_id,
          name: tc.name,
          isHidden: tc.is_hidden,
          passed: tc.passed,
          mismatchReason: tc.mismatch_reason,
          actualOutput: tc.actual_output,
          expectedOutput: tc.expected_output,
        })),
      };
    } else {
      // Map backend QueryResult to frontend QueryExecutionResult
      return {
        status: data.success ? 'IDLE' : (data.error_type || 'SYNTAX_ERROR'),
        executionTimeMs: data.execution_time_ms,
        columns: data.columns || [],
        rows: data.rows || [],
        rowCount: data.row_count || 0,
        errorMessage: data.error,
      };
    }
  } catch (err: any) {
    return {
      status: 'SYNTAX_ERROR',
      executionTimeMs: 0,
      columns: [],
      rows: [],
      rowCount: 0,
      errorMessage: err.message || 'Execution failed. Check backend connection.',
    };
  }
}

export async function getSubmissionHistory(): Promise<SubmissionRecord[]> {
  try {
    return await apiRequest<SubmissionRecord[]>('/progress/submissions');
  } catch {
    return [];
  }
}
