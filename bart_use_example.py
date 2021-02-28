from transformers import BartForConditionalGeneration, BartTokenizer, AdamW
import torch
from torch.utils.data import DataLoader

import create_data

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BartForConditionalGeneration.from_pretrained("facebook/bart-base", force_bos_token_to_be_generated=True)
tok = BartTokenizer.from_pretrained("facebook/bart-base")

# use example
# a = "UN Chief Says There Is No <mask> in Syria"
# print(tok.batch_decode(model.generate(tok(a, return_tensors='pt')['input_ids']), skip_special_tokens=True))

# Fine-tuning
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
epochs_num = 10

model = BartForConditionalGeneration.from_pretrained("facebook/bart-base", force_bos_token_to_be_generated=True)
model.to(device)
model.train()
optimizer = AdamW(model.parameters(), lr=5e-5)

dataset = create_data.QuestionPremiseDataset(create_data.data)
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [400, len(dataset) - 400])

train_loader = DataLoader(train_dataset)
test_loader = DataLoader(test_dataset)
for epoch in range(epochs_num):
    for batch in train_loader:
        question, premise, is_a_true_premise = batch
        q_tok = tok(question, return_tensors='pt')
        question_input_ids = q_tok['input_ids'].to(device)
        question_attention_mask = q_tok['attention_mask'].to(device)

        premise_tok = tok(premise, return_tensors='pt')
        premise_input_ids = premise_tok['input_ids'].to(device)

        loss = model(question_input_ids, attention_mask=question_attention_mask, labels=premise_input_ids)[0]

        # print(question)
        # print(tok.batch_decode(model.generate(question_input_ids), skip_special_tokens=True))
        print(loss.item())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print("test")
    for batch in train_loader:
        question, premise, is_a_true_premise = batch
        q_tok = tok(question, return_tensors='pt')
        question_input_ids = q_tok['input_ids'].to(device)

        print(question)
        print(tok.batch_decode(model.generate(question_input_ids), skip_special_tokens=True))
        print()
model.eval()
# Do evaluations
