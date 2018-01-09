# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datarefinery.FieldOperations import compose, remove_columns
from datarefinery.DateFieldOperations import date_parser, explode_date
from datarefinery.TupleOperations import append


def test_empty():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]
    inp = {"date": "20171010"}
    operation = append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date,
                                                         remove_columns(None)))
    (res, err) = operation(inp)
    assert inp == {"date": "20171010"}
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
    assert err is None


def test_some_working():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    inp = {"date": "20171010"}
    operation = append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date,
                                                         remove_columns("hour", "minute", "second")))
    (res, err) = operation(inp)
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
    assert err is None


def test_some_working_remove_non_existing_columns():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    inp = {"date": "20171010"}
    operation = append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date,
                                                         remove_columns("hora", "dia")))
    (res, err) = operation(inp)
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
    assert err is None
