from flask import Blueprint

class NestableBlueprint(Blueprint):
    """
    Hacking in support for nesting blueprints, until hopefully 
    https://github.com/mitsuhiko/flask/issues/593 will be resolved
    """

    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            if self.name in state.app.template_context_processors:
                for processor in state.app.template_context_processors[self.name]:
                    blueprint.context_processor(processor)

            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)
        self.record(deferred)

from flask.ext.classy import FlaskView as FFlaskView
from flask.ext.classy import get_true_argspec
import re


class FlaskView(FFlaskView):
    @classmethod
    def register(cls, app, *args, **kwargs):
        if hasattr(app, 'expected_parameters'):
            cls.ignored_rule_args = app.expected_parameters
        
        return super(FlaskView, cls).register(app, *args,**kwargs)

    @classmethod
    def build_rule(cls, rule, method=None):
        rule_parts = []

        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)

        route_base = cls.get_route_base()
        if route_base:
            rule_parts.append(route_base)

        rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if hasattr(cls, 'ignored_rule_args'):
            ignored_rule_args += cls.ignored_rule_args

        if method:
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append("<%s>" % arg)

        result = "/%s" % "/".join(rule_parts)
        return re.sub(r'(/)\1+', r'\1', result)