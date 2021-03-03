import torch
from torch import nn


class Discriminator(nn.Module):
    def __init__(self, vocab_size):
        super(Discriminator, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(vocab_size, 1)
        )

        self.bce_loss = nn.BCELoss()

    def gen_loss(self, fake):
        fake_preds = 1. - torch.sigmoid(self.net(fake))
        out_fake = self.bce_loss(fake_preds, torch.ones(fake_preds.shape).to(fake_preds.device))
        return out_fake.sum()

    def disc_loss(self, real):
        real_preds = torch.sigmoid(self.net(real))
        out_real = self.bce_loss(real_preds, torch.ones(real_preds.shape).to(real_preds.device))
        return out_real.sum()


def same_words_loss(q_pred_logits, p_ids, tok):
    gt = torch.zeros(tok.vocab_size)
    for idx in p_ids[0]:
        gt[idx] += 1.
    gt = gt.to(q_pred_logits.device)

    pred = q_pred_logits.permute(1, 0).sum(-1)
    return (gt - pred).abs().sum()


def calculate_loss(q_pred, p_ids, tok):
    return same_words_loss(q_pred, p_ids, tok)
