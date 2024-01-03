import streamlit as st
import pickle 
import requests

def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=328d518235eea0333cce47aeb8427674&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
indices = pickle.load(open("indices.pkl", 'rb'))
movies_list=movies['title_x'].values

st.header("My Movie Recommender System")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)


selectvalue = st.selectbox("select movie from dropdown", movies_list)



def get_recommendations(title, cosine_sim=similarity):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    recommend_movie=[]
    recommend_poster=[]
    
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    #movie_indices = [i[0] for i in sim_scores]
    for i in sim_scores:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie.append(movies.iloc[i[0]].title_x)
        recommend_poster.append(fetch_poster(movie_id))

    # Return the top 10 most similar movies
    return recommend_movie,  recommend_poster

if st.button("Show Recommend"):
        movie_name, movie_poster = get_recommendations(selectvalue)
        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10=st.columns(10)
        with col1:
            st.text(movie_name[0])
            st.image(movie_poster[0])
        with col2:
            st.text(movie_name[1])
            st.image(movie_poster[1])
        
        with col3:
            st.text(movie_name[2])
            st.image(movie_poster[2])
        
        with col4:
            st.text(movie_name[3])
            st.image(movie_poster[3])
        
        with col5:
            st.text(movie_name[4])
            st.image(movie_poster[4])
        
        with col6:
            st.text(movie_name[5])
            st.image(movie_poster[5])
        
        with col7:
            st.text(movie_name[6])
            st.image(movie_poster[6])

        with col8:
            st.text(movie_name[7])
            st.image(movie_poster[7])

        with col9:
            st.text(movie_name[8])
            st.image(movie_poster[8])

        with col10:
            st.text(movie_name[9])
            st.image(movie_poster[9])






