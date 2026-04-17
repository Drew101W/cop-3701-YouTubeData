# DB Project - Part E

- DB: Drew Whiting
- GUI: Elijah Zimmerman

## Requirement 1

### Description

Based on a number of criteria provided by the user, select all videos matching that criteria. 

### Query

``` mariadb
SELECT Title, ChannelName FROM Video v JOIN Channel c ON c.ChannelID=v.ChannelID WHERE ...;
```

Where clause varies based on provided search items.

### Image

![260417_10h33m12s_screenshot](/home/eli/Pictures/Screenshots/260417_10h33m12s_screenshot.png)

## Requirement 2

### Description

Given a channel name, select all videos posted by that channel.

### Query

``` mariadb
SELECT Title FROM Video v JOIN Channel c ON c.ChannelID=v.ChannelID WHERE ChannelName LIKE '%<provided name>%';
```

Allows for partial or full match.

### Image

![260417_10h34m47s_screenshot](/home/eli/Pictures/Screenshots/260417_10h34m47s_screenshot.png)

## Requirement 3

### Description

Select what percentage of each category makes us the trending page.

### Query

``` mariadb
WITH LatestTrending AS (
    SELECT * FROM TrendingSnapshot 
    WHERE TrendingDate = (SELECT MAX(TrendingDate) FROM TrendingSnapshot)
)
SELECT 
    c.CategoryName,
    COUNT(lt.VideoID) AS VideoCount,
    ROUND(COUNT(lt.VideoID) * 100.0 / SUM(COUNT(lt.VideoID)) OVER(), 2) AS Percentage
FROM LatestTrending lt
JOIN Video v ON lt.VideoID = v.VideoID
JOIN Category c ON v.CategoryID = c.CategoryID
GROUP BY c.CategoryName
ORDER BY Percentage DESC;
```

### Image

![260417_10h35m18s_screenshot](/home/eli/Pictures/Screenshots/260417_10h35m18s_screenshot.png)

## Requirement 4

### Description

Select a given channel's statistics from all posted videos.

### Query

``` mariadb
SELECT 
    c.ChannelName,
    c.Country,
    c.SubscriberCount,
    COUNT(DISTINCT v.VideoID) AS TotalUniqueTrendingVideos,
    SUM(ts.Views) AS TotalCumulativeViews,
    SUM(ts.Likes) AS TotalCumulativeLikes,
    SUM(ts.CommentCount) AS TotalCumulativeComments,
    ROUND(AVG(ts.Views), 0) AS AvgViewsPerTrendingSnapshot,
    ROUND(SUM(ts.Likes) / NULLIF(SUM(ts.Views), 0) * 100, 2) AS LikeToViewRatio
FROM Channel c
LEFT JOIN Video v ON c.ChannelID = v.ChannelID
LEFT JOIN TrendingSnapshot ts ON v.VideoID = ts.VideoID
WHERE c.ChannelName = '<channel name>'
GROUP BY c.ChannelID;
```

### Image

![260417_10h39m19s_screenshot](/home/eli/Pictures/Screenshots/260417_10h39m19s_screenshot.png)

## Requirement 5

### Description

Select a given tag's statistics from all posted videos.

### Query

``` mariadb
SELECT 
    t.TagName,
    COUNT(DISTINCT vt.VideoID) AS TotalVideosWithTag,
    SUM(ts.Views) AS TotalCumulativeViews,
    SUM(ts.Likes) AS TotalCumulativeLikes,
    SUM(ts.CommentCount) AS TotalCumulativeComments,
    ROUND(AVG(ts.Views), 0) AS AvgViewsPerSnapshot,
    ROUND(SUM(ts.Likes) / NULLIF(SUM(ts.Views), 0) * 100, 2) AS EngagementRate
FROM Tag t
JOIN VideoTag vt ON t.TagID = vt.TagID
JOIN Video v ON vt.VideoID = v.VideoID
JOIN TrendingSnapshot ts ON v.VideoID = ts.VideoID
WHERE t.TagName = '<tag name>'
GROUP BY t.TagID, t.TagName;
```

### Image

![260417_10h36m04s_screenshot](/home/eli/Pictures/Screenshots/260417_10h36m04s_screenshot.png)
