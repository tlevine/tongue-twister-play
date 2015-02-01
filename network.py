from collections import Counter
import re

from twister import twister
import nltk

def get_twisters():
    stem = nltk.stem.PorterStemmer().stem
    for language, original, translation in twister():
        # Remove parantheses.
        cleaned_translation = re.sub(r'\([^)]*\)', '', translation)
        stems = list(map(stem, nltk.word_tokenize(cleaned_translation)))
        yield language, original, translation, stems

def main():
    twisters = get_twisters()
    scores = word_specialness_scores(twisters)

def dependencies():
    nltk.download('punkt')

def word_specialness_scores(twisters):
    'Determine how special each of the different word stems are.'
    counts = Counter()
    for _, _, _, stems in twisters:
        counts.update(stems)
        break
    return counts



#   scores[word]
twisters = get_twisters()
scores = word_specialness_scores(twisters)
