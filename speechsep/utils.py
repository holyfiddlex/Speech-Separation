#AUTOGENERATED! DO NOT EDIT! File to edit: dev/01_utils.ipynb (unless otherwise specified).

__all__ = ['time_bins', 'stft', 'istft']

#Cell
from .imports import *

#Cell
def time_bins(X, window_size, overlap):
    """
    Create an overlapped version of X
    Parameters
    ----------
    X : ndarray, shape=(n_samples,)
        Input signal to window and overlap
    window_size : int
        Size of windows to take
    window_step : int
        Step size between windows
    Returns
    -------
    X_strided : shape=(nun_windows, window_size)
        2D array of overlapped X
    """
    if window_size % 2 != 0:
        raise ValueError(f"Window size must be even! Recieved {window_size}")
    padding = np.zeros(int(window_size - len(X) % window_size))
    X = np.concatenate((X, padding))
    slide_length = int(window_size*(1-overlap))
    num_windows = (len(X) - window_size) // slide_length
    out = np.ndarray((num_windows,window_size),dtype = X.dtype)

    for i in range(num_windows):
        start = i * slide_length
        out[i] = X[start : start+window_size]
    return out

#Cell
def stft(X, fftsize=512, win_mult=2, overlap=0.5, normalize=False):
    """
    Compute STFT for 1D real valued input X
    """
    win_size = fftsize*win_mult
    X = time_bins(X, win_size, overlap)
    hanning = .54 - .46 * np.cos(2 * np.pi * np.arange(win_size) / (win_size - 1))
    X = X * hanning.reshape((1, win_size))
    X = np.fft.fft(X).T
    #X = np.fft.fft(X)[:win_size//2].T
    if normalize: X*=256/X.max()
    return X

#Cell
def istft(X, fftsize=512, win_mult=2, overlap=0.5, normalize=False):
    #X = np.concatenate((X, X[::-1]), axis=0)
    X = np.fft.ifft(X.T).real
    win_size = len(X[0])
    slider_length = int(win_size*(1-overlap))

    hanning = .54 - .46 * np.cos(2 * np.pi * np.arange(win_size) / (win_size - 1))
    X = X/hanning.reshape((1, win_size))

    inv_audio = X[0][0:win_size-slider_length]
    for i in range(len(X)):
        inv_audio = np.concatenate((inv_audio, X[i][-slider_length:]))
    return(inv_audio)