import pygame
from Mind import Orientation


class Object:
    """Basic object class in object/group model.

    :param groups: groups which object belongs to
    """
    def __init__(self, *groups):
        self.groups = list(groups)
        for gr in self.groups:
            gr.add_object(self)

    def __str__(self):
        return "Object"

    def __repr__(self):
        self.fin = "Object ["
        for gr in self.groups:
            self.fin += str(gr)
            self.fin += ", "
        self.fin = self.fin[:-2] + ("]" if self.groups else "")
        return self.fin

    def add_group(self, gr):
        """Adds groups to object.

        :param gr: group which will object be added to.
        """
        if gr not in self.groups:
            self.groups.append(gr)
            gr.add_object(self)

    @classmethod
    def __tmx_x_init__(cls, obj, Map):
        super().__tmx_x_init__(obj, Map)

    def blit(self):
        super().blit()

    def set_position(self, *arg):
        super().set_position(*arg)

    def move(self, *arg):
        super().move(*arg)


class group(Object):
    """Basic group class in object/group model.

    :param objects: objects which belongs to group
    :param list groups: list of groups group belongs to
    :param bool part: if ``True`` if any object has some function it will belong to group
    """
    def __init__(self, *objects, groups=[], part=False):
        super().__init__(*groups)
        self.objects = list(objects)
        self.part = part
        self.funcs = []
        for f, obj in enumerate(self.objects):
            if self.part or not f:
                for att in dir(obj):
                    if '__call__' in dir(getattr(obj, att)) and att not in\
                      dir(self):
                        self.add_func(att)
            else:
                for p, f in enumerate(list(self.funcs)):
                    if f not in dir(obj):
                        delattr(self, p)
                        del self.funcs[p]
            obj.add_group(self)

    def __str__(self):
        return "Group"

    def __repr__(self):
        self.fin = "Group ["
        for obj in self.objects:
            self.fin += str(obj)
            self.fin += ", "
        self.fin = self.fin[:-2] + ("]" if self.objects else "")
        return self.fin

    def add_func(self, fname):
        """Adds function to group.*
        """
        def f(*args, **kwargs):
            for obj in self.objects:
                getattr(obj, fname)(*args, **kwargs)
        setattr(self, fname, f)
        self.funcs.append(fname)

    def add_object(self, obj):
        """Adds object to group.

        :param obj: object which will be added to group.
        """
        if obj not in self.objects:
            if self.part or not len(self.objects):
                for att in dir(obj):
                    if '__call__' in dir(getattr(obj, att)) and att not in\
                      dir(self):
                        self.funcs.append(att)
            if len(self.objects):
                for p, f in enumerate(list(self.funcs)):
                    if f not in dir(obj):
                        del self.funcs[p]
            self.objects.append(obj)
            obj.add_group(self)

def join(*dicts):
    """Joins dictionaries.*
    """
    fin = {}
    for d in dicts:
        for key in d:
            fin[key] = d[key]
    return fin


