from transformers import BartForSequenceClassification, BartTokenizer, AdamW
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
import shutil
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = 'facebook/bart-base'
out_checkpoint_path = '../checkpoints/bart_grammar_classifier'
n_epochs = 100
use_max = True  # max or sum of words representations after applying encoder on sent
lr = 5e-4
batch_size = 32
split_ratio = 0.7

if os.path.exists(out_checkpoint_path):
    shutil.rmtree(out_checkpoint_path)
os.mkdir(out_checkpoint_path)


def get_models(bart_model_name, device):
    tok = BartTokenizer.from_pretrained(bart_model_name, force_bos_token_to_be_generated=True)
    bart_model = BartForSequenceClassification.from_pretrained(bart_model_name)
    encoder = bart_model.base_model.get_encoder()
    # classification_head = bart_model.classification_head
    classification_head = torch.nn.Sequential(
        torch.nn.Linear(768, 128),
        torch.nn.LeakyReLU(),
        torch.nn.Dropout(0.2),
        torch.nn.Linear(128, 128),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(128, 32),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(32, 3),
        torch.nn.Softmax()
    )
    #
    # classification_head = torch.nn.Sequential(
    #     torch.nn.Linear(768, 1),
    #     torch.nn.Tanh()
    # )

    return tok, encoder.to(device), classification_head.to(device)


tok, encoder, classification_head = get_models(model_name, device)


def classify(input_ids, encoder, classification_head):
    b = encoder(input_ids)['last_hidden_state']
    if use_max:
        b = classification_head(b.permute(0, 2, 1).max(-1)[0])
    else:
        b = classification_head(b.permute(0, 2, 1).sum(-1))
    # return b / 2 + 0.5
    return b[:, 1]


params = list(encoder.parameters())
for layer in params[:-int(len(params) * 0.7)]:
    layer.requires_grad_(False)

encoder_optimizer = AdamW(encoder.parameters(), lr=lr)
clf_head_optimizer = AdamW(classification_head.parameters(), lr=lr)


class COLA(Dataset):
    """ dataset  """
    def __init__(self):
        df = pd.read_csv("../datasets/COLA/in_domain_train.tsv", delimiter='\t', header=None,
                         names=['sentence_source', 'label', 'label_notes', 'sentence'])
        self.sentences = df.sentence.values
        self.labels = df.label.values

        # self.sentences = [tok(sent, add_special_tokens=True)['input_ids'] for sent in df.sentence.values]
        # self.max_len = max([len(s) for s in self.sentences])
        # self.sentences = [s + [tok.pad_token_id] * (self.max_len - len(s)) for s in self.sentences]

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, item):
        return self.sentences[item], self.labels[item]

    @staticmethod
    def get_train_test_loaders(split_ratio=0.7, batch_size=32):
        dataset = COLA()
        split_idx = int(len(dataset) * split_ratio)
        train_dataset, test_dataset = torch.utils.data.random_split(dataset, [split_idx, len(dataset) - split_idx])
        train_loader = DataLoader(train_dataset, batch_size=batch_size)
        test_loader = DataLoader(test_dataset, batch_size=batch_size)
        return dataset, train_loader, test_loader


def collate_fn(batch, tok, max_len=20, device=None):
    """ padding """
    sents, labels = batch
    new_batch = ([], [])
    for i in range(len(sents)):
        if sents[i].strip().count(' ') <= max_len:
            new_batch[0].append(sents[i])
            new_batch[1].append(labels[i])
    sents = new_batch[0]
    padded_input_ids = tok.pad(tok(sents))['input_ids']
    return torch.tensor(padded_input_ids, device=device), torch.stack(new_batch[1]).to(device)


dataset, train_loader, test_loader = COLA.get_train_test_loaders(split_ratio=split_ratio, batch_size=batch_size)
print(f"Dataset size: {len(dataset)}")

ce_loss = torch.nn.BCELoss().to(device)
for ei in range(n_epochs):
    print_test_epoch = True
    if print_test_epoch:
        total = 0
        correct = 0
        for batch_num, batch in enumerate(test_loader):
            sent, label = batch
            sent = tok.pad(tok(sent))['input_ids']
            with torch.no_grad():
                pred = classify(torch.tensor(sent, device=device), encoder, classification_head) > 0.5
            correct += (label == pred.cpu()).sum().item()
            total += batch_size

        print(f"epoch {ei} test accuracy: {correct / total}")

    for batch_num, batch in enumerate(train_loader):
        sent, label = collate_fn(batch, tok, max_len=20, device=device)
        pred = classify(sent, encoder, classification_head)
        _loss = ce_loss(pred, label.type(torch.float))
        encoder_optimizer.zero_grad()
        clf_head_optimizer.zero_grad()
        _loss.backward()
        encoder_optimizer.step()
        clf_head_optimizer.step()

    save_model = True
    if save_model:
        sd1 = encoder.state_dict()
        sd2 = classification_head.state_dict()
        sd1_tmp_path = f"{out_checkpoint_path}/encoder_checkpoint_new.pt"
        sd1_real_path = f"{out_checkpoint_path}/encoder_checkpoint.pt"
        sd2_tmp_path = f"{out_checkpoint_path}/classification_head_checkpoint_new.pt"
        sd2_real_path = f"{out_checkpoint_path}/classification_head_checkpoint.pt"
        torch.save(sd1, sd1_tmp_path)
        torch.save(sd2, sd2_tmp_path)
        if os.path.exists(sd1_real_path):
            os.remove(sd1_real_path)
        if os.path.exists(sd2_real_path):
            os.remove(sd2_real_path)
        os.rename(sd1_tmp_path, sd1_real_path)
        os.rename(sd2_tmp_path, sd2_real_path)
