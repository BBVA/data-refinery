from datarefinery.TupleOperations import keep_regexp


def test_empty():
    imp = None
    op = keep_regexp("yes_")

    (res, err) = op(imp)

    assert res is None
    assert err == {'yes_': 'no input provided'}


def test_some_working():
    imp = {"yes_name": "Tom", "yes_hire": True, "no_age": 99}
    op = keep_regexp("yes_")

    (res, err) = op(imp)

    assert res == {"yes_name": "Tom", "yes_hire": True}
    assert err is None


def test_no_fields():
    imp = {"no_name": "Tom", "no_hire": True, "no_age": 99}
    op = keep_regexp("yes_")

    (res, err) = op(imp)

    assert res == {}
    assert err is None
