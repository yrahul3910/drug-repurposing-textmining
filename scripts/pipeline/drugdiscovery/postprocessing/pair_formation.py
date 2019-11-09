class PairFormer:
    """
    Forms pairs from adjacent terms.
    """
    def __init__(self, terms: list):
        """
        Initializes a PairFormer.
        :param terms: List of terms.
        """
        self.terms = terms

    def pair(self) -> list:
        """
        Forms pairs of adjacent terms. Credit to https://stackoverflow.com/a/21303286
        :return: List of pairs of adjacent terms.
        """
        return list(zip(self.terms, self.terms[1:]))
