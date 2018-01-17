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


def head_field_and_tail(x):
    return {x[0]: x[1:]}


def test_multiple_working():
    imp = {"hello": "world", "goodbye": "sadness"}
    op = append(["hello", "goodbye"], wrap(head_field_and_tail))

    (res, err) = op(imp)

    assert err is None
    assert res == {"w": "orld", "s": "adness"}
