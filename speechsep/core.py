#AUTOGENERATED! DO NOT EDIT! File to edit: dev/00_core.ipynb (unless otherwise specified).

__all__ = ['load_audio']

#Cell
import fastai2.vision.core as core
import fastai2.vision.data as data
import fastai2.torch_basics as basics

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.io.wavfile
import IPython

from librosa import load
from IPython.display import Audio, display

import speechsep.utils as utils
import speechsep.plot as plot

#Cell
def load_audio(fn, **kwargs):
    return load(fn)