from os import listdir
from os.path import isfile, join
import json


class LowConfidencePruner:
    """
    A pruner that removes objects from a list of dicts that have confidence below a threshold. It is assumed that
    the list of dicts comes from passing an MP3 file to Google Cloud's transcription service.
    """
    def __init__(self, path: str, threshold: float = 0.96):
        """
        Initializes an instance of LowConfidencePruner.
        :param path: Directory to search for JSON files in.
        :param threshold: Threshold to prune at.
        """
        self.path = path
        self.threshold = threshold

    def prune(self) -> list:
        """
        Prunes excerpts and returns a single list of transcripts.
        :return: List of transcripts.
        """
        excerpts = []
        files = [f for f in listdir(self.path) if isfile(join(self.path, f))]

        for file in files:
            with open(join(self.path, file)) as f:
                content = json.load(f)
                high_confidence = filter(lambda x: x['alternatives'][0]['confidence'] > self.threshold, content['response']['results'])
                objs = list(map(lambda x: x['alternatives'][0]['transcript'], high_confidence))

                excerpts += objs

        return excerpts
