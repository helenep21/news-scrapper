import feedparser


def scrape_rss_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:   
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
        })
    return articles
    