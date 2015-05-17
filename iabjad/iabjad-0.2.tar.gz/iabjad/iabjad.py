
# coding: utf-8

# # Abjad Display in Jupyter Notebooks

# In[ ]:

def isIPython():
    try:
        __IPYTHON__
        return True
    except:
        return False


# ## Imports

# Standard library imports:

# In[ ]:

import os
import shutil
import subprocess
import tempfile


# Abjad imports:

# In[ ]:

from abjad.tools import topleveltools
from abjad import *


# If the module is being run from an IPython notebook, we want to import functions that allow us to visualize the typeset music directly in the notebook.

# In[ ]:

if isIPython():
    from IPython.core.display import display_png, display_svg, display_pdf


# ## Graphics

# In[ ]:

# Code inspired by:
#  https://github.com/tiagoantao/abjad-ipython/blob/master/src/abjad-nb.py
def _get_imgs(expr, fmt, lily_opts, trim_cmd=None):
    """Calls lilypond and converts output to (multi-page) Images.
    with given file format.
    """
    imgs = []
    tmpdir = tempfile.mkdtemp()
    # Prints the score into a LilyPond file 
    agent = topleveltools.persist(expr)
    ly_file_path = os.path.join(tmpdir, 'out.ly')
    result = agent.as_ly(ly_file_path)
    
    outpath = os.path.join(tmpdir, 'out')
    # Compile the score into the chosen format (determined by 'lily_opts')
    result = subprocess.call(['lilypond'] + lily_opts + ['-o', outpath, ly_file_path])
    # Is the output a single page?
    try:
        input_img_paths = [tmpdir + os.sep + 'out.{}'.format(fmt)]
    # Is the output in multiple pages? Some formats, like PNG and SVG don't support
    # more than one page
    except:
        # We are going to send all pages
        input_img_paths = []
        for i in range(1000):  # Lets hope you do not have more than 1000 pages
            #  When multiple pages are generated, the filename is generated
            # according to the format string below:
            input_path = tmpdir + os.sep + 'out-page{}.{}'.format((i + 1), fmt)
            if os.path.isfile(input_path):
                input_img_paths.append(input_path)
            else:
                if i == 0:  # No images
                    raise
                else:
                    break

    for input_path in input_img_paths:
        if trim_cmd:
            subprocess.call(trim_cmd(input_path))
        
        with open(input_path, 'rb') as f:
            img = f.read()
            imgs.append(img)
            
    # Remove the temporary directory and its contents
    shutil.rmtree(tmpdir)
    return imgs


# The function `_get_preview()` uses the lilypond `-dpreview=#t` option to automatically crop the image, without the need for external programs. Unfortunately, this only works if the score corresponds to a single system.
# The fact that this function doesn't rely on any external program makes it much faster and more convenient to use.

# In[ ]:

def _get_preview(expr, fmt, lily_opts):
    tmpdir = tempfile.mkdtemp()
    # Prints the score into a LipyPond file 
    agent = topleveltools.persist(expr)
    ly_file_path = os.path.join(tmpdir, 'out.ly')
    result = agent.as_ly(ly_file_path)
    
    # Compile the score into the chosen format (determined by 'lily_opts')
    outpath = os.path.join(tmpdir, 'out')
    result = subprocess.call(['lilypond'] + lily_opts +                              ['-dpreview=#t', # crop the score
                              '-o', outpath, ly_file_path])
    
    input_img_path = os.path.join(tmpdir, 'out.preview.{}'.format(fmt))
    
    with open(input_img_path, 'rb') as f:
        img = f.read()
    
    # Remove the temporary directory and its contents
    shutil.rmtree(tmpdir)
    return img


# ### Handle Different Backends

# #### PNG

# In[ ]:

_png_lily_opts = ['--png']

def _get_pngs(expr):
    def png_trim_cmd(in_):
        return ['convert', in_, '-trim', in_]
    return _get_imgs(expr, fmt='png', lily_opts=_png_lily_opts, trim_cmd=png_trim_cmd)


# #### SVG

# In[ ]:

_svg_lily_opts = ['-dbackend=svg', '-dpoint-and-click=#f']

