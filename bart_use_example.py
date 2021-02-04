from transformers import BartForConditionalGeneration, BartTokenizer, AdamW
import torch
from torch.utils.data import DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Simple pretrained use:
model = BartForConditionalGeneration.from_pretrained("facebook/bart-base", force_bos_token_to_be_generated=True)
tok = BartTokenizer.from_pretrained("facebook/bart-base")

a = "UN Chief Says There Is No <mask> in Syria"
print(tok.batch_decode(model.generate(tok(a, return_tensors='pt')['input_ids']), skip_special_tokens=True))

# Fine-tuning
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
epochs_num = 10

model = BartForConditionalGeneration.from_pretrained("facebook/bart-base", force_bos_token_to_be_generated=True)
model.to(device)
model.train()
optimizer = AdamW(model.parameters(), lr=5e-5)

train_loader = DataLoader(dataset)
for epoch in range(epochs_num):
    for batch in train_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        loss = model(input_ids, attention_mask=attention_mask, labels=labels)[0]

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

model.eval()
# Do evaluations
