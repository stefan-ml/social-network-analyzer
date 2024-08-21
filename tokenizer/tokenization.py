import pickle
from keras.preprocessing.text import Tokenizer

# Funkcija za kreiranje i čuvanje Tokenizer objekta
def createTokenizer(data, nameOfFile, num_words = 2000):
    tokenizer = Tokenizer(num_words=num_words)  # Kreira Tokenizer objekat koji će raditi sa najviše 2000 reči
    tokenizer.fit_on_texts(data)  # Trening tokenizera na osnovu teksta u 'data', kreira rečnik reči
    with open(nameOfFile, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)  # Serijalizuje (čuva) tokenizer objekat u fajl koristeći pickle
    return tokenizer  # Vraća kreirani tokenizer

# Funkcija za učitavanje već sačuvanog Tokenizer objekta iz fajla
def getTokenizer(nameOfFile):
    with open(nameOfFile, 'rb') as handle:
        return pickle.load(handle)  # Učitava i vraća prethodno sačuvan tokenizer objekat iz fajla
