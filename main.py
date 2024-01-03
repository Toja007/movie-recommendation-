#importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#Loading data
df_1 = pd.read_csv('credits.csv')
df_2 = pd. read_csv('movies_1.csv')

print('df_1 shape:',df_1.shape)
print('df_2 shape:',df_2.shape)

df_1.head()
df_2.head()

# renaming 'id' column in df_2 to match the its equivalent in df_1
df_2 = df_2.rename(columns={'id': 'movie_id'})

# merging df_1 and df_2 
movies = df_1.merge(df_2, on='movie_id')
movies.head()
print('movies shape:',movies.shape)


# getting info
movies.info()

movies.isnull().sum()

#recommendation based on movie overview
# instanciating TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
# dealing with null values in overview column
movies['overview'] = movies['overview'].fillna('')
# fitting feature into vectorizer
tfidf_matrix = tfidf.fit_transform(movies['overview'])

# Output the shape of tfidf_matrix
tfidf_matrix.shape

# getting vector similarities
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#Construct a reverse map of indices and movie titles
indices = pd.Series(movies.index, index=movies['title_x']).drop_duplicates()

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    
    for i in sim_scores:
        print(movies.iloc[i[0]].title_x)

get_recommendations('The Dark Knight Rises')

get_recommendations('The Avengers')

#Recommending based on slected features
# Feature selection
features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    movies[feature] = movies[feature].apply(literal_eval)
# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan
# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []
# Define new director, cast, genres and keywords features that are in a suitable form.
movies['director'] = movies['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    movies[feature] = movies[feature].apply(get_list)

movies[['title_x', 'cast', 'director', 'keywords', 'genres']].head(3)

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
# Apply clean_data function to your features.
features = ['movie_id', 'cast', 'keywords', 'director', 'genres']

for feature in features:
    movies[feature] = movies[feature].apply(clean_data)
# creating a soup
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
movies['soup'] = movies.apply(create_soup, axis=1)
# instanciating and fiting soup
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(movies['soup'])

# finding similarities
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
# Reset index of our main DataFrame and construct reverse mapping as before
movies =movies.reset_index()
indices = pd.Series(movies.index, index=movies['title_x'])
results = movies.iloc[indices].iloc[::-1]
get_recommendations('The Dark Knight Rises', cosine_sim=cosine_sim2)

pickle.dump(movies, open('movies_list.pkl', 'wb'))
pickle.dump(cosine_sim2, open('similarity.pkl', 'wb'))
pickle.dump(indices, open('indices.pkl', 'wb'))