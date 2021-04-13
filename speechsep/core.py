# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev/00_core.ipynb (unless otherwise specified).

__all__ = ['load_audio', 'AudioMono', 'duration', 'SpecImage', 'ArrayAudioBase', 'ArraySpecBase', 'ArrayMaskBase',
           'TensorAudio', 'TensorSpec', 'TensorMask', 'Spectify', 'Decibelify', 'Mel_Binify_lib', 'MFCCify', 'create',
           'encodes', 'encodes', 'audio2tensor', 'spec2tensor', 'Resample', 'Clip', 'Normalize', 'PhaseManager']

# Cell
from .imports import *
from .utils import *
from .plot import *
from .base import *

# Cell
load_audio = load

# Cell
class AudioMono(AudioBase):
    _show_args={}
    @classmethod
    def create(cls, fn:Path, sr=None):
        audio = cls(*load_audio(fn),fn)
        if sr: audio.sr = sr
        return audio
    load_file = create

# Cell
@patch_property
def duration(x:AudioMono):
    return len(x.sig)/x.sr

# Cell
class SpecImage(SpecBase): pass

# Cell
class ArrayAudioBase(ArrayBase):
    _show_args = {}
    def show(self, **kwargs):
        return show_audio(self, ctx=ctx, **{**self._show_args, **kwargs})

class ArraySpecBase(ArrayBase):
    _show_args = {}
    def show(self, **kwargs):
        return show_spec(self, ctx=ctx, **{**self._show_args, **kwargs})

class ArrayMaskBase(ArrayBase):
    _show_args = {}
    def show(self, **kwargs):
        return show_mask(self, ctx=ctx, **{**self._show_args, **kwargs})

class TensorAudio(TensorBase):
    _show_args = ArrayAudioBase._show_args
    def show(self, ctx=None, **kwargs):
        return show_audio(self, ctx=ctx, **{**self._show_args, **kwargs})

class TensorSpec(TensorBase):
    _show_args = ArraySpecBase._show_args
    def show(self, ctx=None, **kwargs):
        return show_spec(self, ctx=ctx, **{**self._show_args, **kwargs})

class TensorMask(TensorBase):
    _show_args = ArrayMaskBase._show_args
    def show(self, ctx=None, **kwargs):
        return show_mask(self, ctx=ctx, **{**self._show_args, **kwargs})

# Cell
class Spectify(Transform):
    def __init__(self, sr=48000, stft=stft, istft=istft):
        store_attr('sr, stft, istft', self)
    def encodes(self, audio:AudioBase):
        spec = self.stft(audio.sig)
        return SpecImage(spec, audio.sr, audio.fn)
    def decodes(self, spec:SpecBase):
        audio = self.istft(spec.data)
        return AudioBase(audio, spec.sr, spec.fn)
    def decodes(self, data:ArraySpecBase):
        return SpecImage(data, self.sr)

# Cell
class Decibelify(Transform):
    def encodes(self,spec:SpecBase):
        np.seterr(divide='ignore'); new_data = np.log10(spec.data); np.seterr(divide='warn')
        noise = randomComplex(spec.data.shape)*0.0001
        filt1 = np.isinf(new_data)
        filt2 = np.isnan(new_data)
        new_data = np.where(filt1, 0, new_data)+noise
        if np.isnan(new_data).any():
            print(f"WARNING {np.sum(np.isnan(new_data))} NANS FOUND DECIBELIFY")
        new_data = np.where(filt2, 0, new_data)+noise
        return type(spec)(new_data, spec.sr, spec.fn)

    def decodes(self,spec:SpecBase):
        new_data = np.power(10, spec.data)
        return type(spec)(new_data, spec.sr, spec.fn)

# Cell
class _Decibelify_old(Transform):
    def encodes(self,spec:SpecBase):
        new_data = np.log10(spec.data)
        return type(spec)(new_data, spec.sr, spec.fn)

    def decodes(self,spec:SpecBase):
        new_data = np.power(10, spec.data)
        return type(spec)(new_data, spec.sr, spec.fn)

# Cell
from librosa.feature import melspectrogram
class Mel_Binify_lib(Transform):
    @delegates(melspectrogram)
    def __init__(self, **kwargs):
        self.audio2mel = partial(melspectrogram, **kwargs)
    def encodes(self,audio:AudioBase):
        spec = self.audio2mel(audio.sig, audio.sr)
        return SpecImage(spec, audio.sr)

# Cell
from librosa.feature import mfcc
class MFCCify(Transform):
    @delegates(mfcc)
    def __init__(self, **kwargs):
        self.audio2mfcc = partial(mfcc, **kwargs)
    def encodes(self,audio:AudioBase):
        spec = self.audio2mfcc(audio.sig, audio.sr)
        return SpecImage(spec, audio.sr)

# Cell
@delegates(to=Spectify)
def create(cls:SpecImage, fn, sr=None, **kwargs):
    #Open an `Audio` from path `fn`
    if isinstance(fn,(Path,str)): return cls.create(AudioMono.create(fn,sr))
    elif isinstance(fn,AudioMono): return Spectify(**kwargs)(fn)
    raise ValueError('fn must be AudioMono, Path or str')

SpecImage.create = classmethod(create)

# Cell
AudioMono._tensor_cls = TensorAudio
SpecImage._tensor_cls = TensorSpec

@ToTensor
def encodes(self, o:AudioBase): return o._tensor_cls(audio2tensor(o))
@ToTensor
def encodes(self, o:SpecBase): return o._tensor_cls(spec2tensor(o))

def audio2tensor(aud:AudioBase): return TensorAudio(aud.sig)
def spec2tensor(spec:SpecBase):
    data = complex2real(spec.data)
    return TensorSpec(data)

# Cell
class Resample(Transform):
    def __init__(self, sr): self.sr = sr
    def encodes(self, x:AudioBase): x.sr = self.sr; return x

# Cell
class Clip(Transform):
    def __init__(self, time): self.time = time
    def encodes(self, x:AudioBase):
        new_sig_len = int(self.time*x.sr)
        if len(x.sig) <= new_sig_len:
            x.sig = fill(x.sig, new_sig_len)
        else:
            x.sig = x.sig[:new_sig_len]
        return x

# Cell
class Normalize(Transform):
    #normalize based on highest peak
    def encodes(self, x:SpecBase):
        ratio = np.max(np.abs(x.data))
        norm = x.data/ratio
        return type(x)(norm, x.sr, x.fn)

# Cell
class PhaseManager(Transform):
    def __init__(self, mthd="new_dim", cls=SpecImage):
        assert mthd in ['new_dim', 'remove', 'replace'], 'phase method must be either new_dim, remove or replace'
        store_attr('mthd, cls', self)

    def encodes(self, spec:SpecImage):
        if self.mthd == 'new_dim': return complex2real(spec)

    #BUG ArraySpecBase not Casting to return value
    def decodes(self, spec:TensorSpec)->ArraySpecBase:
        if self.mthd == 'new_dim':
            data = real2complex(spec.data)
            #HACK not sure how else to get the output to be and ArraySpecBase
            # If this is removed Spectify would have to decode a numpy array and that's not always what we want.
            # If it doesn't find how to decode an ndarray it will try to show and ndarray doesn't have that function
            temp = ArraySpecBase(spec.shape, dtype=np.complex)
            temp[:,:] = data
            return temp