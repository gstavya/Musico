import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from app import db

def get_genres():
    doc = db.collection('gstavya').document('music').get()
    data = doc.to_dict()
    array = data.get('genre', [])
    tot = ""
    for i in array:
        tot += i
        tot += " "
    return tot

wc = WordCloud().generate(get_genres())
plt.imshow(wc)