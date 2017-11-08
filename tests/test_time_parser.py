from etlfunc.FieldOperations import time_parser, compose, explode_time
from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import append


def test_empty():
    time_formats = ["%H%M%S"]

    operation = Tr(append(fields=["time"], etl_func=time_parser(time_formats))).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_empty_time_formats():
    time_formats = None

    operation = Tr(append(fields=["time"], etl_func=time_parser(time_formats))).apply()
    (inp, res, err) = operation({"time": "202020"})
    assert inp is not None
    assert inp["time"] == "202020"
    assert res is not None
    assert res == {}
    assert err is not None
    assert err["time"] == "Time formats can't be None"


def test_time_format_incorrect():
    time_formats = ["%H%M%S"]

    operation = Tr(append(fields=["time"], etl_func=time_parser(time_formats))).apply()
    (inp, res, err) = operation({"time": "20,20"})
    assert inp is not None
    assert inp["time"] == "20,20"
    assert res is not None
    assert res == {}
    assert err is not None
    assert err["time"] == "Can not parse time 20,20"


def test_some_working():
    time_formats = ["%H%M%S"]

    operation = Tr(append(fields=["time"], etl_func=compose(time_parser(time_formats), explode_time))).apply()
    (inp, res, err) = operation({"time": "202020"})
    assert inp is not None
    assert inp["time"] == "202020"
    assert res is not None
    assert res["second"] == 20
    assert res["minute"] == 20
    assert res["hour"] == 20
    assert err is not None
    assert err == {}
