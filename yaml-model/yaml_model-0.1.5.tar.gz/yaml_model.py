"""
A very light-weight "model" structure to lazy-load (or generate) and save YAML
from Python objects composed of specialized fields
"""

from contextlib import contextmanager
from functools import wraps

# TODO fix this import in pylint!
# No idea why py fails to import in pylint :(
import py.error  # pylint:disable=import-error
import py.path  # pylint:disable=import-error

from yaml import safe_load as yaml_load, dump as yaml_dump


IMMUTABLE_TYPES = (int, float, str, tuple, None.__class__)
INDEXABLE_TYPES = (int, float, str)


class ValidationError(Exception):
    """
    Raised when model validation failed in some way
    """
    def __init__(self, messages):
        if not isinstance(messages, (tuple, list)):
            messages = [messages]

        self.messages = tuple(messages)

        super(ValidationError, self).__init__("\n".join(self.messages))

    def __add__(self, other):
        if isinstance(other, ValidationError):
            return ValidationError(self.messages + other.messages)

        return super(ValidationError, self).__add__(other)


class NoValueError(Exception):
    """
    Raised when a field has no value, no generator and no default
    """
    def __init__(self, cls, var_name, *args):
        super(NoValueError, self).__init__(*args)
        self.cls = cls
        self.var_name = var_name

    def __str__(self):
        return "No value for field '%s'" % self.var_name


class TransientValueError(Exception):
    """
    Raised to signal that a returned value may not be final, so shouldn't be
    cached, or saved automatically
    """
    def __init__(self, value):
        super(TransientValueError, self).__init__()
        self.value = value


class IndexValueError(Exception):
    """
    Raised when an index value is set to an unindexable value
    """
    def __init__(self, var_name, value):
        super(IndexValueError, self).__init__(
            "Value '%s' (type %s) can't be used for field index for "
            "field '%s'" % (value, type(value), var_name)
        )
        self.var_name = var_name
        self.value = value


def index_value_decorator(func, var_name):
    """
    Decorates a setter function with an indexable type check, raising
    IndexValueError if the value is "not indexable"
    """
    @wraps(func)
    def outer(self, value):
        """
        Wrapped setter, raises IndexValueError when value is invalid
        """
        if not isinstance(value, INDEXABLE_TYPES):
            raise IndexValueError(var_name, value)
        return func(self, value)

    return outer


def hash_value(value):
    """
    Provide a hash for comparing value (in)equality
    """
    try:
        return hash(value)

    except TypeError:
        return hash(value.__repr__())


class OnAccess(object):  # pylint:disable=too-few-public-methods
    """
    Mark a field as having a one-time call associated with it's retrieval
    """
    var_name = None
    func = None

    def __init__(self, func, input_transform=None, output_transform=None):
        self.func = func
        self.input_transform = input_transform
        self.output_transform = output_transform

        self.future_cls = None

    def process_generate_default(self, self_, generate, default):
        """
        Process the generate/default values to get a value
        """
        if generate is not None:
            # TODO generated values aren't marked dirty
            return self.process_value_generator(self_, generate)

        elif default is not None:
            raise TransientValueError(
                self.process_value_generator(self_, default)
            )

        else:
            raise NoValueError(self_.__class__, self.var_name)

    # Needs to be class method so that it can be overridden
    # pylint:disable=no-self-use
    def process_value_generator(self, self_, gen_value):
        """
        Process a generate/default argument for a value
        """
        return gen_value(self_) if callable(gen_value) else gen_value

    def modify_class(self):
        """
        Generate a property to put in place of this object instance on the
        concrete model object
        """
        def getter(self_):
            """
            Getter for the attribute value that checks for a cached value
            before trying to generate/acquire it
            """
            # pylint:disable=protected-access
            try:
                value = self_._dirty_vals[self.var_name]

            except KeyError:
                try:
                    value = self_._lazy_vals[self.var_name]

                except KeyError:
                    try:
                        self_._lazy_vals[self.var_name] = self.func(self_)
                        self_.recheck_dirty(self.var_name)
                        value = self_._lazy_vals[self.var_name]

                    except TransientValueError as ex:
                        value = ex.value

            if self.output_transform:
                return self.output_transform(value)

            else:
                return value

        def setter(self_, value):
            """
            Basic setter to write the value to the cache dict
            """
            if self.input_transform:
                value = self.input_transform(value)

            # pylint:disable=protected-access
            self_._dirty_vals[self.var_name] = value

        f_attrs = self.future_cls[2]
        f_attrs[self.var_name] = property(getter, setter)


