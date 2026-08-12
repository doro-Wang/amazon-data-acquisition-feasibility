import json
from bs4 import BeautifulSoup


# Load saved Amazon HTML from the second extraction run
with open(
    "amazon_review_response_2.html",
    encoding="utf-8"
) as f:
    html = f.read()


soup = BeautifulSoup(
    html,
    "html.parser"
)


# Find reviews
reviews = soup.find_all(
    "li",
    {"data-hook": "review"}
)

print("Reviews found in repeatability run:", len(reviews))


review_data = []


# Extract fields
for review in reviews:

    # Review ID
    review_id = review.get("id")

    # Reviewer name
    reviewer = review.find(
        "span",
        {"class": "a-profile-name"}
    )

    reviewer = (
        reviewer.get_text(strip=True)
        if reviewer
        else None
    )

    # Rating
    rating = review.find(
        "i",
        {"data-hook": "review-star-rating"}
    )

    rating = (
        rating.get_text(" ", strip=True)
        if rating
        else None
    )

    # Date
    date = review.find(
        "span",
        {"data-hook": "review-date"}
    )

    date = (
        date.get_text(" ", strip=True)
        if date
        else None
    )

    # Review title
    title = review.find(
        "a",
        {"data-hook": "review-title"}
    )

    if title:
        title_text = title.get_text(
            " ",
            strip=True
        )

        if "out of 5 stars" in title_text:
            title_text = title_text.split(
                "stars"
            )[-1].strip()

        title = title_text

    else:
        title = None

    # Review body
    body = review.find(
        "span",
        {"data-hook": "review-body"}
    )

    body = (
        body.get_text(" ", strip=True)
        if body
        else None
    )

    # Verified purchase
    verified = review.find(
        "span",
        {"data-hook": "avp-badge"}
    )

    verified_purchase = bool(verified)

    review_data.append(
        {
            "review_id": review_id,
            "reviewer": reviewer,
            "rating": rating,
            "date": date,
            "title": title,
            "body": body,
            "verified_purchase": verified_purchase
        }
    )


# Save second-run output
with open(
    "reviews_repeatability.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        review_data,
        f,
        indent=2,
        ensure_ascii=False
    )


# Print repeatability run output
for review in review_data:

    print("----------------")
    print("ID:", review["review_id"])
    print("Reviewer:", review["reviewer"])
    print("Rating:", review["rating"])
    print("Date:", review["date"])
    print("Title:", review["title"])
    print("Body:", review["body"])
    print(
        "Verified Purchase:",
        review["verified_purchase"]
    )
