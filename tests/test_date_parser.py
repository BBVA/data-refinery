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

from datarefinery.FieldOperations import compose
from datarefinery.DateFieldOperations import date_parser, explode_date
from datarefinery.TupleOperations import append


def test_empty():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]

    operation = append(fields=["date"], etl_func=date_parser(date_formats))
    (res, err) = operation(None)

    assert res is None
    assert err == {'date': "Date can't be None: None"}


def test_empty_date_formats():
    date_formats = None

    inp = {"date": "20171010"}
    operation = append(fields=["date"], etl_func=date_parser(date_formats))

    (res, err) = operation(inp)
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is None
    assert err is not None
    assert err["date"] == "Date formats can't be None"


def test_date_format_incorrect():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]
    inp = {"date": "2017,10,10"}
    operation = append(fields=["date"], etl_func=date_parser(date_formats))
    (res, err) = operation(inp)
    assert inp is not None
    assert inp["date"] == "2017,10,10"
    assert res is None
    assert err is not None
    assert err["date"] == "Can not parse date 2017,10,10"


def test_some_working():
    date_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S", "%m%d", "%Y-%m-%d", "%Y%m%d"]
    inp = {"date": "20171010"}
    operation = append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date))
    (res, err) = operation(inp)
    assert inp is not None
    assert inp["date"] == "20171010"
    assert res is not None
    assert res["second"] == 0
    assert res["minute"] == 0
    assert res["hour"] == 0
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is None


def test_sequential_use():
    date_formats = ["%Y-%m-%d"]
    inp = {"date": "2017-10-10"}
    operation = append(fields=["date"], etl_func=compose(date_parser(date_formats), explode_date))
    (res, err) = operation(inp)
    assert inp is not None
    assert inp["date"] == "2017-10-10"
    assert res is not None
    assert res["second"] == 0
    assert res["minute"] == 0
    assert res["hour"] == 0
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is None

    inp = {"date": "0"}
    (res, err) = (None, None)
    (res, err) = operation(inp)
    assert inp is not None
    assert res is None
    assert err == {'date': 'Can not parse date 0'}

    inp = {"date": "2017-10-10"}
    (res, err) = (None, None)
    (res, err) = operation(inp)
    assert inp is not None
    assert inp["date"] == "2017-10-10"
    assert res is not None
    assert res["second"] == 0
    assert res["minute"] == 0
    assert res["hour"] == 0
    assert res["day"] == 10
    assert res["month"] == 10
    assert res["year"] == 2017
    assert err is None
