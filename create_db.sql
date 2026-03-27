CREATE TABLE Channel (
    ChannelID VARCHAR(50) PRIMARY KEY,
    ChannelName VARCHAR(255) NOT NULL,
    Country VARCHAR(100),
    SubscriberCount INT
);

CREATE TABLE Category (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
);

CREATE TABLE Region (
    RegionCode VARCHAR(5) PRIMARY KEY,
    RegionName VARCHAR(100) NOT NULL
);

CREATE TABLE Tag (
    TagID INT PRIMARY KEY,
    TagName VARCHAR(100) NOT NULL
);

CREATE TABLE Video (
    VideoID VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(500) NOT NULL,
    Description TEXT,
    PublishDate DATE,
    ChannelID VARCHAR(50),
    CategoryID INT,
    FOREIGN KEY (ChannelID) REFERENCES Channel(ChannelID),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
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
    Views INT,
    Likes INT,
    CommentCount INT,
    Dislikes INT,
    PRIMARY KEY (VideoID, RegionCode, TrendingDate),
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID),
    FOREIGN KEY (RegionCode) REFERENCES Region(RegionCode)
);

CREATE TABLE VideoStatisticsSummary (
    VideoID VARCHAR(50) PRIMARY KEY,
    TotalTrendingDays INT,
    MaxViews INT,
    AvgLikes FLOAT,
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID)
);
