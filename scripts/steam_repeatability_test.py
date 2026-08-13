import requests


appid = "230410"

base_url = f"https://store.steampowered.com/appreviews/{appid}"

params = {
    "json": 1,
    "language": "all",
    "purchase_type": "all",
    "filter": "recent",
    "num_per_page": 20,
    "cursor": "*"
}


def fetch_reviews():
    response = requests.get(
        base_url,
        params=params
    )

    print("HTTP status:", response.status_code)

    data = response.json()

    reviews = data.get("reviews", [])

    review_ids = [
        review.get("recommendationid")
        for review in reviews
    ]

    return reviews, review_ids


# Run 1
print("=== Run 1 ===")

reviews_run1, ids_run1 = fetch_reviews()

print("Reviews found:", len(reviews_run1))


# Run 2
print("\n=== Run 2 ===")

reviews_run2, ids_run2 = fetch_reviews()

print("Reviews found:", len(reviews_run2))


# Compare results
print("\n=== Repeatability Result ===")

print(
    "Review count consistent:",
    len(reviews_run1) == len(reviews_run2)
)

print(
    "Review IDs consistent:",
    ids_run1 == ids_run2
)

print(
    "Run 1 unique IDs:",
    len(set(ids_run1))
)

print(
    "Run 2 unique IDs:",
    len(set(ids_run2))
)
fields = [
    "recommendationid",
    "language",
    "review",
    "timestamp_created",
    "voted_up",
    "votes_up"
]

for field in fields:
    missing = sum(
        1 for review in reviews_run1
        if review.get(field) in [None, ""]
    )

    print(
        field,
        "missing:",
        missing,
        "/",
        len(reviews_run1)
    )
