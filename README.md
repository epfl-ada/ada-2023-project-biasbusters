# From Red Carpets to Revenue Streams: Understanding the Dynamics of Film Accolades, Commerce, and Cultural Influence

## Abstract

The 95th Academy Awards drew an average of 18.7 million viewers in the US, marking a significant 12% increase from the previous year. This surge in viewership prompts a fundamental question: What role does a movie's plot play in determining its success? Using the extensive CMU Movie Corpus Dataset with over 40,000 plot summaries, our study aims to uncover the core elements that define a film's triumph. We delve into these narrative components, aiming to understand their pivotal role in guiding a movie's path toward both commercial success and lasting cultural impact. By dissecting these elements, our analysis aims to differentiate between unique narrative features and common themes. Ultimately, our goal is to illuminate the nuanced influence of plot originality on a movie's journey within the dynamic landscape of cinematic achievement.

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

## Awards and Recognition
To access the winners and nominees of the Oscar awards, we use the [<strong>The Oscar Award, 1927 - 2023</strong>](https://www.kaggle.com/datasets/unanimad/the-oscar-award) by Raphael Fontes. We merge this with the CMU corpus using inner join to create a "awarded" database of movies.

## Methods

### Step 1: Data Preprocessing

#### Textual Cleaning
 - Tokenisation: Split the text into individual words or tokens after removing the stopwords like 'the', 'it', 'a'.
 - Lemmatisation: Reduce words to their base or root form to unify variations of the same word ("running" to "run").
 - Convert text into word embeddings (Word2Vec) to represent text numerically for analysis.

#### Metadata Cleaning
- Check for missing or null values in metadata columns and impute them.
- Conduct EDA to understand distributions, correlations, and outliers in the dataset, guiding further preprocessing steps and analysis strategies.
- Convert categorical data (like movie genres, countries) into a numerical format suitable for analysis, using hot-encoding.
- Merge or inner-join the plot summaries with metadata based on common identifiers (such as movie IDs) to create a comprehensive dataset for analysis.

### Step 2: Feature Extraction

#### Using Python packages

- Key_Words: Use a named entity recognition (NER) or keyword extraction task to identify key words or phrases from the plot summary. This could be a list or a frequency count of significant words. Extracting key themes or words that frequently appear in plot. For example, certain themes like 'love', 'war', 'adventure' might be more prevalent in higher-grossing movies. This column can be in form of comma-separated keywords, or the main keyword

- Movie_Tropes: Use of the character.metadata file along with application of topic modeling (e.g., Latent Dirichlet Allocation - LDA) to uncover prevalent themes or recurring tropes across plot summaries. For example, Adventure Quest, Love Triangle, Hero's Journey, Redemption Arc, Time Loop, Fish Out of Water, etc.


#### Using a fine-tuned Llama2 model

- Emotional_Tone: Similar to sentiment analysis, but focusing on a wider range of emotions like suspense, humor, tragedy, etc. This might require a few-shot approach with examples. This column could be in format of comma-separated emotions or just the main emotion of the plot

- topic_presence_score: Proportions of different topics identified in the summary, using techniques like Latent Dirichlet Allocation (LDA). For example, topics might be labeled as "romance", "conflict", "adventure", etc.

- Target_Audience: Infer the target audience (e.g., children, adults, families) based on the plot. This might involve identifying certain keywords or themes associated with different audience groups. Could be done via zero-shot

- Abstractness_Level: Assessing the level of abstractness or concreteness in the plot summary. Use a model to rate the abstractness on a scale (e.g., 1 to 5), where higher values indicate more abstract language. This could involve defining criteria for what constitutes abstract vs. concrete language. Note: it's rather plot feature, than movie feature

- Temporal_Setting: Identifying the time period in which the movie is set. Extract mentions of specific years, eras, or historical periods from the plot summary. Values: 'modern', 'future', 'past'

- Location_Setting: Identifying the primary geographical setting of the movie. Detect and extract mentioned locations, whether they are real (e.g., New York, Mars) or fictional (e.g., Middle Earth). Values: the main location or binary ('real' and 'fictional' location)

- Resolution_Clarity: Assessing how clearly the resolution of the plot is described in the summary. Rate the clarity of the plot resolution on a scale (e.g. 1-5), with higher values indicating a more clearly described resolution.

- Mood_Descriptor: Identifying the overall mood of the plot (e.g., dark, lighthearted, suspenseful, inspiring, motivating). Use sentiment analysis or a similar approach to classify the mood conveyed by the plot summary. Column can contain the main mood descriptor, or comma-separated list of moods

- Narrative_Perspective: Determining the narrative perspective used in the plot summary (e.g., first person, third person). Analyze the use of pronouns and narrative style to identify the perspective.

- Moral_Lesson: Identifying any explicit or implicit moral or lesson in the plot. Use thematic analysis to identify morals or lessons, which are often implicit in the plot summary. Values: binary value indicating presence/absence of moral lesson in the plot

- Engagement_Level: Estimating the level of engagement (e.g. 1-5) the plot is likely to elicit from viewers. Develop criteria for engagement (e.g., presence of suspense, action, emotional depth) and rate the summary accordingly. We don't have to specify each of these criteria, but rather can include these criteria in prompt for LLM

### Step 3: Calculating Correlations

Once we have our metrics in place, we will calculate the correlations between the commericial success, cultural impact, and the likelihood of being nominated or winning an oscar. We utilize statistical methods (e.g., Pearson correlation coefficient, Spearman's rank correlation) to quantify the strength and direction of relationships between pairs of variables.

### Step 4: Visualisation

We illustrate the correlations using visual aids like correlation matrices, scatter plots, or heatmaps to better comprehend relationships among the three variables.

### Step 5: Classification (under consideration)

#### Feature processing
- Identifying the primary language(s) in which the movie is presented. Multilingual movies might have varying audience reception.
- Incorporating information about lead actors, directors, and prominent crew members, considering their past associations with award-winning films.
- Utilizing identified storytelling elements or tropes (from the Movie_Tropes column) as categorical features that might contribute to award success.
- Encoding movie genres as categorical variables to assess if specific genres have higher chances of receiving awards.
- Extracting temporal features such as release year, month, or season to understand if release timing influences awards.
- Incorporating box office revenue, profitability metrics, or budget information as numerical features.
-  Creating interactions between features (e.g., actor-director collaboration, genre-trope combinations) to capture potential synergies.

#### Building the classifier
- Split the now-merged dataset into training and test sets, maintaining class distribution, to train and evaluate the model.
- Choose a suitable classification algorithm (e.g., Random Forest, Logistic Regression, Gradient Boosting) considering the nature of the problem (binary classification for award prediction) and dataset characteristics.
- Train the chosen classifier on the training dataset using selected features and the target label (movie winning an award).
- Evaluate the trained model's performance on the test dataset using appropriate evaluation metrics (e.g., accuracy, precision, recall, F1-score) to assess its predictive capabilities.
- Optimize the model's hyperparameters using techniques like grid search or random search to enhance performance.
- Employ k-fold cross-validation techniques to ensure robustness and validate the model's performance across different subsets of the data.

## Timeline Proposal

### Week 1: Data Preprocessing and Integration

- Gather CMU Movie Corpus Dataset, supplementary data, and additional features.
- Perform initial text cleaning, tokenization, and handle missing values in plot summaries.
- Check metadata completeness and begin feature engineering.

### Week 2: Feature Extraction and Initial Correlation Analysis (:round_pushpin: We are here)

- Finalize text cleaning, lemmatization, and handle stopwords.
- Complete feature extraction: keywords, tropes, and other defined features using NLP methods.
- Begin computing preliminary correlations among commercial success, cultural impact, and awards.

### Week 3: Deepened Correlation Analysis and Model Preparation

- Calculate comprehensive correlations between identified features and success metrics.
- Generate and refine initial visual representations for correlations.
- If applicable, initiate model development: prepare features and start model training.

### Week 4: Model Evaluation and Data Story Initiation

- Evaluate and refine the trained model's performance, conduct validation against test data.
- Continue enhancing visual representations for inclusion in the data story.
- Begin compiling project findings, insights, and visualizations into the initial structure of the data story.

### Week 5: Data Story Finalization and Presentation Preparation

- Complete the data story by incorporating project findings, insights, and refined visualizations.
- Review and validate the data story, ensuring it effectively communicates the project's objectives and outcomes.
- Prepare and rehearse the presentation to articulate project methodologies, findings, and conclusions effectively.

## Team Organisation

- Arumdhati and Simon will work on the NLP methods, feature extraction using LLMs, and classification (under consideration).
- Hans Kristian and Daniil will work on EDA, correlation metrics and classification (under consideration).
- German will work on the presentation

## Questions for TAs
