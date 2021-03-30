from transformers import BartForConditionalGeneration, BartTokenizer, AdamW
import torch
from torch.utils.data import DataLoader
import random
import load_data
from datetime import datetime
import losses

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

checkpoint_path = "../checkpoints/checkpoint.pt"
dataset_path = "../datasets/our/qp_dataset.json"
model_name = 'facebook/bart-base'
lr = 5e-5
n_epochs = 10

print(f"start time: {datetime.now().strftime('%H:%M:%S')}")
print(f'using device {device}')
print(f'using model: {model_name}')
print(f"checkpoint path:{checkpoint_path}")
print(f"lr: {lr}")

model = BartForConditionalGeneration.from_pretrained(model_name, force_bos_token_to_be_generated=True)
model.to(device)
model.train()
tok = BartTokenizer.from_pretrained(model_name)

discriminator = losses.Discriminator(tok.vocab_size).to(device)

# for param in model.base_model.parameters():
#     param.requires_grad = False

BART_params = list(model.parameters())
for i, param in enumerate(model.parameters()):
    if i > len(BART_params) - 20:
        param.requires_grad_(False)
    else:
        param.requires_grad_(True)

optimizer = AdamW(model.parameters(), lr=lr)
disc_optimizer = torch.optim.Adam(discriminator.parameters(), lr=lr)

dataset = load_data.QuestionPremiseDataset(dataset_path, tok, with_facts=True)

split_idx = int(len(dataset) * 0.7)
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [split_idx, len(dataset) - split_idx])

train_loader = DataLoader(train_dataset)
test_loader = DataLoader(test_dataset)
print_test_each_time = 10
for epoch in range(n_epochs):
    curr_loss = 0.
    for i, batch in enumerate(train_loader):

        question, premise, fact = batch
        if fact[0] == '':
            q_tok = tok(question, return_tensors='pt')
            question_input_ids = q_tok['input_ids'].to(device)
            question_attention_mask = q_tok['attention_mask'].to(device)

            premise_tok = tok(premise, return_tensors='pt')
            premise_input_ids = premise_tok['input_ids'].to(device)

            # loss = model(question_input_ids, attention_mask=question_attention_mask, labels=premise_input_ids)[0]
            q_model_pred = model(question_input_ids)['logits'][0].softmax(-1)
            loss = losses.calculate_loss(q_model_pred, premise_input_ids, tok) - discriminator.gen_loss(q_model_pred)
            curr_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        else:
            fact = fact.to(device)
            loss = discriminator.disc_loss(fact)
            disc_optimizer.zero_grad()
            loss.backward()
            disc_optimizer.step()

        if i != 0 and i % 200 == 0:
            print(f"epoch {epoch} step {i}: {curr_loss / 200}")
            curr_loss = 0.
            if i % 5000 == 0:
                print("test")
                for batch in test_loader:
                    if random.random() > print_test_each_time / len(test_loader):
                        continue
                    question, premise, _ = batch
                    q_tok = tok(question, return_tensors='pt')
                    question_input_ids = q_tok['input_ids'].to(device)

                    print(question)
                    print(tok.batch_decode(model.generate(question_input_ids), skip_special_tokens=True))
                    print()

    # save_model
