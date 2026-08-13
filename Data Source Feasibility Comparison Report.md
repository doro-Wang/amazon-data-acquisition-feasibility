# Data Source Feasibility Comparison Report

## 1. Objective

The objective of this assessment is to identify a suitable public data source for building the first recurring user-generated text ingestion prototype.

Candidate sources are evaluated based on their ability to provide sufficient user-generated content, support repeatable automated collection, and minimize operational complexity.

Three candidate sources were tested:

- Amazon
- Steam
- Hacker News

The assessment focuses on small controlled tests rather than large-scale data collection. The goal is to compare the practical feasibility of each source under the same evaluation framework and recommend the most suitable source for the initial recurring ingestion pipeline.

## 2. Evaluation Framework

The following dimensions are used consistently across all candidate sources.

| Dimension | Evaluation Criteria |
|---|---|
| Data Availability | Availability of user-generated text and relevant data |
| Accessibility | Ability to access data without login, gated APIs, or manual intervention |
| Repeatability | Consistency of results across repeated collection attempts |
| Scalability | Ability to expand collection across additional records, pages, or threads |
| Data Quality | Completeness and stability of collected fields |
| Maintenance Complexity | Engineering effort required to maintain recurring collection |

Each dimension is scored from 1 to 5, where a higher score indicates stronger feasibility for recurring automated ingestion.

## 3. Amazon Evaluation

### 3.1 Initial Cross-Category Validation

A preliminary cross-category validation was conducted to assess whether Amazon consistently provides product metadata and customer review content across different product categories.

Five representative product categories were reviewed:

| Category | Example Product | Product Data | Review Data | Main Limitation |
|---|---|---|---|---|
| Beauty & Health | Estée Lauder Foundation 36-Hour Long-Wear | Available | Partial | Full review access requires login |
| Electronics | Apple AirPods Pro (2nd Generation) | Available | Partial | Full review access requires login |
| Books | The Old Man and the Sea | Available | Partial | Full review access requires login |
| Clothing, Shoes, Jewelry & Watches | Crocs Unisex | Available | Partial | Full review access requires login |
| Home, Garden & Tools | Ninja Professional Plus Blender | Available | Partial | Full review access requires login |

Across all five categories, Amazon consistently provided product metadata such as product title, price, rating, rating count, images, and product descriptions. Customer review content was also available, including reviewer information, review dates, review text, and other review-related metadata.

However, full customer review access consistently required authentication. This indicated that while Amazon provides rich user-generated content across categories, access restrictions may limit its suitability for a fully automated recurring ingestion pipeline.

Based on this initial validation, the Beauty & Health product was selected for a deeper technical feasibility test.

#### Deep-Dive Test Product

| Field | Value |
|---|---|
| Product | Estée Lauder Foundation 36-Hour Long-Wear |
| Category | Beauty & Health |
| ASIN | B0FWCZJCSY |

The selected product provided both product metadata and customer review information suitable for further acquisition testing.

### Product Data Availability

| Field               | Available |
| ------------------- | --------- |
| Product title       | Yes       |
| Brand               | Yes       |
| Price               | Yes       |
| Rating              | Yes       |
| Rating count        | Yes       |
| Product images      | Yes       |
| Product description | Yes       |

### Customer Review Data Availability

#### Top Reviews:

| Field             | Available |
| ----------------- | --------- |
| Reviewer name     | Yes       |
| Review date       | Yes       |
| Review text       | Yes       |
| Helpful votes     | Yes       |
| Purchased variant | Yes       |
| Verified purchase | Yes       |

#### Full Review Access

| Field              | Result                       |
| ------------------ | ---------------------------- |
| Full review access | Login required               |


### 3.2 Automated Review Acquisition Test

The Beauty & Health example, Estée Lauder Foundation 36-Hour Long-Wear (ASIN: B0FWCZJCSY), was selected for deeper technical feasibility testing.

#### Method

