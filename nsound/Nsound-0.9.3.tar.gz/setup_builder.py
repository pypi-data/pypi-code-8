#!/usr/bin/env python

"""

$Id: setup_builder.py.in 893 2015-06-07 00:46:23Z weegreenblobbie $

This is a config file for python distutils to build Nsound as a Python module.

"""

import distutils.sysconfig
from distutils.core import setup, Extension
import os
import shutil

# Select compiler if defined in shell environment

CC = os.getenv('CC')
CXX = os.getenv('CXX')

if CXX:
    os.environ['CC'] = CXX

elif CC is None:

    # Use C++ compiler detected by scons

    os.environ['CC'] = "g++"

# Always delete CXX since it breaks the link step on Linux

if CXX is not None:
    del os.environ['CXX']

# Work around, copy swig/Nsound.py to current directory
swig_nsound_py = os.path.join("swig", "Nsound.py")
nsound_py = "Nsound.py"
shutil.copyfile(swig_nsound_py, nsound_py)

include_path       = [r'/usr/include/python2.7', r'/home/nhilton/development/nsound/nsound_ws/src', ]
library_path       = [r'/usr/lib/python2.7/config-x86_64-linux-gnu', ]
libraries          = ['ao', 'portaudio']
extra_compile_args = ['-std=c++11']
extra_link_args    = []
sources            = [
    r'swig/nsound_wrap.cxx',
    r'src/Nsound/AudioBackend.cc',
    r'src/Nsound/AudioBackendLibao.cc',
    r'src/Nsound/AudioBackendLibportaudio.cc',
    r'src/Nsound/AudioPlayback.cc',
    r'src/Nsound/AudioPlaybackRt.cc',
    r'src/Nsound/AudioStream.cc',
    r'src/Nsound/AudioStreamSelection.cc',
    r'src/Nsound/Buffer.cc',
    r'src/Nsound/BufferSelection.cc',
    r'src/Nsound/BufferWindowSearch.cc',
    r'src/Nsound/CircularBuffer.cc',
    r'src/Nsound/Clarinet.cc',
    r'src/Nsound/Cosine.cc',
    r'src/Nsound/DelayLine.cc',
    r'src/Nsound/DrumBD01.cc',
    r'src/Nsound/DrumKickBass.cc',
    r'src/Nsound/EnvelopeAdsr.cc',
    r'src/Nsound/FFTChunk.cc',
    r'src/Nsound/FFTransform.cc',
    r'src/Nsound/Filter.cc',
    r'src/Nsound/FilterAllPass.cc',
    r'src/Nsound/FilterBandPassFIR.cc',
    r'src/Nsound/FilterBandPassIIR.cc',
    r'src/Nsound/FilterBandPassVocoder.cc',
    r'src/Nsound/FilterBandRejectFIR.cc',
    r'src/Nsound/FilterBandRejectIIR.cc',
    r'src/Nsound/FilterCombLowPassFeedback.cc',
    r'src/Nsound/FilterDC.cc',
    r'src/Nsound/FilterDelay.cc',
    r'src/Nsound/FilterFlanger.cc',
    r'src/Nsound/FilterHighPassFIR.cc',
    r'src/Nsound/FilterHighPassIIR.cc',
    r'src/Nsound/FilterIIR.cc',
    r'src/Nsound/FilterLeastSquaresFIR.cc',
    r'src/Nsound/FilterLowPassFIR.cc',
    r'src/Nsound/FilterLowPassIIR.cc',
    r'src/Nsound/FilterMovingAverage.cc',
    r'src/Nsound/FilterParametricEqualizer.cc',
    r'src/Nsound/FilterPhaser.cc',
    r'src/Nsound/FilterSlinky.cc',
    r'src/Nsound/FilterStageIIR.cc',
    r'src/Nsound/FilterTone.cc',
    r'src/Nsound/FluteSlide.cc',
    r'src/Nsound/Generator.cc',
    r'src/Nsound/GeneratorDecay.cc',
    r'src/Nsound/Granulator.cc',
    r'src/Nsound/GuitarBass.cc',
    r'src/Nsound/Hat.cc',
    r'src/Nsound/Kernel.cc',
    r'src/Nsound/Mesh2D.cc',
    r'src/Nsound/MeshJunction.cc',
    r'src/Nsound/Mixer.cc',
    r'src/Nsound/MixerNode.cc',
    r'src/Nsound/OrganPipe.cc',
    r'src/Nsound/Plotter.cc',
    r'src/Nsound/Pluck.cc',
    r'src/Nsound/Pulse.cc',
    r'src/Nsound/ReverberationRoom.cc',
    r'src/Nsound/RngTausworthe.cc',
    r'src/Nsound/Sawtooth.cc',
    r'src/Nsound/Sine.cc',
    r'src/Nsound/Spectrogram.cc',
    r'src/Nsound/Square.cc',
    r'src/Nsound/StreamOperators.cc',
    r'src/Nsound/Stretcher.cc',
    r'src/Nsound/TicToc.cc',
    r'src/Nsound/Triangle.cc',
    r'src/Nsound/Utils.cc',
    r'src/Nsound/Vocoder.cc',
    r'src/Nsound/Wavefile.cc',]
download_url       = 'http://sourceforge.net/projects/nsound/files/nsound/nsound-0.9.3/nsound-0.9.3.tar.gz/download'

nsound_module = Extension(
    '_Nsound',
    extra_compile_args = extra_compile_args,
    extra_link_args    = extra_link_args,
    include_dirs       = include_path,
    language           = 'c++',
    libraries          = libraries,
    library_dirs       = library_path,
    sources            = sources,
)

setup(
    name    = "Nsound",
    version = "0.9.3",
    author  = "Nick Hilton et al",
    author_email = "weegreenblobbie@yahoo.com",

    description = \
"""    Nsound is a C++ library and Python module for audio synthesis
    featuring dynamic digital filters. Nsound lets you easily shape
    waveforms and write to disk or plot them. Nsound aims to be as
    powerful as Csound but easy to use.
""",

    py_modules = ["Nsound"],
    ext_modules = [nsound_module],

    url = "http://nsound.sourceforge.net",
    download_url = download_url,
)

# Workaround cleanup
os.remove(nsound_py)


# :mode=python: