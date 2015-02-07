import functools

from error import InjectionError

class Registry(object):
    def __init__(self):
        self.factories = {}
        self.components = {}

    def validate(self, component, factory):
        code = factory.func_code

        # factories must not have any arguments
        if not code.co_argcount == 0:
            raise InjectionError(
                "Factory {f} is not a valid dependency of component {c}: "
                "Factory must have no arguments".format(
                    c=str(component),
                    f=str(factory),
                )
            )

    def add(self, component, factory):
        self.validate(component, factory)

        self.factories[id(factory)] = factory

    def create(self, factory):
        factory_id = id(factory)

        if factory_id not in self.components:
            self.components[factory_id] = self.factories[factory_id]()

        return self.components[factory_id]

_registry = Registry()


def inject(*deps):

    def inject_decorator(component):
        for dep in deps:
            _registry.add(component, dep)

        @functools.wraps(component)
        def injector():
            args = [_registry.create(dep) for dep in deps]
            return component(*args)

        return injector

    return inject_decorator

