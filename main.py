import sqlite3
from scraper import scrape_rss_feed

conn = sqlite3.connect("news.db")
cursor = conn.cursor()


SOURCES = {
    "pinknews": {
        "name": "PinkNews",
        "type": "rss-feed",
        "url": "https://www.thepinknews.com/feed/",
        "language": "en"
    },
    "gaytimes": {
        "name": "Gay Times",
        "type": "rss-feed",
        "url": "https://www.gaytimes.com/feed/",
        "language": "en"
    }
}


cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT UNIQUE,
    source TEXT,
    published TEXT
)
""")

for source in SOURCES.values():
    feed = scrape_rss_feed(source["url"])
    for entry in feed:
        try:
            cursor.execute("INSERT INTO articles (title, link, source, published) VALUES (?, ?, ?, ?)",
                    (entry["title"], entry["link"], source["name"], entry["published"]))
        except sqlite3.IntegrityError:
            # Skip duplicates based on link
            pass

conn.commit()
conn.close()
