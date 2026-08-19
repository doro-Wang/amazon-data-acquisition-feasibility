import time
import requests
import pandas as pd

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# =========================================================
# 1. Games to collect
# =========================================================

GAMES = {
    "Warframe": 230410,
    "XCOM 2": 268500,
    "Against the Storm": 1336490,
    "V Rising": 1604030,
    "Marvel Rivals": 2767030
}

TARGET_PER_GAME = 2000

BASE_URL = "https://store.steampowered.com/appreviews"


# =========================================================
# 2. Create HTTP session with retry logic
# =========================================================

session = requests.Session()

retry_strategy = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=1,
    status_forcelist=[
        429,
        500,
        502,
        503,
        504
    ],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

session.mount(
    "https://",
    adapter
)


# =========================================================
# 3. Collect reviews for one game
# =========================================================

def collect_game_reviews(
    game_name,
    app_id,
    target=2000
):

    print("\n======================================")
    print("Collecting:", game_name)
    print("App ID:", app_id)
    print("Target:", target)
    print("======================================")

    cursor = "*"
    collected_reviews = []
    seen_ids = set()
    request_number = 0

    while len(collected_reviews) < target:

        request_number += 1

        params = {
            "json": 1,
            "language": "all",
            "purchase_type": "all",
            "review_type": "all",
            "filter": "recent",
            "num_per_page": 100,
            "cursor": cursor
        }

        url = f"{BASE_URL}/{app_id}"

        try:
            response = session.get(
                url,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            break

        except ValueError:
            print("Invalid JSON response.")
            break

        reviews = data.get(
            "reviews",
            []
        )

        if not reviews:
            print("No more reviews returned.")
            break

        new_reviews = 0

        for review in reviews:

            review_id = review.get(
                "recommendationid"
            )

            if review_id in seen_ids:
                continue

            seen_ids.add(
                review_id
            )

            author = review.get(
                "author",
                {}
            )

            record = {
                "game_name": game_name,
                "app_id": app_id,
                "review_id": review_id,

                "steam_id": author.get(
                    "steamid"
                ),

                "num_games_owned": author.get(
                    "num_games_owned"
                ),

                "num_reviews": author.get(
                    "num_reviews"
                ),

                "playtime_forever": author.get(
                    "playtime_forever"
                ),

                "playtime_last_two_weeks": author.get(
                    "playtime_last_two_weeks"
                ),

                "playtime_at_review": author.get(
                    "playtime_at_review"
                ),

                "last_played": author.get(
                    "last_played"
                ),

                "language": review.get(
                    "language"
                ),

                "review": review.get(
                    "review"
                ),

                "timestamp_created": review.get(
                    "timestamp_created"
                ),

                "timestamp_updated": review.get(
                    "timestamp_updated"
                ),

                "voted_up": review.get(
                    "voted_up"
                ),

                "votes_up": review.get(
                    "votes_up"
                ),

                "votes_funny": review.get(
                    "votes_funny"
                ),

                "weighted_vote_score": review.get(
                    "weighted_vote_score"
                ),

                "comment_count": review.get(
                    "comment_count"
                ),

                "steam_purchase": review.get(
                    "steam_purchase"
                ),

                "received_for_free": review.get(
                    "received_for_free"
                ),

                "written_during_early_access": review.get(
                    "written_during_early_access"
                ),

                "primarily_steam_deck": review.get(
                    "primarily_steam_deck"
                )
            }

            collected_reviews.append(
                record
            )

            new_reviews += 1

            if len(collected_reviews) >= target:
                break

        print(
            f"Request {request_number}:",
            f"+{new_reviews} reviews |",
            f"Total = {len(collected_reviews)}"
        )

        next_cursor = data.get(
            "cursor"
        )

        if not next_cursor:
            print("No next cursor returned.")
            break

        if next_cursor == cursor:
            print("Cursor did not change.")
            break

        cursor = next_cursor

        time.sleep(0.5)

    print(
        f"Finished {game_name}:",
        len(collected_reviews),
        "reviews collected"
    )

    return collected_reviews


# =========================================================
# 4. Collect all games
# =========================================================

all_reviews = []

for game_name, app_id in GAMES.items():

    reviews = collect_game_reviews(
        game_name,
        app_id,
        TARGET_PER_GAME
    )

    all_reviews.extend(
        reviews
    )


# =========================================================
# 5. Convert to DataFrame
# =========================================================

df = pd.DataFrame(
    all_reviews
)


print("\n======================================")
print("FINAL DATASET SUMMARY")
print("======================================")

print(
    "Total reviews:",
    len(df)
)

print(
    "\nReviews by game:"
)

print(
    df["game_name"].value_counts()
)

print(
    "\nUnique review IDs:",
    df["review_id"].nunique()
)

print(
    "\nDuplicate review IDs:",
    df["review_id"].duplicated().sum()
)


# =========================================================
# 6. Save dataset
# =========================================================

output_path = "data/steam_reviews.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8"
)

print(
    "\nDataset saved to:",
    output_path
)
