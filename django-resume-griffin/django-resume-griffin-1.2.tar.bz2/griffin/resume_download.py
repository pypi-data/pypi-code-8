import os, datetime
from django.template import loader, Template, Context
from django.conf import settings

from django.utils import html

from asena.views import token_protect

import logging, pprint
logger = logging.getLogger(__name__)

try:
    import pypandoc
    pypandoc.get_pandoc_formats()
    PANDOC_AVAILABLE=True
except OSError as e:
    logger.warn(e)
    PANDOC_AVAILABLE=False

DEFAULT_DATE_FORMAT='%Y%m%d_%H%M%S'

def _get_default_filename():
    now = datetime.datetime.now()
    snow = now.strftime(DEFAULT_DATE_FORMAT)
    return 'resume_%s'%(snow)

def write_rst(request, rst_template, context, filename=None):
    if not filename:
        filename = _get_default_filename()
    rst_filename = '%s.rst'%filename
    destination = os.path.join(settings.MEDIA_ROOT, 'resume_download')
    destination_rst = os.path.join(destination, rst_filename)
    
    if not os.path.exists(destination):
        os.makedirs(destination)
        
    with open(destination_rst, 'w+') as f:
        t = loader.get_template(rst_template)
        rst_content = html.clean_html(t.render(Context(context)))
        logger.debug("Writing %s bytes to %s"%(len(rst_content),
            destination_rst))
        try:
            f.write(rst_content)
        except UnicodeEncodeError as e:
            logger.error(rst_content[e.start:e.end])
            logger.error(rst_content[e.start-20:e.end+20])
            logger.error("%d, %d"%(e.start, e.end))
            f.close()
        f.close()
        
    return destination_rst
    
@token_protect()
def save_to_media_docutils(request, rst_template, context, format, filename=None):
    from docutils.core import publish_file, publish_programmatically
    if not filename:
        filename = _get_default_filename()
    final_filename = '%s.%s'%(filename, format)
    destination = os.path.join(settings.MEDIA_ROOT, 'resume_download')
    destination_final = os.path.join(destination, final_filename)
        
    source_rst = write_rst(request, rst_template, context, filename)
    
    # Finally, convert to the desired format.
    if format == 'rst':
        destination_final = source_rst
    else:
        logger.debug("Converting %s to %s"%(source_rst, destination_final))
        publish_file(
            source_path=source_rst,
            destination_path=destination_final,
            #reader_name='standalone', # default
            writer_name=str(format)
        )
        
        
    media_link = settings.MEDIA_URL + 'resume_download/' + final_filename
        
    logger.debug("Media link for resume is %s"%media_link)
    
    return media_link

# If pandoc is available we can download resumes on-the-fly.

@token_protect()
def save_to_media(request, rst_template, context, format, filename=None):
    DOCUTILS_FOR = getattr(settings, 'GRIFFIN_DOCUTILS_FOR', [])
    
    if (not PANDOC_AVAILABLE) or (format in DOCUTILS_FOR):
        return save_to_media_docutils(request, rst_template, context, format, filename=None)
    
    if not filename:
        filename = _get_default_filename()
        
    final_filename = '%s.%s'%(filename, format)
    destination = os.path.join(settings.MEDIA_ROOT, 'resume_download')
    destination_final = os.path.join(destination, final_filename)
        
    destination_rst = write_rst(request, rst_template, context, filename)
    
    # Finally, convert to the desired format.
    if format == 'rst':
        destination_final = destination_rst
    else:
        logger.debug("Converting %s to %s (with pandoc)"%(
            destination_rst, destination_final))
        try:
            pypandoc.convert(destination_rst, format, outputfile=destination_final)
        except ImportError as ie:
            logger.error(ie)
            return None
        
    media_link = settings.MEDIA_URL + 'resume_download/' + final_filename
        
    logger.debug("Media link for resume is %s"%media_link)
    
    return media_link