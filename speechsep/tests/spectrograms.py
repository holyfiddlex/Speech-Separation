import numpy as np
from scipy.io import wavfile
# from scipy.signal import stft, istft
# from scipy.signal import spectrogram
from librosa.core.spectrum import griffinlim
from librosa.core import stft, istft
import matplotlib.pyplot as plt

AUDIO_FILE = "data/AudioTest1_full.wav"

def create_spec_from_file(file_name):
    sample_rate, data = wavfile.read(file_name)
    wavfile.write("data/test.wav", sample_rate, data)
    spectrogram = stft(data[:,0].astype(np.float))
    return spectrogram, sample_rate

def save_spectrogram_to_file(spectrogram, sample_rate):
    data2 = istft(spectrogram)
    wavfile.write("data/test2.wav", sample_rate, data2)

if __name__ == '__main__':
    spectrogram, sample_rate = create_spec_from_file(AUDIO_FILE)
    
    # plt.pcolormesh(range(len(spectrogram[0])), range(len(spectrogram)), np.abs(spectrogram))
    # plt.show()

    spectrogram[:10,:] = 0
    print(spectrogram[0,0])
    # plt.pcolormesh(range(len(spectrogram[0])), range(len(spectrogram)), np.abs(spectrogram))
    # plt.show()

    save_spectrogram_to_file(spectrogram, sample_rate)