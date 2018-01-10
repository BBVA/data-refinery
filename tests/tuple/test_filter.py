from datarefinery.TupleOperations import filter_tuple, wrap


def only_true_values(x):
    return x


def test_empty():
    inp = None
    op = filter_tuple(["a"], wrap(only_true_values))

    (res, err) = op(inp)

    assert res is None
    assert err == {'a': 'a not found'}


def test_some_positive_filter():
    inp = {"a": True}
    op = filter_tuple(["a"], wrap(only_true_values))

    (res, err) = op(inp)

    assert res == {"a": True}
    assert err is None


def test_some_negative():
    inp = {"a": False}
    op = filter_tuple(["a"], wrap(only_true_values))

    (res, err) = op(inp)

    assert res is None
    assert err is None
