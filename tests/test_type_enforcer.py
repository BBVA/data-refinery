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

from datarefinery.field_operations import type_enforcer


def test_empty():
    operation = type_enforcer(lambda x: int(x))
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operation = type_enforcer(None)
    (res, err) = operation("1")
    assert res is None
    assert err is not None
    assert err == "a enforcer function is required"


def test_all_empty():
    operation = type_enforcer(None)
    (res, err) = operation("1")
    assert res is None
    assert err is not None
    assert err == "a enforcer function is required"


def test_some_working():
    operation = type_enforcer(lambda x: int(x))
    (res, err) = operation("1")
    assert res is not None
    assert res == 1
    assert err is None


def test_type_error():
    operation = type_enforcer(lambda x: int(x))
    (res, err) = operation("x")
    assert res is None
    assert err is not None
    assert err == "can't cast x to enforced type invalid literal for int() with base 10: 'x'"
