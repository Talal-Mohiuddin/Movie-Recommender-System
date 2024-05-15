import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Search a Movie', movies['title'].values)


def fetch_poster(movie_title):
    api_key = "76b6f0267c4c8ebff5025853361149b0"
    response = requests.get('https://api.themoviedb.org/3/search/movie', params={'api_key': api_key, 'query': movie_title})
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    return None



def recommend(movie):
    movie_index = movies[movies['title'].str.lower() == movie.lower()].index
    if len(movie_index) == 0:
        return []
    movie_index = movie_index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    movies_poster = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_title)
        recommended_movies.append((movie_title))
        movies_poster.append((poster_url))
    return recommended_movies , movies_poster

   
if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    if recommendations:
        st.write('Recommended Movies:')
        num_columns = 3
        col1, col2, col3 = st.columns(num_columns)
        for i, movie in enumerate(recommendations):
            poster_url = posters[i]
            with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
                if poster_url:
                    st.image(poster_url, caption=movie, width=150)
                else:
                    st.write(movie)
    else:
        st.write('Movie not found.')




