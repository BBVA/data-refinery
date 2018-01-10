from datarefinery.TupleOperations import fusion, wrap


def test_empty():
    imp = None
    op = fusion(["a", "b", "c"], "tot", wrap(sum))

    (res, err) = op(imp)

    assert res is None
    assert err == {"tot": "no input provided"}


def test_some_working():
    imp = {"a": 1, "b": 1, "c": 1}
    op = fusion(["a", "b", "c"], "tot", wrap(sum))

    (res, err) = op(imp)

    assert res == {"tot": 3}
    assert err is None


def test_some_field_missing():
    imp = {"a": 1, "b": 1}
    op = fusion(["a", "b", "c"], "tot", wrap(sum))

    (res, err) = op(imp)

    assert res is None
    assert err == {"tot": "c not found"}


def test_none_field_found():
    """
    TODO: must return all the field names not found

    :return:
    """
    imp = {}
    op = fusion(["a", "b", "c"], "tot", wrap(sum))

    (res, err) = op(imp)

    assert res is None
    assert err == {"tot": "a not found"}
