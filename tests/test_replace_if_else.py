from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import substitution
from etlfunc.FieldOperations import replace_if_else


def test_empty_input_if_then():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    def _fn_else(x):
        return x + 2

    operation = Tr(substitution(["a"], replace_if_else(_fn_cond, _fn_then))).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_empty_input_if_then_else():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    def _fn_else(x):
        return x + 2

    operation = Tr(substitution(["a"], replace_if_else(_fn_cond, _fn_then, _fn_else))).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_cond_true_replace_if_then():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    operation = Tr(substitution(["a"], replace_if_else(_fn_cond, _fn_then))).apply()
    (inp, res, err) = operation({"a": 0})
    assert inp is not None
    assert res is not None
    assert "a" in res
    assert res["a"] == 1
    assert err is not None
    assert err == {}


def test_cond_true_replace_if_then_default_else():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    operation = Tr(substitution(["a"], replace_if_else(_fn_cond, _fn_then))).apply()
    (inp, res, err) = operation({"a": 100})
    assert inp is not None
    assert res is not None
    assert "a" in res
    assert res["a"] == 100
    assert err is not None
    assert err == {}


def test_cond_false_replace_if_then_else():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    def _fn_else(x):
        return x + 2

    operation = Tr(substitution(["a"], replace_if_else(_fn_cond, _fn_then, _fn_else))).apply()
    (inp, res, err) = operation({"a": 100})
    assert inp is not None
    assert res is not None
    assert "a" in res
    assert res["a"] == 102
    assert err is not None
    assert err == {}
