from fanstatic import Library, Resource
import js.jquery

library = Library('cropper', 'resources')
cropper_css = Resource(library, 'cropper.css', minified='cropper.min.css')
cropper = Resource(
    library, 'cropper.js',
    minified='cropper.min.js', depends=[cropper_css, js.jquery.jquery])
