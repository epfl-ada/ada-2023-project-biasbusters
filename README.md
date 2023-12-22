# From Red Carpets to Revenue Streams: Understanding the Dynamics of Film Accolades, Commerce, and Cultural Influence

Datastory webpage: https://arundhatibala.github.io/ada-times/

Datastory notebook: https://github.com/epfl-ada/ada-2023-project-biasbusters/blob/main/datastory.ipynb

## Abstract
In the realm of cinematic expression, a tension often exists between artistic merit and commercial profitability. Acclaimed screenwriter Woody Allen famously said: “If my films don't show a profit, I know I'm doing something right.” Contrasting the financial success stories of Marvel movies, Allen's perspective raises a fundamental question: Are cultural and commercial successes inherently opposed in the movie industry?

Utilizing the CMU Movie Corpus Dataset, comprising of more than 40,000 plot summaries, our research aims to deploy NLP to extract relevant plot features. Analyzing their impact on success metrics, we seek to examine exclusivity or similarity in the characteristics of movies considered succesful by each camp. Ultimately, our goal is to understand the interplay between plot originality and movie success, potentially providing explanations to the underlying mechanisms that steer certain films towards commercial triumph, cultural resonance, or both.

## Authors

Hans Kristian Bjørgo Kværum <br>
Arundhati Balasubramaniam <br>
Semen Matrenok <br>
Daniil Likhobaba <br>
German Gavrilenko <br>


## Research questions
1. How do plot characteristics differ between films that receive critical acclaim and those that are popular with general audiences?
2. How frequent and passionately are movies praised or critiqued for their plot in movie reviews and critics?
3. To what extent do awards like the Oscars and Golden Globes correlate with a movie's commercial or cultural success?
4. Are there specific genres or themes that tend to receive more recognition in prestigious awards despite their commercial success or lack thereof?
5. How do movies that introduce innovative storytelling techniques fare in terms of industry recognition, audience reception, and commercial success?
6. Is there a discernable relationship between the characteristics of characters (age, gender, ethnicity, tropes) and the types of movies that receive awards and cultural/commercial success?
7. Do movies with intricate plot structures or non-linear narratives tend to receive more cultural recognition?

## Supplementary Datasets Utilized

In order to enhance our analysis, we integrated several external data sources with the CMU Movie Corpus dataset. These additional datasets allowed us to enrich our analysis with more comprehensive plot features and commercial and cultural metrics.

### Commercial Metrics
We incorporated variables to create a score for commercial success. These variables include:

- **Box-office Revenue**
- **Budget**
- **Return on Investment (ROI)**
- **Lifetime Gross**

For a broader range of movies, we utilized data from [**The Movies Dataset**](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset), which provided lifetime revenue and budget values, supplementing the limited revenue data in the CMU corpus.

### Cultural Metrics
To evaluate a movie's cultural impact, we employed two distinct approaches:

1. **IMDb Ratings**: We considered absolute ratings from IMDb to gauge overall viewer reception and impact.

2. **Sentiment Analysis of Movie Reviews**: We analyzed the polarity of movie reviews to understand the depth of a movie's cultural influence, acknowledging that significant impact can arise from both positive acclaim and controversial content.

The data for these analyses were sourced from two datasets:

- [**IMDB Dataset of 50K Movie Reviews**](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)
- [**MovieLens 20M Dataset**](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv)

This integration of supplementary datasets enriched our analysis, enabling a more holistic understanding of movies' commercial success and cultural impact.

### Rotten tomatoes dataset
### Boxoffice Mojo

## Project Methodology

### 1. Community Detection with Louvain Method
- Utilized the **Louvain method** to cluster movies based on their genre similarities, creating distinct communities.

### 2. Community Aggregation for Topic Modelling
- Created a "document" for each community by **aggregating all genres** within that community.

### 3. Data Preparation for Topic Modelling
- Converted the aggregated genre data into a **term-frequency matrix**, making it suitable for topic modeling.

### 4. Application of Latent Dirichlet Allocation (LDA)
- Employed **LDA for topic modelling** to uncover underlying themes in each movie community.

### 5. Visualization and Interpretation
- **Visualized and interpreted** the LDA results to label and define the communities, offering nuanced insights.

### 6. Hard-Assignment of Movies to Communities
- Predominantly used **hard-assignment** for movies to communities based on a high probability threshold (above 0.5).

### 7. Linear Regression Evaluation and Implementation
- Implemented a custom **linear regression function in log-space**.
- Performed **K-fold cross-validation** with k=5 splits, focusing on Mean Squared Error (MSE) for model evaluation.
- Calculated key metrics such as **average MSE, Root Mean Squared Logarithmic Error (RMSLE), and R-squared values**.

### 8. Decision on Imputation Strategies
- For 'audience_rating_count', chose **Linear Regression** over KNN due to better performance in capturing variance in log-transformed data.
- For 'tomato_rating_count', selected the **best KNN model (k=108)** as it outperformed linear regression in both avg. MSE and R-squared in log space.

### 9. Imputation of Missing Data
- Applied **Linear Regression for imputing 'audience_rating_count'**.
- Used **KNN with k=108 for imputing 'tomato_rating_count'**.

## Team Contribution 

- Simon: extracting features from plots (`mood`, `target_audience`, `originality_score`, etc) using LLM, regression analysis for critics
- Arundhati: scraping additional data from the Internet, presentation and data story
- Hans Kristian: scraping additional data from the Internet; the main part of data story about graph communities
- Daniil and German: regression analysis for revenue, imdb reviews, creating datastory notebook, critics analysis
