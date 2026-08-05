# Amazon Data Acquisition Feasibility Report

## Test Case 1: Beauty & Health

### Product Information

| Field        | Value                                     |
| ------------ | ----------------------------------------- |
| Product Name | Estée Lauder Foundation 36-Hour Long-Wear |
| Category     | Beauty & Health                           |
| ASIN         | B0FWCZJCSY                                |
| URL          | https://www.amazon.com/Est%C3%A9e-Lauder-Foundation-36-Hour-Long-Wear/dp/B0FWCZJCSY/ref=sr_1_1_sspa?crid=2VT5I9X13N7KQ&dib=eyJ2IjoiMSJ9.Fyf926sXdVWf0AEptavW1Cu-k2WJjC-h-bNGQHPyjlyQ6kaNPB5rlLq4wQyvry1ZesdsvNVPdkk5mvwWhQa80MgsGs-Gv9OHao-4cT5yLDKihcLZkd117tZlBm5PKBdpGQoA0YICmEj8umaLVZ_QliOSUUBAgKDFfh-9JD-REQCvo4-ohXPdDzZkLr33EdFvY6qlYdF1DIVn7--fLm1yO-VRcWPgSpSetb3hwjAwCkpHpa8KRvoxV3F0cLBHw9oKAsa29FgdlTqORKJaRPMzc_9tRCZTlSAgqcn19Ff0QfU.8XeJIjTu5qLNONxGFa7E5FsR0bhXPvQuoSw-Vm_-LKk&dib_tag=se&keywords=foundation&qid=1785232918&rdc=1&sprefix=foundati%2Caps%2C445&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1‘|
| Page access  | Yes                                       |

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

## Phase 2: Review Data Pipeline Feasibility

### 2.1 Review Field Accessibility Test

#### Method

A baseline automated acquisition test was conducted using Python requests to evaluate whether Amazon review data could be directly extracted from the returned HTML response.

#### Result

| Metric | Result |
|---|---|
| HTTP status | 200 |
| Product page accessible | Yes |
| Review data in HTML response | No |
| Review objects extracted | 0 |

#### Observation

The Amazon review page was accessible through an HTTP request, but customer review content was not included in the initial HTML response.


### 2.2 Anonymous Access Restriction Test

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

## 2.3 Authenticated Review Extraction Test

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

## 2.4 Review Pagination Test

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

## 2.5 Repeatability Test

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

## Test Case 2: Electronics

### Product Information

| Field | Value |
|---|---|
| Product Name | Apple AirPods Pro (2nd Generation) |
| Category | Electronics |
| ASIN | B0GSRYXZM5 |
| URL |https://www.amazon.com/gp/aw/d/B0GSRYXZM5/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=e3c968b5c76dacc77f4e8cd1d2d21b99&hsa_cr_id=0&qid=1785306511&sr=1-2-9e67e56a-6f64-441f-a281-df67fc737124&i=aps&aref=1R5JVN1fve&ref_=sbx__sbtcd_asin_0_img&pd_rd_w=EvVEE&content-id=amzn1.sym.8de9b3d5-f5c5-40e9-9b39-d65f08d6ea68%3Aamzn1.sym.8de9b3d5-f5c5-40e9-9b39-d65f08d6ea68&pf_rd_p=8de9b3d5-f5c5-40e9-9b39-d65f08d6ea68&pf_rd_r=1D6F0H4A48CMJ54YAAT2&pd_rd_wg=esFwe&pd_rd_r=af3a9e13-36a1-4ad2-8019-bcf2afd6468a&th=1|
| Page access | Yes |

### Product Data Availability

| Field | Available |
|---|---|
| Product title | Yes |
| Brand | Yes |
| Price | Yes |
| Rating | Yes |
| Rating count | Yes |
| Product images | Yes |
| Product description | Yes |

### Customer Review Data Availability

#### Top Reviews

| Field | Available |
|---|---|
| Reviewer name | Yes |
| Review date | Yes |
| Review text | Yes |
| Helpful votes | Yes |
| Purchased variant | Yes |
| Verified purchase | Yes |


#### Full Review Access

| Field | Result |
|---|---|
| Full review access | Login required |


## Test Case 3: Books

### Product Information

| Field | Value |
|---|---|
| Product Name | The Old Man and the Sea |
| Category | Books |
| ASIN | 1476787840 |
| URL |https://www.amazon.com/Old-Man-Sea-Hemingway-Library/dp/1476787840/ref=sr_1_1?crid=1O2QKAJYXCX7Y&dib=eyJ2IjoiMSJ9.T3eFJXzevi463zGias550Pk2BVjNJxD2VlfvxvOAThYFXiXDkh0XN3AMkFDDT414zWfZuETIS_t8EMjnFiSxY8l4a-woC8HefA5IeRqY7p5cAY-Ftyodk4e-pOVo48lGwtspPmHjKKu2mlzOQfOuRkmDy_2EDE5FWFu6uhVjtja3Zx76_LXU3he03fjWozaFmrHfQw8TuTJPJx0lFNwgYG-9FxGV64TeWTLsd1nEWfM.vUB2PrswnQ6HXCwTxDVgl20FWu1U3vdZSZH001Ttku0&dib_tag=se&keywords=old+man+and+the+sea&qid=1785307653&s=books&sprefix=old+man+and+the+sea+%2Cstripbooks%2C411&sr=1-1|
| Page access | Yes |


