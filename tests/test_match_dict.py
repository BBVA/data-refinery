from etlfunc.FieldOperations import match_dict
from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import substitution


def test_empty():
    operation = Tr(substitution(fields=["hello"], etl_func=match_dict(None))).apply()
    (inp, res, err) = operation({"hello": "world"})
    assert inp is not None
    assert inp["hello"] == "world"
    assert res is not None
    assert res == {}
    assert err is not None
    assert err["hello"] == "You need a dict for matching"


def test_some_working():
    operation = Tr(substitution(fields=["hello"], etl_func=match_dict({"world": "world of Ooo"}))).apply()
    (inp, res, err) = operation({"hello": "world"})
    assert inp is not None
    assert inp["hello"] == "world"
    assert res is not None
    assert "hello" in res
    assert res["hello"] == "world of Ooo"
    assert err is not None
    assert err == {}


def test_not_matching():
    operation = Tr(substitution(fields=["hello"], etl_func=match_dict({"who": "Tom"}))).apply()
    (inp, res, err) = operation({"hello": "world"})
    assert inp is not None
    assert inp["hello"] == "world"
    assert res is not None
    assert res == {}
    assert err is not None
    assert err["hello"] == "world not found on dictionary"
