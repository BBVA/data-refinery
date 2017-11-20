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

from datarefinery.Tr import Tr
from datarefinery.tuple.TupleOperations import alternative, substitution, wrap


def test_empty():
    operation = Tr(alternative(
        substitution(["a"], etl_func=lambda x: (None, "nop")),
        substitution(["b"], etl_func=wrap(lambda x: x+1))
    )).apply()
    (inp, res, err) = operation(None)
    assert inp is None
    assert res is not None
    assert res == {}
    assert err is not None
    assert err == {}


def test_some_working():
    def _fail_etl_func(i, e=None):
        return None, "nop"

    operation = Tr(alternative(
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["b"], etl_func=wrap(lambda x: x + 1))
    )).apply()
    (inp, res, err) = operation({"a": "jajaja", "b": 1})
    assert inp is not None
    assert "a" in inp
    assert inp["a"] == "jajaja"
    assert "b" in inp
    assert inp["b"] == 1
    assert res is not None
    assert "a" not in res
    assert "b" in res
    assert res["b"] == 2
    assert err is not None
    assert err == {}


def test_multiple_alternatives():
    def _fail_etl_func(i, e=None):
        return None, "nop"

    operation = Tr(alternative(
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["a"], etl_func=_fail_etl_func),
        substitution(["b"], etl_func=wrap(lambda x: x + 1))
    )).apply()
    (inp, res, err) = operation({"a": "jajaja", "b": 1})
    assert inp is not None
    assert "a" in inp
    assert inp["a"] == "jajaja"
    assert "b" in inp
    assert inp["b"] == 1
    assert res is not None
    assert "a" not in res
    assert "b" in res
    assert res["b"] == 2
    assert err is not None
    assert err == {}
