"""
Create False-Promise set of questions (that google search fails on those patterns with high probability)
and True-Promise set.
The dataset contains triples of (question, the premise in the question, premise is false or true).

How we create the sets:
    1. using conceptnet...

"""
import random

from torch.utils.data import Dataset

data = []

""" rule 1: Inventions """
inventor_product = [
    ("Bill Gates", "windows"),

]

founder_company = [
    ("bill gates", "microsoft"),
    ("Elon Mask", "Tesla"),
    ("Mark Zuckerberg", "Facebook"),
    ("Henry Ford", "Ford"),
    ("Jeff Bezos", "Amazon"),
    ("apple", "Steve Jobs")
]
founder_current_CEO_not_founder = [
    ("apple", "Tim Cook")
]
founder_company_questions_starts = ["when did", "when", "how did", "how", "where", "where did", "in which way",
                                    "why did", "who was involved when"]

for i in range(len(founder_company)):
    for j in range(len(founder_company)):
        for q_s in founder_company_questions_starts:
            data.append((f"{q_s} {founder_company[i][0]} found {founder_company[j][1]}?",
                         f"{founder_company[i][0]} found {founder_company[j][1]}", i == j))

        data.append((f"how much {founder_company[i][1]} that was founded by {founder_company[j][0]} worth?",
                     f"{founder_company[i][0]} found {founder_company[j][1]}", i == j))

        data.append((f"what was the motive of {founder_company[i][0]} to found {founder_company[j][1]}?",
                     f"{founder_company[i][0]} found {founder_company[j][1]}", i == j))

# when did x1 found y1?  True Premise
# when did x2 found y2?  True Premise
# when did x1 found y2?  False Premise


""" rule 2: colored animals """

# how may legs does a green dog have?      premise - dogs can be green      False Premise
# where is the natural living place of yellow penguins?
animals = ["dog", "cat", "elephant", "wolf"]
real_colors = ["brown", "gray"]
fake_colors = ["green", "purple", "blue", "pink"]
for a in animals:
    for c in real_colors:
        data.append((f"why {c} {a} has 2 heads?", f"{a} can be {c} colored", True))
        data.append((f"how many legs does a {c} {a} has?", f"{a} has legs and {a} can be {c} colored", True))
        data.append((f"how many arms does a {c} {a} has?", f"{a} has arms and {a} can be {c} colored", False))
        data.append((f"where is the natural living place of {c} {a}s?", f"{a} can be {c} colored", True))
    for c in fake_colors:
        data.append((f"why {c} {a} has 2 heads?", f"{a} can be {c} colored", False))
        data.append((f"how many legs does a {c} {a} has?", f"{a} has legs and {a} can be {c} colored", False))
        data.append((f"how many arms does a {c} {a} has?", f"{a} has arms and {a} can be {c} colored", False))
        data.append((f"where is the natural living place of {c} {a}s?", f"{a} can be {c} colored", False))

# Pink animals

animals = ["pig", "ostrich"]
real_colors = ["pink"]
fake_colors = ["yellow", "purple", "blue"]
for a in animals:
    for c in real_colors:
        data.append((f"why {c} {a} has 2 heads?", f"{a} can be {c} colored", True))
        data.append((f"how many legs does a {c} {a} has?", f"{a} has legs and {a} can be {c} colored", True))
        data.append((f"how many arms does a {c} {a} has?", f"{a} has arms and {a} can be {c} colored", False))
        data.append((f"where is the natural living place of {c} {a}s?", f"{a} can be {c} colored", True))
    for c in fake_colors:
        data.append((f"why {c} {a} has 2 heads?", f"{a} can be {c} colored", False))
        data.append((f"how many legs does a {c} {a} has?", f"{a} has legs and {a} can be {c} colored", False))
        data.append((f"how many arms does a {c} {a} has?", f"{a} has arms and {a} can be {c} colored", False))
        data.append((f"where is the natural living place of {c} {a}s?", f"{a} can be {c} colored", False))

# 2 legs animals


# 2 hands 2 legs animals - monkeys...


""" rule 3: not true fact with why at start """

# why dog has 2 heads?
# why the ski is yellow?


"""Holiday and country"""

# when hanocka is celebrated in Egypt?

jewish_holidays = ['Hanocka', 'Passover', 'Sukot']
countries = ['US', 'Germany', 'Netherlands', 'Egypt', 'France']
for holiday in jewish_holidays:
    data.append((f"When {holiday} is celebrated in Israel?", f"{holiday} is celebrated in Israel", True))
    for country in countries:
        data.append((f"When {holiday} is celebrated in {country}?", f"{holiday} is celebrated in {country}", False))

""" songs and singer """
# how many views in youtube does "On Beach Line" by Bach has?
songs_singers = [
    ("ABC", "DEF"),
]

for i in range(len(songs_singers)):
    for j in range(len(songs_singers)):
        data.append((
            f"how many views in youtube does {songs_singers[i][0]} by {songs_singers[j][1]} has?",
            f"the song is {songs_singers[i][0]} is by {songs_singers[j][1]}",
            i == j
        ))


class QuestionPremiseDataset(Dataset):
    def __init__(self, data_triples, shuffle=True):
        self.data_triples = data_triples
        if shuffle:
            random.shuffle(self.data_triples)

    def __len__(self):
        return len(self.data_triples)

    def __getitem__(self, item):
        return self.data_triples[item]


# test
if __name__ == '__main__':
    dataset = QuestionPremiseDataset(data)
    print(len(dataset))
    for i in range(10):
        print(dataset[i])

"""

    Wikidata Inventor-Gadget Query:
    
    SELECT ?inventor ?inventorLabel ?gadget ?gadgetLabel WHERE {
      ?gadget wdt:P61 ?inventor.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }

    
    Business-Founder
    SELECT DISTINCT ?business ?founder ?businessLabel ?officialname  ?stockexchangeLabel
    WHERE {
       ?business wdt:P31/wdt:P279* wd:Q4830453 .
       ?business wdt:P414 ?stockexchange .
       SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } .
       OPTIONAL { ?business wdt:P112 ?founder } .
       OPTIONAL { ?business wdt:P1448 ?officialname FILTER( LANG(?officialname) = "en" ) } .
    }
    ORDER BY ?business
"""
