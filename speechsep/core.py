# AUTOGENERATED! DO NOT EDIT! File to edit: dev/00_core.ipynb (unless otherwise specified).

__all__ = ['load_audio', 'AudioMono', 'duration', 'SpecImage', 'MaskBinary', 'MaskcIRM', 'show_batch', 'show', 'show',
           'show', 'ArrayAudioBase', 'ArraySpecBase', 'ArrayMaskBase', 'TensorAudio', 'TensorSpec', 'TensorMask',
           'encodes', 'encodes', 'encodes', 'audio2tensor', 'spec2tensor', 'mask2tensor', 'Spectify', 'Decibelify',
           'Mel_Binify_lib', 'MFCCify', 'create', 'Resample', 'Clip', 'PhaseManager']

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
class MaskBinary(MaskBase):
    def __mul__(self, spec):
        new_spec = SpecImage(spec.data*self.data, spec.sr, spec.fn)
        return new_spec
    @classmethod
    def generate(cls, joined, spec):
        return cls((joined.data <= spec.data)*1)

# Cell
class MaskcIRM(MaskBase):
    def __mul__(self, spec):
        new_spec = SpecImage(spec.data*self.data, spec.sr, spec.fn)
        return new_spec
    @classmethod
    def generate(cls, joined, spec):
        return cls((joined.data <= spec.data)*1)

# Cell
@typedispatch
def show_batch(x:(AudioBase, SpecBase, MaskBase), y, samples, ctxs=None, max_n=10, rows=None, cols=None, figsize=None, **kwargs):
    if ctxs is None: ctxs = get_grid(min(len(samples), max_n), rows=rows, cols=cols, figsize=figsize)
    ctxs = show_batch[object](x, y, samples, ctxs=ctxs, max_n=max_n, **kwargs)
    return ctxs

@patch
@delegates(Line2D)
def show(x:AudioBase, ctx=None, **kwargs): return show_audio(x, ctx=ctx, **merge(x._show_args, kwargs))

@patch
@delegates(setup_graph)
def show(x:SpecImage, ctx=None, **kwargs): return show_spec(x, ctx=ctx, **merge(x._show_args, kwargs))

@patch
@delegates(setup_graph)
def show(x:MaskBase, ctx=None, **kwargs): return show_mask(x, ctx=ctx, **merge(x._show_args, kwargs))

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
AudioMono._tensor_cls = TensorAudio
SpecImage._tensor_cls = TensorSpec
MaskBase._tensor_cls = TensorMask
@ToTensor
def encodes(self, o:AudioBase): return o._tensor_cls(audio2tensor(o))
@ToTensor
def encodes(self, o:SpecBase): return o._tensor_cls(spec2tensor(o))
@ToTensor
def encodes(self, o:MaskBase):  return o._tensor_cls(mask2tensor(o))

def audio2tensor(aud:AudioBase): return TensorAudio(aud.sig)
def spec2tensor(spec:SpecBase): return TensorSpec(spec.data)
def mask2tensor(mask:MaskBase):  return TensorMask(mask.data)

# Cell
class Spectify(Transform):
    def __init__(self, sr=48000, stft=stft, istft=istft):
        store_attr(self, 'sr, stft, istft')
    def encodes(self, audio:AudioMono):
        spec = self.stft(audio.sig)
        return SpecImage(spec, audio.sr, audio.fn)
    def decodes(self, spec:SpecBase):
        audio = self.istft(spec.data)
        return AudioMono(audio, spec.sr, spec.fn)
    def decodes(self, data:ArraySpecBase):
        return SpecImage(data, self.sr)

# Cell
class Decibelify(Transform):
    def __init__(self): pass
    def encodes(self,spec:SpecImage):
        spec.data = np.log(spec.data)
        return spec
    def decodes(self,spec:SpecImage):
        spec.data = np.exp(spec.data)
        return spec

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
@patch_clsmthd
@delegates(to=Spectify)
def create(cls:SpecImage, fn, sr=None, **kwargs):
    #Open an `Audio` from path `fn`
    if isinstance(fn,(Path,str)): return cls.create(AudioMono.create(fn,sr))
    elif isinstance(fn,AudioMono): return Spectify(**kwargs)(fn)
    raise ValueError('fn must be AudioMono, Path or str')

# Cell
class Resample(Transform):
    def __init__(self, sr): self.sr = sr
    def encodes(self, x:AudioBase): x.sr = self.sr; return x

# Cell
class Clip(Transform):
    def __init__(self, time): self.time = time
    def encodes(self, x:AudioBase):
        new_sig_len = int(self.time*x.sr)
        diff = abs(len(x.sig) - new_sig_len)
        if len(x.sig) <= new_sig_len:
            x.sig = np.pad(x.sig, (0,diff), 'constant', constant_values=(0, 0))
        else:
            x.sig = x.sig[:new_sig_len]
        return x

# Cell
class PhaseManager(Transform):
    def __init__(self, mthd="new_dim", cls=SpecImage):
        assert mthd in ['new_dim', 'remove', 'replace'], 'phase method must be either new_dim, remove or replace'
        store_attr(self, 'mthd, cls')

    def encodes(self, spec:SpecImage):
        if self.mthd == 'new_dim': return complex2real(spec)

    #BUG ArraySpecBase not Casting to return value
    def decodes(self, spec:TensorSpec)->ArraySpecBase:
        if self.mthd == 'new_dim':
            spec = real2complex(spec)
            #HACK not sure how else to get the output to be and ArraySpecBase
            # If this is removed Spectify would have to decode a numpy array and that's not always what we want.
            # If it doesn't find how to decode an ndarray it will try to show and ndarray doesn't have that function
            temp = ArraySpecBase(spec.shape, dtype=np.complex)
            temp[:,:] = spec
            return temp