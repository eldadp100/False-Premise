import torch
from transformers import BartForSequenceClassification

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

bart_checkpoint_path = '../checkpoints/bart_grammar_classifier'
train_our_bart = False
bart_model = BartForSequenceClassification.from_pretrained(bart_checkpoint_path).to(device)

bart_state_dict = bart_model.state_dict()
embed_words_matrix = bart_state_dict['model.encoder.embed_tokens.weight']
embed_pos_matrix = bart_state_dict['model.encoder.embed_positions.weight']

model_without_embedding = bart_model.model.get_encoder()


def classify_with_bart(_input):
    embedded_inputs = _input @ embed_words_matrix  # check it does word-by-word
    embedded_inputs += embed_pos_matrix[:len(_input)]  # TODO

    b = embedded_inputs.unsqueeze(0)
    for layer in model_without_embedding.layers:
        b = layer(b, torch.ones((1, 1, b.shape[1], b.shape[1]), dtype=torch.float, device='cuda'))[0]

    out = bart_model.classification_head(b.permute(0, 2, 1).sum(-1))
    return out[0][1]


# example
if __name__ == '__main__':
    _input = torch.rand(10, 50265)  # vector of size len x 50265

    embedded_inputs = _input @ embed_words_matrix  # check it does word-by-word
    embedded_inputs += embed_pos_matrix[:len(_input)]  # TODO

    b = model_without_embedding.layers[0](embedded_inputs.unsqueeze(0), torch.ones((1, 1, 10, 10), dtype=torch.float))
    bart_model.classification_head(b[0])
