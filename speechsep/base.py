# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev/00b_core.base.ipynb (unless otherwise specified).

__all__ = ['ResampleSignal', 'AudioBase', 'SpecBase', 'show_batch']

# Cell
from .imports import *
from .plot import *

# Cell
def ResampleSignal(sr_new):
    def _inner(sig, sr):
        '''Resample using faster polyphase technique and avoiding FFT computation. Taken from FastaiAudio by LimeAI'''
        if(sr == sr_new): return sig
        sr_gcd = math.gcd(sr, sr_new)
        resampled = resample_poly(sig, int(sr_new/sr_gcd), int(sr/sr_gcd), axis=-1)
        #resampled = resampled.astype(np.float32)
        return resampled
    return _inner

# Cell
class AudioBase():
    _show_args={}
    def __init__(self,sig,_sr,fn=None):
        store_attr(self, 'sig,_sr,fn')
    def __repr__(self): self.listen(); return f'{self.__str__()}'
    def __str__(self): return f'{self.fn}, {self.duration}secs at {self.sr} samples per second'
    def listen(self): display(Audio(self.sig, rate=self.sr))
    @property
    def data(self): return self.sig
    @data.setter
    def data(self, new_data): self.sig = new_data
    @property
    def sr(self): return self._sr
    @sr.setter
    def sr(self, new_sr):
        if self._sr != new_sr: self.sig = ResampleSignal(new_sr)(self.sig, self.sr)
        self._sr = new_sr
    @property
    def duration(self): return len(self.sig)/self.sr
    @delegates(Line2D)
    def show(self, ctx=None, **kwargs): return show_audio(self, ctx=ctx, **merge(self._show_args, kwargs))

# Cell
class SpecBase():
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
    @delegates(setup_graph)
    def show(self, ctx=None, **kwargs): return show_spec(self, ctx=ctx, **merge(self._show_args, kwargs))

# Cell
@typedispatch
def show_batch(x:(AudioBase, SpecBase), y, samples, ctxs=None, max_n=10, rows=None, cols=None, figsize=None, **kwargs):
    if ctxs is None: ctxs = get_grid(min(len(samples), max_n), rows=rows, cols=cols, figsize=figsize)
    ctxs = show_batch[object](x, y, samples, ctxs=ctxs, max_n=max_n, **kwargs)
    return ctxs