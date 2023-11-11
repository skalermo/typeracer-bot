import os
import time

import torch
import torch.nn.functional as F


vocabulary = ['~', ' ', '!', '"', "'", '(', ')', ',', '-', '.', ':', ';', '?',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
              '`',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
idx2char = {k: v for k, v in enumerate(vocabulary, start=0)}
char2idx = {v: k for k, v in idx2char.items()}
SEPARATOR = '~'


def encode_text_batch(text_batch):
    text_batch_targets_lens = [len(text) for text in text_batch]
    text_batch_targets_lens = torch.IntTensor(text_batch_targets_lens)

    text_batch_concat = ''.join(text_batch)
    text_batch_targets = [char2idx[c] for c in text_batch_concat]
    text_batch_targets = torch.IntTensor(text_batch_targets)

    return text_batch_targets, text_batch_targets_lens


def decode_predictions(text_batch_logits):
    text_batch_tokens = F.softmax(text_batch_logits, 2).argmax(2)  # [T, batch_size]
    text_batch_tokens = text_batch_tokens.cpu().numpy().T  # [batch_size, T]

    text_batch_tokens_new = []
    for text_tokens in text_batch_tokens:
        text = [idx2char[idx] for idx in text_tokens]
        text = ''.join(text)
        text_batch_tokens_new.append(text)

    return text_batch_tokens_new


def remove_duplicates(text: str):
    if len(text) == 0:
        return ''

    if len(text) > 1:
        letters = [text[0]] + [letter for idx, letter in enumerate(text[1:], start=1) if text[idx] != text[idx-1]]
    else:
        letters = [text[0]]

    return ''.join(letters)


def correct_prediction(word: str):
    parts = word.split(SEPARATOR)
    parts = [remove_duplicates(part) for part in parts]
    corrected_word = ''.join(parts)
    return corrected_word


def find_last_exp_dir(exp_name: str, top_dir: str = 'runs') -> str:
    # find the most recently created dir
    models_dir = max(x[0] for x in os.walk(top_dir) if exp_name in x[0])
    return models_dir


def setup_exp_dirs(exp_name: str) -> str:
    experiment_name = f'{exp_name}_{int(time.time())}'
    path = f'runs/{experiment_name}'
    if not os.path.exists(path):
        os.makedirs(path)
    return path
