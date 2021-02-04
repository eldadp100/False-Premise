"""
Create False-Promise set of questions (that google search fails on those patterns with high probability)
and True-Promise set.
The dataset contains triples of (question, the premise in the question, premise is false or true).

How we create the sets:
    1. using conceptnet...

"""

import json
import urllib3
from torch.utils.data import Dataset

"""
 This code is adapted from https://github.com/fitosegrera/python-conceptnet/blob/master/ConceptNet.py
"""


class ConceptNet:
    def __init__(self):
        self.url = "http://conceptnet5.media.mit.edu/data/5.4/"

    def lookup(self, lang, term):
        url_to_search = self.url + "c/" + lang + "/" + term
        data = urllib3.urlopen(url_to_search)
        json_data = json.load(data)

        "edges"

    def relation(self, rel, concept):
        url_to_search = self.url + "search?rel=/r/" + rel + "&end=/c/en/" + concept
        data = urllib3.urlopen(url_to_search)
        json_data = json.load(data)

        "edges"

    def termsAssociation(self, term1, term2, limit, lang):
        url_to_search = self.url + "assoc/list/en/" + term1 + "," + term2 + "@-1?limit=" + str(
            limit) + "&filter=/c/" + lang
        data = urllib3.urlopen(url_to_search)
        json_data = json.load(data)

        "similar"


class QuestionPremiseDataset(Dataset):
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, item):
        pass
