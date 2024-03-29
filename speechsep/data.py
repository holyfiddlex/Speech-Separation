# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev/03_data.ipynb (unless otherwise specified).

__all__ = ['get_audio_files', 'AudioBlock', 'audio_extensions']

# Cell
from .imports import *
from .core import *
from .masks import *

# Cell
audio_extensions = set(k for k,v in mimetypes.types_map.items() if v.startswith('audio/'))

def get_audio_files(path, recurse=True, folders=None):
    "Get image files in `path` recursively, only in `folders`, if specified."
    return get_files(path, extensions=audio_extensions, recurse=recurse, folders=folders)

def AudioBlock(cls=AudioMono): return TransformBlock(type_tfms=cls.create, batch_tfms=IntToFloatTensor)