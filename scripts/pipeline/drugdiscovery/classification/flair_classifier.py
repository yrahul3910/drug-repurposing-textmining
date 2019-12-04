from flair.data import Sentence
from flair.models import SequenceTagger
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import TokenEmbeddings, StackedEmbeddings, PooledFlairEmbeddings, ELMoEmbeddings
from flair.trainers import ModelTrainer
from typing import List


class FlairClassifier:
    """
    Runs Named Entity Recognition (NER) using FLAIR.
    """

    def __init__(self, save_dir='../ner/models/v1/'):
        self.save_dir = save_dir

    def train(self, dataset: str = 'bc5cdr', bs: int = 4, lr: float = 0.1, epochs: int = 150) -> None:
        """
        Trains the model. Code adapted from https://github.com/shreyashub/BioFLAIR.
        :param dataset - The dataset to train on. Must be present in the data/ folder.
        :param bs - The batch size to use.
        :param lr - The learning rate to use.
        :param epochs - The maximum number of epochs to run for.
        :return: None
        """
        columns = {0: 'text', 3: 'ner'}

        # this is the folder in which train, test and dev files reside
        data_folder = '../data/ner/' + dataset

        # init a corpus using column format, data folder and the names of the train, dev and test files
        corpus: Corpus = ColumnCorpus(data_folder, columns,
                                      train_file='train.txt',
                                      test_file='test.txt',
                                      dev_file='dev.txt')
        tag_type = 'ner'
        tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

        embedding_types: List[TokenEmbeddings] = [
            PooledFlairEmbeddings('pubmed-forward'),
            PooledFlairEmbeddings('pubmed-backward'),
            ELMoEmbeddings('pubmed'),
        ]
        embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

        tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                                embeddings=embeddings,
                                                tag_dictionary=tag_dictionary,
                                                tag_type=tag_type,
                                                use_crf=True)
        #  initialize trainer
        trainer: ModelTrainer = ModelTrainer(tagger, corpus)

        #  start training
        trainer.train(self.save_dir,
                      learning_rate=lr,
                      mini_batch_size=bs,
                      max_epochs=epochs)

    def classify(self, sentences: list) -> list:
        """
        Classifies a list of sentences, returning NER results.
        :return List of medical term strings
        """
        results = []

        tagger = SequenceTagger.load(self.save_dir + 'best-model.pt')
        for sentence in sentences:
            flair_sentence = Sentence(sentence)
            tagger.predict(flair_sentence)

            tokens = [token.text for token in flair_sentence.get_spans('ner') if token.tag == 'Entity']
            results.append(tokens)

        return results
