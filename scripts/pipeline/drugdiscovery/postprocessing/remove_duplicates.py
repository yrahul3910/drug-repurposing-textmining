import itertools


class DuplicateRemover:
    """
    Removes adjacent duplicates in terms.
    """
    def __init__(self, terms: list):
        """
        Initializes a DuplicateRemover.
        :param terms: List of strings. Each string is a set of terms separated by spaces.
        """
        self.terms_list = terms

    def remove(self) -> list:
        """
        Removes adjacent duplicate terms. Code from https://stackoverflow.com/a/3463582.
        :return: List of terms, of which no adjacent terms are the same.
        """
        excerpts = []
        for terms in self.terms_list:
            excerpts.append([terms[i] for i in range(len(terms)) if i == len(terms) - 1 or terms[i] != terms[i + 1]])

        return excerpts
