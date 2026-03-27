import pandas as pd
import json
import os

# create output folder
os.makedirs("data", exist_ok=True)

# load dataset
df = pd.read_csv("dataset/USvideos.csv")

# -----------------------
# CHANNELS TABLE
# -----------------------

channels = df[['channel_title']].drop_duplicates().reset_index(drop=True)
channels['ChannelID'] = channels.index + 1
channels['Country'] = 'US'
channels['SubscriberCount'] = 1000000

channels = channels[['ChannelID','channel_title','Country','SubscriberCount']]
channels.columns = ['ChannelID','ChannelName','Country','SubscriberCount']

channels.to_csv("data/channels.csv", index=False)

# mapping channel name -> id
channel_map = dict(zip(channels.ChannelName, channels.ChannelID))


# -----------------------
# VIDEOS TABLE
# -----------------------

videos = df[['video_id','title','description','publish_time','category_id','channel_title']].drop_duplicates()

videos['ChannelID'] = videos['channel_title'].map(channel_map)

videos = videos[['video_id','title','description','publish_time','ChannelID','category_id']]
videos.columns = ['VideoID','Title','Description','PublishDate','ChannelID','CategoryID']

videos.to_csv("data/videos.csv", index=False)


# -----------------------
# TRENDING SNAPSHOTS
# -----------------------

snapshots = df[['video_id','trending_date','views','likes','dislikes','comment_count']]

snapshots['RegionCode'] = 'US'

snapshots = snapshots[['video_id','RegionCode','trending_date','views','likes','comment_count','dislikes']]
snapshots.columns = ['VideoID','RegionCode','TrendingDate','Views','Likes','CommentCount','Dislikes']

snapshots.to_csv("data/trending_snapshots.csv", index=False)


# -----------------------
# REGIONS TABLE
# -----------------------

regions = pd.DataFrame({
    "RegionCode": ["US"],
    "RegionName": ["United States"]
})

regions.to_csv("data/regions.csv", index=False)


# -----------------------
# CATEGORIES TABLE
# -----------------------

with open("dataset/US_category_id.json") as f:
    data = json.load(f)

cats = []

for item in data['items']:
    cats.append({
        "CategoryID": int(item['id']),
        "CategoryName": item['snippet']['title']
    })

categories = pd.DataFrame(cats)

categories.to_csv("data/categories.csv", index=False)


# -----------------------
# TAGS TABLE
# -----------------------

tag_set = set()

for tag_string in df['tags']:
    tags = tag_string.replace('"','').split('|')
    for t in tags:
        if t != '[none]':
            tag_set.add(t.strip())

tags_df = pd.DataFrame(list(tag_set), columns=['TagName'])
tags_df['TagID'] = tags_df.index + 1
tags_df = tags_df[['TagID','TagName']]

tags_df.to_csv("data/tags.csv", index=False)

tag_map = dict(zip(tags_df.TagName, tags_df.TagID))


# -----------------------
# VIDEO TAGS TABLE
# -----------------------

rows = []

for _, row in df.iterrows():
    video = row['video_id']
    tags = row['tags'].replace('"','').split('|')

    for t in tags:
        if t in tag_map:
            rows.append((video, tag_map[t]))

videotags = pd.DataFrame(rows, columns=['VideoID','TagID']).drop_duplicates()

videotags.to_csv("data/videotags.csv", index=False)


print("All CSV files generated successfully!")



# Path to your data (either ZIP or extracted CSV)
data_path = "dataset/USvideos.zip"

# Check if the file is a ZIP
if data_path.endswith(".zip"):
    with zipfile.ZipFile(data_path) as z:
        # List all files inside the ZIP
        files = z.namelist()
        # Find the first CSV file
        csv_file = next((f for f in files if f.endswith(".csv")), None)
        if csv_file is None:
            raise FileNotFoundError("No CSV file found inside the ZIP.")
        # Read CSV directly from ZIP
        with z.open(csv_file) as f:
            df = pd.read_csv(f)
else:
    # If it's already a CSV
    df = pd.read_csv(data_path)

print(df.head())