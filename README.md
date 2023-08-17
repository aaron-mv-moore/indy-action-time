# Indy Action Time 

## Description
This project seeks to explore and predict non-emergency service requests response time for residents of Indianapolis, IN. The [Mayor's Action Center](https://www.indy.gov/activity/mayors-action-center-services) in Indianapolis, IN routes requests for services to the appropriate city department. [Request Indy](https://www.indy.gov/agency/mayors-action-center) is the point of contact with an online submisison form and phone number available for Indianapolis residents.

A non-technical explanation and a dashboard will be available upon completion of this project. 

## Goals
* Identify the average time for a non-emergency service requests to be closed 
* Identify drivers of non-emergency service requests' response times 
* Identify areas of improvement for Mayor Action Center
* Predict response time frame for non-emergency service requests with a classification machine learning model

## Plan
### Acquire
* Mayor's Action Center (MAC) service data was acquire from [Open Indy](https://data.indy.gov/datasets/IndyGIS::mayors-action-center-service-cases/about).
<!-- * Demographic data for the entire state of Indiana was acquired from the [United States Census Bureau](https://data.census.gov) using Census Tracts as the geographic unit interest.
  * Assistance using [this article](https://towardsdatascience.com/scraping-us-census-data-via-cenpy-9aeab12c877e) as a guide. -->
### Prepare
* MAC Data Cleaning
  * Address null values
  * Address duplicates
  * Address outliers
  * Address errors, mistakes, and inconsistencies
* Mac Data Preparation
  * Feature engineering
  * Encoding/scaling
  * Clustering
  <!-- * Format addresses for geocoding
  * Geocode the addresses from MAC -->
<!-- * Census Data Preparation
  * Address areas of concern such as outliers, null values, incorrect data entry, etc.
* MAC-Census Preparation
  * Left join data uaing geocodeed addresses from MAC on the left
  * Drop unnecessary features
  * Create target feature
  * Split the data -->
### Explore
* Conduct univariate analysis on each feature of interest
* Conduct bivariate exploratory analysis with target and each feature of interest
* Conduct bivariate exploratory analysis on non-target features that may have relationships
* Conduct multivariate exploratory analysis with feature sub-groups

#### Hypothesis/Questions
* Is there a relationship between zip codes and response times?
* Is there a relationship between keywords and response times?
* Is there a relationship between subcategories and response times?
* Is there a relationship beteen the number of open cases and response times?
* Is there a relationship between the number of open cases in a zip code and response times?
* Is there a relationship between the number of open cases for a keyword and repsonse times?
* Is there a relationship between the number of open cases for a subcategory and response times?
* Is there a relationship between the number of open cases for a keyword in a zip code and response times?
* Is there a relationship between the number of open cases for a subcategory in a zip code and response times?
### Model
* [Multi-class evaluation](https://towardsdatascience.com/comprehensive-guide-on-multiclass-classification-metrics-af94cfb83fbd) - F1 Score 
  * True Positives Type 1: Actual and predicted is 1 week
  * True Positives Type 2: Actual and predicted is 2 weeks
  * False Positives: Predicted as 1 or 2 weeks response time, but actual was 3, 4, or 5 weeks
  * False Negatives: Predicted as 3, 4, or 5 weeks, but actual was 1 or 2 weeks
<!-- The different response ratings are excellent, great, good, fair, and poor. What do we care about? We want all of them to be accurate if we are giving a time prediction. 
What do we want to avoid? We want o avoid telling someone there will be an excellent reponse time when it would be poor. That will lead to very annoyed individuals. False Positive's for excellent, great, and good if we estimate that it will have a poor  -->
* Baseline
  * Use the most common class as the prediction for all
  * Evaluate using F1 Score
* Classification Models:
  * Decision Tree, Random Forest, K-Nearest Neighbors, Logistic Regression, C-Support Vector Classification, and Gradient Boosting Classifier
* Test the best Model
### Conclude 
* Summarize
* Recommend
* Identify next steps

## Data Dictionary TBD
| Original Name | Cleaned Name | Definition | 
|:--------------|:-------------|:-----------|
| TBD | TBD | TBD |
<!-- | STATEFP10|  |
| COUNTYFP10|  |
| TRACTCE10|  |
| BLOCKCE10|  |
| NAME10|  |
| MTFCC10 |  |
| UR10|  |
| UACE10|  |
| UATYP10 |  |
| FUNCSTAT10|  |
| ALAND10|  |
| AWATER10|  |
| INTPTLAT10 |  |
| INTPTLON10 |  | -->

## Steps to Reproduce
1. Clone this repo
2. 

## Takeaways TBD
* 

## Recommendations TBD
* 

<!-- ## Sources:
* https://www2.census.gov/geo/pdfs/reference/GARM/Ch10GARM.pdf -->

