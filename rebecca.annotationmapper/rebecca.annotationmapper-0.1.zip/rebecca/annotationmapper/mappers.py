# -*- coding:utf-8 -*-

import logging
import inspect
from pyramid.config.views import DefaultViewMapper

logger = logging.getLogger(__name__)


class AnnotationViewMapper(DefaultViewMapper):
    def __init__(self, **kw):
        super(AnnotationViewMapper, self).__init__(**kw)

    def create_annotations(self, view):
        sig = inspect.signature(view)
        annotations = ({name: self.create_annotation(p) for name, p in sig.parameters.items() if p.annotation != inspect.Signature.empty})
        return annotations

    def create_annotation(self, parameter):
        annotation_name = parameter.default if parameter.default != inspect.Signature.empty else parameter.name
        return parameter.annotation(annotation_name)

    def __call__(self, view):
        mapped_view = super(AnnotationViewMapper, self).__call__(view)
        annotations = self.create_annotations(view)
        def wrapper(context, request):
            annotated_args = {k: v(request) for k, v in annotations.items()}
            return mapped_view(context, request, **annotated_args)

        return wrapper