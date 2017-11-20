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

from datarefinery.FieldOperations import linear_category


def test_empty():
    operator = linear_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operator = linear_category(None)
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_all_empty():
    operator = linear_category(None)
    (res, err) = operator(None)
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_simple():
    operator = linear_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator("niño")
    assert res is not None
    assert res == 2
    assert err is None


def test_zero_categories():
    operator = linear_category([])
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"
