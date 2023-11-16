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

## Methods

### Step 1: Data Preprocessing

### Step 2: Feature Extraction

#### Using native Python packages

- Key_Words: Use a named entity recognition (NER) or keyword extraction task to identify key words or phrases from the plot summary. This could be a list or a frequency count of significant words. Extracting key themes or words that frequently appear in plot. For example, certain themes like 'love', 'war', 'adventure' might be more prevalent in higher-grossing movies. This column can be in form of comma-separated keywords, or the main keyword

- 


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
