-- ============================================
-- 健身记录 App - Supabase 数据库初始化 SQL
-- 在 Supabase SQL Editor 中执行此脚本
-- ============================================

-- 1. 训练记录表
CREATE TABLE IF NOT EXISTS workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID DEFAULT auth.uid(),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    exercise_name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT '力量训练',
    sets INTEGER DEFAULT 3,
    reps INTEGER DEFAULT 10,
    weight_kg NUMERIC(6,1) DEFAULT 0,
    duration_min INTEGER DEFAULT 0,
    notes TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 饮食记录表
CREATE TABLE IF NOT EXISTS meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID DEFAULT auth.uid(),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    meal_type TEXT NOT NULL DEFAULT '早餐',
    food_name TEXT NOT NULL,
    calories INTEGER DEFAULT 0,
    protein_g NUMERIC(6,1) DEFAULT 0,
    carbs_g NUMERIC(6,1) DEFAULT 0,
    fat_g NUMERIC(6,1) DEFAULT 0,
    notes TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 身体指标表
CREATE TABLE IF NOT EXISTS body_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID DEFAULT auth.uid(),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    weight_kg NUMERIC(5,1) DEFAULT 0,
    chest_cm NUMERIC(5,1),
    waist_cm NUMERIC(5,1),
    hips_cm NUMERIC(5,1),
    left_arm_cm NUMERIC(5,1),
    right_arm_cm NUMERIC(5,1),
    left_thigh_cm NUMERIC(5,1),
    right_thigh_cm NUMERIC(5,1),
    notes TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 索引优化查询
CREATE INDEX IF NOT EXISTS idx_workouts_date ON workouts(date DESC);
CREATE INDEX IF NOT EXISTS idx_workouts_user ON workouts(user_id);
CREATE INDEX IF NOT EXISTS idx_meals_date ON meals(date DESC);
CREATE INDEX IF NOT EXISTS idx_meals_user ON meals(user_id);
CREATE INDEX IF NOT EXISTS idx_body_metrics_date ON body_metrics(date DESC);
CREATE INDEX IF NOT EXISTS idx_body_metrics_user ON body_metrics(user_id);

-- 5. 启用 Row Level Security (可选：如果使用 auth)
ALTER TABLE workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE body_metrics ENABLE ROW LEVEL SECURITY;

-- 6. RLS 策略 — 允许匿名访问（本地使用 anon key）
-- 生产环境请改为严格的用户隔离策略
CREATE POLICY "Enable all for anon" ON workouts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for anon" ON meals FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for anon" ON body_metrics FOR ALL USING (true) WITH CHECK (true);
