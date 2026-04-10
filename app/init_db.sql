-- ============================================
-- COMPLETE DATABASE SETUP
-- ============================================

-- ============================================
-- 1. CREATE TABLES
-- ============================================

-- CATEGORY TABLE
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ARTIST/GROUP TABLE
CREATE TABLE artist_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    bio TEXT,
    avatar_image TEXT,
    website_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- MAIN TRACKS TABLE
CREATE TABLE tracks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    cover_image TEXT,
    duration VARCHAR(20),
    release_date DATE,
    is_published BOOLEAN DEFAULT true,
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    artist_group_id INT REFERENCES artist_groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- TRACKS DETAIL TABLE
CREATE TABLE tracks_detail (
    id SERIAL PRIMARY KEY,
    track_id INT UNIQUE REFERENCES tracks(id) ON DELETE CASCADE,
    youtube_link TEXT,
    full_description TEXT,
    lyrics TEXT,
    producer VARCHAR(255),
    writer VARCHAR(255),
    bpm INT,
    key_signature VARCHAR(10),
    total_plays INT DEFAULT 0,
    total_likes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- NEW RELEASES TABLE
CREATE TABLE new_releases (
    id SERIAL PRIMARY KEY,
    track_id INT UNIQUE REFERENCES tracks(id) ON DELETE CASCADE,
    release_status VARCHAR(50) DEFAULT 'upcoming',
    release_date DATE NOT NULL,
    is_featured BOOLEAN DEFAULT false,
    days_countdown INT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 2. CREATE INDEXES
-- ============================================

CREATE INDEX idx_tracks_category ON tracks(category_id);
CREATE INDEX idx_tracks_artist ON tracks(artist_group_id);
CREATE INDEX idx_tracks_created ON tracks(created_at DESC);
CREATE INDEX idx_tracks_published ON tracks(is_published);
CREATE INDEX idx_new_releases_date ON new_releases(release_date DESC);
CREATE INDEX idx_new_releases_status ON new_releases(release_status);

-- ============================================
-- 3. CREATE AUTO-UPDATE FUNCTION
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 4. AUTO-CREATE TRIGGERS FOR ALL TABLES
-- ============================================

DO $$
DECLARE
    tbl_name TEXT;
BEGIN
    FOR tbl_name IN 
        SELECT table_name 
        FROM information_schema.columns 
        WHERE column_name = 'updated_at' 
        AND table_schema = 'public'
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS update_%I_updated_at ON %I', tbl_name, tbl_name);
        EXECUTE format('
            CREATE TRIGGER update_%I_updated_at
            BEFORE UPDATE ON %I
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column()',
            tbl_name, tbl_name
        );
    END LOOP;
END;
$$;

-- ============================================
-- 5. INSERT TEST DATA
-- ============================================

-- Insert categories
INSERT INTO categories (name, slug, description) VALUES 
('Hip Hop', 'hip-hop', 'Best hip hop beats'),
('Jazz', 'jazz', 'Smooth jazz vibes'),
('Electronic', 'electronic', 'Electronic dance music'),
('Lo-fi', 'lo-fi', 'Chill lo-fi beats'),
('R&B', 'r-and-b', 'Rhythm and blues');

-- Insert artist groups
INSERT INTO artist_groups (name, bio, website_url) VALUES 
('Burning Bridge Records', 'Independent record label', 'https://burningbridge.com'),
('Jazzy M', 'Smooth jazz artist', 'https://jazzym.com'),
('Beat Master', 'Electronic beat producer', 'https://beatmaster.com');

-- Insert tracks
INSERT INTO tracks (title, cover_image, duration, release_date, is_published, category_id, artist_group_id) VALUES 
('ONE OF A KIND', 'https://example.com/cover1.jpg', '3:45', '2024-01-15', true, 1, 1),
('Midnight Jazz', 'https://example.com/cover2.jpg', '4:20', '2024-02-01', true, 2, 2),
('Electric Dreams', 'https://example.com/cover3.jpg', '5:10', '2024-02-10', true, 3, 3),
('Chill Study Beats', 'https://example.com/cover4.jpg', '2:30', '2024-02-15', true, 4, 1),
('Soul Night', 'https://example.com/cover5.jpg', '3:55', '2024-02-20', true, 5, 2);

-- Insert track details
INSERT INTO tracks_detail (track_id, youtube_link, full_description, lyrics, producer, writer, bpm, key_signature) VALUES 
(1, 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'A unique blend of hip hop and electronic vibes...', 'Verse 1: Lorem ipsum...', 'Metro Boomin', 'The Weeknd', 140, 'Am'),
(2, 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Smooth jazz for late nights...', 'Jazz instrumental', 'Jazzy M', 'Jazzy M', 120, 'C#'),
(3, 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Electronic dance music to move you...', 'No lyrics', 'Beat Master', 'Beat Master', 128, 'Fm');

-- Insert new releases
INSERT INTO new_releases (track_id, release_status, release_date, is_featured, days_countdown) VALUES 
(1, 'just_released', '2024-01-15', true, 0),
(2, 'upcoming', '2024-03-01', true, 7),
(3, 'new', '2024-02-10', false, 0);

-- ============================================
-- 6. VERIFY SETUP (Output will show in logs)
-- ============================================

DO $$
DECLARE
    table_count INT;
    trigger_count INT;
BEGIN
    -- Count tables
    SELECT COUNT(*) INTO table_count 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE';
    
    -- Count triggers
    SELECT COUNT(*) INTO trigger_count 
    FROM pg_trigger 
    WHERE tgname LIKE 'update_%_updated_at';
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE '✅ DATABASE SETUP COMPLETE!';
    RAISE NOTICE '==========================================';
    RAISE NOTICE '📊 Tables created: %', table_count;
    RAISE NOTICE '⚡ Triggers created: %', trigger_count;
    RAISE NOTICE '==========================================';
END;
$$;

-- Show all tables
\dt

-- Show all triggers
SELECT tgname AS trigger_name, relname AS table_name 
FROM pg_trigger 
JOIN pg_class ON pg_trigger.tgrelid = pg_class.oid 
WHERE tgname LIKE 'update_%_updated_at'
ORDER BY relname;