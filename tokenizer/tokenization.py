import pickle
from keras.preprocessing.text import Tokenizer



def createTokenizer(data,nameOfFile,num_words = 2000):
    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(data)
    with open(nameOfFile, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return tokenizer

def getTokenizer(nameOfFile):
    with open(nameOfFile, 'rb') as handle:
        return pickle.load(handle)
