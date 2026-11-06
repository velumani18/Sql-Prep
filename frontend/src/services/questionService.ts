import { apiRequest } from './apiClient';
import { QuestionDetail, SyntheticDatabase, TableDefinition } from '../types';
import { mockQuestionDetail, mockDatabases, mockInterviewQuestions, InterviewQuestionItem } from './mockData';

export async function getQuestionList(filters?: {
  topic_id?: string;
  difficulty?: string;
  database_id?: string;
  search?: string;
}): Promise<any[]> {
  try {
    const params = new URLSearchParams();
    if (filters?.topic_id) params.append('topic_id', filters.topic_id);
    if (filters?.difficulty) params.append('difficulty', filters.difficulty);
    if (filters?.database_id) params.append('database_id', filters.database_id);
    if (filters?.search) params.append('search', filters.search);

    const queryString = params.toString() ? `?${params.toString()}` : '';
    const res = await apiRequest<{ total: number; questions: any[] }>(`/questions${queryString}`);
    return res.questions;
  } catch (err) {
    console.warn('Failed to fetch questions from backend, falling back to mock data:', err);
    return mockInterviewQuestions;
  }
}

export async function getQuestionBySlug(slugOrId: string): Promise<QuestionDetail> {
  try {
    const data = await apiRequest<any>(`/questions/${slugOrId}`);
    
    // Map backend BankQuestion / Question payload to QuestionDetail
    return {
      id: data.id,
      slug: data.slug,
      title: data.title,
      difficulty: data.difficulty.toLowerCase() as 'easy' | 'medium' | 'hard',
      topic: data.topic || 'SQL Fundamentals',
      topicSlug: data.topic_id || 'sql-fundamentals',
      databaseId: data.database_id,
      databaseName: data.database_id.replace('db-', '') + '_db',
      acceptanceRate: data.difficulty === 'easy' ? '85.2%' : data.difficulty === 'medium' ? '64.1%' : '42.8%',
      prompt: data.prompt,
      requirements: [
        'Single valid SQL query statement.',
        data.order_matters ? 'Strict row ordering required (ORDER BY).' : 'Row ordering does not matter (evaluated via multiset comparison).',
        data.check_column_names ? 'Output column names and aliases must match specifications.' : 'Output column order will be matched.',
      ],
      starterCode: data.starter_code,
      officialSolution: {
        sql: '-- Click to reveal solution in official tab',
        explanation: data.detailed_explanation || 'Reference approach provided in explanations tab.',
      },
      hints: data.hints || ['Break down the query into FROM, WHERE, and SELECT clauses.', 'Test table column types in the schema explorer.'],
      sampleExpectedOutput: {
        columns: data.expected_output?.columns || ['col1', 'col2'],
        rows: data.expected_output?.sample_rows || [],
      },
      testCases: (data.test_cases || []).map((tc: any) => ({
        id: tc.id,
        name: tc.name,
        description: tc.description,
        isHidden: tc.is_hidden,
        expectedColumns: data.expected_output?.columns || [],
        expectedRows: tc.is_hidden ? [] : (data.expected_output?.sample_rows || []),
      })),
    };
  } catch (err) {
    console.warn(`Failed to fetch question '${slugOrId}' from backend:`, err);
    if (slugOrId === mockQuestionDetail.slug || !slugOrId) {
      return mockQuestionDetail;
    }
    return {
      ...mockQuestionDetail,
      slug: slugOrId,
      title: slugOrId.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    };
  }
}

export async function getQuestionSolution(questionId: string): Promise<{
  id: string;
  title: string;
  solution_sql: string;
  alternative_solution?: string;
  detailed_explanation: string;
}> {
  try {
    return await apiRequest<any>(`/questions/${questionId}/solution`);
  } catch {
    return {
      id: questionId,
      title: 'Solution',
      solution_sql: '-- Solution unavailable offline',
      detailed_explanation: 'Connect to the backend engine to view official solution.',
    };
  }
}

export async function getDatabaseSchema(databaseId: string): Promise<SyntheticDatabase> {
  try {
    const data = await apiRequest<any>(`/databases/${databaseId}/schema`);
    return {
      id: data.id,
      name: data.name,
      displayName: data.display_name,
      description: data.description,
      tables: data.tables.map((tbl: any) => ({
        name: tbl.name,
        description: tbl.description || `Table ${tbl.name} in ${data.name}`,
        rowCount: tbl.row_count || 0,
        columns: tbl.columns.map((col: any) => ({
          name: col.name,
          type: col.type,
          isPrimaryKey: col.is_primary_key,
          isForeignKey: col.is_foreign_key,
          references: col.references,
          nullable: col.nullable,
          description: col.description,
        })),
        sampleData: [],
      })),
    };
  } catch (err) {
    console.warn(`Failed to fetch schema for '${databaseId}', falling back:`, err);
    const found = mockDatabases.find(db => db.id === databaseId || db.name === databaseId);
    return found || mockDatabases[0];
  }
}

export async function previewTableData(
  databaseId: string,
  tableName: string,
  limit: number = 10
): Promise<{
  tableName: string;
  columns: string[];
  rows: any[][];
  rowCount: number;
}> {
  try {
    const data = await apiRequest<any>(`/databases/${databaseId}/tables/${tableName}?limit=${limit}`);
    return {
      tableName: data.table_name,
      columns: data.columns_list || data.columns.map((c: any) => c.name),
      rows: data.sample_rows || [],
      rowCount: data.row_count || 0,
    };
  } catch (err) {
    console.warn(`Failed to preview table '${tableName}':`, err);
    return {
      tableName,
      columns: ['id'],
      rows: [[1]],
      rowCount: 1,
    };
  }
}

export async function getInterviewQuestions(): Promise<InterviewQuestionItem[]> {
  try {
    const questions = await getQuestionList();
    return questions.map((q) => ({
      id: q.id,
      slug: q.slug,
      title: q.title,
      difficulty: q.difficulty.toLowerCase() as 'easy' | 'medium' | 'hard',
      topic: q.topic || 'SQL Fundamentals',
      databaseName: q.database_id.replace('db-', '') + '_db',
      acceptanceRate: `${q.acceptance_rate}%`,
      companies: q.company_tags || ['Amazon', 'Google'],
      isSolved: q.is_solved,
    }));
  } catch {
    return mockInterviewQuestions;
  }
}
