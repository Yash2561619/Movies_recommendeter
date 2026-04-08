import pickle
import pandas as pd
import streamlit as st
import requests
import os


# --- HELPER FUNCTIONS ---

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    try:
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        # Fallback image if the API fails or poster is missing
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movies_id))
    return recommended_movie, recommended_movie_posters


# --- DATA LOADING ---

# This ensures the app looks in the same folder as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_path = os.path.join(BASE_DIR, 'movies_dict.pkl')
similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')

# Load files with error handling
try:
    movies_dict = pickle.load(open(movies_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open(similarity_path, 'rb'))
except FileNotFoundError:
    st.error(
        f"Error: Could not find model files at {BASE_DIR}. Ensure movies_dict.pkl and similarity.pkl are uploaded.")
    st.stop()
except Exception as e:
    st.error("Error loading model files. If using Git LFS, ensure 'packages.txt' contains 'git-lfs'.")
    st.stop()

# --- STREAMLIT UI ---

st.title("Movies Recommendation System")

selected_movie_name = st.selectbox("Select Movie", movies['title'].values)

if st.button("Recommend"):
    recommended_movie, recommended_movie_posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for index, col in enumerate(cols):
        with col:
            st.text(recommended_movie[index])
            st.image(recommended_movie_posters[index])