from flair.data import Sentence
from flair.models import SequenceTagger
from drugdiscovery.postprocessing import DuplicateRemover, PairFormer


class TwinClassifier:
    """
    Uses two FLAIR classifiers to run the classification and post-
    processing parts of the pipeline. One standard "NER" model
    classifies all medical terms, while another disease-only model
    recognizes only diseases. We form pairs and then purge pairs
    of diseases to get rid of at least some false positives.
    """

    def __init__(self, disease_dir='../ner/models/v1', ner_dir='../ner/models/v1/'):
        """
        Initializes the twin classifier model
        :param disease_dir: The path to the trained disease-only model
        :param ner_dir: The path to the trained regular model
        """
        self.ner_model = SequenceTagger.load(ner_dir + 'best-model.pt')
        self.disease_model = SequenceTagger.load(disease_dir + 'best-model.pt')

    def classify(self, sentences: list) -> list:
        """
        Classifies a list of sentences, returning pairs.
        :return List of pairs.
        """
        results = []  # classification results from NER model
        diseases = []  # classification results from disease-only model

        final_pairs = []  # final pairs (this is returned)

        for sentence in sentences:
            # Process the regular NER first
            flair_sentence = Sentence(sentence)
            self.ner_model.predict(flair_sentence)

            tokens = [token.text for token in flair_sentence.get_spans('ner') if token.tag == 'Entity']
            results.append(tokens)

            # Now the disease-only part
            flair_sentence = Sentence(sentence)
            self.disease_model.predict(flair_sentence)

            tokens = [token.text for token in flair_sentence.get_spans('ner') if token.tag == 'Disease']
            diseases.append(tokens)

        # Run post-processing
        deduper = DuplicateRemover(results)
        deduped = deduper.remove()

        pf = PairFormer(deduped)
        pairs = pf.pair()

        # Get medical terms
        diseases = [item for sublist in diseases for item in sublist]
        diseases = list(set(diseases))

        for pair in pairs:
            # Check if both are diseases
            if pair[0] in diseases and pair[1] in diseases:
                continue

            # Or if both are not diseases
            if pair[0] not in diseases and pair[1] not in diseases:
                continue

            final_pairs.append(pair)

        return final_pairs
