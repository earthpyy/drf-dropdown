from dropdown import utils


def test_simple():
    assert utils.dot_to_relation('x.y') == 'x__y'


def test_three_dots():
    assert utils.dot_to_relation('x.y.z') == 'x__y__z'
