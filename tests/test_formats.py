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

from datarefinery.TupleOperations import keep
from datarefinery.CombineOperations import secuential
from datarefinery.tuple.Formats import from_json, to_json, csv_to_map, map_to_csv


def test_reader_json_empty():
    operation = secuential(from_json, keep(fields=["who"]))
    (transformed_output, transformed_error) = operation(None)
    assert transformed_output is None
    assert transformed_error == {'who': "Can't parse"}


def test_reader_json_some_working():
    operation = secuential(from_json, keep(fields=["who"]))
    (transformed_output, transformed_error) = operation('{"who": "anciano"}')
    assert "who" in transformed_output
    assert transformed_output["who"] == "anciano"
    assert transformed_error is None


def test_writer_json_empty():
    operation = secuential(keep(fields=["who"]), to_json)
    (transformed_output, transformed_error) = operation(None)
    assert transformed_output is None
    assert transformed_error == {'who': 'who not found'}


def test_writer_json_some_working():
    operation = secuential(keep(fields=["who"]), to_json)
    (transformed_output, transformed_error) = operation({"who": "anciano"})

    assert transformed_output is not None
    assert transformed_output == '{"who": "anciano"}'
    assert transformed_error is None


def test_reader_csv_empty():
    operation = secuential(csv_to_map(["who"]), keep(fields=["who"]))
    (transformed_output, transformed_error) = operation(None)
    assert transformed_output is None
    assert transformed_error == {'who': 'no input'}


def test_reader_csv_some_working():
    operation = secuential(csv_to_map(["who"]), keep(fields=["who"]))
    (transformed_output, transformed_error) = operation('"anciano"\r\n')
    assert transformed_output is not None
    assert "who" in transformed_output
    assert transformed_output["who"] == "anciano"
    assert transformed_error is None


def test_writer_csv_empty():
    operation = secuential(keep(fields=["who"]), map_to_csv(["who"]))
    (transformed_output, transformed_error) = operation(None)
    assert transformed_output is None
    assert transformed_error == {'who': 'who not found'}


def test_writer_csv_some_working():
    operation = secuential(keep(fields=["who"]), map_to_csv(["who"]))
    (transformed_output, transformed_error) = operation({"who": "anciano"})
    assert transformed_output is not None
    assert transformed_output == '"anciano"'
    assert transformed_error is None


def test_writer_csv_multiples_lines():
    lines_in = [
        {"who": "Thorin"},
        {"who": "Dwalin"},
        {"who": "Balin"},
        {"who": "Kíli"},
        {"who": "Fíli"},
        {"who": "Dori"},
        {"who": "Nori"},
        {"who": "Ori"},
        {"who": "Óin"},
        {"who": "Glóin"},
        {"who": "Bifur"},
        {"who": "Bofur"},
        {"who": "Bombur"}
    ]
    lines_out_expected = [
        '"Thorin"',
        '"Dwalin"',
        '"Balin"',
        '"Kíli"',
        '"Fíli"',
        '"Dori"',
        '"Nori"',
        '"Ori"',
        '"Óin"',
        '"Glóin"',
        '"Bifur"',
        '"Bofur"',
        '"Bombur"'
    ]

    operation = secuential(keep(fields=["who"]), map_to_csv(["who"]))

    lines_out = [operation(x)[0] for x in lines_in]

    assert lines_out_expected == lines_out
