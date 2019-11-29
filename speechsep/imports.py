import fastai2.vision.core as core
import fastai2.vision.data as data
import fastai2.torch_basics as basics
from functools import partial
from pathlib import Path
from nbdev.tools import *
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