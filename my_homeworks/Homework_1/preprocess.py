'''
Предобработка
'''
import re
import string
import pandas as pd
import nltk
import subprocess
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from dvc.api import DVCFileSystem

stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()
stopword = set(stopwords.words('english'))
stopword.update(['user', 'peopl', 'dont', 'fuck', 'im'])


def clean_text(text):
    '''
    Регулярка + стоп-слова + стеммер + лемматизатор
    '''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    text = " ".join(text)
    return text


def count(label):
    '''
    Порог для классификатора
    '''
    if label > 0.4:
        return 1
    return 0


def load_data():
    '''
    Загрузка данных и предобработка
    '''
    subprocess.run(['dvc', 'pull'])
    df_pd = pd.read_csv('data/Ethos_Dataset_Binary.csv', delimiter=';')
    df_pd.rename(columns={'isHate': 'label'}, inplace=True)
    df_pd.loc[:, 'label'] = df_pd.label.apply(count)
    df_pd['comment'] = df_pd['comment'].apply(clean_text)

    return df_pd
