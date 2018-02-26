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

from datarefinery.tuple_operations import substitution
from datarefinery.field_operations import replace_if_else


def test_empty_input_if_then():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    operation = substitution(["a"], replace_if_else(_fn_cond, _fn_then))
    (res, err) = operation(None)
    assert res is None
    assert err == {'a': 'a not found'}


def test_empty_input_if_then_else():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    def _fn_else(x):
        return x + 2

    operation = substitution(["a"], replace_if_else(_fn_cond, _fn_then, _fn_else))
    (res, err) = operation(None)
    assert res is None
    assert err == {'a': 'a not found'}


def test_cond_true_replace_if_then():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    operation = substitution(["a"], replace_if_else(_fn_cond, _fn_then))
    (res, err) = operation({"a": 0})
    assert res is not None
    assert "a" in res
    assert res["a"] == 1
    assert err is None


def test_cond_true_replace_if_then_default_else():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    operation = substitution(["a"], replace_if_else(_fn_cond, _fn_then))
    (res, err) = operation({"a": 100})
    assert res is not None
    assert "a" in res
    assert res["a"] == 100
    assert err is None


def test_cond_false_replace_if_then_else():
    def _fn_cond(x):
        return x == 0

    def _fn_then(x):
        return x + 1

    def _fn_else(x):
        return x + 2

    operation = substitution(["a"], replace_if_else(_fn_cond, _fn_then, _fn_else))
    (res, err) = operation({"a": 100})
    assert res is not None
    assert "a" in res
    assert res["a"] == 102
    assert err is None
