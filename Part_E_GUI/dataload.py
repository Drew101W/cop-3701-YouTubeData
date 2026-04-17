import csv
import mariadb
import sys

def connect_db():
    try:
        conn = mariadb.connect(
            user="root",
            password="e",
            unix_socket="/run/mysqld/mysqld.sock",
            database="YouTube"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

conn = connect_db()
cur = conn.cursor()

# 1. Wipe everything
# MariaDB requires disabling foreign key checks to truncate tables with relationships
cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
tables = ["Channel", "Category", "Region", "Video", "Tag", "VideoTag", "TrendingSnapshot"]
for table in tables:
    cur.execute(f"TRUNCATE TABLE {table};")
cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
conn.commit()

# 2. Load simple tables
def load_simple_csv(table_name, file_path, columns):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = [row[col] if row[col] != '' else None for col in columns]
            # Use ? for placeholders in MariaDB
            placeholders = ", ".join(["?"] * len(columns))
            col_string = ", ".join(columns)
            # Use INSERT IGNORE for "ON CONFLICT DO NOTHING" behavior
            cur.execute(
                f"INSERT IGNORE INTO {table_name} ({col_string}) VALUES ({placeholders});",
                tuple(values)
            )
    conn.commit()

print("Loading reference tables...")
load_simple_csv("Channel", "data/channels.csv", ["ChannelID", "ChannelName", "Country", "SubscriberCount"])
load_simple_csv("Category", "data/categories.csv", ["CategoryID", "CategoryName"])
load_simple_csv("Region", "data/regions.csv", ["RegionCode", "RegionName"])
load_simple_csv("Tag", "data/tags.csv", ["TagID", "TagName"])

# 3. Load Videos
print("Loading Videos...")
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
            INSERT IGNORE INTO Video (VideoID, Title, Description, PublishDate, ChannelID, CategoryID)
            VALUES (?, ?, ?, ?, ?, ?);
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
print("Loading VideoTags...")
seen_videotags = set()
with open("data/videotags.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pair = (row["VideoID"], row["TagID"])
        if pair in seen_videotags:
            continue
        seen_videotags.add(pair)

        cur.execute("""
            INSERT IGNORE INTO VideoTag (VideoID, TagID)
            VALUES (?, ?);
        """, (row["VideoID"], row["TagID"]))
conn.commit()

# 5. Load TrendingSnapshot
print("Loading Trending Snapshots...")
seen_trending = set()
with open("data/trending_snapshots.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["VideoID"], row["RegionCode"], row["TrendingDate"])
        if key in seen_trending:
            continue
        seen_trending.add(key)

        # convert 17.14.11 -> 2017-11-14
        try:
            yy, dd, mm = row["TrendingDate"].split(".")
            formatted_date = f"20{yy}-{mm}-{dd}"
        except ValueError:
            formatted_date = None

        cur.execute("""
            INSERT IGNORE INTO TrendingSnapshot
            (VideoID, RegionCode, TrendingDate, Views, Likes, CommentCount, Dislikes)
            VALUES (?, ?, ?, ?, ?, ?, ?);
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

print("All CSV files loaded successfully into MariaDB.")
