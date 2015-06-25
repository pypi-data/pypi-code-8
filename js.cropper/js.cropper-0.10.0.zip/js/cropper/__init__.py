from fanstatic import Library, Resource

library = Library('cropper', 'resources')
cropper_css = Resource(library, 'cropper.css', minified='cropper.min.css')
cropper = Resource(
    library, 'cropper.js', minified='cropper.min.js', depends=[cropper_css])