A baseline automated acquisition test was conducted using Python `requests` to evaluate whether Amazon review data could be directly extracted from the returned HTML response.

#### Result

| Metric | Result |
|---|---|
| HTTP status | 200 |
| Product page accessible | Yes |
| Review data in HTML response | No |
| Review objects extracted | 0 |

#### Observation

The Amazon review page was accessible through an HTTP request, but customer review content was not included in the initial HTML response.


### 3.3 Anonymous Access Restriction Test

#### Method

The review page was accessed through a standard browser session to evaluate whether review content could be accessed without additional authentication.

#### Result

| Metric | Result |
|---|---|
| Review page accessible | Redirected to sign-in |
| Login required | Yes |
| Manual intervention required | Yes |

#### Observation

Accessing full review content through a browser session triggered an Amazon sign-in requirement, indicating that authentication may be a limitation for recurring automated collection.

### 3.4 Authenticated Review Extraction Test

### Objective

This test evaluates whether customer reviews can be extracted after authentication and whether structured review fields are available for downstream analysis.

### Method

An authenticated Amazon browser session was used to access the customer review page.

The returned HTML response was collected and parsed using Python `BeautifulSoup`.

Review objects were identified using Amazon's review HTML structure:

data-hook="review"

### Result

| Metric | Result |
|---|---|
| Authentication required | Yes |
| Review page accessibility | Successful |
| Review objects extracted | 8 |
| Extraction method | HTML parsing |
| Structured review fields available | Yes |

### Accessible Review Fields

| Field | Available | Notes |
|---|---|---|
| Review ID | Yes | Unique review identifier available in HTML attributes |
| Reviewer name | Yes | Extracted from review profile information |
| Rating | Yes | Star rating available |
| Review date | Yes | Review date available |
| Review title | Yes | Review title available |
| Review text | Yes | Full review content available |
| Verified purchase | Yes | Verification badge available when displayed |

### Sample Extraction Output

{
  "review_id": "R2HYGL19WKA0G1",
  "reviewer": "Susie Smith",
  "rating": "5.0 out of 5 stars",
  "date": "Reviewed in the United States on May 7, 2026",
  "title": "Quality",
  "body": "Really lasts well on your face",
  "verified_purchase": true
}

### Observation

Authenticated access enables structured extraction of customer review data. However, authentication requirements introduce additional complexity for automated recurring collection.

### 3.5 Review Pagination Test

### Objective

This test evaluates whether Amazon review data can be collected across multiple pages without additional manual intervention.

### Method

After extracting reviews from the initial accessible review set, additional review pages were tested through the Amazon review interface.

The test evaluated whether:

- additional pages could be accessed directly
- review extraction could continue automatically
- additional user actions were required

### Result

| Metric | Result |
|---|---|
| Page 1 review extraction | Successful |
| Page 2 direct access | Not available in testing environment |
| Additional request required | Yes |
| Manual intervention required | Yes |

### Observation

Additional review pages were not directly accessible through a standard pagination workflow in the tested environment.

Instead, requesting more reviews triggered an additional request process, requiring manual intervention. This limits the ability to continuously collect reviews through an automated pipeline.

### 3.6 Repeatability Test

### Objective

This test evaluates whether the review extraction process produces consistent results across repeated collection attempts.

### Method

The same review extraction workflow was repeated using the same product and the same parsing logic.

The extracted review count, review IDs, and review fields were compared between two extraction runs to evaluate consistency.

### Result

| Metric | Run 1 | Run 2 |
|---|---|---|
| Reviews extracted | 8 | 8 |
| Review IDs consistency | Yes | Yes |
| Review fields consistency | Yes | Yes |

### Observation

The extraction process produced consistent results across repeated runs under the same authenticated access conditions.

The number of extracted reviews and review identifiers remained unchanged between the two runs, indicating that the review extraction method is reproducible.

However, repeatability was validated only for the initially accessible review set. Expanding this process to larger-scale collection may still be affected by Amazon's additional review access restrictions.

### 3.7 Source Evaluation Scorecard

