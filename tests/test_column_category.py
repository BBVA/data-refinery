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

from datarefinery.field_operations import column_category


def test_empty():
    operator = column_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operator = column_category(None)
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_all_empty():
    operator = column_category(None)
    (res, err) = operator(None)
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_simple():
    operator = column_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator("niño")
    assert res is not None
    assert err is None
    assert res == {"bebé": 0, "niño":  1, "joven": 0, "adulto": 0, "anciano": 0}


def test_zero_categories():
    operator = column_category([])
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_different_category():
    operator = column_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator("buzo")
    assert res is None
    assert err is not None
    assert err == "value buzo not found on categories"