class LoadOnAccess(OnAccess):  # pylint:disable=too-few-public-methods
    """
    Mark a field as being lazy loaded with the _load method of the model
    class
    """
    def __init__(self,
                 default=None,
                 generate=None,
                 index=False,
                 *args,
                 **kwargs):
        def loader(self_):
            """
            Loader function to load the model and return the requested
            attribute value if possible. Fall back to default/generated values
            """
            try:
                self_.load()
                # pylint:disable=protected-access
                return self_._lazy_vals[self.var_name]

            except (py.error.ENOENT, FileNotFoundError, KeyError):
                return self.process_generate_default(self_, generate, default)

        super(LoadOnAccess, self).__init__(loader, *args, **kwargs)
        self.index = index

    def modify_class(self):
        # pylint:disable=no-member
        super(LoadOnAccess, self).modify_class()
        f_attrs = self.future_cls[2]
        f_attrs.setdefault('_load_on_access', []).append(self.var_name)

        if self.index:
            f_attrs.setdefault('_indexed_fields', []).append(self.var_name)
            f_attrs[self.var_name] = property(
                f_attrs[self.var_name].fget,
                index_value_decorator(
                    f_attrs[self.var_name].fset, self.var_name
                )
            )


class ModelReference(OnAccess):
    """
    A model reference field that adds both a model field, and a _slug field
    that reference each other
    """
    def __init__(self,
                 builder_func,
                 stored=True,
                 default=None,
                 generate=None,
                 *args,
                 **kwargs):
        self.builder_func = builder_func
        self.stored = stored
        self.default = default
        self.generate = generate

        super(ModelReference, self).__init__(
            self.model_builder, *args, **kwargs
        )

    @property
    def slug_var_name(self):
        """
        The name of the slug property for this model field
        """
        return "%s_slug" % self.var_name

    def process_value_generator(self, self_, gen_value):
        """
        Process a generate/default argument for a slug value
        """
        is_model = isinstance(gen_value, Model)

        # Get value from callable, unless it's a Model instance
        if not is_model and callable(gen_value):
            value = gen_value(self_)
        else:
            value = gen_value

        if is_model:
            return value.slug  # pylint:disable=no-member

        return value

    def slug_builder(self, self_):
        """
        Builder to get the slug from the model object
        """
        if self_.has_value(self.var_name):
            return getattr(self_, self.var_name).slug

        return self.process_generate_default(self_,
                                             self.generate,
                                             self.default)

    def model_builder(self, self_):
        """
        Builder to create a model object from the associated slug
        """
        try:
            return self.builder_func(self_)

        except NoValueError:
            raise NoValueError(self_.__class__, self.var_name)

    def modify_class(self):
        super(ModelReference, self).modify_class()

        if self.stored:
            slug_field = LoadOnAccess(generate=self.slug_builder)

        else:
            slug_field = OnAccess(self.slug_builder)

        slug_field.var_name = self.slug_var_name
        slug_field.future_cls = self.future_cls
        slug_field.modify_class()


class ModelMeta(type):
    """
    Metaclass for replacing OnAccess and child classes in fields with their
    associated caching behaviour
    """
    def __new__(mcs, f_clsname, f_bases, f_attrs):
        f_cls = (f_clsname, f_bases, f_attrs)
        for name, val in list(f_attrs.items()):
            if isinstance(val, OnAccess):
                val.var_name = name
                val.future_cls = f_cls
                val.modify_class()

        return super(ModelMeta, mcs).__new__(mcs, f_clsname, f_bases, f_attrs)


