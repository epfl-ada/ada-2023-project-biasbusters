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

## Table of Contents

1. [Research Questions](#research-questions)
2. [Supplementary Datasets](#supplementary-datasets)
3. [Methods](#methods)
4. [Team Organisation](#team-organisation)
5. [Questions for TAs](#questions-for-tas)


## Research questions
1. How do plot characteristics differ between films that receive critical acclaim and those that are popular with general audiences?
2. How frequent and passionately are movies praised or critiqued for their plot in movie reviews and critics?
3. To what extent do awards like the Oscars and Golden Globes correlate with a movie's commercial or cultural success?
4. Are there specific genres or themes that tend to receive more recognition in prestigious awards despite their commercial success or lack thereof?
5. How do movies that introduce innovative storytelling techniques fare in terms of industry recognition, audience reception, and commercial success?
6. Is there a discernable relationship between the characteristics of characters (age, gender, ethnicity, tropes) and the types of movies that receive awards and cultural/commercial success?
7. Do movies with intricate plot structures or non-linear narratives tend to receive more cultural recognition?

## Supplementary Datasets

Much of our intended analysis is dependent of data not present in the CMU Movie Corpus dataset. We therefore plan to incorporate external data sources to supplement the plot features.

### Commerical Metrics
To create a score for commerical success, we will carefully choose variables that indicate how well a movie performed at the box office. These variables include box-office revenue, budget, ROI, and perhaps lifetime gross. As revenue is only available for ∼10% of the movies in CMU corpus, we plan to use  [<strong>The Movies Dataset</strong>](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) to access lifetime revenue and budget values for broader amount of movies.

## Cultural Metrics
To assess a movie's cultural impact, we consider utilizing either absolute ratings from IMDb or sentiment analysis/polarity of movie reviews. This approach recognizes that significant cultural impact is not solely tied to positive acclaim but can also stem from controversial or polarizing content. To gather the necessary data, we will access the [<strong>IMDB Dataset of 50K Movie Reviews</strong>](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) and [<strong>MovieLens 20M Dataset
</strong>](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv).

## Methodology
As our project will follow a typical data science structure with data processing, feature extraction, feature engineering and model tuning, this section will mainly focus on how we plan to address the proposed research questions through our analysis.

### Q1: Plot Characteristics of Critically Acclaimed vs. Popular Films
After succesfully extracting relevant plot features from the movie summaries (using an instruct tuned Llama 2 13B Chat model in zero- or few-shot learning manner), we would conduct a comparative analysis to explore similarity across features. Selecting movies based on their commercial and cultural rating, we could explore (genre-wise) how critically acclaimed movies differs from commercially focused ones.

### Q2: Plot Praise/Critique
Using sentiment analysis and topic modelling, we could analyse what aspects of a movie (plot, characters, visuals) reviews are most frequently concerned about. This should indicate how important the plot is for viewer perception. 

### Q3: Awards and Success
Through our rating system, we could analyse the scores of winners and nominees across categories. By conducting hypothesis testing, we could for instance explore whether these awards are biased or neutral. 

### Q4: Genre/Theme Recognition in Awards 
Building on the previous research question, we could analyse whether certain genres or prevalent movie themes are more prone to getting recognised by awards.

### Q5: Importance of Innovative Storytelling
We could incorporate few methods of mapping movies to some metric space in order to estimate their originality. We could use some advanced LLMs from [<strong>Massive Text Embedding Benchmark (MTEB) Leaderboard</strong>](https://huggingface.co/spaces/mteb/leaderboard) to obtain embeddings for plot summaries. These embeddings are trained to meet metric space properties. As for plots and movies features extracted in the previous steps we could use some dimensionality reduction methods such as PCA and t-SNE and estimate distance between objects by utilising euclidean distance. Another method of estimating movies originality could imply the usage of LLM (e.g., the previously mentioned Llama 13B Chat) in order to predict the ending of the movies stories and then obtaining an originality score by estimation of the distances between predicted endings and the genuin ones. The distance could be computed between the corresponding text embeddings.

### Q6: Character Diversity
From the plot summaries, we can extract characters and their features (age, gender, ethnicity, tropes), and analyse whether certain characteristics are associated with successful movies.

### Q7: Plot Complexity
Analysing sentiment trajectory, text complexity (e.g: Flesch Reading Ease, Gunning Fog index), topic modelling and event detection, we could quantify a movie's complexity.

## Team Contribution 

- Simon: extracting features from plots (`mood`, `target_audience`, `originality_score`, etc) using LLM, regression analysis for critics
- Arundhati: scraping additional data from the Internet, presentation and data story
- Hans Kristian: scraping additional data from the Internet; the main part of data story about graph communities
- Daniil and German: regression analysis for revenue, imdb reviews, creating datastory notebook
