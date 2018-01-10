from datarefinery.TupleOperations import append, wrap


def head_and_tail(x):
    return {"head": x[0], "tail": x[1:]}


def test_empty():
    imp = None
    op = append(["hello"], wrap(head_and_tail))

    (res, err) = op(imp)

    assert res is None
    assert err == {"hello": "hello not found"}


def test_some_working():
    imp = {"hello": "world"}
    op = append(["hello"], wrap(head_and_tail))

    (res, err) = op(imp)

    assert res == {"head": "w", "tail": "orld"}
    assert err is None
