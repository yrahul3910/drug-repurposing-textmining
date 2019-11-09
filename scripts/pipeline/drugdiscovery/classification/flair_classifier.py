from flair.data import Sentence
from flair.models import SequenceTagger


class FlairClassifier:
    """
    Runs Named Entity Recognition (NER) using FLAIR.
    """
    def __init__(self):
        pass

    def classify(self, sentences: list) -> list:
        """
        Classifies a list of sentences, returning NER results.
        :return List of medical term strings
        """
        results = []

        tagger = SequenceTagger.load('pos')
        for sentence in sentences:
            tokens = []
            flair_sentence = Sentence(sentence)
            tagger.predict(flair_sentence)

            for token in flair_sentence.get_spans('pos'):
                if token.tag == 'NOUN':
                    tokens.append(token.text)

            results.append(tokens)

        return results