## Evaluation Criteria

The following scorecard was created to evaluate potential data sources consistently.

| Dimension | Evaluation Criteria |
|---|---|
| Data Availability | Availability of product metadata and required review fields |
| Accessibility | Ease of accessing product and review data |
| Repeatability | Consistency across multiple collection attempts |
| Scalability | Ability to collect reviews across pages and products |
| Data Quality | Completeness and stability of collected fields |
| Maintenance Complexity | Login requirements, manual intervention, and access restrictions |

## Amazon Source Evaluation

| Dimension | Score | Evaluation |
|---|---|---|
| Data Availability | 5/5 | Product metadata and structured review fields are available. Extracted review data includes review ID, reviewer name, rating, date, title, text, and verified purchase information. |
| Accessibility | 3/5 | Product pages are accessible, but review access requires authentication. Anonymous access does not expose review data. |
| Repeatability | 4/5 | Repeated extraction attempts under the same authenticated conditions produced consistent review counts and review IDs. |
| Scalability | 2/5 | Initial review extraction is possible, but additional review access requires a request process, limiting multi-page collection. |
| Data Quality | 4/5 | Review data contains rich user-generated content and structured attributes, although some fields may vary depending on review availability. |
| Maintenance Complexity | 2/5 | Authentication requirements, manual review access requests, and access restrictions increase pipeline maintenance effort. |

## Overall Assessment

| Source | Overall Score |
|---|---|
| Amazon | 20/30 |

## Conclusion

Amazon provides high-quality product and review data suitable for downstream analysis. The main challenges are not data availability or extraction quality, but rather access restrictions and scalability.

While authenticated extraction is feasible, building a fully automated recurring review data pipeline would require additional handling for authentication, access management, and review volume limitations.

## 4. Steam Evaluation

### 4.1 Review Data Accessibility Test

#### Objective

This test evaluated whether Steam user review data could be accessed directly without login, authentication, or an API key.

#### Method

A public Steam review endpoint was tested using the Warframe application.

| Field | Value |
|---|---|
| Product | Warframe |
| App ID | 230410 |
| Data Format | JSON |
| Authentication Required | No |
| API Key Required | No |

The review endpoint was accessed using Python `requests` with parameters specifying language, purchase type, review ordering, and the number of reviews per request.

#### Result

| Metric | Result |
|---|---|
| HTTP status | 200 |
| Reviews returned | 20 |
| Login required | No |
| API key required | No |
| Structured JSON available | Yes |

The returned response also included aggregate review information:

| Metric | Result |
|---|---:|
| Review score | 8 |
| Review score description | Very Positive |
| Total positive reviews | 591,357 |
| Total negative reviews | 82,240 |
| Total reviews | 673,597 |

#### Accessible Review Fields

The returned review objects contained structured fields suitable for downstream analysis, including:

- Review ID
- User information
- Review text
- Language
- Timestamp
- Recommendation outcome
- Helpful votes
- Funny votes
- Purchase information
- Playtime information
- Refund status
- Early access status

#### Observation

Steam review data was directly accessible through a public JSON response without requiring authentication or manual interaction.

The structured response format substantially simplifies automated extraction compared with HTML-based scraping.

### 4.2 Pagination and Scalability Test

#### Objective

This test evaluated whether Steam reviews could be collected across multiple result pages without duplication or manual intervention.

#### Method

Steam's cursor-based pagination mechanism was tested across three consecutive review batches.

Each request collected up to 20 reviews and used the returned cursor value to retrieve the next batch.

#### Result

| Page | Reviews Collected | HTTP Status |
|---|---:|---:|
| 1 | 20 | 200 |
| 2 | 20 | 200 |
| 3 | 20 | 200 |

A total of 60 reviews were collected.

| Metric | Result |
|---|---:|
| Total reviews collected | 60 |
| Unique review IDs | 60 |
| Duplicate review IDs | 0 |
| Manual intervention required | No |

#### Observation

