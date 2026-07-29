# amazon-data-acquisition-feasibility
Evaluating Amazon as a recurring source for structured product and review data acquisition.
## Objective
The goal is to determine:
- what information can be collected from Amazon product pages
- whether the data is accessible consistently
- whether customer reviews can be collected at meaningful scale
- whether Amazon is suitable for a recurring ingestion pipeline


## Tested Categories

The feasibility study covers multiple Amazon product categories:

- Beauty & Health
- Electronics
- Books
- Clothing, Shoes, Jewelry & Watches
- Home, Garden & Tools


## Evaluation Criteria

Each product page was evaluated based on:

### Product Data
- Product Name
- Category
- ASIN
- URL
- page access
- Product title
- Brand (or Author for books)
- Price
- Rating
- Rating count
- Product images
- Product description


### Customer Review Data
- Reviewer name
- Review date
- Review text
- Helpful votes
- Purchased variant
- Verified purchase

### Accessibility
- Product page accessibility
- Top reviews accessibility
- Full review accessibility



## Key Findings

### Product Data

Amazon product pages generally expose structured product data, including product information, pricing, ratings, and descriptions.

### Customer Reviews

A limited number of customer reviews may be visible directly on product pages. However, full review access requires login, which creates limitations for recurring automated collection.

### Accessibility

During manual testing, product pages were consistently accessible. No CAPTCHA, missing content, or unstable page behavior were observed.


## Conclusion

Amazon appears suitable for collecting product metadata.

However, using Amazon as a recurring customer review data source requires further investigation due to login requirements limitations.

