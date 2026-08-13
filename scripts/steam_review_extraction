import json
import requests


# Steam App ID for Warframe
appid = "230410"


# Build Steam review API URL
url = (
    f"https://store.steampowered.com/appreviews/{appid}"
    "?json=1"
    "&language=all"
    "&purchase_type=all"
    "&filter=recent"
    "&num_per_page=20"
)


# Send request
response = requests.get(url)

print("HTTP status:", response.status_code)


# Parse JSON response
data = response.json()


# Print query summary for debugging
print("Query summary:")
print(data.get("query_summary"))


# Get reviews
reviews = data.get("reviews", [])

print("Reviews found:", len(reviews))


# Store structured review data
review_data = []


for review in reviews:

    author = review.get("author", {})

    review_data.append(
        {
            "review_id": review.get("recommendationid"),
            "steam_id": author.get("steamid"),
            "language": review.get("language"),
            "review_text": review.get("review"),
            "timestamp_created": review.get("timestamp_created"),
            "timestamp_updated": review.get("timestamp_updated"),
            "voted_up": review.get("voted_up"),
            "votes_up": review.get("votes_up"),
            "votes_funny": review.get("votes_funny"),
            "weighted_vote_score": review.get("weighted_vote_score"),
            "comment_count": review.get("comment_count"),
            "steam_purchase": review.get("steam_purchase"),
            "received_for_free": review.get("received_for_free"),
            "refunded": review.get("refunded"),
            "written_during_early_access": review.get(
                "written_during_early_access"
            ),
            "playtime_forever": author.get("playtime_forever"),
            "playtime_last_two_weeks": author.get(
                "playtime_last_two_weeks"
            ),
            "playtime_at_review": author.get("playtime_at_review"),
            "last_played": author.get("last_played")
        }
    )


# Save reviews to JSON
with open(
    "steam_reviews.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        review_data,
        f,
        indent=2,
        ensure_ascii=False
    )


print("Saved reviews:", len(review_data))


# Print a short sample
for review in review_data[:3]:

    print("----------------")
    print("Review ID:", review["review_id"])
    print("Language:", review["language"])
    print("Voted Up:", review["voted_up"])
    print("Votes Up:", review["votes_up"])
    print("Created:", review["timestamp_created"])
    print("Review:", review["review_text"][:300])
