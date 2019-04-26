from scipy import spatial
import spacy
from profiler import timefunc

@timefunc
def load_language_resource(descriptor):
    print(spacy.info(vector_descriptor))
    nlp = spacy.load(vector_descriptor)
    return nlp

@timefunc
def word_vector_math(nlp, source, remove_word, add_word):
    man = nlp.vocab[source].vector
    woman = nlp.vocab[remove_word].vector
    queen = nlp.vocab[add_word].vector
    king = nlp.vocab['king'].vector
    
    # We now need to find the closest vector in the vocabulary to the result of "queen" - "woman" + "man" 
    maybe_king = queen - woman + man
    return maybe_king


@timefunc
def compute_word_vector_similarities(nlp, target_word):
    cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)
    
    computed_similarities = []
    
    for word in nlp.vocab:
        # Ignore words without vectors
        if not word.has_vector:
            continue
    
        similarity = cosine_similarity(target_word, word.vector)
        computed_similarities.append((word, similarity))
    
    computed_similarities = sorted(computed_similarities, key=lambda item: -item[1])
    return computed_similarities


if __name__ == "__main__":    
    vector_descriptor = 'en_core_web_md'
    nlp = load_language_resource(vector_descriptor)
    maybe_king = word_vector_math(nlp, 'queen', 'woman', 'man')
    computed_similarities = compute_word_vector_similarities(nlp, maybe_king)    
    print([w[0].text for w in computed_similarities[:10]])
    # ['Queen', 'QUEEN', 'queen', 'King', 'KING', 'king', 'KIng', 'KINGS', 'kings', 'Kings']