### Product Data Availability

| Field | Available |
|---|---|
| Product title | Yes |
| Author | Yes |
| Price | Yes |
| Rating | Yes |
| Rating count | Yes |
| Product images | Yes |
| Product description | Yes |
| Format | Yes |


### Customer Review Data Availability

#### Top Reviews

| Field | Available |
|---|---|
| Reviewer name | Yes |
| Review date | Yes |
| Review text | Yes |
| Helpful votes | Yes |
| Purchased variant | Yes |
| Verified purchase | Yes |


#### Full Review Access

| Field | Result |
|---|---|
| Full review access | Login required |

## Test Case 4: Clothing, Shoes, Jewelry & Watches

### Product Information

| Field | Value |
|---|---|
| Product Name | Crocs Unisex |
| Category | Clothing, Shoes, Jewelry & Watches |
| ASIN | B001526RFY |
| URL |https://www.amazon.com/crocs-Unisex-Classic-White-Women/dp/B001526RFY/ref=sr_1_1_mod_primary_new?dib=eyJ2IjoiMSJ9.E2mDZcI3gAQ7gU-jF7tDWDL4Z6v_aMsHwldhuORJJeiQt6oerxUlPGhIKBZwe4FmQ42JFiY5cHwVAHXbyAd2j1zlrCTCtZ9O4jhbju-ViNE1kOmTrAPozBoONzSf-ekZ0O6kPerpWRuWdkWpRvDNz3ODa5mApIKBIjhak3IGXYgBYI0AH0xCMqJkJNmJYtHgGcNH5IjcaVcai4Z2dg-FwuiOln6q6bWr4KV2V0QFQGTCQrcNb1-A6NuYJhdRzFU8bAMvBP6x33kWI3bZR-YKw9U1zljFsvY2HbNglDDDQR8.8orvzB1JQDrY_Ue8cU-XWOF_YTZpHgAepEd_evE0vps&dib_tag=se&keywords=crocs&qid=1785308104&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=8-1&th=1&psc=1|
| Page access | Yes |


### Product Data Availability

| Field | Available |
|---|---|
| Product title | Yes |
| Brand | Yes |
| Price | Yes |
| Rating | Yes |
| Rating count | Yes |
| Product images | Yes |
| Product description | Yes |


### Customer Review Data Availability

#### Top Reviews

| Field | Available |
|---|---|
| Reviewer name | Yes |
| Review date | Yes |
| Review text | Yes |
| Helpful votes | Yes |
| Purchased variant | Yes |
| Verified purchase | Yes |


#### Full Review Access

| Field | Result |
|---|---|
| Full review access | Login required |

## Test Case 5: Home, Garden & Tools

### Product Information

| Field | Value |
|---|---|
| Product Name | Ninja Professional Plus Blender |
| Category | Home, Garden & Tools |
| ASIN | B0855B5Z6F |
| URL |https://www.amazon.com/Ninja-BN701-Professional-capacity-Crushing/dp/B0855B5Z6F/ref=sr_1_1?crid=2YB72JA7ZJDCP&dib=eyJ2IjoiMSJ9.QCJMlmIhaIKDbkSG-h3ZGOxHzqX9_7EivYhjn96C0-qmMj0CkLZVr81k2Y7LaXEuWQ4TeS9IOMLdz2ofnXZuB-1FwnUnSCEI7ahyHz8DRjRZk6HIBZyx2raLMHteM07sZ_-C2DOn6d3dbfLIP6aPHvOmb9CvVI5b06OX2LAt744OEbt1xRpdd0fsRzSxMhg-5D2R8gwO_JbQW3ORqqOi_25ESzAmYAeyiGFC7JNYl00.ruxOTLqDRaYGQfnWkVD7N5l7pAcNCLGLfiWeSENe-T8&dib_tag=se&keywords=Ninja%2BProfessional%2BBlender&qid=1785309363&sprefix=%2Caps%2C418&sr=8-1&th=1|
| Page access | Yes |


### Product Data Availability

| Field | Available |
|---|---|
| Product title | Yes |
| Brand | Yes |
| Price | Yes |
| Rating | Yes |
| Rating count | Yes |
| Product images | Yes |
| Product description | Yes |


### Customer Review Data Availability

#### Top Reviews

| Field | Available |
|---|---|
| Reviewer name | Yes |
| Review date | Yes |
| Review text | Yes |
| Helpful votes | Yes |
| Purchased variant | Yes |
| Verified purchase | Yes |


#### Full Review Access

| Field | Result |
|---|---|
| Full review access | Login required |

# Overall Findings

| Category | Product Data | Review Data | Main Limitation |
|---|---|---|---|
| Beauty & Health | Available | Partial review access | Full reviews require login |
| Electronics | Available | Partial review access | Full reviews require login |
| Books | Available | Partial review access | Full reviews require login |
| Clothing, Shoes, Jewelry & Watches | Available | Partial review access | Full reviews require login |
| Home, Garden & Tools | Available | Partial review access | Full reviews require login |
