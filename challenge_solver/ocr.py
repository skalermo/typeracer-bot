from pathlib import Path

import numpy as np
import cv2
import torch
from challenge_solver.training.src.model import CRNN
from challenge_solver.training.src.utils import correct_prediction, decode_predictions


def read_from_challenge_image(image: np.array) -> str:
    im = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
    im_height, im_width, _ = im.shape
    strip_height = im_height // 5
    strips = np.array([im[i * strip_height:(i + 1) * strip_height, :] for i in range(5)])

    model = CRNN(66)
    model.load_state_dict(torch.load(Path(__file__).parent / 'trained_models' / 'crnn_13650_finetuned.pt', map_location=torch.device('cpu')))
    logits = model(
        (torch.tensor(strips) / 255).permute(0, 3, 1, 2)
    )
    predicted = ' '.join(map(lambda x: correct_prediction(x), decode_predictions(logits)))
    return predicted