def _get_svgs(expr):
    def svg_trim_cmd(in_):
        #  Unfortunately, it is impossible to supress the GUI
        # when using Inkscape from the command line, which is
        # extremely annoying.
        return ['inkscape', '--verb=FitCanvasToDrawing',
                            '--verb=FileSave',
                            '--verb=FileQuit',
                            in_]
    return _get_imgs(expr, fmt='svg',
                     lily_opts=_svg_lily_opts,
                     trim_cmd=svg_trim_cmd)


# #### PDF

# In[ ]:

_pdf_lily_opts = ['--pdf']

def _get_pdfs(expr):
    def pdf_trim_cmd(in_):
        return ['convert', in_, '-trim', in_]
    return _get_imgs(expr, fmt='pdf', lily_opts=_pdf_lily_opts, trim_cmd=pdf_trim_cmd)

# Get PDF as a single file
def _get_pdf_pages(expr):
    return _get_imgs(expr, fmt='pdf', lily_opts=_pdf_lily_opts, trim_cmd=None)


# ### Showing a Score in IPython
# 
# These functions are meant to be used only in IPython (in a Jupyter notebook, for example).
# They are only accessible if the user is in fact loading the module from an IPython session.
# 
# Two variants are defined:
# 
# - `ishow()`: this is the most general function. It can be used to display any kind of score.
#      On the other hand, it depends on using an external program, such as ImageMagick or Inkscape
#      to crop the images, which makes it rather slow and inconvenient.
#      The advantage is that it can display multi-page scores in the notebook.
#      
# - `ishow_preview()` or its synonym `ishow_()`: this function displays only the first system of the score.
#       It is not dependent on any external program to crop the image, and as a result is much faster and
#       more convenient.
#       If you're sure your score fits in a single system, this is the function to use.
#       
# These functions all take the same arguments:
# 
# - `expr`, a music expression (like a [`Score`](http://abjad.mbrsi.org/api/tools/scoretools/Score.html),
#     a [`Staff`](http://abjad.mbrsi.org/api/tools/scoretools/Staff.html),
#     a [`Voice`](http://abjad.mbrsi.org/api/tools/scoretools/Voice.html) or
#     a [`LilyPondFile`](http://abjad.mbrsi.org/api/tools/lilypondfiletools/LilyPondFile.html))
# - `fmt`, the file format to use when rendering the score
# - `pdf`, a boolean parameter that controls whether a link to a PDF is added after the score.
#     This is useful if you want to provide a printable copy of the score.

# In[ ]:

if isIPython():
    def ishow_preview(expr, fmt='svg', pdf=False):
        """A replacement for Ajbad's show function for IPython Notebook
           Optimized for speed; Renders only the first system of the score.
        """
        assert '__illustrate__' in dir(expr)
        
        if fmt == 'png':
            png = _get_preview(expr, 'png', _png_lily_opts)
            display_png(png, raw=True)

        if fmt == 'svg':
            svg = _get_preview(expr, 'svg', _svg_lily_opts)
            display_svg(svg, raw=True)

        if fmt == 'pdf':
            pdf = _get_preview(expr, 'pdf', _pdf_lily_opts)
            display_pdf(pdf, raw=True)
        
        #  Unless we are only generating a PDF, we may want to
        # include a link to a pdf file, so that the user
        # can whatch the score in high quality, suitable for
        # printing.
        #  The IPython display_pdf() function generates a link
        # to the embedded PDF file, suitable for printing.
        if fmt != 'pdf' and pdf:
            pdfs = _get_pdf_pages(expr)
            for pdf in pdfs:
                display_pdf(pdf, raw=True)
    
    def ishow_(expr, fmt='svg', pdf=False):
        """Alias for 'ishow_preview'. Saves some typing."""
        return ishow_preview(expr, fmt, pdf)
        
        
    def ishow(expr, fmt='png', pdf=True):
        """A replacement for Ajbad's show function for IPython Notebook"""
        assert '__illustrate__' in dir(expr)

        if fmt == 'png':
            pngs = _get_pngs(expr)
            for png in pngs:
                display_png(png, raw=True)

        if fmt == 'svg':
            svgs = _get_svgs(expr)
            for svg in svgs:
                display_svg(svg, raw=True)

        if fmt == 'pdf':
            pdfs = _get_pdfs(expr)
            for pdf in pdfs:
                display_pdf(pdf, raw=True)

        #  Unless we are only generating a PDF, we want to
        # include a link to a pdf file, so that the user
        # can whatch the score in high quality, suitable for
        # printing.
        #  The IPython display_pdf() function generates a link
        # to the embedded PDF file, suitable for printing.
        if fmt != 'pdf' and pdf:
            pdfs = _get_pdf_pages(expr)
            for pdf in pdfs:
                display_pdf(pdf, raw=True)


