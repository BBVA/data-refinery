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

from datarefinery.field_operations import min_max_normalization


def test_empty():
    operation = min_max_normalization(0, 100)
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operation = min_max_normalization(None, None)
    (res, err) = operation(0)
    assert res is None
    assert err is not None
    assert err == "Min value required"


def test_all_empty():
    operation = min_max_normalization(None, None)
    (res, err) = operation(None)
    assert res is None
    assert err is not None
    assert err == "Min value required"


def test_some_working():
    operation = min_max_normalization(0, 100)
    (res, err) = operation(50)
    assert res is not None
    assert res == 0.5
    assert err is None


def test_equal_input():
    operation = min_max_normalization(100, 100)
    (res, err) = operation(50)
    assert res is None
    assert err is not None
    assert err == "Min > Max"


def test_unordered_input():
    operation = min_max_normalization(100, 50)
    (res, err) = operation(50)
    assert res is None
    assert err is not None
    assert err == "Min > Max"
