from collections import Counter, defaultdict
import re

from twister import twister
import nltk

def get_twisters():
    stem = nltk.stem.PorterStemmer().stem
    for language, original, translation in twister():
        # Remove parantheses.
        if translation != None:
            cleaned_translation = re.sub(r'\([^)]*\)', '', translation)
            stopwords = nltk.corpus.stopwords.words()
            stems = [stem(word.lower()) for word in nltk.word_tokenize(cleaned_translation) if word not in stopwords]
            yield language, original, translation, stems

def build_network():
    twisters = list(get_twisters())
    linking_words = get_linking_words(twisters)

    twisters_data = twisters_dict(twisters)
    stem_twisters = defaultdict(set)
    for _, original, _, stems in twisters:
        for stem in stems:
            if stem in linking_words:
                stem_twisters[stem].add(original)
                twisters_data[original]['linking_words'].add(stem)

    network = stem_twisters, twisters_data
    return network

def query_network(network, twister_original):
    stem_twisters, twisters_data = network
    for linking_word in twisters_data[twister_original]['linking_words']:
        for twister in stem_twisters[linking_word]:
            yield twisters_data[twister]

def get_linking_words(twisters):
    counts = word_counts(twisters)
    filtered_counts = {k:v for k,v in counts.items() if v > 1 and v < 110}
    return set(filtered_counts.keys())

def twisters_dict(twisters):
    x = {}
    for language, original, translation, stems in twisters:
        x[original] = {
            'language': language,
            'original': original,
            'translation': translation,
            'linking_words': set(),
        }
    return x 

def dependencies():
    nltk.download('punkt')
    nltk.download('stopwords')

def word_counts(twisters):
    'Determine how special each of the different word stems are.'
    counts = Counter()
    for _, _, _, stems in twisters:
        counts.update(stems)
    return counts

def sorted_counts(counts):
    'Use this to calibrate the removal of junk.'
    remove_ones = filter(lambda pair: pair[1] > 1, counts.items())
    return sorted(remove_ones, key = lambda pair: pair[1])
