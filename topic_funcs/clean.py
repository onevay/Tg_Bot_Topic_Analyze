from nltk.corpus import stopwords
import nltk
from pymystem3 import Mystem
from topic_funcs.censor import remove_russian_mat

def punctions_del(st):
    punctions = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~1234567890"
    for i in range(len(st)):
        if(i >= len(st)):
            break
        if st[i] in punctions:
            st = st[:i] + st[i + 1:]
    return st

def mstem(st):
    m = Mystem()
    return m.lemmatize(st)

nltk.download('stopwords')
stop_words = stopwords.words('russian')

def cleaning_and_normalize(lst):
    words = list(word for word in lst if word not in stop_words)
    words = remove_russian_mat(words)
    return words