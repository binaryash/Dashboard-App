import feedparser

def get_feeds():
    rss_url = "http://url-of-your-rss-feeds"
    feed = feedparser.parse(rss_url)
    entries = feed.entries
    return entries
