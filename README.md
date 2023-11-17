# From Red Carpets to Revenue Streams: Understanding the Dynamics of Film Accolades, Commerce, and Cultural Influence

## Abstract
In the realm of cinematic expression, a tension often exists between artistic merit and commercial profitability. Acclaimed screenwriter Woody Allen famously said: “If my films don't show a profit, I know I'm doing something right.” Contrasting the financial success stories of Marvel movies, Allen's perspective raises a fundamental question: Are cultural and commercial successes inherently opposed in the movie industry?

Utilizing the CMU Movie Corpus Dataset, comprising of more than 40,000 plot summaries, our research aims to deploy NLP to extract relevant plot features. Analyzing their impact on success metrics, we seek to examine exclusivity or similarity in the characteristics of movies considered succesful by each camp. Ultimately, our goal is to understand the interplay between plot originality and movie success, potentially providing explanations to the underlying mechanisms that steer certain films towards commercial triumph, cultural resonance, or both.

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
4. [Timeline Proposal](#timeline-proposal)
5. [Team Organisation](#team-organisation)
6. [Questions for TAs](#questions-for-tas)


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
To create a score for commerical success, we will carefully choose variables that indicate how well a movie performed at the box office. These variables include box-office revenue, budget, ROI, and perhaps lifetime gross. As revenue is only available for ∼10% of the movies in CMU corpus, we plan to use  [<strong>Global Movie Franchise Revenue and Budget Data</strong>](https://www.kaggle.com/datasets/thedevastator/global-movie-franchise-revenue-and-budget-data/data) by 'The Devastator' to access lifetime gross and budget values for each movie.

## Cultural Metrics
To assess a movie's cultural impact, we consider utilizing either absolute ratings from IMDb or sentiment analysis/polarity of movie reviews. This approach recognizes that significant cultural impact is not solely tied to positive acclaim but can also stem from controversial or polarizing content. To gather the necessary data, we will access the [<strong>IMDb Movie Reviews</strong>](https://paperswithcode.com/dataset/imdb-movie-reviews) by Andrew L. Maas and [<strong>IMDB Movie Ratings Dataset
</strong>](https://www.kaggle.com/datasets/thedevastator/imdb-movie-ratings-dataset) by 'The Devastator'.

## Awards and Recognition
To access the winners and nominees of the Oscar awards, we use the [<strong>The Oscar Award, 1927 - 2023</strong>](https://www.kaggle.com/datasets/unanimad/the-oscar-award) by Raphael Fontes. We merge this with the CMU corpus using inner join to create a "awarded" database of movies.

## Methodology
As our project will follow a typical data science structure with data processing, feature extraction, feature engineering and model tuning, this section will mainly focus on how we plan to address the proposed research questions through our analysis.

### Q1: Plot Characteristics of Critically Acclaimed vs. Popular Films
After succesfully extracting relevant plot features from the movie summaries (using a fine-tuned Llama2 model), we would conduct a comparative analysis to explore similarity across features. Selecting movies based on their commercial and cultural rating, we could explore (genre-wise) how critically acclaimed movies differs from commercially focused ones.

### Q2: Plot Praise/Critique
Using sentiment analysis and topic modelling, we could analyse what aspects of a movie (plot, characters, visuals) reviews are most frequently concerned about. This should indicate how important the plot is for viewer perception. 

### Q3: Awards and Success
Through our rating system, we could analyse the scores of winners and nominees across categories. By conducting hypothesis testing, we could for instance explore whether these awards are biased or neutral. 

### Q4: Genre/Theme Recognition in Awards 
Building on the previous research question, we could analyse whether certain genres or prevalent movie themes are more prone to getting recognised by awards.

### Q5: Importance of Innovative Storytelling
By using a similarity/distance metric (e.g: cosine similarity, euclidean distance) we could quantify the originality of a movie. As high-dimensional spaces require more data to achieve similar density as lower-dimensional spaces, we might consider limiting the amount of features and compute similarity genre-wise.

### Q6: Character Diversity
From the plot summaries, we can extract characters and their features (age, gender, ethnicity, tropes), and analyse whether certain characteristics are associated with successful movies.

### Q7: Plot Complexity
Analysing sentiment trajectory, text complexity (e.g: Flesch Reading Ease, Gunning Fog index), topic modelling and event detection, we could quantify a movie's complexity.


## Timeline Proposal

### Week 1: Data Preprocessing and Integration

- Dataset: initial analysis, preprocessing and incorporating external data.
- NLP: text cleaning, tokenization, and handle missing values in plot summaries.

### Week 2: Feature Extraction and Correlation Analysis (:round_pushpin: We are here)

- Complete feature extraction: keywords, tropes, and other features using NLP.
- Prepare scores and features for analysis

### Week 3: Deepen Correlation Analysis and Model Preparation

- Calculate correlations between identified features and success metrics.
- Generate visual representations for correlations.
- Initiate model development: prepare features and start model training.

### Week 4: Model Evaluation and Data Story Initiation

- Evaluate model performance and tune hyperparameters.
- Enhancing visual representations for inclusion in the data story.
- Begin compiling project findings, insights, and visualizations into the initial structure of the data story.

### Week 5: Data Story Finalization and Presentation Preparation

- Complete data story by incorporating project findings, insights, and refined visualizations.
- Review the data story on: credibility, validity, storytelling
- Prepare/rehearse communication to articulate project methodologies, findings, and conclusions concisely.

## (Tentative) Team Organisation 

- Arundhati and Simon will work on the NLP methods, feature extraction using LLMs, and classification (under consideration).
- Daniil and Hans Kristian will work on EDA, correlation metrics and classification (under consideration).
- German will work on the presentation and data story.
