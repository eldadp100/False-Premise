import torch
from torch.utils.data import Dataset
import random
import json


class QuestionPremiseDataset(Dataset):
    def __init__(self, dataset_path, tok, shuffle=True, with_facts=True):
        self.with_facts = with_facts
        with open(dataset_path) as f:
            self.data = json.load(f)
        self.keys = list(self.data.keys())
        if shuffle:
            random.shuffle(self.keys)
        facts = []
        with open('../datasets/our/facts.txt') as f:
            for line in f:
                facts.append(line[:-1])
                if len(facts) > len(self.keys):
                    break

        self.facts_dataset = FactsDataset(facts, tok)
        self.facts_dataset_keys = list(range(len(self.facts_dataset)))

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, item):
        if self.with_facts:
            if random.random() > 0.5:
                fact = ""
            else:
                fact = self.facts_dataset[random.choice(self.facts_dataset_keys)]

            return self.keys[item], ", ".join(self.data[self.keys[item]]), fact
        return self.keys[item], ", ".join(self.data[self.keys[item]])


class FactsDataset(Dataset):
    def __init__(self, facts_list, tok):
        self.tok = tok

        tmp_items = [tok(s)['input_ids'] for s in facts_list]
        tmp_items = [ti for ti in tmp_items if len(ti) < 12]
        self.max_size = max([len(ti) for ti in tmp_items])

        self.items = tmp_items
        # self.items = []
        # for ti in tmp_items:
        #     sent_vec = torch.rand(max_size, tok.vocab_size)
        #     for i, x in enumerate(ti):
        #         sent_vec[i][x] += 2
        #     sent_vec = sent_vec.softmax(-1)
        #     self.items.append(sent_vec)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        sent_vec = torch.rand(self.max_size, self.tok.vocab_size)
        for i, x in enumerate(self.items[item]):
            sent_vec[i][x] += 2
        sent_vec = sent_vec.softmax(-1)
        return sent_vec


# class QuestionAnswerDataset(Dataset):
#     def __init__(self, dataset_path, shuffle):
#         with open(dataset_path) as f:
#             self.data = json.load(f)
#         self.keys = list(self.data.keys())
#         if shuffle:
#             random.shuffle(self.keys)
#     def __len__(self):
#         return len(self.keys)
#
#     def __getitem__(self, item):
#         return self.keys[item], ", ".join(self.data[self.keys[item]])


# test
if __name__ == '__main__':
    from torch.utils.data import DataLoader

    dataset = QuestionPremiseDataset("../datasets/our/qp_dataset.json")

    dl = DataLoader(dataset, batch_size=32)
    for i in dl:
        print(i[0])

#
# class QuestionPremiseDatasetWithPremiseClassification(Dataset):
#     def __init__(self, data_triples, shuffle=True):
#         self.data_triples = []  # TODO
#         if shuffle:
#             random.shuffle(self.data_triples)
#
#     def __len__(self):
#         return len(self.data_triples)
#
#     def __getitem__(self, item):
#         return self.data_triples[item]
