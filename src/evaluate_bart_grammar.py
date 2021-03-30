import torch
import train_grammar_bart

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = 'facebook/bart-base'
from_checkpoint_path = '../checkpoints/bart_grammar_classifier'
tok, encoder, clf_head = train_grammar_bart.get_models(model_name, device)


def load_encoder_clf(checkpoint_path, enc, clf):
    sd_enc = torch.load(f"{checkpoint_path}/encoder_checkpoint.pt", map_location=device)
    sd_clf = torch.load(f"{checkpoint_path}/classification_head_checkpoint.pt", map_location=device)
    enc.load_state_dict(sd_enc)
    clf.load_state_dict(sd_clf)


load_encoder_clf(from_checkpoint_path, encoder, clf_head)
_, _, test_loader = train_grammar_bart.COLA.get_train_test_loaders()
print(f"Test size: {len(test_loader)}")

total = 0
correct = 0
for batch_num, batch in enumerate(test_loader):
    sent, label = batch
    sent = tok(sent)['input_ids']
    with torch.no_grad():
        pred = train_grammar_bart.classify(torch.tensor(sent, device=device), encoder, clf_head)
    if pred > 0.5:
        correct += 1 if label == 1 else 0
    else:
        correct += 1 if label == 0 else 0
    total += 1

print(f"test accuracy: {correct / total}")
