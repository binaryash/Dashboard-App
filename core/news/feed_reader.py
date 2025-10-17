import feedparser
import json
import os


def get_feeds():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to feeds.json in the same folder
    json_path = os.path.join(script_dir, "feeds.json")

    # Read the JSON file
    with open(json_path, "r") as f:
        data = json.load(f)

    all_entries = []

    # Loop through each feed
    for feed_info in data["feeds"]:
        # Validate that source and type are present
        if not feed_info.get("source") or not feed_info.get("type"):
            raise ValueError(f"Feed must have both 'source' and 'type' fields")

        # Parse the RSS feed
        feed = feedparser.parse(feed_info["url"])

        # Add metadata to each entry
        for entry in feed.entries:
            entry["feed_name"] = feed_info["name"]
            entry["source"] = feed_info["source"]
            entry["type"] = feed_info["type"]
            entry["categories"] = feed_info.get("categories", [])

            # Extract image URL from various possible locations
            image_url = None

            # Check for media:content (Times of India uses this)
            if hasattr(entry, "media_content"):
                image_url = entry.media_content[0]["url"]

            # Check for enclosures (Times of India also uses this)
            elif hasattr(entry, "enclosures") and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get("type", "").startswith("image"):
                        image_url = enclosure.get("url")
                        break

            # Check for media:thumbnail
            elif hasattr(entry, "media_thumbnail"):
                image_url = entry.media_thumbnail[0]["url"]

            # Check in description for img tags (The Hindu sometimes has this)
            elif hasattr(entry, "description"):
                import re

                img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.description)
                if img_match:
                    image_url = img_match.group(1)

            entry["image_url"] = image_url
            all_entries.append(entry)

    return all_entries
