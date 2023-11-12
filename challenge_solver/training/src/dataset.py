import json
import os

import numpy as np
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms.functional as F
from sklearn.model_selection import train_test_split

from src.utils import SEPARATOR


class CustomPad:
    def __call__(self, image):
        w, h = image.size
        padding = (0, 0, 410 - w, 0)
        padded = F.pad(image, padding, 255, 'constant')
        return padded


class AliceDataset(Dataset):
    def __init__(self, data_dir, image_fns, image_labels):
        self.data_dir = data_dir
        self.image_fns = image_fns
        self.image_labels = image_labels

    def __len__(self):
        return len(self.image_fns)
        # return 16

    def __getitem__(self, index):
        image_fn = self.image_fns[index]
        image_fp = os.path.join(self.data_dir, image_fn)
        image = Image.open(image_fp).convert('RGB')
        image = self.transform(image)
        return image, self.image_labels[index]

    def transform(self, image):
        transform_ops = transforms.Compose([
            transforms.Grayscale(3),
            CustomPad(),
            transforms.ToTensor(),
        ])
        return transform_ops(image)


def get_dataloaders(data_dir_path, test_data_dir_path, batch_size=4) -> (DataLoader, DataLoader, DataLoader, list[str]):
    with open(data_dir_path + '/labels.json', 'r') as f:
        labels = json.load(f)

    sizes = labels['sizes']
    labels = labels['labels']
    letters = sorted(list(set(''.join(labels.values()))))
    vocabulary = [SEPARATOR] + letters

    # target images have width 410
    sizes = dict(filter(lambda item: item[1][0] <= 410, sizes.items()))

    labels = {k: labels[k] for k in sizes}
    ids = np.arange(len(labels))
    ids_train, ids_valid = train_test_split(ids, train_size=0.8, test_size=0.2, random_state=0)
    image_fns = np.array([f'{k}.jpg' for k in labels])
    image_labels = np.array([v for v in labels.values()])

    train_set = AliceDataset(data_dir_path + '/images', image_fns[ids_train], image_labels[ids_train])
    valid_set = AliceDataset(data_dir_path + '/images', image_fns[ids_valid], image_labels[ids_valid])
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=2)
    valid_loader = DataLoader(valid_set, batch_size=batch_size, shuffle=False, num_workers=2)

    with open(test_data_dir_path + '/labels.json', 'r') as f:
        labels = json.load(f)

    labels = labels['labels']
    image_fns = np.array([f'{k}.jpg' for k in labels])
    image_labels = np.array([v for v in labels.values()])
    test_set = AliceDataset(test_data_dir_path + '/images', image_fns, image_labels)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=1)

    return train_loader, valid_loader, test_loader, vocabulary


def get_finetune_dataloaders(data_dir_path: str, batch_size: int = 4) -> (DataLoader, DataLoader):
    with open(data_dir_path + '/labels.json', 'r') as f:
        labels = json.load(f)

    sizes = labels['sizes']
    labels = labels['labels']
    letters = sorted(list(set(''.join(labels.values()))))
    vocabulary = [SEPARATOR] + letters
    labels = {k: labels[k] for k in sizes}
    ids = np.arange(len(labels))
    ids_train, ids_valid = train_test_split(ids, train_size=0.91, test_size=0.09, random_state=0)
    image_fns = np.array([f'{k}.jpg' for k in labels])
    image_labels = np.array([v for v in labels.values()])

    train_set = AliceDataset(data_dir_path + '/images', image_fns[ids_train], image_labels[ids_train])
    test_set = AliceDataset(data_dir_path + '/images', image_fns[ids_valid], image_labels[ids_valid])
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=1)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=1)
    return train_loader, test_loader, vocabulary
