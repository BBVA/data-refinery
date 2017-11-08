from etlfunc.FieldOperations import type_enforcer


def test_empty():
    operation = type_enforcer(lambda x: int(x))
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operation = type_enforcer(None)
    (res, err) = operation("1")
    assert res is None
    assert err is not None
    assert err == "a enforcer function is required"


def test_all_empty():
    operation = type_enforcer(None)
    (res, err) = operation("1")
    assert res is None
    assert err is not None
    assert err == "a enforcer function is required"


def test_some_working():
    operation = type_enforcer(lambda x: int(x))
    (res, err) = operation("1")
    assert res is not None
    assert res == 1
    assert err is None


def test_type_error():
    operation = type_enforcer(lambda x: int(x))
    (res, err) = operation("x")
    assert res is None
    assert err is not None
    assert err == "can't cast x to enforced type invalid literal for int() with base 10: 'x'"
