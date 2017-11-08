from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import alternative, substitution, wrap


def test_empty():
    operation = Tr(alternative(
        substitution(["a"], etl_func=lambda x: (None, "nop")),
        substitution(["b"], etl_func=wrap(lambda x: x + 1))
    )).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_some_working():
    def _fail_etl_func(i, e=None):
        return None, "nop"

    operation = Tr(alternative(
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["b"], etl_func=wrap(lambda x: x + 1))
    )).apply()
    (inp, res, err) = operation({"a": "jajaja", "b": 1})
    assert inp is not None
    assert "a" in inp
    assert inp["a"] == "jajaja"
    assert "b" in inp
    assert inp["b"] == 1
    assert res is not None
    assert "a" not in res
    assert "b" in res
    assert res["b"] == 2
    assert err is not None
    assert err == {}


def test_multiple_alternatives():
    def _fail_etl_func(i, e=None):
        return None, "nop"

    operation = Tr(alternative(
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["b"], etl_func=wrap(lambda x: x + 1))
    )).apply()
    (inp, res, err) = operation({"a": "jajaja", "b": 1})
    assert inp is not None
    assert "a" in inp
    assert inp["a"] == "jajaja"
    assert "b" in inp
    assert inp["b"] == 1
    assert res is not None
    assert "a" not in res
    assert "b" in res
    assert res["b"] == 2
    assert err is not None
    assert err == {}
