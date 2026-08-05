# amazon-data-acquisition-feasibility
Evaluating Amazon as a recurring source for structured product and review data acquisition.

## Objective
The goal of this feasibility assessment is to evaluate whether Amazon can serve as a reliable recurring data source.

The assessment evaluates:

- what product and review fields are accessible
- whether review data can be collected consistently
- whether review pagination and extraction scale reliably
- what limitations affect automated recurring collection
- whether Amazon is suitable for downstream analytical pipelines

## Tested Categories

The feasibility study covers multiple Amazon product categories:

- Beauty & Health
- Electronics
- Books
- Clothing, Shoes, Jewelry & Watches
- Home, Garden & Tools


## Evaluation Dimensions

### Data Availability
- Product metadata
- Review fields

### Accessibility
- Page accessibility
- Review accessibility

### Repeatability
- Multiple collection attempts
- Consistency of returned data

### Scalability
- Pagination behavior
- Reviews collected per product

### Data Quality
- Completeness
- Stability of fields

### Maintenance Complexity
- Login requirements
- Manual intervention
- Access restrictions


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

