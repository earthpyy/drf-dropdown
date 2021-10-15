class DropdownRegistry:
    """Function registry for dropdown in the application"""

    def __init__(self):
        self.registry = {}

    def register(self, key=None, dropdown_func=None):
        if key is None and dropdown_func is None:
            # @register()
            return self.register_function
        elif key is not None and dropdown_func is None:
            if callable(key):
                # @register
                return self.register_function(key)
            else:
                # @register('somekey') or @register(key='somekey')
                def dec(func):
                    return self.register(key, func)

                return dec
        elif key is not None and dropdown_func is not None:
            # register.tag('somekey', somefunc)
            self.register_function(dropdown_func, key)
            return dropdown_func
        else:
            raise ValueError('Unsupported arguments.')

    def register_function(self, func, key: str = None):
        key = key or getattr(func, '_decorated_function', func).__name__

        if key in self.registry:
            raise ValueError(f'Duplicated key named `{key}`.')

        self.registry[key] = func
        return func


default_registry = DropdownRegistry()
register = default_registry.register
