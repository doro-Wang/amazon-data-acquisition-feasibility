import requests
from urllib.parse import quote


appid = "230410"

base_url = f"https://store.steampowered.com/appreviews/{appid}"

params = {
    "json": 1,
    "language": "all",
    "purchase_type": "all",
    "filter": "recent",
    "num_per_page": 20
}


all_review_ids = []
cursor = "*"


for page in range(1, 4):

    params["cursor"] = cursor

    response = requests.get(
        base_url,
        params=params
    )

    print(f"\nPage {page}")
    print("HTTP status:", response.status_code)

    data = response.json()

    reviews = data.get("reviews", [])

    print("Reviews found:", len(reviews))

    review_ids = [
        review.get("recommendationid")
        for review in reviews
    ]

    print("First review ID:", review_ids[0] if review_ids else None)
    print("Last review ID:", review_ids[-1] if review_ids else None)

    all_review_ids.extend(review_ids)

    # Steam returns the cursor for the next batch
    cursor = data.get("cursor")

    print("Next cursor:", cursor)

    if not reviews or not cursor:
        break


print("\n--- Summary ---")
print("Total reviews collected:", len(all_review_ids))
print("Unique review IDs:", len(set(all_review_ids)))
