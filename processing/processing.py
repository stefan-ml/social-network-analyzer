import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer 

def convertToLower(data, field):
    data[field] = data[field].str.lower()
    return data


stopwords_list = stopwords.words('english')
from nltk.corpus import stopwords
", ".join(stopwords.words('english'))
STOPWORDS = set(stopwords.words('english'))
def cleaning_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

def applyCleaningStopwords(data, field):
    data[field] = data[field].apply(lambda text: cleaning_stopwords(text))
    return data

english_punctuations = string.punctuation
punctuations_list = english_punctuations
def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)

def applyCleaningPuntation(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_punctuations(x))
    return data


def cleaning_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)

def applyCleaningRepeatingChar(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_repeating_char(x))
    return data

def cleaning_email(data):
    return re.sub('@[^\s]+', ' ', data)

def applyCleaningEmail(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_email(x))
    return data

def cleaning_URLs(data):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',data)

def applyCleaningURLs(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_URLs(x))
    return data


def cleaning_numbers(data):
    return re.sub('[0-9]+', '', data)

def applyCleaningNumbers(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_numbers(x))
    return data

tokenizer = RegexpTokenizer(r'\w+')
def applyTokenizer(data, field = "text"):
    data[field] = data[field].apply(tokenizer.tokenize)
    return data

st = nltk.PorterStemmer()
def stemming_on_text(data):
    text = [st.stem(word) for word in data]
    return data

def applyStemming(data, field = "text"):
    data[field] = data[field].apply(lambda x: stemming_on_text(x))
    return data

lm = nltk.WordNetLemmatizer()
def lemmatizer_on_text(data):
    text = [lm.lemmatize(word) for word in data]
    return data

def applyLemmatizer(data, field = "text"):
    data[field] = data[field].apply(lambda x: lemmatizer_on_text(x))
    return data

def applyPreprocessing(data, field = "text"):
    data = convertToLower(data, field)
    data = applyCleaningStopwords(data, field)
    data = applyCleaningPuntation(data, field)
    data = applyCleaningRepeatingChar(data, field)
    data = applyCleaningEmail(data, field)
    data = applyCleaningURLs(data, field)
    data = applyCleaningNumbers(data, field)
    data = applyTokenizer(data, field)
    data = applyStemming(data, field)
    data = applyLemmatizer(data, field)
    return data