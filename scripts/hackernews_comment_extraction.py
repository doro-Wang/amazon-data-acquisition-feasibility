import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


STORY_ID = 49270953
BASE_URL = "https://hacker-news.firebaseio.com/v0/item"


# Create a session with retry logic
session = requests.Session()

retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)


# Fetch story
story_url = f"{BASE_URL}/{STORY_ID}.json"

story_response = session.get(
    story_url,
    timeout=10
)

print("Story HTTP status:", story_response.status_code)

story = story_response.json()

top_level_comment_ids = story.get("kids", [])

print(
    "Top-level comment IDs found:",
    len(top_level_comment_ids)
)


comments = []
failed_ids = []


# Fetch first 20 top-level comments
for comment_id in top_level_comment_ids[:20]:

    comment_url = f"{BASE_URL}/{comment_id}.json"

    try:
        response = session.get(
            comment_url,
            timeout=10
        )

        if response.status_code != 200:
            print(
                f"Failed comment {comment_id}:",
                response.status_code
            )
            failed_ids.append(comment_id)
            continue

        comment = response.json()

        if not comment:
            failed_ids.append(comment_id)
            continue

        comments.append(
            {
                "comment_id": comment.get("id"),
                "author": comment.get("by"),
                "text": comment.get("text"),
                "timestamp": comment.get("time"),
                "parent_id": comment.get("parent"),
                "child_comment_ids": comment.get("kids", [])
            }
        )

        print(
            f"Collected {len(comments)}:",
            comment_id
        )

        # Small delay between requests
        time.sleep(0.2)

    except requests.exceptions.RequestException as e:

        print(
            f"Request failed for {comment_id}:",
            e
        )

        failed_ids.append(comment_id)


print("\n--- Summary ---")

print(
    "Comments collected:",
    len(comments)
)

print(
    "Failed comment requests:",
    len(failed_ids)
)

print(
    "Failed IDs:",
    failed_ids
)


# Save JSON
with open(
    "hackernews_comments.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        comments,
        f,
        indent=2,
        ensure_ascii=False
    )


# Print first 3 samples
for comment in comments[:3]:

    print("----------------")
    print(
        "Comment ID:",
        comment["comment_id"]
    )
    print(
        "Author:",
        comment["author"]
    )
    print(
        "Timestamp:",
        comment["timestamp"]
    )
    print(
        "Parent ID:",
        comment["parent_id"]
    )
    print(
        "Child replies:",
        len(comment["child_comment_ids"])
    )
    print(
        "Text:",
        comment["text"]
    )
