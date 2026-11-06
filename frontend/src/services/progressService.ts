import { apiRequest } from './apiClient';

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  avatar_url: string;
  streak_days: number;
  longest_streak: number;
  xp: number;
  level_title: string;
  rank_level: number;
  next_rank_xp: number;
  rank_progress_percentage: number;
  last_active?: string;
}

export interface BadgeInfo {
  key: string;
  title: string;
  description: string;
  badge_type: 'topic' | 'level_milestone' | 'streak';
  icon: string;
  earned_at: string;
}

export interface LevelProgress {
  level_number: number;
  title: string;
  description?: string;
  total_topics: number;
  completed_topics: number;
  total_questions: number;
  solved_questions: number;
  completion_percentage: number;
  is_completed: boolean;
  milestone_badge?: BadgeInfo;
}

export interface TopicProgress {
  topic_slug: string;
  title: string;
  level_number: number;
  level_title: string;
  is_completed: boolean;
  total_questions: number;
  attempted_questions: number;
  solved_questions: number;
  completion_rate: number;
  accuracy_rate: number;
  badge?: BadgeInfo;
}

export interface WeakTopic {
  topic_slug: string;
  title: string;
  level_number: number;
  failed_attempts_count: number;
  unsolved_questions_count: number;
  accuracy_percentage: number;
  reason: string;
  recommended_action: string;
  lesson_url: string;
  practice_url: string;
}

export interface RecommendedTopic {
  topic_slug: string;
  title: string;
  level_number: number;
  level_title: string;
  reason: string;
  recommended_action: 'continue_curriculum' | 'review_weak_topic';
  lesson_url: string;
  practice_url: string;
}

export interface DailyActivity {
  date: string;
  day_name: string;
  submissions_count: number;
  active: boolean;
}

export interface SubmissionRecord {
  id: string;
  user_id: string;
  question_id: string;
  question_title: string;
  database_id: string;
  topic_slug?: string;
  difficulty: string;
  status: string;
  submitted_sql: string;
  execution_time_ms: number;
  passed_test_cases: number;
  total_test_cases: number;
  xp_awarded: number;
  error_message?: string;
  created_at: string;
}

export interface ProgressSummary {
  user: UserProfile;
  overall_progress_percentage: number;
  total_questions: number;
  solved_questions_count: number;
  attempted_questions_count: number;
  easy_solved: number;
  easy_total: number;
  medium_solved: number;
  medium_total: number;
  hard_solved: number;
  hard_total: number;
  total_submissions: number;
  accepted_submissions: number;
  submission_accuracy_percentage: number;
  question_accuracy_percentage: number;
  total_topics_count: number;
  completed_topics_count: number;
  level_progress: LevelProgress[];
  topic_progress: TopicProgress[];
  weak_topics: WeakTopic[];
  recommended_topic?: RecommendedTopic;
  recent_submissions: SubmissionRecord[];
  badges: BadgeInfo[];
  weekly_activity: DailyActivity[];
}

export const progressService = {
  async getSummary(): Promise<ProgressSummary> {
    return await apiRequest<ProgressSummary>('/progress/summary');
  },

  async getLevelProgress(): Promise<LevelProgress[]> {
    return await apiRequest<LevelProgress[]>('/progress/levels');
  },

  async getTopicProgress(): Promise<TopicProgress[]> {
    return await apiRequest<TopicProgress[]>('/progress/topics');
  },

  async getWeakTopics(): Promise<WeakTopic[]> {
    return await apiRequest<WeakTopic[]>('/progress/weak-topics');
  },

  async getRecommendedTopic(): Promise<RecommendedTopic | null> {
    return await apiRequest<RecommendedTopic | null>('/progress/recommended');
  },

  async getBadges(): Promise<BadgeInfo[]> {
    return await apiRequest<BadgeInfo[]>('/progress/badges');
  },

  async reset(): Promise<void> {
    await apiRequest('/progress/reset', { method: 'POST' });
  },
};
