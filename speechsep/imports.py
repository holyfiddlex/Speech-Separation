from fastai.basics import *
from fastai.callback.all import *
from fastai.data.all import *
from fastai.vision.all import *
from functools import partial
from pathlib import Path
from nbdev.imports import test_eq

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from IPython.display import Audio, display

import math
import scipy
import numpy as np
from librosa import load
from scipy.signal import resample_poly