from etlfunc.FieldOperations import date_parser, compose, explode_date
from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import append


def test_empty():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = Tr(append(fields=["date"], etl_func=date_parser(date_formats))).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_empty_date_formats():
    date_formats = None

    operation = Tr(append(fields=["date"], etl_func=date_parser(date_formats))).apply()
    (inp, res, err) = operation({"date": "20171010"})
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is not None
    assert res == {}
    assert err is not None
    assert err["date"] == "Date formats can't be None"


def test_date_format_incorrect():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = Tr(append(fields=["date"], etl_func=date_parser(date_formats))).apply()
    (inp, res, err) = operation({"date": "2017,10,10"})
    assert inp is not None
    assert inp["date"] == "2017,10,10"
    assert res is not None
    assert res == {}
    assert err is not None
    assert err["date"] == "Can not parse date 2017,10,10"


def test_some_working():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = Tr(append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date))).apply()
    (inp, res, err) = operation({"date": "20171010"})
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is not None
    assert res["second"] == 0
    assert res["minute"] == 0
    assert res["hour"] == 0
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is not None
    assert err == {}
