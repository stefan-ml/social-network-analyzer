import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer 

# Konverzija svih slova u tekstu u mala slova
def convertToLower(data, field):
    data[field] = data[field].str.lower()  # Konvertuje sve karaktere u mala slova
    return data

# Uvoz liste stop reči (reči koje se često koriste, ali ne doprinose mnogo smislu, npr. "and", "the")
stopwords_list = stopwords.words('english')
from nltk.corpus import stopwords
", ".join(stopwords.words('english'))
STOPWORDS = set(stopwords.words('english'))  # Set stop reči za engleski jezik

# Brisanje stop reči iz teksta
def cleaning_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])  # Zadržava samo reči koje nisu stop reči

# Iteracija kroz DataFrame i brisanje stop reči iz tekstualnog polja
def applyCleaningStopwords(data, field):
    data[field] = data[field].apply(lambda text: cleaning_stopwords(text))  # Primena funkcije za brisanje stop reči
    return data

english_punctuations = string.punctuation
punctuations_list = english_punctuations
# Brisanje znakova interpunkcije iz teksta
def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)  # Translator za brisanje znakova interpunkcije
    return text.translate(translator)  # Primena translatora na tekst

# Iteracija kroz DataFrame i brisanje znakova interpunkcije iz tekstualnog polja
def applyCleaningPuntation(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_punctuations(x))  # Primena funkcije za brisanje znakova interpunkcije
    return data

# Uklanjanje ponavljajućih karaktera (npr. "hellooo" postaje "helo")
def cleaning_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)  # Zamena ponavljajućih karaktera jednim

# Iteracija kroz DataFrame i uklanjanje ponavljajućih karaktera iz tekstualnog polja
def applyCleaningRepeatingChar(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_repeating_char(x))  # Primena funkcije za uklanjanje ponavljajućih karaktera
    return data

# Brisanje email adresa iz teksta
def cleaning_email(data):
    return re.sub('@[^\s]+', ' ', data)  # Zamena email adresa sa praznim prostorom

# Iteracija kroz DataFrame i brisanje email adresa iz tekstualnog polja
def applyCleaningEmail(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_email(x))  # Primena funkcije za brisanje email adresa
    return data

# Brisanje URL adresa iz teksta
def cleaning_URLs(data):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',data)  # Zamena URL adresa sa praznim prostorom

# Iteracija kroz DataFrame i brisanje URL adresa iz tekstualnog polja
def applyCleaningURLs(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_URLs(x))  # Primena funkcije za brisanje URL adresa
    return data

# Brisanje brojeva iz teksta
def cleaning_numbers(data):
    return re.sub('[0-9]+', '', data)  # Zamena brojeva sa praznim prostorom

# Iteracija kroz DataFrame i brisanje brojeva iz tekstualnog polja
def applyCleaningNumbers(data, field = "text"):
    data[field] = data[field].apply(lambda x: cleaning_numbers(x))  # Primena funkcije za brisanje brojeva
    return data

# Tokenizacija teksta (razdvajanje teksta na reči)
tokenizer = RegexpTokenizer(r'\w+')
def applyTokenizer(data, field = "text"):
    data[field] = data[field].apply(tokenizer.tokenize)  # Primena tokenizacije na tekst
    return data

# Stemovanje teksta (smanjivanje reči na njihov osnovni oblik, npr. "running" postaje "run")
st = nltk.PorterStemmer()
def stemming_on_text(data):
    text = [st.stem(word) for word in data]  # Primena stemovanja na svaku reč u tekstu
    return data

# Iteracija kroz DataFrame i stemovanje teksta
def applyStemming(data, field = "text"):
    data[field] = data[field].apply(lambda x: stemming_on_text(x))  # Primena funkcije za stemovanje teksta
    return data

# Lematizacija teksta (smanjivanje reči na njihov osnovni oblik, npr. "better" postaje "good")
lm = nltk.WordNetLemmatizer()
def lemmatizer_on_text(data):
    text = [lm.lemmatize(word) for word in data]  # Primena lematizacije na svaku reč u tekstu
    return data

# Iteracija kroz DataFrame i lematizacija teksta
def applyLemmatizer(data, field = "text"):
    data[field] = data[field].apply(lambda x: lemmatizer_on_text(x))  # Primena funkcije za lematizaciju teksta
    return data

# Preprocesiranje teksta u oblik pogodan za dalju analizu
def applyPreprocessing(data, field = "text"):
    data = convertToLower(data, field)  # Konverzija svih slova u mala slova
    data = applyCleaningStopwords(data, field)  # Brisanje stop reči
    data = applyCleaningPuntation(data, field)  # Brisanje znakova interpunkcije
    data = applyCleaningRepeatingChar(data, field)  # Uklanjanje ponavljajućih karaktera
    data = applyCleaningEmail(data, field)  # Brisanje email adresa
    data = applyCleaningURLs(data, field)  # Brisanje URL adresa
    data = applyCleaningNumbers(data, field)  # Brisanje brojeva
    data = applyTokenizer(data, field)  # Tokenizacija teksta
    data = applyStemming(data, field)  # Stemovanje teksta
    data = applyLemmatizer(data, field)  # Lematizacija teksta
    return data 
