from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import substitution
from etlfunc.FieldOperations import replace_if


def test_some_working():
    def _if_part(x):
        return x == 0

    def _fun_part(x):
        return x+1

    operation = Tr(substitution(["a"], replace_if(_if_part, _fun_part))).apply()
    (inp, res, err) = operation({"a": 0})
    assert inp is not None
    assert res is not None
    assert "a" in res
    assert res["a"] == 1
    assert err is not None
    assert err == {}


def test_empty():
    def _if_part(x):
        return x == 0

    def _fun_part(x):
        return x+1

    operation = Tr(substitution(["a"], replace_if(_if_part, _fun_part))).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}
