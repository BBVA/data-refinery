from datarefinery.TupleOperations import alternative, keep


def test_empty():
    inp = None
    op = alternative(keep(["a"]), keep(["b"]))

    (res, err) = op(inp)

    assert res is None
    assert err == {"b": "b not found"}


def test_one_alternative():
    inp = {"a": 0}
    op = alternative(keep(["a"]))

    (res, err) = op(inp)

    assert res == {"a": 0}
    assert err is None


def test_two_alternatives():
    inp = {"b": 0}
    op = alternative(keep(["a"]), keep(["b"]))

    (res, err) = op(inp)

    assert res == {"b": 0}
    assert err is None


def test_multiple_alternatives():
    inp = {"c": 0}
    op = alternative(keep(["a"]), keep(["b"]), keep(["c"]))

    (res, err) = op(inp)

    assert res == {"c": 0}
    assert err is None
