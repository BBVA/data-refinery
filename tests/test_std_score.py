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

from datarefinery.field_operations import std_score_normalization


def test_empty():
    operation = std_score_normalization(55, 100)
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_all_empty():
    operation = std_score_normalization(None, None)
    (res, err) = operation(None)
    assert res is None
    assert err is not None
    assert err == "average is required"


def test_empty_definition():
    operation = std_score_normalization(None, None)
    (res, err) = operation(50)
    assert res is None
    assert err is not None
    assert err == "average is required"


def test_some_working():
    operation = std_score_normalization(79, 8)
    (res, err) = operation(85)
    assert res is not None
    assert res == 0.75
    assert err is None


def test_some_working_2():
    operation = std_score_normalization(70, 5)
    (res, err) = operation(74)
    assert res is not None
    assert res == 0.8
    assert err is None


def test_zero_deviation():
    operation = std_score_normalization(70, 0)
    (res, err) = operation(74)
    assert res is None
    assert err is not None
    assert err == "std deviation must be != 0"
