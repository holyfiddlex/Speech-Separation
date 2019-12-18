#AUTOGENERATED! DO NOT EDIT! File to edit: dev/02_plot.ipynb (unless otherwise specified).

__all__ = ['setup_graph', 'ColorMeshPlotter', 'cmap_dict', 'cmap', 'pre_plot', 'post_plot', 'show_audio', 'show_spec',
           'show_mask', 'hear_audio']

#Cell
from .imports import *
from .base import *

#Cell
def setup_graph(title='', x_label='', y_label='', fig_size=None):
    fig = plt.figure()
    if fig_size != None:
        fig.set_size_inches(fig_size[0], fig_size[1])
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

#Cell
class ColorMeshPlotter():
    def __init__(self, **kwargs):
        self._plot = partial(plt.pcolormesh, **kwargs)
    def __call__(self, spec, title='', x_label='', y_label='', fig_size=None):
        setup_graph(title=title, x_label=x_label, y_label=y_label, fig_size=fig_size)
        self._plot(abs(spec[:spec.shape[0]//2]))

#Cell
cmap_dict = {'red':  ((0.0, 0.0156, 0.0156),
                      (0.3, 1.0, 1.0),
                      (0.6, 1.0, 1.0),
                      (1.0, 1.0, 1.0)),
             'green':((0.0, 0.125, 0.125),
                       (0.3, 1.0, 1.0),
                       (0.6, 1.0, 1.0),
                       (1.0, 1.0, 0.0)),
             'blue': ((0.0, 0.25, 0.25),
                      (0.3, 1.0, 1.0),
                      (0.6, 0.17, 0.17),
                      (1.0, 0.0, 0.0))}
cmap = matplotlib.colors.LinearSegmentedColormap(None,cmap_dict,256)

#Cell
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

#Cell
@delegates(plt.plot)
def show_audio(aud, ax=None, pltsize=None, title=None, ctx=None, x_label=None, y_label=None, axis=False, **kwargs):
    ax, aud = pre_plot(aud, AudioBase, ax, pltsize, ctx)
    ax.plot(aud, **kwargs)
    return post_plot(ax, title, x_label, y_label, axis)

#Cell
@delegates(plt.pcolormesh)
def show_spec(spec, ax=None, pltsize=None, title=None, ctx=None, x_label=None, y_label=None, axis=False, **kwargs):
    ax, spec = pre_plot(spec, SpecBase, ax, pltsize, ctx)
    ax.pcolormesh(np.abs(spec.data[:spec.data.shape[0]//2]), **kwargs)
    return post_plot(ax, title, x_label, y_label, axis)

#Cell
@delegates(plt.pcolormesh)
def show_mask(mask, ax=None, pltsize=None, title=None, ctx=None, x_label=None, y_label=None, axis=False, **kwargs):
    ax, mask = pre_plot(mask, MaskBase, ax, pltsize, ctx)
    ax.pcolormesh(mask, **kwargs)
    return post_plot(ax, title, x_label, y_label, axis)

#Cell
def hear_audio(aud, sr=48000, **kwargs):
    if isinstance(aud, AudioBase):  display(Audio(aud.sig, rate=aud.sr))
    else:                           display(Audio(aud, rate=sr))