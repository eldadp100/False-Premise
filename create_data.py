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
    ("Mark Zuckerberg", "Facebook")
]
for i in range(len(founder_company)):
    for j in range(len(founder_company)):
        data.append((f"when did {founder_company[i][0]} found {founder_company[j][1]}?",
                     f"{founder_company[i][0]} found {founder_company[j][1]}", i == j))
        data.append((f"how much {founder_company[i][1]} that founded by {founder_company[j][i]} worth?",
                     f"{founder_company[i][0]} found {founder_company[j][1]}", i == j))

# when did x1 found y1?  True Premise
# when did x2 found y2?  True Premise
# when did x1 found y2?  False Premise


""" rule 2: colored animals """

# how may legs does a green dog have?      premise - dogs can be green      False Premise
# where is the natural living place of yellow penguins?
animals = ["dog", "cat", "elephant"]
real_colors = ["brown", "gray"]
fake_colors = ["green", "purple", "blue"]
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
        return self.data_triples[i]
