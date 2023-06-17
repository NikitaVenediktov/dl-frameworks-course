import os
import random

import streamlit as st
import pandas as pd

@st.cache
def get_data_movie_final():
     return pd.read_csv('./data/clean_data/movie_final.csv')


st.set_page_config(layout="wide")
df_data = get_data_movie_final()
st.title('Nikitas Project)))')
st.markdown("""
lol kek jeburek
""")
# st.write(df_data)

#Делаем визуализацию интерактивной плашки название фильма
st.sidebar.header('Select film to display')
movie_title = df_data['movie_title'].unique().tolist()
movie_title_selected = st.sidebar.multiselect('Movie title', movie_title)

#создаем маску с выбором фильма
mask_movie_title = df_data['movie_title'].isin(movie_title_selected)

#накладываем маску с выбором фильма
df_data_filtered = df_data[mask_movie_title]
st.write(df_data_filtered)

#Делаем визуализацию интерактивной плашки имя персонажа
st.sidebar.header('Select speaker to display')
speaker_name = df_data_filtered['names'].unique().tolist()
speaker_name_selected = st.sidebar.multiselect('Speaker name', speaker_name)

#создаем маску с выбором перса
mask_speaker_name = df_data['names'].isin(speaker_name_selected)
#накладываем маску с выбором фильм
df_data_filtered1 = df_data[mask_speaker_name & mask_movie_title]
st.title(print(mask_speaker_name))
if df_data_filtered1 is None:
    st.write(df_data_filtered)
else:
    st.write(df_data_filtered1)

st.write



def show():
    st.write(
        """
        ## 📚 Text Annotation

        Welcome to the text annotation tool! Label some text and all of your
        annotations will be preserved in `st.session_state`!
        """
    )

    data = [
        "I love this movie! It's so entertaining.",
        "This book is boring and poorly written.",
        "The food at that restaurant was delicious.",
        "I had a terrible experience with their customer service.",
        "The weather today is perfect for outdoor activities.",
    ]

    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "data" not in st.session_state:
        st.session_state.data = data.copy()
        st.session_state.current_text = data[0]

    def annotate(label):
        st.session_state.annotations[st.session_state.current_text] = label
        if st.session_state.data:
            st.session_state.current_text = random.choice(st.session_state.data)
            st.session_state.data.remove(st.session_state.current_text)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.data:
            st.write(
                "Annotated:",
                len(st.session_state.annotations),
                "– Remaining:",
                len(st.session_state.data),
            )
            st.write("### Text")
            st.write(st.session_state.current_text)
            st.button("Positive 😄", on_click=annotate, args=("positive",))
            st.button("Negative 😞", on_click=annotate, args=("negative",))
            st.button("Neutral 😐", on_click=annotate, args=("neutral",))
        else:
            st.success(
                f"🎉 Done! All {len(st.session_state.annotations)} texts annotated."
            )
    with col2:
        st.write("### Annotations")
        st.write(st.session_state.annotations)


if __name__ == "__main__":
    show()