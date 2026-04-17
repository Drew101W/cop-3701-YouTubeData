import mariadb
import sys
from tabulate import tabulate

def connect_db():
    try:
        conn = mariadb.connect(
            user="your_username",
            password="your_password",
            host="127.0.0.1",
            port=3306,
            database="your_database_name"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def run_query(query, params=None):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        results = cur.fetchall()
        headers = [i[0] for i in cur.description]
        print("\n" + tabulate(results, headers=headers, tablefmt="psql"))
    except mariadb.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def menu():
    while True:
        print("\n--- Video Database CLI ---")
        print("1. Search Videos (Multi-Criteria)")
        print("2. Search Videos by Channel (Partial Match)")
        print("3. View Trending Category Percentages")
        print("4. View Channel Statistics")
        print("5. View Tag Statistics")
        print("6. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1':
            title = input("Enter partial title (leave blank for any): ")
            channel = input("Enter channel name (leave blank for any): ")
            
            query = "SELECT Title, ChannelName FROM Video v JOIN Channel c ON c.ChannelID=v.ChannelID WHERE 1=1"
            params = []
            if title:
                query += " AND v.Title LIKE ?"
                params.append(f"%{title}%")
            if channel:
                query += " AND c.ChannelName LIKE ?"
                params.append(f"%{channel}%")
            run_query(query, tuple(params))

        elif choice == '2':
            name = input("Enter channel name: ")
            query = "SELECT Title FROM Video v JOIN Channel c ON c.ChannelID=v.ChannelID WHERE ChannelName LIKE ?"
            run_query(query, (f"%{name}%",))

        elif choice == '3':
            query = """
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
            """
            run_query(query)

        elif choice == '4':
            name = input("Enter exact channel name: ")
            query = """
            SELECT 
                c.ChannelName, c.Country, c.SubscriberCount,
                COUNT(DISTINCT v.VideoID) AS TotalUniqueTrendingVideos,
                SUM(ts.Views) AS TotalCumulativeViews,
                SUM(ts.Likes) AS TotalCumulativeLikes,
                SUM(ts.CommentCount) AS TotalCumulativeComments,
                ROUND(AVG(ts.Views), 0) AS AvgViewsPerTrendingSnapshot,
                ROUND(SUM(ts.Likes) / NULLIF(SUM(ts.Views), 0) * 100, 2) AS LikeToViewRatio
            FROM Channel c
            LEFT JOIN Video v ON c.ChannelID = v.ChannelID
            LEFT JOIN TrendingSnapshot ts ON v.VideoID = ts.VideoID
            WHERE c.ChannelName = ?
            GROUP BY c.ChannelID;
            """
            run_query(query, (name,))

        elif choice == '5':
            tag = input("Enter exact tag name: ")
            query = """
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
            WHERE t.TagName = ?
            GROUP BY t.TagID, t.TagName;
            """
            run_query(query, (tag,))

        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    menu()
