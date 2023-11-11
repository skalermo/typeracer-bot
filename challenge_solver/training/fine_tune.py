import argparse
import logging

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
from torch import nn, optim
from torch.utils.tensorboard import SummaryWriter

from src.dataset import get_finetune_dataloaders, get_dataloaders
from src.model import CRNN
from src.utils import find_last_exp_dir, setup_exp_dirs, correct_prediction, decode_predictions, \
    encode_text_batch, char2idx


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp_name",
        default='challenge_finetuning',
        type=str,
    )
    parser.add_argument(
        "--num_epochs",
        default=50,
        type=int,
    )
    parser.add_argument(
        "--model_path",
        type=str,
    )
    parser.add_argument(
        "--batch_size",
        default=8,
        type=int,
    )
    parser.add_argument(
        "--learning_rate",
        default=1e-4,
        type=float,
    )
    parser.add_argument(
        "--clip_norm",
        default=5,
        type=float,
    )
    parser.add_argument(
        "--resume",
        action='store_true',
    )
    args = parser.parse_args()
    return args


def compute_loss(text_batch, text_batch_logits):
    """
    text_batch: list of strings of length equal to batch size
    text_batch_logits: Tensor of size([T, batch_size, num_classes])
    """
    text_batch_logps = F.log_softmax(text_batch_logits, 2)  # [T, batch_size, num_classes]
    text_batch_logps_lens = torch.full(size=(text_batch_logps.size(1),),
                                       fill_value=text_batch_logps.size(0),
                                       dtype=torch.int32).to(device)  # [batch_size]
    text_batch_targets, text_batch_targets_lens = encode_text_batch(text_batch)
    return criterion(text_batch_logps, text_batch_targets, text_batch_logps_lens, text_batch_targets_lens)


if __name__ == '__main__':
    args = parse_args()

    if args.resume:
        exp_dir = find_last_exp_dir(args.exp_name, top_dir='runs')
        checkpoint = torch.load(f'{exp_dir}/last_checkpoint.pt')
    else:
        exp_dir = setup_exp_dirs(args.exp_name)
        with open('src/model.py', 'r') as in_file, \
                open(f'{exp_dir}/model_arch.txt', 'w') as out_file:
            out_file.write(in_file.read())
        with open(f'{exp_dir}/args.txt', 'w') as f:
            f.write(str(args))

    writer = SummaryWriter(exp_dir)
    logging.basicConfig(
        format='%(asctime)s,%(msecs)d - %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO,
        handlers=[
            logging.FileHandler(f'{exp_dir}/logs.txt'),
            logging.StreamHandler(),
        ]
    )
    data_path = 'train_data'
    test_data_path = 'test_data'
    batch_size = args.batch_size
    # batch_size = 16

    *_, vocabulary = get_dataloaders(data_path, test_data_path, batch_size=batch_size)
    train_loader, test_loader, _ = get_finetune_dataloaders(test_data_path, batch_size=batch_size)
    num_chars = len(char2idx)
    print(num_chars)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = CRNN(num_chars)
    model.load_state_dict(torch.load(args.model_path))
    model = model.to(device)
    print(sum([p.numel() for p in model.parameters()]))

    criterion = nn.CTCLoss(blank=0)
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
    lr_scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, verbose=True, patience=5)

    start_epoch = 1

    if args.resume:
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        lr_scheduler.load_state_dict(checkpoint['lr_scheduler_state_dict'])
        start_epoch = checkpoint['epoch'] + 1

    best_acc = 0.0

    for epoch in range(start_epoch, args.num_epochs + 1):
        correct = 0
        total = 0
        epoch_loss_list = []

        model.train()

        for images, labels in train_loader:
            logits = model(images.to(device))
            loss = compute_loss(labels, logits)
            iteration_loss = loss.item()

            if np.isnan(iteration_loss) or np.isinf(iteration_loss):
                continue

            epoch_loss_list.append(iteration_loss)

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), args.clip_norm)
            optimizer.step()

            predicted = list(map(lambda x: correct_prediction(x), decode_predictions(logits)))
            correct += accuracy_score(labels, predicted, normalize=False)
            total += len(labels)

            # del images, labels, logits
            # torch.cuda.empty_cache()
            # gc.collect()

        writer.add_scalar('Train/learning_rate', optimizer.param_groups[0]['lr'], epoch)
        epoch_loss = np.mean(epoch_loss_list)
        lr_scheduler.step(epoch_loss)

        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'lr_scheduler_state_dict': lr_scheduler.state_dict(),
        }
        torch.save(checkpoint, f'{exp_dir}/last_checkpoint.pt')

        writer.add_scalar('Loss/train', epoch_loss, epoch)
        logging.info(f'Epoch: {epoch}, Train loss: {epoch_loss:.4f}')

        acc = correct / total
        writer.add_scalar('Accuracy/train', acc, epoch)
        writer.flush()
        logging.info(f'Train accuracy: {acc} %')

        epoch_loss_list = []
        with torch.no_grad():
            model.eval()
            correct_test = 0
            total_test = 0
            for images, labels in test_loader:
                logits = model(images.to(device))
                loss = compute_loss(labels, logits)
                iteration_loss = loss.item()
                epoch_loss_list.append(iteration_loss)
                predicted_test = list(map(lambda x: correct_prediction(x), decode_predictions(logits)))
                correct_test += accuracy_score(labels, predicted_test, normalize=False)
                total_test += len(labels)

        epoch_loss = np.mean(epoch_loss_list)
        writer.add_scalar("Loss/test", epoch_loss, epoch)
        logging.info(f'Epoch: {epoch}, Test loss: {epoch_loss:.4f}')

        test_acc = correct / total
        writer.add_scalar('Accuracy/test', test_acc, epoch)
        writer.flush()
        logging.info(f'Test accuracy: {test_acc} %')
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), f'{exp_dir}/best_model.pt')

    writer.close()
