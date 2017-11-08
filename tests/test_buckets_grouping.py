from etlfunc.FieldOperations import buckets_grouping

from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import substitution


def test_empty():
    operation = Tr(substitution(["a"], etl_func=buckets_grouping(25, 75))).apply()
    (inp, res, err) = operation(None)
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_empty_definition():
    operation = Tr(substitution(["a"], etl_func=buckets_grouping(None, None))).apply()
    (imp, res, err) = operation({"a": 0.3})
    assert res is not None
    assert res == {}
    assert err is not None
    assert "a" in err
    assert err["a"] == "buckets not provided"


def test_all_empty():
    operation = Tr(substitution(["a"], etl_func=buckets_grouping(None, None))).apply()
    (imp, res, err) = operation(None)
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_some_working():
    operation = Tr(substitution(["a"], etl_func=buckets_grouping(0.25, 0.5))).apply()
    (imp, res, err) = operation({"a": 0.3})
    assert res is not None
    assert "a" in res
    assert res["a"] == 2
    assert err is not None
    assert err == {}


def test_final_bucket():
    operation = buckets_grouping(100.00, 500.00, 1000.00, 10000.00, 100000.00)
    (res, err) = operation(134575.38)
    assert res is not None
    assert res == 6
    assert err is None

