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

from datarefinery.FieldOperations import buckets_grouping

from datarefinery.Tr import Tr
from datarefinery.tuple.TupleOperations import substitution


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