Cursor-based pagination successfully retrieved multiple consecutive review batches.

All 60 collected reviews had unique review IDs, indicating that the pagination workflow could expand collection beyond the initial response without duplication.

This provides strong support for automated recurring ingestion at larger volumes.

### 4.3 Repeatability Test

#### Objective

This test evaluated whether the same Steam review request produced consistent results across repeated collection attempts.

#### Method

The same request parameters were executed twice using the same application, filter settings, page size, and starting cursor.

The number of reviews and review IDs returned in both runs were compared.

#### Result

| Metric | Result |
|---|---|
| Run 1 reviews | 20 |
| Run 2 reviews | 20 |
| Review count consistent | Yes |
| Review IDs consistent | Yes |
| Run 1 unique IDs | 20 |
| Run 2 unique IDs | 20 |

#### Observation

The two controlled extraction runs returned the same number of reviews and the same review IDs.

This indicates strong short-term repeatability under identical request conditions.

### 4.4 Data Quality Test

#### Objective

This test evaluated the completeness of core review fields required for downstream sentiment and text analysis.

#### Method

The first 20 collected reviews were checked for missing values across selected core fields.

#### Result

| Field | Missing Values |
|---|---:|
| recommendationid | 0 / 20 |
| language | 0 / 20 |
| review | 0 / 20 |
| timestamp_created | 0 / 20 |
| voted_up | 0 / 20 |
| votes_up | 0 / 20 |

#### Observation

No missing values were found across the selected core fields in the controlled sample.

Steam also provides a direct recommendation signal through `voted_up`, which is particularly useful for sentiment-related downstream analysis.

### 4.5 Steam Scorecard

| Dimension | Score | Evaluation |
|---|---:|---|
| Data Availability | 5/5 | Steam provides large volumes of user-generated review text together with timestamps, recommendation signals, voting metadata, and user-related attributes. |
| Accessibility | 5/5 | Review data was accessible through a public JSON response without login, API key, or manual intervention. |
| Repeatability | 5/5 | Repeated controlled requests returned the same review count and review IDs. |
| Scalability | 5/5 | Cursor-based pagination successfully collected 60 unique reviews across three consecutive batches without manual intervention. |
| Data Quality | 5/5 | No missing values were found in the selected core fields across the 20-review sample. |
| Maintenance Complexity | 5/5 | Structured JSON, direct programmatic access, and straightforward cursor-based pagination minimize extraction and maintenance complexity. |

**Overall Score: 30/30**

### 4.6 Steam Assessment

Steam performed strongly across all six evaluation dimensions in the controlled tests.

The source provides high-volume user-generated review text, structured sentiment-related metadata, public programmatic access, reliable cursor-based pagination, and strong short-term repeatability. The JSON response structure also reduces the parsing and maintenance burden associated with HTML-based extraction.

Based on the current controlled tests, Steam is a strong candidate for the first recurring ingestion prototype. The 30/30 score reflects performance within the tested environment and does not imply that long-term source behavior or access conditions cannot change.

## 5. Hacker News Evaluation

### 5.1 Comment Data Accessibility Test

#### Objective

This test evaluated whether Hacker News discussion data could be accessed directly without login, authentication, or an API key.

#### Method

A public Hacker News story was selected for controlled testing.

| Field | Value |
|---|---|
| Story | 2026 Eclipse Webcams |
| Story ID | 49270953 |
| Data Format | JSON |
| Authentication Required | No |
| API Key Required | No |

The story endpoint was first accessed to retrieve the story metadata and top-level comment IDs.

The first 20 top-level comments were then retrieved individually through the public item endpoint.

#### Result

| Metric | Result |
|---|---|
| Story HTTP status | 200 |
| Top-level comment IDs found | 29 |
| Comments collected | 20 |
| Failed comment requests | 0 |
| Login required | No |
| API key required | No |
| Structured JSON available | Yes |

#### Accessible Comment Fields

The collected comments included:

