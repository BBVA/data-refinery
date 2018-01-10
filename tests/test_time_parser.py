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
from datarefinery.DateFieldOperations import time_parser, explode_time
from datarefinery.TupleOperations import append


def test_empty():
    time_formats = ["%H%M%S"]

    operation = append(fields=["time"], etl_func=time_parser(time_formats))
    (res, err) = operation(None)
    assert res is None
    assert err == {'time': "Time can't be None: None"}


def test_empty_time_formats():
    time_formats = None

    inp = {"time": "202020"}
    operation = append(fields=["time"], etl_func=time_parser(time_formats))
    (res, err) = operation(inp)
    assert inp is not None
    assert inp["time"] == "202020"
    assert res is None
    assert err is not None
    assert err["time"] == "Time formats can't be None"


def test_time_format_incorrect():
    time_formats = ["%H%M%S"]

    inp = {"time": "20,20"}
    operation = append(fields=["time"], etl_func=time_parser(time_formats))
    (res, err) = operation(inp)

    assert inp is not None
    assert inp["time"] == "20,20"
    assert res is None
    assert err is not None
    assert err["time"] == "Can not parse time 20,20"


def test_some_working():
    time_formats = ["%H%M%S"]
    inp = {"time": "202020"}
    operation = append(fields=["time"], etl_func=compose(time_parser(time_formats), explode_time))
    (res, err) = operation(inp)
    assert inp is not None
    assert inp["time"] == "202020"
    assert res is not None
    assert res["second"] == 20
    assert res["minute"] == 20
    assert res["hour"] == 20
    assert err is None
