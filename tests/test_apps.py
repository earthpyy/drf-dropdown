from dropdown import apps


def test_app_name():
    assert apps.DropdownConfig.name == 'dropdown'
