from fastai2.data.all import *
from fastai2.vision.all import *
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