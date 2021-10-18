import pytest

from dropdown.registry import DropdownRegistry


@pytest.fixture(name='registry')
def setup_registry():
    return DropdownRegistry()


def test_register_with_no_parenthesis(registry):

    @registry.register
    def func():
        pass

    assert 'func' in registry.registry
    assert registry.registry['func'].__name__ == 'func'


def test_register_with_no_argument(registry):

    @registry.register()
    def func():
        pass

    assert 'func' in registry.registry
    assert registry.registry['func'].__name__ == 'func'


def test_register_with_key(registry):

    @registry.register('custom')
    def func():
        pass

    assert 'custom' in registry.registry
    assert registry.registry['custom'].__name__ == 'func'
