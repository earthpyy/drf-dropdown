from dropdown import utils


def test_simple():
    assert utils.extract_select_related('x.y') == 'x'


def test_no_relation():
    assert utils.extract_select_related('x') is None


def test_three_dots():
    assert utils.extract_select_related('x.y.z') == 'x__y'


def test_four_dots():
    assert utils.extract_select_related('w.x.y.z') == 'w__x__y'
