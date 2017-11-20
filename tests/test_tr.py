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

import json
from datarefinery.Tr import Tr


def test_empty():
    operation = Tr(None).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_one_tr():
    def _one_tr(i, o, e):
        o.update({"hello": "Tom"})
        return i, o, e
    operation = Tr(_one_tr).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == "Tom"
    assert transformed_error is not None
    assert transformed_error == {}


def test_one_complex_tr():
    def _one_complex(i, o, e):
        o.update({"greet": "Hello {}".format(i['who'])})
        return i, o, e
    operation = Tr(_one_complex).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"who": "Tom"})
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "Tom"
    assert transformed_output is not None
    assert "greet" in transformed_output
    assert transformed_output["greet"] == "Hello Tom"
    assert transformed_error is not None
    assert transformed_error == {}


def test_one_error():
    def _greet(i, o, e):
        if "who" in i:
            o.update({"greet": "Hello {}".format(i['who'])})
        else:
            e.update({"greet": "unknown person"})
        return i, o, e
    operation = Tr(_greet).apply()

    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert "greet" in transformed_error
    assert transformed_error["greet"] == "unknown person"


def test_recovery_error():
    def _greet(i, o, e):
        if "who" in i:
            o.update({"greet": "Hello {}".format(i['who'])})
        else:
            e.update({"greet": "unknown person"})
        return i, o, e

    def _recovery_error(i, o, e):
        if "greet" in e:
            del e["greet"]
            o["greet"] = "Hello world"
        return i, o, e

    operation = Tr(_greet).then(_recovery_error).apply()

    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert transformed_output is not None
    assert "hello" not in transformed_output
    assert "greet" in transformed_output
    assert transformed_output["greet"] == "Hello world"
    assert transformed_error is not None
    assert transformed_error == {}


def test_recovery_error_2tr():
    def _greet(i, o, e):
        if "who" in i:
            o.update({"greet": "Hello {}".format(i['who'])})
        else:
            e.update({"greet": "unknown person"})
        return i, o, e

    def _greet2(i, o, e):
        if "hello" in i:
            o.update({"hello": "hello???"})
        return i, o, e

    def _recovery_error(i, o, e):
        if "greet" in e:
            del e["greet"]
            o["greet"] = "Hello world"
        return i, o, e

    operation = Tr(_greet).then(_greet2).then(_recovery_error).apply()

    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert "greet" in transformed_output
    assert transformed_output["hello"] == "hello???"
    assert transformed_output["greet"] == "Hello world"
    assert transformed_error is not None
    assert transformed_error == {}


def test_init():
    def _to_json(i, o, e):
        return json.loads(i), o, e

    def _one_tr(i, o, e):
        o.update({"hello": "Tom"})
        return i, o, e

    operation = Tr(_one_tr).init(_to_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation('{"hello": "world"}')
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == "Tom"
    assert transformed_error is not None
    assert transformed_error == {}


def test_raw_init():
    def _to_hello(i, o={}, e={}):
        return {"hello": i}, o, e

    def _one_tr(i, o, e):
        o.update({"hello": "Tom"})
        return i, o, e

    operation = Tr(_one_tr).init(_to_hello).apply()
    (transformed_input, transformed_output, transformed_error) = operation('world')
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == "Tom"
    assert transformed_error is not None
    assert transformed_error == {}


def test_peek():
    def _evil(i, o, e):
        i.update({"bad": "very bad"})
        return i, o, e

    def _one_tr(i, o, e):
        o.update({"hello": "Tom"})
        return i, o, e
    operation = Tr(_one_tr).peek(_evil).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == "Tom"
    assert "bad" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}
