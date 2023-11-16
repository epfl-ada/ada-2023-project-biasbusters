# From Red Carpets to Revenue Streams: Understanding the Dynamics of Film Accolades, Commerce, and Cultural Influence

## Abstract

## Authors

Arundhati Balasubramaniam <br>
Daniil Likhobaba <br>
German Gavrilenko <br>
Hans Kristian <br>
Semen Matrenok <br>

## Table of Contents

1. [Research Questions](#research-questions)
2. [Supplementary Datasets](#supplementary-datasets)
3. [Methods](#methods)
4. [Timeline Proposal](#proposed-timeline)
5. [Team Organisation](#organization-within-the-team)
6. [Questions for TAs](#questions-for-tas)


## Research questions
1. To what extent do awards like the Oscars and Golden Globes correlate with commercial success?
How strongly are these awards associated with cultural impact, as indicated by critics' and viewers' reviews?
2. Are there specific genres or themes that tend to receive more recognition in prestigious awards despite their commercial success or lack thereof?
3. How has the correlation between awards, commercial success, and cultural impact evolved over different decades or periods in the film industry?
4. Is there a relationship between the characteristics of characters (age, gender, ethnicity, tropes) and the types of movies that receive awards or commercial success?
5. Do movies with intricate plot structures or non-linear narratives tend to receive more awards despite potential differences in commercial success?

## Supplementary Datasets

Our goal with addtional datasets is to supplement the CMU corpus with addition features for metrics which relate to our datastory.

### Commerical Metrics
To create a score for commerical success, we carefully choose variables that indicate how well a movie did at the box office. These variables include box-office revenue, a return-on-investment, and lifetime gross. While revenue is available to us in the CMU Movie Summary corpus metadata dataset, we use [<strong>Global Movie Franchise Revenue and Budget Data</strong>](https://www.kaggle.com/datasets/thedevastator/global-movie-franchise-revenue-and-budget-data/data) by The Devastator (we can't find their real name) to access lifetime gross and budget values for each movie.

## Cultural Metrics
To score cultural impact, we have the possibility of using iMDB absolute ratings or the absolute sentiment from reviews. We argue that a movie's cultural impact can be either positive or negative. As long as it evokes strong emotions in the viewer, we can characterise it as effective cultural impact. To access these variables, we use [<strong>IMDb Movie Reviews</strong>](https://paperswithcode.com/dataset/imdb-movie-reviews) by Andrew L. Maas and [<strong>IMDB Movie Ratings Dataset
</strong>](https://www.kaggle.com/datasets/thedevastator/imdb-movie-ratings-dataset) by The Devastator (yes, that's their name).

## Methods

### Step 1: Data Preprocessing
