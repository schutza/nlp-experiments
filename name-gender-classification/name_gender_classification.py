from nltk.classify import apply_features
from nltk.corpus import names
import nltk
import random


class NameGenderFeatureExtractor(object):
    def number_of_vowels(self, word):
        return sum(letter in 'aeiou' for letter in word.lower())

    def features(self, word):
        return {
            'suffix_1': word[-1:],
            'suffix_2': word[-2:],
            # 'name_length': len(word),
            # 'first_letter': word[0],
            # 'number_of_vowels': self.number_of_vowels(word),
            # 'ratio_vowels': self.number_of_vowels(word) / len(word)
        }

class NameGenderData(object):
    def __init__(self, feature_extractor):
        self._feature_extractor = feature_extractor
        self._labeled_names = self._label_names()

    def _label_names(self):
        from nltk.corpus import names
        labeled_names = ([(name, 'male') for name in names.words('male.txt')] 
            + [(name, 'female') for name in names.words('female.txt')])
        import random
        random.shuffle(labeled_names)
        print(f'labeled_names: {len(labeled_names)} elements')

        return labeled_names

    def split_train_devtest_test_set(self):
        train_names = self._labeled_names[1500:]
        devtest_names = random.sample(self._labeled_names[500:1500], 100)
        test_names = self._labeled_names[:500]

        train_set = [(self._feature_extractor.features(n), gender) for (n, gender) in train_names]
        devtest_set = [(self._feature_extractor.features(n), gender) for (n, gender) in devtest_names]
        test_set = [(self._feature_extractor.features(n), gender) for (n, gender) in test_names]

        return {
            'train': (train_names, train_set),
            'devtest': (devtest_names, devtest_set),
            'test': (test_names, test_set)
        }

    def evaluate(self, classifier, devtest_set):
        accuracy = nltk.classify.accuracy(classifier, devtest_set)
        print(f'Accuracy: {accuracy}')
        classifier.show_most_informative_features(10)

    def error_analysis(self, classifier, devtest_set):
        errors = []
        for (name, tag) in devtest_set:
            guess = classifier.classify(self._feature_extractor.features(name))
            if guess != tag:
                errors.append( (tag, guess, name) )
        for (tag, guess, name) in sorted(errors):
            print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))




if __name__ == "__main__":
    my_test_names = ['Neo', 'Trinity']

    feature_extractor = NameGenderFeatureExtractor()
    # for name in my_test_names:
    #     print(feature_extractor.features(name))
    # exit()

    data_prep = NameGenderData(feature_extractor)
    split_sets = data_prep.split_train_devtest_test_set()
    train_names, train_set = split_sets['train']
    devtest_names, devtest_set = split_sets['devtest']
    test_names, test_set = split_sets['test']

    classifier = nltk.NaiveBayesClassifier.train(train_set)

    for name in my_test_names:
        print(f'Classification for [{name}]: {classifier.classify(feature_extractor.features(name))}')

    data_prep.evaluate(classifier, devtest_set)
    data_prep.error_analysis(classifier, devtest_names)
