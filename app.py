
import pickle

import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    # api_key = 'ef0d13ddc5f900c422a3007a1a37ecfa'
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ef0d13ddc5f900c422a3007a1a37ecfa&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key = lambda x: x[1])

    recommended_movies =[]
    recommendation_movies_poster =[]

    # we will keep only 5 recommended movie
    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API using movie_id
        recommendation_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommendation_movies_poster



# loading the files from collab after preprocessing
movies_list = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))

# Display app title
st.title("Movie Recommender System ")
st.markdown('<p class="subtitle">Find movies similar to your favorite ones!</p>', unsafe_allow_html=True)


# Movie selection dropdown
selected_movie = st.selectbox(
    "📽️ Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])