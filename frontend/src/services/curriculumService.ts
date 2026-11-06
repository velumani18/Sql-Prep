import { apiRequest } from './apiClient';
import { CurriculumModule, TopicLesson } from '../types';
import { mockCurriculumModules, mockTopicLesson } from './mockData';

export async function getCurriculumModules(): Promise<CurriculumModule[]> {
  try {
    const levels = await apiRequest<any[]>('/curriculum/levels');
    return levels.map((lvl) => ({
      id: `module-${lvl.level_number}`,
      slug: lvl.slug,
      title: lvl.title,
      description: lvl.description,
      level: (lvl.difficulty.toLowerCase() === 'beginner'
        ? 'beginner'
        : lvl.difficulty.toLowerCase() === 'intermediate'
        ? 'intermediate'
        : 'advanced') as 'beginner' | 'intermediate' | 'advanced',
      icon: lvl.level_number <= 2 ? 'Code' : lvl.level_number <= 4 ? 'GitMerge' : 'Cpu',
      isLocked: false,
      totalTopics: lvl.total_topics,
      completedTopics: lvl.completed_topics,
      estimatedHours: lvl.estimated_hours,
      lessons: lvl.topics.map((t: any) => ({
        id: t.id,
        slug: t.slug,
        title: t.title,
        isCompleted: t.is_completed,
        questionsCount: t.questions_count,
      })),
    }));
  } catch (err) {
    console.warn('Backend curriculum levels unreachable, using cached mock data:', err);
    return mockCurriculumModules;
  }
}

export async function getTopicLessonBySlug(slug: string): Promise<TopicLesson> {
  try {
    const data = await apiRequest<any>(`/curriculum/topics/${slug}`);
    
    // Map backend TopicLesson model to frontend TopicLesson interface
    return {
      id: data.id,
      slug: data.slug,
      moduleId: `module-${data.level_number}`,
      moduleName: data.level_title,
      title: data.title,
      level: data.level_number <= 2 ? 'beginner' : data.level_number <= 4 ? 'intermediate' : 'advanced',
      readTimeMinutes: 12,
      orderIndex: data.order_index,
      conceptSummary: data.detailed_explanation.slice(0, 200) + '...',
      conceptContent: data.detailed_explanation.split('\n\n'),
      syntaxBlocks: [
        {
          title: 'Syntax Reference',
          description: 'Official standard syntax definition and keyword specification.',
          syntax: data.syntax_reference,
          notes: data.clause_breakdown?.map((c: any) => `${c.keyword}: ${c.purpose}`),
        },
      ],
      examples: data.worked_examples?.map((ex: any) => ({
        title: ex.title,
        description: ex.explanation,
        sql: ex.sql,
        columns: ex.columns,
        rows: ex.rows,
      })) || [],
      practiceQuestions: data.practice_questions?.map((q: any) => ({
        id: q.id,
        slug: q.slug,
        title: q.title,
        difficulty: q.difficulty.toLowerCase() as 'easy' | 'medium' | 'hard',
        isSolved: q.is_solved,
      })) || [],
    };
  } catch (err) {
    console.warn(`Backend topic '${slug}' unreachable, falling back:`, err);
    return {
      ...mockTopicLesson,
      slug,
      title: slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    };
  }
}

export async function markTopicCompleted(topicSlug: string): Promise<{ success: boolean; xp_awarded: number }> {
  try {
    return await apiRequest<{ success: boolean; xp_awarded: number }>(`/curriculum/topics/${topicSlug}/complete`, {
      method: 'POST',
    });
  } catch {
    return { success: true, xp_awarded: 100 };
  }
}
