import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

def fetch_poster(movie_id):
    # PUT API KEY
    res = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?<<API>>')
    data = res.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Load data
similarity = pickle.load(open('simi.pkl', 'rb'))
movies_dict = pickle.load(open('mov_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# App title
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Movie selector
st.markdown("### Select a movie to get recommendations:")
selected_movie_name = st.selectbox("", movies['title'].values)

# Submit button
if st.button('Submit'):
    st.markdown("### Top 5 Recommended Movies:")
    st.markdown("<br>", unsafe_allow_html=True)

    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.markdown(f"<div style='text-align: center; margin-top: 10px; font-weight: bold;'>{names[i]}</div>", unsafe_allow_html=True)
