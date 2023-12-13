import pandas as pd
import numpy as np
import support

def get_imdb_dataset():
    imdb_title_basics = pd.read_csv('Data/imdb/title.basics.tsv', sep='\t')
    imdb_title_ratings = pd.read_csv('Data/imdb/title.ratings.tsv', sep='\t')
    imdb_df = pd.merge(left=imdb_title_basics, right=imdb_title_ratings, how='inner', on='tconst')

    # imdb_df = imdb_df[imdb_df['titleType'] == 'movie'].reset_index(drop=True)

    # Standardize nan-values
    imdb_df = support.standardize_nan(imdb_df)

    # imdb_df = imdb_df[~imdb_df['genres'].isna()].reset_index(drop=True)
    imdb_df['genres'] = imdb_df['genres'].apply(lambda x: str(x).split(',') if not pd.isna(x) else np.nan)

    imdb_df = imdb_df[['tconst', 'titleType', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'numVotes']]
    imdb_df.columns = ['imdb_id', 'title_type', 'movie_name', 'is_adult', 'release_year', 'runtime_minutes', 'genres', 'avg_rating', 'num_votes']

    return imdb_df

# Processed CMU Corpus Dataset 
def get_augmented_cmu():
    metadata_llm_df = pd.read_csv('Output/dataset_with_llm_features.csv')
    imdb_keys_df = pd.read_csv('Output/imdb_keys.csv')

    merge_df = pd.merge(left=metadata_llm_df, right=imdb_keys_df, how='inner', on=['movie_name', 'release_year'])
    merge_df = support.standardize_nan(merge_df)
    
    return merge_df


def get_awards_dataset():
    awards_df = pd.read_csv('Output/awards.csv')
    return awards_df