"""
Portfolio

"""
import os
import datetime
import inspect
import utils
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, render_template, flash
from flask_classy import FlaskView, route
from flask_assets import Environment
import jinja2
import warnings

# ------------------------------------------------------------------------------

import pkginfo
NAME = pkginfo.NAME
__version__ = pkginfo.VERSION
__author__ = pkginfo.AUTHOR
__license__ = pkginfo.LICENSE
__copyright__ = pkginfo.COPYRIGHT

# ------------------------------------------------------------------------------

class Portfolio(FlaskView):
    """ Portfolio """

    LAYOUT = "layout.html"  # The default layout
    META_DATA = "META_DATA"
    assets = None
    _app = None
    _bind = set()
    _template_paths = set()
    _static_paths = set()
    _context = dict(
        PORTFOLIO_NAME=NAME,
        PORTFOLIO_VERSION=__version__,
        APP_NAME="",
        APP_VERSION="",
        YEAR=datetime.datetime.now().year,
        GOOGLE_ANALYTICS_ID=None,
        LOGIN_ENABLED=False,
        LOGIN_OAUTH_ENABLED=False,
        LOGIN_OAUTH_CLIENT_IDS=[],
        LOGIN_OAUTH_BUTTONS=[],
        META_DATA=dict(
            title="",
            description="",
            url="",
            image="",
            site_name="",
            object_type="",
            locale="",
            keywords=[],
            use_opengraph=True,
            use_googleplus=True,
            use_twitter=True
        )
    )

    @classmethod
    def init(cls, flask_or_import_name, directory=None, config=None):
        """
        Allow to register all subclasses of Portfolio at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param directory: The directory containing your project's Views, Templates and Static
        :param config: string of config object. ie: "app.config.Dev"
        """
        if isinstance(flask_or_import_name, Flask):
            app = flask_or_import_name
        else:
            app = Flask(flask_or_import_name)

        app.wsgi_app = ProxyFix(app.wsgi_app)

        if config:
            app.config.from_object(config)

        if directory:
            app.template_folder = directory + "/templates"
            app.static_folder = directory + "/static"

        cls._app = app
        cls.assets = Environment(cls._app)

        # Register templates
        if cls._template_paths:
            loader = [cls._app.jinja_loader] + list(cls._template_paths)
            cls._app.jinja_loader = jinja2.ChoiceLoader(loader)

        # Register static
        if cls._static_paths:
            loader = [cls._app.static_folder] + list(cls._static_paths)
            cls.assets.load_path = loader

        # init_app
        for _app in cls._bind:
            _app(cls._app)

        # Register all views
        for subcls in cls.__subclasses__():
            route_base = subcls.route_base
            _cls_name = subcls.__name__
            if not route_base:
                route_base = utils.dasherize(utils.underscore(_cls_name))
            subcls.register(cls._app, route_base=route_base)

        return cls._app

    @classmethod
    def bind(cls, kls):
        """
        To bind middlewares that needs the 'app' object to init
        Bound middlewares will be assigned on cls.init()
        """
        if not hasattr(kls, "__call__"):
            raise TypeError("From Portfolio.bind: '%s' is not callable" % kls)
        cls._bind.add(kls)
        return kls

    @classmethod
    def render(cls, data={}, view_template=None, layout=None, **kwargs):
        """
        To render data to the associate template file of the action view
        :param data: The context data to pass to the template
        :param view_template: The file template to use. By default it will map the classname/action.html
        :param layout: The body layout, must contain {% include __view_template__ %}
        """
        if not view_template:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split(".")[-1]
            action_name = stack[3]      # The method being called in the class
            view_name = cls.__name__    # The name of the class without View

            if view_name.endswith("View"):
                view_name = view_name[:-4]
            view_template = "%s/%s.html" % (view_name, action_name)

        data = data if data else dict()
        data["__"] = cls._context if cls._context else {}
        if kwargs:
            data.update(kwargs)

        data["__view_template__"] = view_template

        return render_template(layout or cls.LAYOUT, **data)

    @classmethod
    def __(cls, **kwargs):
        """
        Assign a global view context to be used in the template
        :params **kwargs:
        """
        cls._context.update(kwargs)

    @classmethod
    def get_config(cls, key, default=None):
        """
        Shortcut to access the config in your class
        :param key: The key to access
        :param default: The default value when None
        :returns mixed:
        """
        return cls._app.config.get(key, default)

    @classmethod
    def meta_data(cls, **kwargs):
        """
        Meta allows you to add meta data to site
        :params **kwargs:

        meta keys we're expecting:
            title (str)
            description (str)
            url (str) (Will pick it up by itself if not set)
            image (str)
            site_name (str) (but can pick it up from config file)
            object_type (str)
            keywords (list)
            locale (str)

            **Boolean By default these keys are True
            use_opengraph
            use_twitter
            use_googleplus

        """
        meta_data = cls._context.get(cls.META_DATA, {})

        for k, v in kwargs.items():
            if k == "keywords" and not isinstance(k, list):
                raise ValueError("Meta keyword must be a list")
            meta_data[k] = v
        cls.__(_name_=meta_data)

    @staticmethod
    def flash_error(message):
        """ Set an error message """
        flash(message, "error")

    @staticmethod
    def flash_success(message):
        """ Set an success message """
        flash(message, "success")

    @staticmethod
    def flash_info(message):
        """ Set an info message """
        flash(message, "info")

    #
    @classmethod
    def register_component_template_static(cls, root_pkg=None,
                                           template="templates",
                                           static="static"):
        """
        Register a component's template directory and static
        :param root_pkg: str - The root dir,
                        or the dotted resource package (package.path.path,
                        usually __name__ of templates and static
        :param template: str - The template dir name. If root_dir is none,
                        template should be a path
        :param static: str - The static dir name. If root_dir is none,
                        static should be a path
        """
        if root_pkg:
            if not os.path.isdir(root_pkg) and "." in root_pkg:
                root_pkg = utils.get_pkg_resources_filename(root_pkg)

            template_path = os.path.join(root_pkg, template)
            static_path = os.path.join(root_pkg, static)
        else:
            template_path = template
            static_path = static

        if os.path.isdir(template_path):
            template_path = jinja2.FileSystemLoader(template_path)
            cls._template_paths.add(template_path)
        else:
            warnings.warn("Component registration: Not a template directory '%s' " % template_path)

        if os.path.isdir(static_path):
            cls._static_paths.add(static_path)
        else:
            warnings.warn("Component registration: Not a static directory '%s' " % static_path)

    @classmethod
    def extends__(cls, kls):
        """
        A view decorator to extend another view class or function to itself
        It will inherit all its methods and propeties and use them on itself

        -- EXAMPLES --

        class Index(Portfolio):
            pass

        index = Index()

        ::-> As decorator on classes ::
        @index.extends__
        class A(object):
            def hello(self):
                pass

        @index.extends__
        class C()
            def world(self):
                pass

        ::-> Decorator With function call ::
        @index.extends__
        def hello(self):
            pass

        """
        if inspect.isclass(kls):
            for _name, _val in kls.__dict__.items():
                if not _name.startswith("__"):
                    setattr(cls, _name, _val)
        elif inspect.isfunction(kls):
            setattr(cls, kls.__name__, kls)
        return cls