- Comment ID
- Author
- Comment text
- Timestamp
- Parent ID
- Child comment IDs

#### Observation

Hacker News discussion data was directly accessible through public JSON endpoints without authentication or manual intervention.

Unlike Steam, comments are retrieved through individual item IDs rather than a batch review endpoint. This introduces additional request overhead when collecting larger discussion threads.

The comment text is also returned in HTML-formatted content, meaning downstream cleaning is required before text analysis.

### 5.2 Collection Reliability Test

#### Objective

This test evaluated whether multiple Hacker News comments could be collected successfully within a single automated workflow.

#### Method

The first 20 top-level comment IDs from the selected story were retrieved sequentially.

Retry logic, request timeouts, and exception handling were included to reduce the impact of temporary connection failures.

#### Result

| Metric | Result |
|---|---:|
| Comments requested | 20 |
| Comments collected | 20 |
| Failed requests | 0 |
| Successful collection rate | 100% |

#### Observation

All 20 requested comments were successfully collected during the controlled test.

An earlier request attempt encountered a temporary SSL connection error, but the issue was resolved after adding retry and timeout handling.

This suggests that automated collection is feasible, although basic request-resilience logic should be included in a recurring ingestion pipeline.

### 5.3 Repeatability Test

#### Objective

This test evaluated whether repeated collection attempts produced consistent results under the same conditions.

#### Method

The same story and first 20 top-level comments were collected twice.

The review count, comment IDs, and full comment records were compared across both runs.

#### Result

| Metric | Result |
|---|---|
| Run 1 comments | 20 |
| Run 2 comments | 20 |
| Comment count consistent | Yes |
| Comment IDs consistent | Yes |
| Full comment records consistent | Yes |
| Run 1 unique IDs | 20 |
| Run 2 unique IDs | 20 |

#### Observation

The two controlled runs returned the same number of comments, the same comment IDs, and identical comment records.

This indicates strong short-term repeatability for the tested discussion thread.

### 5.4 Data Quality Test

#### Objective

This test evaluated the completeness of selected fields required for downstream text analysis and relational storage.

#### Method

The 20 collected comments from the first run were checked for missing values across five core fields.

#### Result

| Field | Missing Values |
|---|---:|
| comment_id | 0 / 20 |
| author | 1 / 20 |
| text | 1 / 20 |
| timestamp | 0 / 20 |
| parent_id | 0 / 20 |

#### Observation

Most core fields were complete in the controlled sample.

However, one comment was missing an author and one was missing comment text. In addition, comment text may contain HTML tags and encoded HTML entities.

These issues would require missing-value handling and HTML cleaning during downstream preprocessing.

### 5.5 Hacker News Scorecard

| Dimension | Score | Evaluation |
|---|---:|---|
| Data Availability | 4/5 | Hacker News provides substantial user-generated discussion text together with comment IDs, authors, timestamps, and parent-child relationships. However, it does not provide direct rating or recommendation labels comparable to Steam reviews. |
| Accessibility | 5/5 | Story and comment data were accessible through public JSON endpoints without login, API key, or manual intervention. |
| Repeatability | 5/5 | Two controlled runs returned the same comment count, IDs, and full records. |
| Scalability | 4/5 | Discussion trees can be expanded through comment IDs and child relationships, but comments must generally be retrieved item by item, increasing request volume. |
| Data Quality | 4/5 | Core fields were mostly complete, but author and text each had one missing value in the 20-comment sample, and text requires HTML cleaning. |
| Maintenance Complexity | 4/5 | The API structure is straightforward, but recurring ingestion requires retry logic, HTML cleaning, and traversal of nested comment structures. |

**Overall Score: 26/30**

### 5.6 Hacker News Assessment

Hacker News performed well as a publicly accessible source of user-generated discussion text.

The source requires no authentication or API key, provides structured JSON responses, and demonstrated strong repeatability in the controlled tests.

