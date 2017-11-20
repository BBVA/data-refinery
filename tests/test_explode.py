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
from datarefinery.tuple.TupleOperations import append
from datarefinery.FieldOperations import explode


def check_dict_by_field(current: dict, expected: dict):
    for k, v in expected.items():
        assert (k in current), "{} field expected but not found".format(k)
        assert current[k] == v, "expect that {} == {} for {}".format(current[k], v, k)


def test_empty():
    operation = Tr(append(["a"], explode("a"))).apply()
    (inp, res, err) = operation(None)
    assert res == {}


def test_field_not_found():
    operation = Tr(append(["offer"], explode("offer"))).apply()
    (inp, res, err) = operation({"one": 1})
    assert res is not None
    assert err is not None
    assert "offer" in err
    assert err["offer"] == "offer not found"


def test_field_object_one_field():
    operation = Tr(append(["nested"], explode("nested"))).apply()
    (inp, res, err) = operation({"nested": {"one": 1}})
    expected = {"nested_one": 1}
    check_dict_by_field(res, expected)


def test_field_object_two_fields():
    operation = Tr(append(["nested"], explode("nested"))).apply()
    (inp, res, err) = operation({"nested": {"one": 1, "two": 2}})

    expected = {"nested_one": 1, "nested_two": 2}
    check_dict_by_field(res, expected)


def test_field_list_one_row_one_field():
    operation = Tr(append(["nested"], explode("nested"))).apply()
    (inp, res, err) = operation({"nested": [{"one": 1}]})

    expected = {"nested_one": 1}
    check_dict_by_field(res, expected)


def test_field_list_two_rows_one_field():
    operation = Tr(append(["nested"], explode("nested"))).apply()
    (inp, res, err) = operation({"nested": [{"one": 1}, {"one": 1}]})

    expected = {"nested_one": 1, "nested_one_1": 1}
    check_dict_by_field(res, expected)


def test_field_list_two_rows_two_fields():
    operation = Tr(append(["nested"], explode("nested"))).apply()
    (inp, res, err) = operation({"nested": [{"one": 1, "two": 2}, {"one": 1, "two": 3}]})

    expected = {"nested_one": 1, "nested_one_1": 1, "nested_two": 2, "nested_two_1": 3}
    check_dict_by_field(res, expected)


def test_field_list_two_rows_two_different_fields():
    operation = Tr(append(["nested"], explode("nested"))).apply()
    (inp, res, err) = operation({"nested": [{"one": 1, "two": 2}, {"one": 1, "three": 3}]})

    expected = {"nested_one": 1, "nested_one_1": 1, "nested_two": 2, "nested_three_1": 3}
    check_dict_by_field(res, expected)
