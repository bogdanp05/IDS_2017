import nltk
from nltk.corpus import gutenberg
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from numpy import unique
import config as cfg
import csv
import operator
import time

#Run just once
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

path = cfg.path
wnl = WordNetLemmatizer()

#Book Titles
titles = gutenberg.fileids()

#List of stopwords
stopwords = stopwords.words('english')


##  TEXT PREPROCESING
# Lemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

#Punctuation
punctuation = string.punctuation+'``'+'--'+"''"

time_start = time.clock()

#Case Fold, Lemmatize, Punctuation, Stopwords
def cleaning(book):
    text = str(book).split('u')
    
    output = []
    for item in book:
        #remove punctuation
        #remove stopwords
        if item not in punctuation and item.lower() not in stopwords and len(item)>1:
            #there are also combined punctuation as "!--"
            if any(punct in punctuation for punct in item) == 0:
                #case fold -> lemmatize --> tokenize
                word = word_tokenize(wordnet_lemmatizer.lemmatize(item.lower()))
                output.append(word[0].encode('utf-8'))
    return output

#TEST
for title in titles:
    book = gutenberg.words(title)
    cleaned = cleaning(book)
    print(title)
    print("Length before cleaning: \t" + str(len(book)) )
    print("Length after cleaning: \t" + str(len(cleaned)) )