However, compared with Steam, Hacker News requires more individual HTTP requests, additional handling for nested discussion structures, and text cleaning for HTML-formatted content. It also lacks direct rating or recommendation fields that can serve as explicit sentiment labels.

Hacker News is therefore technically feasible for recurring ingestion, but it introduces more preprocessing and collection complexity than Steam.

## 6. Side-by-Side Comparison

The three candidate sources were evaluated using the same six dimensions to support a consistent comparison.

| Dimension | Amazon | Steam | Hacker News |
|---|---:|---:|---:|
| Data Availability | 5/5 | 5/5 | 4/5 |
| Accessibility | 3/5 | 5/5 | 5/5 |
| Repeatability | 4/5 | 5/5 | 5/5 |
| Scalability | 2/5 | 5/5 | 4/5 |
| Data Quality | 4/5 | 5/5 | 4/5 |
| Maintenance Complexity | 2/5 | 5/5 | 4/5 |
| **Overall Score** | **20/30** | **30/30** | **26/30** |

### 6.1 Key Trade-offs

Amazon provides the richest combination of product metadata and customer review attributes. However, the controlled tests identified significant access and scalability limitations. Full review access required authentication, anonymous requests did not expose usable review content, and additional review access required manual intervention.

Steam provided both high-volume user-generated review text and structured sentiment-related metadata. Review data was accessible through a public JSON response without login or an API key, cursor-based pagination worked across multiple batches, and repeated requests produced consistent results. These characteristics reduce both ingestion complexity and ongoing maintenance effort.

Hacker News also provided strong public accessibility and repeatability. Its structured discussion data includes comment text, timestamps, authors, and parent-child relationships. However, larger-scale collection requires more individual requests, comment text requires HTML cleaning, and the source does not provide an explicit rating or recommendation signal comparable to Steam.

### 6.2 Overall Comparison

From a data richness perspective, Amazon and Steam both provide strong user-generated content.

From an engineering perspective, however, Steam demonstrated the strongest balance of accessibility, repeatability, scalability, data quality, and low maintenance complexity.

Hacker News is also technically feasible and could be useful for community-discussion ingestion, but its data structure requires more preprocessing and request management than Steam.

Amazon remains valuable as a potential future source, but its current access restrictions make it less suitable for the first recurring ingestion prototype.

## 7. Recommendation

Steam is recommended as the source for the first recurring ingestion prototype.

The recommendation is based on the results of the controlled feasibility tests rather than data volume alone.

Steam demonstrated several practical advantages:

- Public programmatic access without login or API key
- Structured JSON responses
- High-volume user-generated review content
- Direct recommendation signals suitable for sentiment analysis
- Cursor-based pagination
- Consistent repeated extraction
- Complete core fields in the controlled sample
- Low extraction and maintenance complexity

These characteristics make Steam the most suitable source for validating the next stage of the ingestion architecture.

Amazon may be reconsidered in a later phase if a more reliable review access method becomes available. Hacker News may also be useful as an additional source for community-discussion data once the core ingestion framework has been validated.

## 8. Supporting Evidence

Supporting scripts and sample outputs used in the feasibility tests are included in this repository.

### Amazon

Scripts:
- `scripts/amazon_review_extraction.py`
- `scripts/amazon_repeatability_test.py`

Sample outputs:
- `sample_outputs/amazon_reviews_sample.json`
- `sample_outputs/amazon_repeatability_result.txt`

### Steam

Scripts:
- `scripts/steam_review_extraction.py`
- `scripts/steam_pagination_test.py`
- `scripts/steam_repeatability_test.py`

Sample outputs:
- `sample_outputs/steam_reviews_sample.json`
- `sample_outputs/steam_pagination_result.txt`
- `sample_outputs/steam_repeatability_result.txt`

### Hacker News

Scripts:
- `scripts/hackernews_comment_extraction.py`
- `scripts/hackernews_repeatability_test.py`

Sample outputs:
- `sample_outputs/hackernews_comments_sample.json`
- `sample_outputs/hackernews_repeatability_result.txt`
