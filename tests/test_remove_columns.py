from etlfunc.FieldOperations import date_parser, compose, explode_date, remove_columns
from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import append


def test_empty():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = Tr(append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date,
                                                            remove_columns(None)))).apply()
    (inp, res, err) = operation({"date": "20171010"})
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is not None
    assert "second" in res
    assert "minute" in res
    assert "hour" in res
    assert "day" in res
    assert "month" in res
    assert "year" in res
    assert res["second"] == 0
    assert res["minute"] == 0
    assert res["hour"] == 0
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is not None
    assert err == {}


def test_some_working():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = Tr(append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date,
                                                            remove_columns("hour", "minute", "second")))).apply()
    (inp, res, err) = operation({"date": "20171010"})
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is not None
    assert "second" not in res
    assert "minute" not in res
    assert "hour" not in res
    assert "day" in res
    assert "month" in res
    assert "year" in res
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is not None
    assert err == {}


def test_some_working_remove_non_existing_columns():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = Tr(append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date,
                                                            remove_columns("hora", "dia")))).apply()
    (inp, res, err) = operation({"date": "20171010"})
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is not None
    assert "second" in res
    assert "minute" in res
    assert "hour" in res
    assert "day" in res
    assert "month" in res
    assert "year" in res
    assert res["second"] == 0
    assert res["minute"] == 0
    assert res["hour"] == 0
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is not None
    assert err == {}
