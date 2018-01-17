from datarefinery.TupleOperations import substitution, wrap


def add_one(x):
    return x+1


def test_empty():
    imp = None
    op = substitution(["cant"], wrap(add_one))

    (res, err) = op(imp)

    assert res is None
    assert err == {"cant": "cant not found"}


def test_some_working():
    imp = {"cant": 0}
    op = substitution(["cant"], wrap(add_one))

    (res, err) = op(imp)

    assert res == {"cant": 1}
    assert err is None


def test_multiple_working():
    imp = {"cant": 0, "sum": 1}
    op = substitution(["cant", "sum"], wrap(add_one))

    (res, err) = op(imp)

    assert err is None
    assert res == {"cant": 1, "sum": 2}
