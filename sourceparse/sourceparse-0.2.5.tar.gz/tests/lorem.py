@decorated(somehow)
@extra
class Base(object):
    """This is the base class.
    """

    def method1(self):
        """ method1 of Base
        """
        return


class Sub1(Base):
    """This is the first subclass.
    """


class MixinUser(Sub2, Mixin):
    """Overrides method1 and method2
    """

    def method1(self, foo, bar):
        """ method1 of MixinUser
        """
        return

    @manytimes
    @decorated
    def method2(self, foo, baz=None):
        """ method2 of MixinUser
        """
        return

# comment


def my_function(foo):
    """ Stand-alone function.
    """
    return


@deprecated
def my_decorated_function(foo, bar):
    """ Another stand-alone function.
    """
    return
