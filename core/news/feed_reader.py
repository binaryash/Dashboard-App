import feedparser
import json
import os


def get_feeds(page=1, per_page=9, source=None, feed_type=None, category=None):
    """
    Get feeds with optional filtering by source, type, and category

    Args:
        page: Current page number
        per_page: Number of entries per page
        source: Filter by source (e.g., "The Hindu", "Times of India")
        feed_type: Filter by type (e.g., "National", "International", "Business", "Sports")
        category: Filter by category (e.g., "Politics", "Economy", "World News")
    """
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

        # Apply filters at feed level
        if source and feed_info["source"] != source:
            continue
        if feed_type and feed_info["type"] != feed_type:
            continue
        if category and category not in feed_info.get("categories", []):
            continue

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

            # Set placeholder if no image found
            entry["image_url"] = image_url if image_url else "https://placehold.co/600x300"
            all_entries.append(entry)

    # Calculate pagination
    total_entries = len(all_entries)
    total_pages = (total_entries + per_page - 1) // per_page  # Ceiling division

    # Get the current page's entries
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_entries = all_entries[start_idx:end_idx]

    return {
        "entries": paginated_entries,
        "page": page,
        "per_page": per_page,
        "total_entries": total_entries,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages
    }


def get_filter_options():
    """
    Get all available filter options from feeds.json
    Returns dict with sources, types, and categories
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "feeds.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    sources = set()
    types = set()
    categories = set()

    for feed_info in data["feeds"]:
        sources.add(feed_info["source"])
        types.add(feed_info["type"])
        categories.update(feed_info.get("categories", []))

    return {
        "sources": sorted(list(sources)),
        "types": sorted(list(types)),
        "categories": sorted(list(categories))
    }
