# AUTOGENERATED! DO NOT EDIT! File to edit: dev/05_Masks.ipynb (unless otherwise specified).

__all__ = ['safe_div', 'MaskBase', 'MaskBinary', 'MaskcIRM', 'Maskify']

# Cell
from .imports import *
from .plot import *
from .utils import *
from .base import *
from .core import *

# Cell
def safe_div(x,y):
    return np.divide(x,y, out=np.zeros_like(x.data), where=y!=0)

# Cell
class MaskBase():
    _show_args={}
    def __init__(self, data): store_attr(self, 'data')
    @property
    def shape(self):
        return self.data.shape
    @classmethod
    def create(cls, specs, mix_spec):
        return [cls.generate(spec, mix_spec) for spec in specs]
    def __mul__(self, spec):
        raise NotImplementedError('This function needs to be implemented before use')
    def __rmul__(self, spec):
        return self*spec
    def generate(self, spec, mix_spec):
        raise NotImplementedError('This function needs to be implemented before use')
    @delegates(setup_graph)
    def show(self, ctx=None, **kwargs): return show_mask(self, ctx=ctx, **merge(self._show_args, kwargs))


# Cell
class MaskBinary(MaskBase):
    def __init__(self, data, threshold=1):
        store_attr(self, 'data')
    def __mul__(self, spec):
        new_spec = SpecBase(spec.data*self.data, spec.sr, spec.fn)
        return new_spec
    @classmethod
    def generate(cls, spec, mix_spec):
        Binary = (safe_div(abs(spec.data),abs(mix_spec.data)) >= 1)*1
        return cls(Binary)

# Cell
class MaskcIRM(MaskBase):
    def __mul__(self, spec):
        return SpecBase(spec.data*self.data, spec.sr)

    @classmethod
    def generate(cls, spec, mix_spec):
        cIRM = safe_div(spec.data, mix_spec.data)
        return cls(cIRM)

# Cell
class Maskify(TupleTransform):
    as_item_force=True
    def __init__(self, MaskType=MaskcIRM, Aud2Spec=Spectify()):
        store_attr(self, "MaskType, Aud2Spec")
    def encodes(self, audioList)->None:
        specList = [self.Aud2Spec(a) for a in audioList]
        joined = AudioBase(join_audios(audioList), audioList[0].sr)
        mix_spec = self.Aud2Spec(joined)
        maskList = self.MaskType.create(specList, mix_spec)
        for m in maskList:
            self.Aud2Spec.decode(mix_spec*m).listen()
        return mix_spec, maskList
    def decodes(self, spec_mask)->None:
        mix_spec, maskList = spec_mask
        self.Aud2Spec.decode(mix_spec).listen()
        for m in maskList:
            self.Aud2Spec.decode(mix_spec*m).listen()
        return [self.Aud2Spec.decode(spec*m) for m in maskList]