class PairFormer:
    """
    Forms pairs from adjacent terms.
    """
    def __init__(self, terms: list, merge: bool = True):
        """
        Initializes a PairFormer.
        :param terms: List of terms.
        :param merge: Set to True if you used merge in DuplicateRemover
        """
        self.terms = terms
        self.merge = merge

    def pair(self) -> list:
        """
        Forms pairs of adjacent terms. Credit to https://stackoverflow.com/a/21303286
        :return: List of pairs of adjacent terms.
        """
        if self.merge:
            return list(zip(self.terms, self.terms[1:]))
        else:
            return [list(zip(terms, terms[1:])) for terms in self.terms]