# ### Exporting the Score
# 
# These functions are meant to be used either in a notebook or from vanilla Python.
# They are meant to export (or render) the score to a file.
# The file format is taken from the extension in the filename.
# 
# Th functions are analogous to the `ishow()`, `ishow_()`, and `ishow_preview()` functions:
# 
# - `export()`: this is the most general function. It can be used to export any kind of score.
#      On the other hand, like `ishow()`, it depends on using an external program, such as ImageMagick or Inkscape
#      to crop the images, which makes it rather slow and inconvenient.
#      The advantage is that it can display multi-page scores in the notebook.
#      
# - `export_preview()` or its synonym `export_()`: this function exports only the first system of the score.
#       It is not dependent on any external program to crop the image, and as a result is much faster and
#       more convenient.
#       If you're sure your score fits in a single system, this is the function to use.
#       
# These functions all take the same arguments:
# 
# - `expr`, a music expression (like a [`Score`](http://abjad.mbrsi.org/api/tools/scoretools/Score.html),
#     a [`Staff`](http://abjad.mbrsi.org/api/tools/scoretools/Staff.html),
#     a [`Voice`](http://abjad.mbrsi.org/api/tools/scoretools/Voice.html) or
#     a [`LilyPondFile`](http://abjad.mbrsi.org/api/tools/lilypondfiletools/LilyPondFile.html))
# - `filename`, the absolute or relative path to the file to which you want to export the score.
#     The file format is taken from the file extension.
# - `pdf`, a boolean parameter that controls whether a link to a PDF is added after the score.
#     This is useful if you want to provide a printable copy of the score.

# In[ ]:

def export_preview(expr, filename, show=True):
    """Exports the first system of the music."""
    
    _, fmt = os.path.splitext(filename)
    
    if fmt == '.png':
        img = _get_preview(expr, 'png', _png_lily_opts)
        if show and isIPython():
            display_png(img, raw=True)

    elif fmt == '.svg':
        img = _get_preview(expr, 'svg', _svg_lily_opts)
        if show and isIPython():
            display_svg(img, raw=True)

    elif fmt == '.pdf':
        img = _get_preview(expr, 'pdf', _pdf_lily_opts)
        if show and isIPython():
            display_pdf(img, raw=True)
    
    else:
        raise Exception("Unsupported file extension.")
    
    _save_img(img, filename)
    

def export_(expr, filename, show=True):
    """Alias for export_preview."""
    return export_preview(expr, filename, show)


def export(expr, filename, show=True):
    """NOTE: if extension is 'svg' or 'png' assumes the output is a single page."""

    _, fmt = os.path.splitext(filename)
    
    if fmt == '.png':
        pages = _get_pngs(expr)
        if show and isIPython():
            for page in pages:
                display_png(page, raw=True)
            
    elif fmt == '.svg':
        pages = _get_svgs(expr)
        if show and isIPython():
            for page in pages:
                display_svg(page, raw=True)
    
    else:
        raise Exception("Unsupported file extension.")
    
    _save_img(pages[0], filename)


# The function `_save_img()` avoids code duplication in the `export()` and `export_preview()` functions.

# In[ ]:

# Not tested yet
def _save_img(img, filename):
    # Create the directory for the file
    try:
        # Try to create a new directory
        os.makedirs(os.path.dirname(filename))
    except:
        #  If it fails, it's probably because the directory
        # already exists, and the failure can be ignored.
        pass
    
    with open(filename, 'w') as f:
        f.write(img)

