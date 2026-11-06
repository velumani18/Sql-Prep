// Database and Schema Types
export interface ColumnDefinition {
  name: string;
  type: string;
  isPrimaryKey?: boolean;
  isForeignKey?: boolean;
  references?: string;
  nullable?: boolean;
  description?: string;
}

export interface TableDefinition {
  name: string;
  description: string;
  rowCount: number;
  columns: ColumnDefinition[];
  sampleData: Record<string, any>[];
}

export interface SyntheticDatabase {
  id: string;
  name: string;
  displayName: string;
  description: string;
  tables: TableDefinition[];
}

// Curriculum and Lesson Types
export interface PracticeQuestionSummary {
  id: string;
  title: string;
  slug: string;
  difficulty: 'easy' | 'medium' | 'hard';
  isSolved?: boolean;
}

export interface LessonExample {
  title: string;
  description: string;
  sql: string;
  columns: string[];
  rows: (string | number | null)[][];
}

export interface TopicLesson {
  id: string;
  slug: string;
  moduleId: string;
  moduleName: string;
  title: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  readTimeMinutes: number;
  orderIndex: number;
  conceptSummary: string;
  conceptContent: string[];
  syntaxBlocks: {
    title: string;
    description: string;
    syntax: string;
    notes?: string[];
  }[];
  examples: LessonExample[];
  practiceQuestions: PracticeQuestionSummary[];
  nextLessonSlug?: string;
  prevLessonSlug?: string;
}

export interface CurriculumModule {
  id: string;
  slug: string;
  title: string;
  description: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  icon: string;
  isLocked: boolean;
  prerequisites?: string[];
  totalTopics: number;
  completedTopics: number;
  estimatedHours: number;
  lessons: {
    id: string;
    slug: string;
    title: string;
    isCompleted: boolean;
    questionsCount: number;
  }[];
}

// Question & Practice Types
export interface TestCase {
  id: string;
  name: string;
  description: string;
  isHidden: boolean;
  expectedColumns: string[];
  expectedRows: (string | number | null)[][];
}

export interface QuestionDetail {
  id: string;
  slug: string;
  title: string;
  difficulty: 'easy' | 'medium' | 'hard';
  topic: string;
  topicSlug: string;
  databaseId: string;
  databaseName: string;
  acceptanceRate: string;
  prompt: string;
  requirements: string[];
  starterCode: string;
  officialSolution: {
    sql: string;
    explanation: string;
    timeComplexity?: string;
  };
  hints: string[];
  sampleExpectedOutput: {
    columns: string[];
    rows: (string | number | null)[][];
  };
  testCases: TestCase[];
}

// Query Execution & Evaluation Types
export type ExecutionStatus = 'IDLE' | 'RUNNING' | 'ACCEPTED' | 'WRONG_ANSWER' | 'SYNTAX_ERROR';

export interface QueryExecutionResult {
  status: ExecutionStatus;
  executionTimeMs: number;
  columns: string[];
  rows: (string | number | null)[][];
  rowCount: number;
  errorMessage?: string;
  xpAwarded?: number;
  isFirstSolve?: boolean;
  gamificationMessage?: string;
  testCaseResults?: {
    testCaseId: string;
    name: string;
    isHidden: boolean;
    passed: boolean;
    actualOutput?: {
      columns: string[];
      rows: (string | number | null)[][];
    };
    expectedOutput?: {
      columns: string[];
      rows: (string | number | null)[][];
    };
    mismatchReason?: string;
  }[];
}

// User & Dashboard Types
export interface UserProfile {
  id: string;
  name: string;
  username: string;
  email: string;
  avatarUrl: string;
  xpPoints: number;
  currentStreak: number;
  maxStreak: number;
  solvedCount: {
    easy: number;
    medium: number;
    hard: number;
    total: number;
  };
}

export interface RecentAttempt {
  id: string;
  questionId: string;
  questionTitle: string;
  questionSlug: string;
  difficulty: 'easy' | 'medium' | 'hard';
  status: 'solved' | 'attempted';
  timestamp: string;
  executionTimeMs: number;
}

