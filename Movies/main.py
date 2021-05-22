import csv
import re
from string import punctuation

import requests
import csv
import pickle
import nltk
from nltk import word_tokenize

#nltk.download('movie_reviews')
from nltk.corpus import movie_reviews, stopwords

imdb = "C:/Users/JAASWIN D KOTIAN/PycharmProjects/Movie_analysis/Movies/Imdb.csv"

# Now we write them to the empty CSV file
corpus = []
with open(imdb, 'rt',encoding='utf8') as csvfile:
    lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
    for row in lineReader:
        corpus.append({"label": row[1], "text": row[0]})

trainingDataSet = []

for i,j in zip(corpus,range(len(corpus))):
    try:
        i['id'] = j
        i['text'] = i['text']
        trainingDataSet.append(i)
    except:
        print("Error while fetching")

#print(trainingDataSet[0])

def build_test_set(keyword):
    url = "https://imdb8.p.rapidapi.com/title/get-user-reviews"
    url1 = "https://imdb8.p.rapidapi.com/title/auto-complete"
    querystring1 = {"q": str(keyword)}
    headers = {
        'x-rapidapi-key': "1a7f74979cmsh0afbb5dc9f14367p100610jsn8db2e6ad11e1",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }
    response1 = requests.request("GET", url1, headers=headers, params=querystring1).json()
    id = response1['d'][0]['id']
    querystring = {"tconst": str(id)}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    reviews = []
    for i in range(0, len(response['reviews'])):
        reviews.append({'text': response['reviews'][i]['reviewText'], 'label': None})
    return reviews


#search_term = input("Enter the Movie : ")
#test_data_set = build_test_set(search_term)
#print(test_data_set)
print("Testset prepared...")

class PreprocessTexts:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation))

    def process_texts(self, list_of_texts):
        processed_tweets = []
        for text in list_of_texts:
            if text["label"] is not None:
                if text["label"] == "positive" or text["label"] == "negative":
                    processed_tweets.append((self._process_text(text["text"]), text["label"]))
            else:
                processed_tweets.append((self._process_text(text["text"]), None))

        return processed_tweets

    def _process_text(self, tweet):
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)

        words = []
        for word in tweet:
            if word not in self._stopwords:
                words.append(word)
        return words


text_processor = PreprocessTexts()
preprocessed_training_set = text_processor.process_texts(trainingDataSet)
#preprocessed_test_set = text_processor.process_texts(test_data_set)
print("Processed...")



def build_vocabulary(preprocessed_training_data):
    all_words = []

    for (words, sentiment) in preprocessed_training_data:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()

    return word_features


training_data_features = build_vocabulary(preprocessed_training_set)


def extract_features(text):
    text_words = set(text)
    features = {}
    for word in training_data_features:
        is_feature_in_words = word in text_words
        features[word] = is_feature_in_words
    return features


training_features = nltk.classify.apply_features(extract_features, preprocessed_training_set)
print("Features extracted...")

#NBayesClassifier = nltk.NaiveBayesClassifier.train(training_features)


f = open('C:/Users/JAASWIN D KOTIAN/PycharmProjects/Movie_analysis/Movies/my_classifier.pickle', 'rb')
NBayesClassifier = pickle.load(f)
f.close()


#print(predict(search_term))

