from nltk.classify import apply_features
from nltk.corpus import names
import nltk
import random
from itertools import groupby

from xml.etree import ElementTree
import pandas as pd

class DialogActFeatureExtractor(object):

    def bag_of_words(self, post):
        bag_of_words = {}
        for word in nltk.word_tokenize(post):
            bag_of_words[f'contains({word.lower()})'] = True
        return bag_of_words

    def features(self, post, history):
        features = {}
        # attach bag of words
        contained_words = self.bag_of_words(post)
        features = {**features, **contained_words}
        # attach previous dialog act

        return features


class DialogActData(object):
    def __init__(self, feature_extractor):
        self._feature_extractor = feature_extractor

    


def dialogue_act_features(post):
     features = {}
     for word in nltk.word_tokenize(post):
         features['contains({})'.format(word.lower())] = True
         return features

if __name__ == "__main__":
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    print(ElementTree.tostring(posts[0]).decode())

    users = map(lambda x: x.get('user'), posts)
    classes = map(lambda x: x.get('class'), posts)
    utterances = map(lambda x: x.text, posts)

    data = {
        'User': pd.Series(users),
        'Class': pd.Series(classes),
        'Utterance': pd.Series(utterances)
    }

    df = pd.DataFrame(data)
    print(data['User'].value_counts())
    # exit()

    for post in posts[0:500]:
        print(f"POST: {post.text} - DIALOG ACT: {post.get('class')}")
    exit()

    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))