class mov_type:
    """Basic class for all types of game objects.

    :param Map: Map for all objects
    :param picture: picture for all objects
    :param groups: groups for all objects
    :param int width: width for all objects
    :param int height: height for all objects
    :param str name: type name for all objects
    :param dict props: properties for all objects
    """
    def __init__(Type, Map, picture, *groups, width=None, height=None,
          name="", props={}, logic=None):
        Type.Map = Map
        Type.picture = picture
        Type.groups = groups
        Type.type = name
        if width:
            Type.width = width
        if height:
            Type.height = height
        Type.props = props
        Type.logic = logic if logic else Logic([[], [], [], []])
        class ret(Object, Orientation.map_obj):
            def __init__(self, x, y, name, *groups, width=None,
              height=None, props={}, Map=None, picture=None, logic=None):
                Object.__init__(self, *groups + Type.groups)
                width = Type.width if width == None else width
                height = Type.height if height == None else height
                Map = Type.Map if not Map else Map
                if (not self.width or self.height) and Map.gid_point:
                    Obj = Orientation.point(x, y, Map.in_map, name,
                      True)
                elif (not width and height) and Map.gid_line:
                    Obj = Orientation.line(q_points(x, y, x + width, y +
                      height, Map.in_map), Map.in_map, name, True)
                else:
                    Obj = Orientation.rect(x, y, width, height, Map.in_map,
                      name, True)
                Orientation.map_obj.__init__(self, name, Type.type,
                  join(props, Type.props), Type.picture, Map, Obj)
                self.logic = logic if logic else Type.logic
                for f in self.logic[0]:
                    f(self)
                for lc in self.logic.lc:
                    lc.bind(self)

            @classmethod
            def __tmx_x_init__(cls, obj, Map):
                super().__tmx_x_init__(obj, Map)
                return cls(cls.obj.x, cls.obj.y, cls.name,
                  width=cls.width if cls.width else None,
                  height=cls.height if cls.height else None,
                  props=cls.properties, Map=Map)

            def blit(self):
                super().blit()
                for f in self.logic[1]:
                    f(self)

            def set_position(self, x, y):
                super().set_position(x, y)
                for f in self.logic[2]:
                    f(self)

            def move(self, x, y):
                super().move(x, y)
                for f in self.logic[3]:
                    f(self)
            
        Type.cls = ret

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

    def __tmx_x_init__(self, obj, Map):
        return self.cls.__tmx_x_init__(obj, Map)


class Logic:
    """Basic logic class for move type.*
    """
    def __init__(self, lf):
        self.lf = lf
        self.lc = []

    def __getitem__(self, n):
        return self.lf[n]

    def __add__(self, other):
        self.lc += other.lc
        for p, l in enumerate(self.lf):
            l += other.lf[p]
        return self


def init_logic(fnc):
    """Decorator for init logic functions.
    """
    ret = [[fnc], [], [], []]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[0] = ret[1] + ret[2] + ret[3]
    return Logic(ret)


def blit_logic(fnc):
    """Decorator for blit logic functions.
    """
    ret = [[], [fnc], [], []]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[1] = ret[0] + ret[2] + ret[3]
    return Logic(ret)


def set_pos_logic(fnc):
    """Decorator for set_position logic functions.
    """
    ret = [[], [], [fnc], []]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[2] = ret[0] + ret[1] + ret[3]
    return Logic(ret)


def move_logic(fnc):
    """Decorator for move logic functions.
    """
    ret = [[], [], [], [fnc]]
    if type(fnc) == Logic:
        ret = fnc.lf
        ret[3] = ret[0] + ret[1] + ret[2]
    return Logic(ret)


class logic_class(Logic):
    """Decorator for logic class.
    """
    def __init__(self, cls):
        self.cls = cls
        self.lf = []
        self.lc = [self]
        self.lf.append([getattr(self.cls, "__init__", False)] if
          getattr(self.cls, "__init__", False) else [])
        self.lf.append([getattr(self.cls, "blit", False)] if
          getattr(self.cls, "blit", False) else [])
        self.lf.append([getattr(self.cls, "set_position", False)] if
          getattr(self.cls, "set_position", False) else [])
        self.lf.append([getattr(self.cls, "move", False)] if
          getattr(self.cls, "move", False) else [])

    def bind(self, obj):
        """Binds logic class with type's object.*
        """
        for att in dir(self.cls):
            if att[:2] != "__" and att not in ("blit", "set_position",
              "move"):
                At = getattr(self.cls, att)
                if callable(At):
                    def f(*args, **kwargs):
                        At(obj, *args, **kwargs)
                    setattr(obj, att, f)
                else:
                    setattr(obj, att, At)

@init_logic
@set_pos_logic
@move_logic
def Subject(self):
    """Subject logic for ``move_type`` logic.
    """
    self.Map.set_camera_pos(self.x, self.y)
