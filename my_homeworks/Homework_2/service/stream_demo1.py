import os
import random

import streamlit as st
import pandas as pd

@st.cache_data
def get_data_movie_final():
     return pd.read_csv('./data/clean_data/movie_emotion.csv')


st.set_page_config(layout="wide")
df_data = get_data_movie_final()
st.title('''Задание 2.1 \n ### Speaker + Emotions
         ''')

#Делаем визуализацию интерактивной плашки название фильма
st.sidebar.header('Select film to display')
movie_title = df_data['movie_title'].unique().tolist()
movie_title_selected = st.sidebar.multiselect('Movie title', movie_title)

#создаем маску с выбором фильма
mask_movie_title = df_data['movie_title'].isin(movie_title_selected)

#накладываем маску с выбором фильма
df_data_filtered = df_data[mask_movie_title]
# st.write(df_data_filtered)

#Делаем визуализацию интерактивной плашки имя персонажа
st.sidebar.header('Select dialog to display')
speaker_name = df_data_filtered['names'].unique().tolist()
speaker_name_selected = st.sidebar.multiselect('Speaker name', speaker_name)

#создаем маску с выбором перса
mask_speaker_name = df_data['names'].isin(speaker_name_selected)
#накладываем маску с выбором фильм
df_data_filtered1 = df_data[mask_speaker_name & mask_movie_title]
# st.write(df_data_filtered1)


#статистика по кину 
stat_film = df_data_filtered['emotion'].value_counts()
st.markdown("""
#### Таблица эмоций по фильму
""")
st.write(stat_film)

# статистика по персонажу
stat_speaker = df_data_filtered1['emotion'].value_counts()
st.markdown("""
#### Таблица эмоций по фильму и персонажу
""")
st.write(stat_speaker)

st.markdown("""
            Сырая таблица
            """)
st.write(df_data)