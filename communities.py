import pandas as pd
import itertools
import networkx as nx
import community as community_louvain
import matplotlib.cm as cm
import json
from gensim.utils import simple_preprocess
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# @Function return a dataframe with top_n genres per community
def community_top_n_genres(genre_community, top_n):
    # Group by 'community' and aggregate the top n genres for each community
    community_top_genres = (genre_community.drop(columns=['color']).groupby('community')
                                .apply(lambda group: group.nlargest(top_n, 'count'))
                                .reset_index(level=0, drop=True)
                                .reset_index())
    # Concatenate 'genre' & 'count'
    community_top_genres['genre_count'] = community_top_genres.apply(lambda x: f"{x['genres']} ({x['count']})", axis=1)
    # Generate dict from 
    top_n_dict = {}
    for c in set(community_top_genres['community']):    
        top_n_dict[f'community {c}'] = community_top_genres[community_top_genres['community'] == c]['genre_count'].to_list()
    return pd.DataFrame(top_n_dict)


# @Function topic modelling on community genres
def community_topic_detection(genre_community, lemmatizer, stop_words, num_topics):
    
    # Generate document for topic modelling from genre_community
    def generate_doc(genre_community, community):
        genres = genre_community[genre_community['community'] == community]['genres'].tolist()
        doc = ' '.join(genres).lower().replace('-', ' ')
        tokens = [word for word in simple_preprocess(doc) if word not in stop_words]
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
        
        return lemmatized_tokens
    
    # Create a doc for each community
    community_docs = {community: generate_doc(genre_community, community) for community in set(genre_community['community'].unique())}

    # Create a dictionary for each community
    community_dictionaries = {community: corpora.Dictionary([doc]) for community, doc in community_docs.items()}

    # Create a corpus for each community using the corresponding dictionary
    community_corpora = {community: community_dictionaries[community].doc2bow(doc) for community, doc in community_docs.items()}

    # Calculate TF weights for each term within each community
    tf_models = {community: models.TfidfModel([community_corpora[community]]) for community in community_corpora}
    tf_weighted_corpora = {community: tf_models[community][community_corpora[community]] for community in community_corpora}
    
    community_lda_models = {}
    for community, corpus in tf_weighted_corpora.items():
        dictionary = community_dictionaries[community]
        lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=15)
        community_lda_models[community] = lda_model

    # Now you can print the topics for each community
    for community, lda_model in community_lda_models.items():
        print(f"Community {community} topics:")
        for topic in lda_model.print_topics(num_words=10):
            print(topic)
    
    
# @Function compute probabilities for soft assignment
def community_soft_assignment(genre_to_community_dict, genres_list, movie_wikipedia_id):
    # Initialize counters for genre occurrences in communities
    community_counters = {community: 0 for community in set(genre_to_community_dict.values())}
    
    # Count the number of genres that map to each community
    for genre in genres_list:
        community = genre_to_community_dict.get(genre)
        if community is not None:
            community_counters[community] += 1
    
    # Total number of genres for the movie
    total_genres = len(genres_list)
    
    # Calculate probabilities for each community
    if total_genres > 0:  # Ensure we don't divide by zero
        prob_dict = {f'prob_c{community}': count / total_genres for community, count in community_counters.items()}
    else:
        prob_dict = {f'prob_c{community}': 0 for community in community_counters.keys()}
    
    prob_dict['movie_wikipedia_id'] = movie_wikipedia_id
    
    return prob_dict


    
