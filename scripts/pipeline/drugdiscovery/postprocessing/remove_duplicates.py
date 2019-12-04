from functools import reduce
from operator import add
import itertools

class DuplicateRemover:
    """
    Removes adjacent duplicates in terms.
    """
    def __init__(self, terms: list, merge: bool = True):
        """
        Initializes a DuplicateRemover.
        :param terms: List of lists of strings. Each string is a term.
        :param merge: If True, merges all the lists.
        """
        self.terms_list = terms
        self.merge = merge

    def remove(self) -> list:
        """
        Removes adjacent duplicate terms. Code from https://stackoverflow.com/a/3463582.
        :return: List of terms, of which no adjacent terms are the same.
        """
        excerpts = []

        if self.merge:
            terms_list = reduce(add, self.terms_list)

            # Handle the 1D case
            excerpts += [key for key, group in itertools.groupby(terms_list)]
        else:
            # Handle the 2D case
            terms_list = self.terms_list
            for terms in terms_list:
                excerpts.append(
                    [terms[i] for i in range(len(terms)) if i == len(terms) - 1 or terms[i] != terms[i + 1]]
                )

        return excerpts
