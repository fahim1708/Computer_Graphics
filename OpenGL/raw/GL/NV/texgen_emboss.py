'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_texgen_emboss'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_texgen_emboss',error_checker=_errors._error_checker)
GL_EMBOSS_CONSTANT_NV=_C('GL_EMBOSS_CONSTANT_NV',0x855E)
GL_EMBOSS_LIGHT_NV=_C('GL_EMBOSS_LIGHT_NV',0x855D)
GL_EMBOSS_MAP_NV=_C('GL_EMBOSS_MAP_NV',0x855F)

