from etlfunc.FieldOperations import min_max_normalization


def test_empty():
    operation = min_max_normalization(0, 100)
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operation = min_max_normalization(None, None)
    (res, err) = operation(0)
    assert res is None
    assert err is not None
    assert err == "Min value required"


def test_all_empty():
    operation = min_max_normalization(None, None)
    (res, err) = operation(None)
    assert res is None
    assert err is not None
    assert err == "Min value required"


def test_some_working():
    operation = min_max_normalization(0, 100)
    (res, err) = operation(50)
    assert res is not None
    assert res == 0.5
    assert err is None


def test_equal_input():
    operation = min_max_normalization(100, 100)
    (res, err) = operation(50)
    assert res is None
    assert err is not None
    assert err == "Min > Max"


def test_unordered_input():
    operation = min_max_normalization(100, 50)
    (res, err) = operation(50)
    assert res is None
    assert err is not None
    assert err == "Min > Max"
