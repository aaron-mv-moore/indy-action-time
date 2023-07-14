# Indy Action Time 

## Description
The [Mayor's Action Center](https://www.indy.gov/activity/mayors-action-center-services) in Indianapolis, IN routes requests for services to the appropriate city department. [Request Indy](https://www.indy.gov/agency/mayors-action-center) is the point of contact with an online submisison form and phone number available for Indianapolis residents. This project seeks to explore and predict non-emergency service requests response time for residents of Indianapolis, IN.

## Project Goals
* Identify the average time for a non-emergency service requests to be closed
* Identify drivers of non-emergency service requests' response times
* Identify areas of improvement for M
* Predict response timeframe for non-emergency service requests with a classification machine learning model

## Project Plan
### Acquire
* Mayor's Action Center (MAC) service data was acquire from [Open Indy](https://data.indy.gov/datasets/IndyGIS::mayors-action-center-service-cases/about) using the API.
* Demographic data for the entire state of Indiana was acquired from the [United States Census Bureau]() using Census Tracts as the geographic unit interest.
> * Assistance using [this article](https://towardsdatascience.com/scraping-us-census-data-via-cenpy-9aeab12c877e) as a guide.
### Prepare
* MAC Data Preparation
> * Address null values
> * Format addresses for geocoding
> * Geocode the addresses from MAC
* Census Data Preparation
> * Address areas of concern such as outliers, null values, incorrect data entry, etc.
* MAC-Census Preparation
> * Left join data uaing geocodeed addresses from MAC on the left
> * Drop unnecessary features
> * Create target feature
> * Split the data
### Explore
* Conduct univariate analysis on each feature of interest
* Conduct bivariate exploratory analysis with target and each feature of interest
* Conduct bivariate exploratory analysis on non-target features that may have relationships
* Conduct multivariate exploratory analysis with feature sub-groups
### Model
* Identify appropriate evaluation metric
* Create a baseline model and evaluate
* Create multiple models and identify the best performing
* Test best model 
### Conclude 
* Summarize
* Recommend
* Identify next steps

## Data Dictionary
| Feature | Definition | 
|:--------|:-----------|
|  |  |
|  |  |
|  | |
|  | |
|  |  |


## Steps to Reproduce
1. Clone this repo
2. 

## Takeaways
* 

## Recommendations
* 

