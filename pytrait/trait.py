import inspect


class Trait(type):
    """A class that cannot be inherited but that can be a superclass using the __subclasscheck__ dundler method."""

    def __new__(cls, name, bases, kwargs):
        newcls = super().__new__(cls, name, bases, kwargs)

        # forbid instanciation
        def __new__(cls, *args, **kwargs):
            raise SyntaxError(f"{cls} is a Trait and it cannot be instantiated")

        newcls.__new__ = __new__

        # forbid inheritance
        def __init_subclass__(self, /, **kwargs):
            raise SyntaxError(f"{cls} is a Trait and cannot be inherited")

        newcls.__init_subclass__ = __init_subclass__

        return newcls

    def __instancecheck__(cls, instance) -> bool:
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subcls: type) -> bool:
        methods = {key: value for key, value in cls.__dict__.items() if inspect.isfunction(value)}

        for key in ["__new__", "__init_subclass__"]:
            del methods[key]

        return all(hasattr(subcls, name) for name, _ in methods.items())
