class IrrelevantTermRemover:
    """
    Removes irrelevant medical terms from each excerpt in a list.
    """
    def __init__(self, excerpts: list, terms: list = None):
        """
        Initializes an instance of IrrelevantTermRemover
        :param excerpts: List of str excerpts.
        :param terms: List of terms to remove. If None, uses a default list.
        """
        self.excerpts = excerpts
        if terms is None:
            self.term_list = [
                'pharmacy',
                'health',
                'allergist',
                'patient',
                'biochemical',
                'medication',
                'symptom',
                'urologist',
                'polypharmacy',
                'relief',
                'nutrient',
                'dr',
                'herbal',
                'care',
                'healthcare',
                'prognosis',
                'die',
                'death',
                'insurance',
                'remittance',
                'relapse',
                'physician',
                'decease',
                'practitioner',
                'anesthesia',
                'anesthesiology',
                'icu',
                'medicare',
                'etiology'
            ]
        else:
            self.term_list = terms

    def remove(self) -> list:
        """
        Removes all words in the list from each string in the excerpts list.
        :return: List of strings, with irrelevant terms removed.
        """
        final_excerpts = []  # all excerpts after removing taboo words
        for text in self.excerpts:
            split_text = text.split()
            cleaned_cur_excerpt = []

            for word in split_text:
                include = True
                for taboo_word in self.term_list:
                    if taboo_word.lower() in word.lower():
                        include = False
                        break

                if include:
                    cleaned_cur_excerpt.append(word)

            final_excerpts.append(' '.join(cleaned_cur_excerpt))

        return final_excerpts
