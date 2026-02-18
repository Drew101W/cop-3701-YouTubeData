# cop-3701-YouTubeData
# YouTube Trending Content Analytics Database

## Application Domain
This project is in the **data analytics and database systems** domain. It focuses on storing and analyzing YouTube’s daily trending videos to understand engagement and popularity trends over time.

## Project Goals
The goal of this project is to build a **content analytics database** for YouTube trending videos. The database will allow analysis of how videos grow in popularity using engagement metrics such as views, likes, and comments.

Main goals:
- Store daily trending video data across multiple regions
- Track engagement changes over time
- Analyze growth rates using SQL window functions
- Support text search on video titles, tags, and descriptions

## Intended Users
- Data analysts
- Students and researchers
- Content creators interested in trending patterns

## Data Source
This project uses the **YouTube Trending Videos Dataset**, collected using the YouTube API.

Dataset details:
- Daily records of trending videos
- Covers multiple regions (US, GB, DE, CA, FR, and others)
- Up to 200 trending videos per region per day
- Includes video title, channel name, publish date, tags, description, views, likes, dislikes, and comment count
- Category information provided through JSON files

## Project Scope
The project will:
- Design a relational database schema
- Import CSV and JSON data into the database
- Use SQL window functions to calculate growth rates
- Create indexes to support fast queries and text search

Database Design Overview (Part B Update)

This database is designed using an Entity-Relationship model that includes:
Strong entities: Video, Channel, Category, Region, Tag
A weak entity: TrendingSnapshot (dependent on Video and Region)
An associative entity: VideoTag (resolves many-to-many between Video and Tag)
The TrendingSnapshot entity models time-series data and uses a composite primary key (VideoID, RegionCode, TrendingDate).

The design includes:
One-to-many relationships (Channel to Video)
Many-to-many relationships (Video to Tag)
One-to-one relationship (Video to VideoStatisticsSummary)

Unique or Difficult Aspects

The most complex aspect of the design is modeling daily trending records as a weak entity. Each trending record depends on both a Video and a Region, requiring a composite primary key and identifying relationships. Additionally, modeling tags required creating an associative entity to correctly resolve a many-to-many relationship.
