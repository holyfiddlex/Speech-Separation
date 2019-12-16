#AUTOGENERATED! DO NOT EDIT! File to edit: dev/00_core.ipynb (unless otherwise specified).

__all__ = ['load_audio', 'ResampleSignal', 'AudioBase', 'AudioMono', 'duration', 'SpecImage', 'MaskBase', 'MaskBinary',
           'show_batch', 'pre_plot', 'post_plot', 'show', 'show_audio', 'show', 'show_spec', 'show', 'show_mask',
           'hear_audio', 'ArrayAudioBase', 'ArraySpecBase', 'ArrayMaskBase', 'TensorAudio', 'TensorSpec', 'TensorMask',
           'encodes', 'encodes', 'encodes', 'audio2tensor', 'spec2tensor', 'mask2tensor', 'Spectify', 'create',
           'Resample', 'Clip', 'PhaseManager', 'complex2real', 'real2complex']

#Cell
from .imports import *
from .utils import *
from .plot import *

#Cell
@delegates(load)
def load_audio(fn, **kwargs):
    return load(fn)

#Cell
def ResampleSignal(sr_new):
    def _inner(sig, sr):
        '''Resample using faster polyphase technique and avoiding FFT computation. Taken from FastaiAudio by LimeAI'''
        if(sr == sr_new): return sig
        sr_gcd = math.gcd(sr, sr_new)
        resampled = resample_poly(sig, int(sr_new/sr_gcd), int(sr/sr_gcd), axis=-1)
        #resampled = resampled.astype(np.float32)
        return resampled
    return _inner

#Cell
class AudioBase():
    _show_args={}
    def __init__(self,sig,_sr,fn=None):
        store_attr(self, 'sig,_sr,fn')
        self.data = self.sig
    def __repr__(self): self.listen(); return f'{self.__str__()}'
    def __str__(self): return f'{self.fn}, {self.duration}secs at {self.sr} samples per second'
    def listen(self): display(Audio(self.sig, rate=self.sr))
    @property
    def sr(self): return self._sr
    @sr.setter
    def sr(self, new_sr):
        if self._sr != new_sr: self.sig = ResampleSignal(new_sr)(self.sig, self.sr)
        self._sr = new_sr
    @property
    def duration(self): return len(self.sig)/self.sr

#Cell
class AudioMono(AudioBase):
    _show_args={}
    @classmethod
    def create(cls, fn, sr=None):
        audio = cls(*load_audio(fn),fn)
        if sr: audio.sr = sr
        return audio
    load_file = create

#Cell
@patch_property
def duration(x:AudioMono):
    return len(x.sig)/x.sr

#Cell
class SpecImage():
    _show_args={}
    def __init__(self, data, sr, fn=None):
        store_attr(self, 'data, sr, fn')
        self._plt_params = {}
    @property
    def plt_params(self): return self._plt_params
    @plt_params.setter
    @delegates(plt.pcolormesh)
    def plt_params(self, **kwargs):
        self._plot = partial(plt.pcolormesh, **kwargs)
        self._plt_params = dict(**kwargs)

#Cell
class MaskBase():
    def __init__(self, data):
        store_attr(self, 'data')
    @property
    def shape(self):
        return self.data.shape
    @classmethod
    def create(cls, audios):
        self.adjust(audios)
        joined = join_audios(audios)
        return [cls(self.generate(joined, aud)) for aud in audios]
    def adjust(self, audios):
        pass
    def __mult__(self, spec):
        raise NotImplementedError('This function needs to be implemented before use')
    def generate(self, joined, aud):
        raise NotImplementedError('This function needs to be implemented before use')

#Cell
class MaskBinary(MaskBase):
    def __mult__(self, spec): pass
    def __generate__(self, joined, aud): pass

#Cell
@typedispatch
def show_batch(x:(AudioBase, SpecImage, MaskBase), y, samples, ctxs=None, max_n=10, rows=None, cols=None, figsize=None, **kwargs):
    if ctxs is None: ctxs = get_grid(min(len(samples), max_n), rows=rows, cols=cols, figsize=figsize)
    ctxs = show_batch[object](x, y, samples, ctxs=ctxs, max_n=max_n, **kwargs)
    return ctxs

def pre_plot(o, cls, ax=None, pltsize=None, ctx=None):
    ax = ifnone(ax,ctx)
    if ax is None: _,ax = plt.subplots(figsize=pltsize)
    if isinstance(o, cls): o = o.data;
    elif not isinstance(o,np.ndarray): o=array(o)
    return ax, o

def post_plot(ax, title, x_label, y_label, axis=False):
    if title is not None: ax.set_title(title)
    if x_label is not None: ax.set_xlabel(x_label)
    if y_label is not None: ax.set_ylabel(y_label)
    if not axis: ax.axis('off')
    return ax

