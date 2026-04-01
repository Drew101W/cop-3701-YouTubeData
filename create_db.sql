DROP TABLE IF EXISTS VideoTag;
DROP TABLE IF EXISTS TrendingSnapshot;
DROP TABLE IF EXISTS Video;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Channel;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Region;

CREATE TABLE Channel (
    ChannelID INT PRIMARY KEY,
    ChannelName VARCHAR(255),
    Country VARCHAR(50),
    SubscriberCount INT
);

CREATE TABLE Category (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(255)
);

CREATE TABLE Region (
    RegionCode VARCHAR(5) PRIMARY KEY,
    RegionName VARCHAR(100)
);

CREATE TABLE Video (
    VideoID VARCHAR(50) PRIMARY KEY,
    Title TEXT,
    Description TEXT,
    PublishDate TIMESTAMP,
    ChannelID INT,
    CategoryID INT,
    FOREIGN KEY (ChannelID) REFERENCES Channel(ChannelID),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);

CREATE TABLE Tag (
    TagID INT PRIMARY KEY,
    TagName VARCHAR(255)
);

CREATE TABLE VideoTag (
    VideoID VARCHAR(50),
    TagID INT,
    PRIMARY KEY (VideoID, TagID),
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID),
    FOREIGN KEY (TagID) REFERENCES Tag(TagID)
);

CREATE TABLE TrendingSnapshot (
    VideoID VARCHAR(50),
    RegionCode VARCHAR(5),
    TrendingDate DATE,
    Views BIGINT,
    Likes BIGINT,
    CommentCount BIGINT,
    Dislikes BIGINT,
    PRIMARY KEY (VideoID, RegionCode, TrendingDate),
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID),
    FOREIGN KEY (RegionCode) REFERENCES Region(RegionCode)
);