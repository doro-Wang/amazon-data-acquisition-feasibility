import requests


STORY_ID = 49270953
BASE_URL = "https://hacker-news.firebaseio.com/v0/item"


def fetch_top_level_comments(limit=20):

    story_url = f"{BASE_URL}/{STORY_ID}.json"

    story_response = requests.get(
        story_url,
        timeout=10
    )

    story = story_response.json()

    comment_ids = story.get("kids", [])[:limit]

    comments = []

    for comment_id in comment_ids:

        comment_url = f"{BASE_URL}/{comment_id}.json"

        response = requests.get(
            comment_url,
            timeout=10
        )

        if response.status_code != 200:
            continue

        comment = response.json()

        if not comment:
            continue

        comments.append(
            {
                "comment_id": comment.get("id"),
                "author": comment.get("by"),
                "text": comment.get("text"),
                "timestamp": comment.get("time"),
                "parent_id": comment.get("parent")
            }
        )

    return comments


# Run 1
print("=== Run 1 ===")

run1 = fetch_top_level_comments()

print("Comments found:", len(run1))


# Run 2
print("\n=== Run 2 ===")

run2 = fetch_top_level_comments()

print("Comments found:", len(run2))


# Compare IDs
ids_run1 = [
    comment["comment_id"]
    for comment in run1
]

ids_run2 = [
    comment["comment_id"]
    for comment in run2
]


print("\n=== Repeatability Result ===")

print(
    "Comment count consistent:",
    len(run1) == len(run2)
)

print(
    "Comment IDs consistent:",
    ids_run1 == ids_run2
)

print(
    "Full comment records consistent:",
    run1 == run2
)

print(
    "Run 1 unique IDs:",
    len(set(ids_run1))
)

print(
    "Run 2 unique IDs:",
    len(set(ids_run2))
)


# Data quality check
print("\n=== Data Quality Check ===")

fields = [
    "comment_id",
    "author",
    "text",
    "timestamp",
    "parent_id"
]

for field in fields:

    missing = sum(
        1
        for comment in run1
        if comment.get(field) in [None, ""]
    )

    print(
        f"{field} missing:",
        missing,
        "/",
        len(run1)
    )
