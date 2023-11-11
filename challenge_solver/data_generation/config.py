import inspect
import os
from pathlib import Path

import imgaug.augmenters as iaa
from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    GeneratorCfg,
)

from data_generation.custom_augmentations import WaveWarp, CustomLine

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
OUT_DIR = CURRENT_DIR / "output"
DATA_DIR = CURRENT_DIR
BG_DIR = DATA_DIR / "bg_white"
CHAR_DIR = DATA_DIR / "char"
FONT_DIR = DATA_DIR / "font"
FONT_LIST_DIR = DATA_DIR / "font_list"
TEXT_DIR = DATA_DIR / "text"

font_cfg = dict(
    font_dir=FONT_DIR,
    font_list_file=FONT_LIST_DIR / "font_list.txt",
    font_size=(28, 29),
)


def base_cfg(
    name: str, corpus, corpus_effects=None, layout_effects=None, layout=None, gray=True
):
    return GeneratorCfg(
        num_image=60_000,
        save_dir=OUT_DIR / name,
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            gray=gray,
            layout_effects=layout_effects,
            layout=layout,
            corpus=corpus,
            corpus_effects=corpus_effects,
            height=27,
        ),
    )


def eng_word_data():
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                # text_paths=[TEXT_DIR / "eng_text.txt"],
                text_paths=[TEXT_DIR / "alice_in_wonderland.txt"],
                num_word=(3, 6),
                filter_by_chars=True,
                chars_file=CHAR_DIR / "eng.txt",
                **font_cfg
            ),
        ),
        corpus_effects=Effects(
            [
                Padding(p=1, w_ratio=(0.1, 0.11), h_ratio=(0.19, 0.20), center=False),
                DropoutRand(p=0.9, dropout_p=(0.2, 0.6)),
                ImgAugEffect(aug=iaa.ShearX((-30, 30))),
                ImgAugEffect(p=0.9, aug=WaveWarp(frequency=(0.3, 0.7))),
                ImgAugEffect(p=0.9, aug=CustomLine()),
                ImgAugEffect(p=0.9, aug=CustomLine()),
            ]
        ),
    )


# fmt: off
# The configuration file must have a configs variable
configs = [
    eng_word_data(),
]
# fmt: on
