import csv
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="",
    host="localhost"
)

cur = conn.cursor()

# 1. Wipe everything
cur.execute("""
TRUNCATE Channel, Category, Region, Video, Tag, VideoTag, TrendingSnapshot CASCADE;
""")
conn.commit()

# 2. Load simple tables
def load_simple_csv(table_name, file_path, columns):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = [row[col] if row[col] != '' else None for col in columns]
            placeholders = ", ".join(["%s"] * len(columns))
            col_string = ", ".join(columns)
            cur.execute(
                f"INSERT INTO {table_name} ({col_string}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;",
                values
            )
    conn.commit()

load_simple_csv("Channel", "data/channels.csv",
                ["ChannelID", "ChannelName", "Country", "SubscriberCount"])

load_simple_csv("Category", "data/categories.csv",
                ["CategoryID", "CategoryName"])

load_simple_csv("Region", "data/regions.csv",
                ["RegionCode", "RegionName"])

load_simple_csv("Tag", "data/tags.csv",
                ["TagID", "TagName"])

# 3. Load Videos (remove carriage returns, skip duplicates)
seen_videos = set()
with open("data/videos.csv", newline='', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        video_id = row["VideoID"]
        if video_id in seen_videos:
            continue
        seen_videos.add(video_id)

        title = row["Title"].replace("\r", " ").replace("\n", " ") if row["Title"] else None
        description = row["Description"].replace("\r", " ").replace("\n", " ") if row["Description"] else None

        cur.execute("""
            INSERT INTO Video (VideoID, Title, Description, PublishDate, ChannelID, CategoryID)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (VideoID) DO NOTHING;
        """, (
            video_id,
            title,
            description,
            row["PublishDate"] if row["PublishDate"] else None,
            row["ChannelID"] if row["ChannelID"] else None,
            row["CategoryID"] if row["CategoryID"] else None
        ))
conn.commit()

# 4. Load VideoTag
seen_videotags = set()
with open("data/videotags.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pair = (row["VideoID"], row["TagID"])
        if pair in seen_videotags:
            continue
        seen_videotags.add(pair)

        cur.execute("""
            INSERT INTO VideoTag (VideoID, TagID)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (row["VideoID"], row["TagID"]))
conn.commit()

# 5. Load TrendingSnapshot with date conversion YY.DD.MM -> YYYY-MM-DD
seen_trending = set()
with open("data/trending_snapshots.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["VideoID"], row["RegionCode"], row["TrendingDate"])
        if key in seen_trending:
            continue
        seen_trending.add(key)

        # convert 17.14.11 -> 2017-11-14
        yy, dd, mm = row["TrendingDate"].split(".")
        formatted_date = f"20{yy}-{mm}-{dd}"

        cur.execute("""
            INSERT INTO TrendingSnapshot
            (VideoID, RegionCode, TrendingDate, Views, Likes, CommentCount, Dislikes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            row["VideoID"],
            row["RegionCode"],
            formatted_date,
            row["Views"] if row["Views"] else None,
            row["Likes"] if row["Likes"] else None,
            row["CommentCount"] if row["CommentCount"] else None,
            row["Dislikes"] if row["Dislikes"] else None
        ))
conn.commit()

cur.close()
conn.close()

print("All CSV files loaded successfully.")
