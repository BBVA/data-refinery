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
from datarefinery.tuple.TupleOperations import keep
from datarefinery.tuple.Formats import from_json, to_json, csv_to_map, map_to_csv


def test_reader_json_empty():
    operation = Tr(keep(fields=["who"])).reader(from_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_reader_json_some_working():
    operation = Tr(keep(fields=["who"])).reader(from_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation('{"who": "anciano"}')
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert "who" in transformed_output
    assert transformed_output["who"] == "anciano"
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_json_empty():
    operation = Tr(keep(fields=["who"])).then(to_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_json_some_working():
    operation = Tr(keep(fields=["who"])).then(to_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"who": "anciano"})
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert transformed_output == '{"who": "anciano"}'
    assert transformed_error is not None
    assert transformed_error == {}


def test_reader_csv_empty():
    operation = Tr(keep(fields=["who"])).reader(csv_to_map(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_reader_csv_some_working():
    operation = Tr(keep(fields=["who"])).reader(csv_to_map(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation('"anciano"\r\n')
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert "who" in transformed_output
    assert transformed_output["who"] == "anciano"
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_csv_empty():
    operation = Tr(keep(fields=["who"])).then(map_to_csv(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_csv_some_working():
    operation = Tr(keep(fields=["who"])).then(map_to_csv(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"who": "anciano"})
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert transformed_output == '"anciano"\r\n'
    assert transformed_error is not None
    assert transformed_error == {}
