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

from datarefinery.FieldOperations import match_dict
from datarefinery.Tr import Tr
from datarefinery.tuple.TupleOperations import substitution


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
