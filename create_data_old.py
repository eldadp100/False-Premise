"""
Create False-Promise set of questions (that google search fails on those patterns with high probability)
and True-Promise set.
The dataset contains triples of (question, the premise in the question, premise is false or true).

How we create the sets:
    1. using conceptnet...

"""

from torch.utils.data import Dataset
import requests

obj = requests.get('http://api.conceptnet.io/c/en/example').json()


class ConceptNet:
    def __init__(self):
        self.url = "http://api.conceptnet.io/ld/conceptnet5.7/context.ld.json"

    def lookup(self, lang, term):
        url_to_search = self.url + "c/" + lang + "/" + term
        data = urlopen(url_to_search)
        json_data = json.load(data)

        "edges"

    def relation(self, rel, concept):
        url_to_search = self.url + "search?rel=/r/" + rel + "&end=/c/en/" + concept
        data = urlopen(url_to_search)
        json_data = json.load(data)

        "edges"

    def termsAssociation(self, term1, term2, limit, lang):
        url_to_search = self.url + "assoc/list/en/" + term1 + "," + term2 + "@-1?limit=" + str(
            limit) + "&filter=/c/" + lang
        data = urlopen(url_to_search)
        json_data = json.load(data)

        "similar"


class QuestionPremiseDataset(Dataset):
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, item):
        pass


pass