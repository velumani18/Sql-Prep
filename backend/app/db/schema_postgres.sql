-- ====================================================================
-- SQLForge Learner Progress & Motivation Schema (PostgreSQL)
-- ====================================================================

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'usr-demo',
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces',
    xp INT NOT NULL DEFAULT 0,
    streak_days INT NOT NULL DEFAULT 1,
    longest_streak INT NOT NULL DEFAULT 1,
    last_activity_date VARCHAR(20),
    level_title VARCHAR(100) NOT NULL DEFAULT 'SQL Apprentice',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 2. User Topic Progress
CREATE TABLE IF NOT EXISTS user_topic_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_slug VARCHAR(100) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    CONSTRAINT uq_user_topic UNIQUE (user_id, topic_slug)
);

CREATE INDEX IF NOT EXISTS idx_topic_progress_user ON user_topic_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_topic_progress_slug ON user_topic_progress(topic_slug);

-- 3. User Question Status
CREATE TABLE IF NOT EXISTS user_question_status (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id VARCHAR(50) NOT NULL,
    topic_slug VARCHAR(100),
    difficulty VARCHAR(20) NOT NULL DEFAULT 'easy',
    is_solved BOOLEAN NOT NULL DEFAULT FALSE,
    first_solved_at TIMESTAMPTZ,
    attempts_count INT NOT NULL DEFAULT 0,
    failed_attempts_count INT NOT NULL DEFAULT 0,
    last_status VARCHAR(30),
    last_submitted_sql TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_question UNIQUE (user_id, question_id)
);

CREATE INDEX IF NOT EXISTS idx_question_status_user ON user_question_status(user_id);
CREATE INDEX IF NOT EXISTS idx_question_status_qid ON user_question_status(question_id);
CREATE INDEX IF NOT EXISTS idx_question_status_topic ON user_question_status(topic_slug);

-- 4. Submissions Log
CREATE TABLE IF NOT EXISTS submissions (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id VARCHAR(50) NOT NULL,
    question_title VARCHAR(200) NOT NULL,
    database_id VARCHAR(50) NOT NULL,
    topic_slug VARCHAR(100),
    difficulty VARCHAR(20) NOT NULL DEFAULT 'easy',
    status VARCHAR(30) NOT NULL,
    submitted_sql TEXT NOT NULL,
    execution_time_ms FLOAT NOT NULL DEFAULT 0.0,
    passed_test_cases INT NOT NULL DEFAULT 0,
    total_test_cases INT NOT NULL DEFAULT 0,
    error_message TEXT,
    xp_awarded INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_submissions_user ON submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_qid ON submissions(question_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);
CREATE INDEX IF NOT EXISTS idx_submissions_created ON submissions(created_at DESC);

-- 5. User Badges & Achievements
CREATE TABLE IF NOT EXISTS user_badges (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_key VARCHAR(100) NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    badge_type VARCHAR(50) NOT NULL DEFAULT 'topic',
    icon VARCHAR(50) NOT NULL DEFAULT 'Award',
    earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_badge UNIQUE (user_id, badge_key)
);

CREATE INDEX IF NOT EXISTS idx_badges_user ON user_badges(user_id);
CREATE INDEX IF NOT EXISTS idx_badges_key ON user_badges(badge_key);

-- 6. User Curriculum Level Milestones
CREATE TABLE IF NOT EXISTS user_level_milestones (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    level_number INT NOT NULL,
    level_title VARCHAR(150) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    xp_awarded INT NOT NULL DEFAULT 0,
    CONSTRAINT uq_user_level UNIQUE (user_id, level_number)
);

CREATE INDEX IF NOT EXISTS idx_milestones_user ON user_level_milestones(user_id);
CREATE INDEX IF NOT EXISTS idx_milestones_lvl ON user_level_milestones(level_number);

