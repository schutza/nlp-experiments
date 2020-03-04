import spacy


NLP = {
    'en': spacy.load('en_core_web_sm'),
    'de': spacy.load('de_core_news_sm')
}