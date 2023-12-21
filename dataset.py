import pandas as pd
import numpy as np
import support
import os

def load_dataset(path):
    df = pd.read_csv(path)
    df = support.standardize_nan(df)
    return df


def concatenate_folder(root):
    df_list = []
    for file in os.listdir(root):
        if str(file).endswith('.xlsx'):
            tmp = pd.read_excel(root + file)
        elif str(file).endswith('.csv'):
            tmp = pd.read_csv(root + file)
        if tmp is not None:
            df_list.append(tmp)
    
    concat_df = pd.concat(df_list, axis=0).drop(columns=['Unnamed: 0']).drop_duplicates().reset_index(drop=True)
    concat_df = support.standardize_nan(concat_df)
    return concat_df


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
    imdb_keys_df = concatenate_folder('Output/imdb/')

    merge_df = pd.merge(left=metadata_llm_df, right=imdb_keys_df, how='inner', on=['movie_name', 'release_year'])
    merge_df = support.standardize_nan(merge_df)
    merge_df = merge_df.drop(columns=['Unnamed: 0'])
    merge_df = merge_df[merge_df['release_year'] <= 2012]
    
    return merge_df


def get_boxofficemojo_dataset():
    boxofficemojo = concatenate_folder('Output/boxofficemojo/')
    boxofficemojo = boxofficemojo[~(boxofficemojo['budget'].isna()) |
                            ~(boxofficemojo['performance_domestic'].isna()) |
                            ~(boxofficemojo['performance_international'].isna()) |
                            ~(boxofficemojo['performance_worldwide'].isna()) |
                            ~(boxofficemojo['domestic_distributor'].isna()) | 
                            ~(boxofficemojo['domestic_opening'].isna()) | 
                            ~(boxofficemojo['releases'].isna())]
    boxofficemojo = boxofficemojo.drop(columns=['source_url'])
    return boxofficemojo

def get_rottentomatoes_dataset():
    df = concatenate_folder('Output/tomato_scores/')
    df = df.replace(0, np.nan)
    return df