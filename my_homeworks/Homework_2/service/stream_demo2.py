import streamlit as st
import pandas as pd

# @st.cache_data
def get_data_movie_final():
     return pd.read_csv('./data/clean_data/movie_emotion.csv')


st.set_page_config(layout="wide")
df_data = get_data_movie_final()


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



st.title('Задание 2.2 \n ### 📚 Интерфейс для аннотации')


def convert(string):
    li = [item.split(',') for item in string]
    return li

st.write(
        """
        Выберите фильм и диалог!! - пока ошибка снизу
        """
    )
df_data = df_data_filtered1
data = df_data['replics'].to_list()
data = convert(data)

st.write("## Вы прекрасны, вот ваш диалог!", data[0])


# @st.cache_data
def data_updater():
    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "data" not in st.session_state:
        st.session_state.data = data[0].copy()
        st.session_state.current_text = st.session_state.data[1]
        st.session_state.prev_text = st.session_state.data[0]


data_updater()


def annotate(label):
    st.session_state.annotations[st.session_state.current_text] = label
    if st.session_state.data:
        st.session_state.prev_text = st.session_state.data[0]
        try:
            st.session_state.current_text = st.session_state.data[1]
        except IndexError:
            pass

        st.session_state.data.remove(st.session_state.prev_text)

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
        st.write('предыдущая реплика:', st.session_state.prev_text)
        st.write('Текущая реплика на оценку:', st.session_state.current_text)
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