@patch
@delegates(Line2D)
def show(x:AudioBase, ctx=None, **kwargs): return show_audio(x, ctx=ctx, **merge(x._show_args, kwargs))

@delegates(plt.plot)
def show_audio(aud, ax=None, pltsize=None, title=None, ctx=None, x_label=None, y_label=None, axis=False, **kwargs):
    ax, aud = pre_plot(aud, AudioBase, ax, pltsize, ctx)
    ax.plot(aud, **kwargs)
    return post_plot(ax, title, x_label, y_label, axis)

@patch
@delegates(setup_graph)
def show(x:SpecImage, ctx=None, **kwargs): return show_spec(x, ctx=ctx, **merge(x._show_args, kwargs))

@delegates(plt.pcolormesh)
def show_spec(spec, ax=None, pltsize=None, title=None, ctx=None, x_label=None, y_label=None, axis=False, **kwargs):
    ax, spec = pre_plot(spec, SpecImage, ax, pltsize, ctx)
    ax.pcolormesh(np.abs(spec.data[:spec.data.shape[0]//2]), **kwargs)
    return post_plot(ax, title, x_label, y_label, axis)

@patch
@delegates(setup_graph)
def show(x:MaskBase, ctx=None, **kwargs): return show_mask(x, ctx=ctx, **merge(x._show_args, kwargs))

@delegates(plt.pcolormesh)
def show_mask(mask, ax=None, pltsize=None, title=None, ctx=None, x_label=None, y_label=None, axis=False, **kwargs):
    ax, mask = pre_plot(mask)
    ax.pcolormesh(maks, **kwargs)
    return post_plot(ax, title, x_label, y_label, axis)

#Cell
def hear_audio(aud, sr=48000, **kwargs):
    if isinstance(aud, AudioBase):  display(Audio(aud.sig, rate=aud.sr))
    else:                           display(Audio(aud, rate=sr))

#Cell
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

#Cell
AudioMono._tensor_cls = TensorAudio
SpecImage._tensor_cls = TensorSpec
MaskBase._tensor_cls = TensorMask
@ToTensor
def encodes(self, o:AudioBase): return o._tensor_cls(audio2tensor(o))
@ToTensor
def encodes(self, o:SpecImage): return o._tensor_cls(spec2tensor(o))
@ToTensor
def encodes(self, o:MaskBase):  return o._tensor_cls(mask2tensor(o))

def audio2tensor(aud:AudioBase): return TensorAudio(aud.sig)
def spec2tensor(spec:SpecImage): return TensorSpec(spec.data)
def mask2tensor(mask:MaskBase):  return TensorMask(mask.data)

#Cell
class Spectify(Transform):
    def __init__(self, sr=48000, fftsize=512, win_mult=2, overlap=0.5, decibel=False, mel_bin=False):
        store_attr(self, 'sr, fftsize, win_mult, overlap, decibel, mel_bin')
    def encodes(self, audio:AudioMono):
        spec = stft(audio.sig, self.fftsize, self.win_mult, self.overlap)
        if self.decibel: pass #TODO Encode
        if self.mel_bin: pass #TODO Encode
        return SpecImage(spec, audio.sr, audio.fn)
    def decodes(self, spec:SpecImage):
        if self.mel_bin: pass #TODO Decode
        if self.decibel: pass #TODO Decode
        audio = istft(spec.data, self.fftsize, self.win_mult, self.overlap)
        return AudioMono(audio, spec.sr, spec.fn)
    def decodes(self, data:ArraySpecBase):
        if self.mel_bin: pass #TODO Decode
        if self.decibel: pass #TODO Decode
        return SpecImage(data, self.sr)

#Cell
@patch_clsmthd
@delegates(to=Spectify)
def create(cls:SpecImage, fn, sr=None, **kwargs):
    #Open an `Audio` from path `fn`
    if isinstance(fn,(Path,str)): return cls.create(AudioMono.create(fn,sr))
    elif isinstance(fn,AudioMono): return Spectify(**kwargs)(fn)
    raise ValueError('fn must be AudioMono, Path or str')

#Cell
class Resample(Transform):
    def __init__(self, sr): self.sr = sr
    def encodes(self, x:AudioBase): x.sr = self.sr; return x

#Cell
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

#Cell
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


def complex2real(spec):
    if np.iscomplexobj(spec.data):
        spec.data = np.concatenate((spec.data.real[..., np.newaxis], spec.data.imag[..., np.newaxis]), axis=-1)
        spec.data = spec.data.T
    return spec

def real2complex(data):
    data = data.numpy().T
    return data[..., 0] + data[..., 1]*1j