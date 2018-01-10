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
from datarefinery.TupleOperations import substitution


def test_empty():
    operation = substitution(fields=["hello"], etl_func=match_dict(None))
    (res, err) = operation({"hello": "world"})
    assert res is None
    assert err is not None
    assert err["hello"] == "You need a dict for matching"


def test_some_working():
    operation = substitution(fields=["hello"], etl_func=match_dict({"world": "world of Ooo"}))
    (res, err) = operation({"hello": "world"})
    assert res is not None
    assert "hello" in res
    assert res["hello"] == "world of Ooo"
    assert err is None


def test_not_matching():
    operation = substitution(fields=["hello"], etl_func=match_dict({"who": "Tom"}))
    (res, err) = operation({"hello": "world"})
    assert res is None
    assert err is not None
    assert err["hello"] == "world not found on dictionary"