# pylint:disable=abstract-class-little-used
class Model(object, metaclass=ModelMeta):
    """
    A model-like base for the YAML data store
    """
    @property
    def slug(self):
        """
        Unique string to identify this instance of the model (like a primary
        key)
        """
        raise NotImplementedError("You must override the 'slug' property")

    def __init__(self):
        self._lazy_vals = {}
        self._lazy_vals_hashes = {}
        self._dirty_vals = {}

    @classmethod
    def data_name(cls):
        """
        Get the data name associated with this model type
        """
        return '%ss' % cls.__name__.lower()

    @classmethod
    def data_dir_path(cls):
        """
        Path parts used to create the data directory
        """
        return py.path.local().join('data', cls.data_name())

    @classmethod
    def data_dir_to_py_path(cls, data_dir, default=None):
        """
        Take a data path and convert it to a py.path.local reference, using
        this model data dir as a base, if nothing is given
        """
        if data_dir is None:
            if default is None:
                return cls.data_dir_path()

            else:
                return cls.data_dir_to_py_path(default)

        elif isinstance(data_dir, (tuple, list)):
            return py.path.local().join(*data_dir)

        else:
            return py.path.local(data_dir)

    @classmethod
    def get_where(cls, var_name, value, new_args=None, new_kwargs=None):
        """
        Generator for objects, filtered where var_name value is equal to the
        value given. If var_name is not an indexed field, this may be very
        slow, as it must fully load every object to query them
        """
        args = (var_name, value)
        kwargs = {
            'new_args': new_args,
            'new_kwargs': new_kwargs,
        }
        if var_name in getattr(cls, '_indexed_fields', ()):
            return cls._get_where_indexed(*args, **kwargs)

        else:
            return cls._get_where_no_index(*args, **kwargs)

    @classmethod
    def _get_where_indexed(cls,
                           var_name,
                           value,
                           new_args=None,
                           new_kwargs=None):
        """
        Generator for objects, using an existing index to filter on var_name
        """
        if not isinstance(value, INDEXABLE_TYPES):
            raise IndexValueError(var_name, value)

        index_value_dir = cls.data_dir_path().join(
            '_i_%s' % var_name, str(value)
        )

        if not index_value_dir.check(dir=True):
            return ()

        for obj in cls.all(data_dir=index_value_dir,
                           skip_non_model=True,
                           new_args=new_args,
                           new_kwargs=new_kwargs):
            yield obj

    @classmethod
    def _get_where_no_index(cls,
                            var_name,
                            value,
                            new_args=None,
                            new_kwargs=None):
        """
        Generator for objects, loading all to filter on var_name
        """
        all_objs = cls.all(new_args=new_args,
                           new_kwargs=new_kwargs)
        for obj in all_objs:
            if getattr(obj, var_name) == value:
                yield obj

    @classmethod
    def all(cls,
            data_dir=None,
            dereference=True,
            skip_non_model=False,
            new_args=None,
            new_kwargs=None):
        """
        Generator for all models of this type
        """
        data_dir = cls.data_dir_to_py_path(data_dir)

        if new_args is None:
            new_args = ()
        if new_kwargs is None:
            new_kwargs = {}

        model_data_dir = cls.data_dir_path()
        try:
            for filename in data_dir.listdir('*.yaml'):
                if dereference:
                    real_path = filename.realpath()
                else:
                    real_path = filename

                if skip_non_model:
                    if real_path.dirname != model_data_dir:
                        continue

                # pylint:disable=too-many-function-args
                yield cls(real_path.basename[:-5], *new_args, **new_kwargs)

        except py.error.ENOENT:
            return ()

    def recheck_dirty(self, fields=None):
        """
        Force the dirty values list to be updated, based on hashes. This takes
        into account in-place modification of objects
        """
        if fields is None:
            fields = list(self._lazy_vals.keys())

        elif isinstance(fields, str):
            fields = (fields,)

        for var_name in fields:
            try:
                value = self._lazy_vals[var_name]

            except KeyError:
                continue

            if value.__class__ in IMMUTABLE_TYPES:
                continue

            new_hash = hash_value(value)

            if var_name in self._lazy_vals_hashes:
                if new_hash != self._lazy_vals_hashes[var_name]:
                    self._dirty_vals[var_name] = value
                    del self._lazy_vals[var_name]

            else:
                self._lazy_vals_hashes[var_name] = new_hash

    def has_value(self, var_name):
        """
        Check if there's a value for the given property
        """
        return (var_name in self._lazy_vals or
                var_name in self._dirty_vals)

    def is_dirty(self, var_name, recheck=True):
        """
        Check if the given property is dirty or not. If the value is mutable, a
        recheck may be necessary to get the correct response
        """
        if recheck:
            self.recheck_dirty(var_name)

        return var_name in self._dirty_vals

    def data_file_path(self):
        """
        Path parts used to create the data filename
        """
        return self.__class__.data_dir_path().join('%s.yaml' % self.slug)

    def update_indexes(self, for_save=False):
        """
        Update all the indexes for this model, removing and adding as
        necessary. If for_save is true, indexes will be updated from the dirty
        data; the assumption being that the dirty data is about to be
        persisted.

        Return True if indexes were updated; False if no changes necessary
        """
        if not getattr(self, '_indexed_fields', None):
            return False  # Nothing updated

        model_file = self.data_file_path()

        for var_name in self._indexed_fields:  # pylint:disable=no-member
            index_dir = self.__class__.data_dir_path().join('_i_%s' % var_name)

            try:
                value = self._lazy_vals[var_name]
            except KeyError:
                value = getattr(self, var_name)

            if not isinstance(value, INDEXABLE_TYPES):
                raise IndexValueError(var_name, value)

            current_index_dir = index_dir.join(str(value))
            current_index_file = current_index_dir.join('%s.yaml' % self.slug)

            if for_save and var_name in self._dirty_vals:
                dirty_value = self._dirty_vals[var_name]
                if not isinstance(dirty_value, INDEXABLE_TYPES):
                    raise IndexValueError(var_name, dirty_value)

                dirty_index_dir = index_dir.join(str(dirty_value))
                dirty_index_file = dirty_index_dir.join('%s.yaml' % self.slug)

                dirty_index_dir.ensure_dir()

                try:
                    current_index_file.remove()
                except py.error.ENOENT:
                    pass

                dirty_index_file.mksymlinkto(model_file)

                if len(current_index_dir.listdir()) is 0:
                    current_index_dir.remove()

            else:
                current_index_dir.ensure_dir()
                if not current_index_file.check():
                    current_index_file.mksymlinkto(model_file)
                    continue

                if not current_index_file.samefile(model_file):
                    current_index_file.remove()
                    current_index_file.mksymlinkto(model_file)

    def delete(self):
        """ Delete the Model data, including indexes """
        if getattr(self, '_indexed_fields', None):
            for var_name in self._indexed_fields:  # pylint:disable=no-member
                index_dir = self.__class__.data_dir_path().join(
                    '_i_%s' % var_name
                )

                try:
                    value = self._lazy_vals[var_name]
                except KeyError:
                    pass
                else:
                    current_index_dir = index_dir.join(str(value))
                    current_index_file = current_index_dir.join(
                        '%s.yaml' % self.slug
                    )

                    try:
                        current_index_file.remove()
                    except py.error.ENOENT:
                        pass

                    if len(current_index_dir.listdir()) is 0:
                        current_index_dir.remove()

        try:
            self.data_file_path().remove()
        except py.error.ENOENT:
            pass

    def exists(self, data_file=None):
        """
        Check to see if the model file exists (if not, maybe it's new)
        """
        return self.__class__.data_dir_to_py_path(
            data_file, default=self.data_file_path()
        ).check()

    def load(self, data_file=None, recheck_dirty=True):
        """
        Fill the object from the job file
        """
        data_file = self.__class__.data_dir_to_py_path(
            data_file, default=self.data_file_path()
        )

        # Mark any dirty data so that it's not lost
        if recheck_dirty:
            self.recheck_dirty()

        with data_file.open() as handle:
            data = yaml_load(handle)
            self.from_dict(data, dirty=False)

    def save(self,
             data_file=None,
             force=False,
             reload=True,
             reload_recheck_dirty=True):
        """
        Save the job data
        """
        if not force:  # if forced, validation is unnecessary
            self.validate()

        if reload and self.exists(data_file):
            self.load(data_file=data_file, recheck_dirty=reload_recheck_dirty)

        data_file = self.__class__.data_dir_to_py_path(
            data_file, default=self.data_file_path()
        )

        # Make the dir first
        data_file.join('..').ensure_dir()

        self.update_indexes(for_save=True)

        yaml_data = self.as_yaml()
        with data_file.open('w') as handle:
            handle.write(yaml_data)

        # Update the lazy vals and rehash
        self._lazy_vals.update(self._dirty_vals)
        self.recheck_dirty(self._dirty_vals.keys())
        self._dirty_vals.clear()

    def validate(self):
        """
        Validate the model fields to make sure they are sane. Raises
        ValidationError on failure
        """
        if not self.slug:
            raise ValidationError('Slug can not be blank')

        return True

    @contextmanager
    def parent_validation(self, klass):
        """
        Context manager to wrap validation with parent validation and combine
        ValidationError messages
        """
        errors = []
        for validate in (super(klass, self).validate, None):
            try:
                if validate:
                    validate()

                else:
                    yield errors

            except ValidationError as ex:
                errors += list(ex.messages)

        if errors:
            raise ValidationError(errors)

    def from_yaml(self, data, dirty=True):
        """
        Deserialize from YAML
        """
        return self.from_dict(yaml_load(data), dirty)

    def as_yaml(self):
        """
        Serialize to YAML
        """
        return yaml_dump(self.as_dict(), default_flow_style=False)

    def from_dict(self, data, dirty=True):
        """
        Deserialize from dict
        """
        if not data:
            return

        if not hasattr(self, '_load_on_access'):
            return

        vals_dict = self._dirty_vals if dirty else self._lazy_vals
        for var_name in self._load_on_access:  # pylint:disable=no-member
            if var_name in data:
                vals_dict[var_name] = data[var_name]

                # Reset values hashes for if this is clean data
                if not dirty:
                    try:
                        del self._lazy_vals_hashes[var_name]
                    except KeyError:
                        pass

                    self.recheck_dirty(var_name)

    def as_dict(self):
        """
        Serialize to dict
        """
        data = {}
        if hasattr(self, '_load_on_access'):
            for var_name in self._load_on_access:  # pylint:disable=no-member
                try:
                    value = getattr(self, var_name)
                    if self.has_value(var_name):
                        data[var_name] = value

                except NoValueError:
                    pass

        return data


class SingletonModel(Model):
    """
    Model with just 1 instance
    """
    @property
    def slug(self):
        """
        Auto generate a slug for this model matching it's model data_name
        """
        return self.__class__.data_name()

    @classmethod
    def data_dir_path(cls):
        return py.path.local().join('data')
