-- 1. Wipe everything one last time
TRUNCATE Channel, Category, Region, Video, Tag, VideoTag, TrendingSnapshot CASCADE;

-- 2. Load Channels, Categories, Regions (Unique enough usually)
\copy Channel FROM 'data/channels.csv' DELIMITER ',' CSV HEADER
\copy Category FROM 'data/categories.csv' DELIMITER ',' CSV HEADER
\copy Region FROM 'data/regions.csv' DELIMITER ',' CSV HEADER

-- 3. Load Videos (Fixing the carriage return AND duplicates)
CREATE TEMP TABLE temp_video (vid TEXT, tit TEXT, des TEXT, pdate DATE, cid INT, catid INT);
\copy temp_video FROM PROGRAM 'tr -d "\r" < data/videos.csv' WITH (FORMAT CSV, HEADER, QUOTE '"')
INSERT INTO Video SELECT DISTINCT ON (vid) * FROM temp_video ON CONFLICT (VideoID) DO NOTHING;
DROP TABLE temp_video;

-- 4. Load Tags
\copy Tag FROM 'data/tags.csv' DELIMITER ',' CSV HEADER

-- 5. Load VideoTag (Ignore if the video/tag combo already exists)
CREATE TEMP TABLE temp_vtag (vid TEXT, tid INT);
\copy temp_vtag FROM 'data/videotags.csv' DELIMITER ',' CSV HEADER
INSERT INTO VideoTag SELECT DISTINCT * FROM temp_vtag ON CONFLICT DO NOTHING;
DROP TABLE temp_vtag;

-- 6. Load TrendingSnapshots (Fixing Date AND Duplicates)
CREATE TEMP TABLE temp_trending (vid TEXT, reg TEXT, t_date TEXT, vws INT, lks INT, cmts INT, dsks INT);
\copy temp_trending FROM 'data/trending_snapshots.csv' DELIMITER ',' CSV HEADER
INSERT INTO TrendingSnapshot (VideoID, RegionCode, TrendingDate, Views, Likes, CommentCount, Dislikes)
SELECT DISTINCT ON (vid, reg, t_date) vid, reg, TO_DATE(t_date, 'YY.DD.MM'), vws, lks, cmts, dsks 
FROM temp_trending 
ON CONFLICT DO NOTHING;
DROP TABLE temp_trending;
