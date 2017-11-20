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

import re
from functools import reduce


def use_input():
    def _app(i, o, e):
        return i, e

    return _app


def use_output():
    def _app(i, o, e):
        return o, e

    return _app


def read_field(f):
    def _app(i, e):
        if f in i:
            return i[f], None
        else:
            return None, "{} not found".format(f)

    return _app


def read_match(regexp):
    pattern = re.compile(regexp)

    def _app(i, e):
        new_input = {
            k: v
            for (k, v) in i.items()
            if pattern.match(k)
        }
        return new_input, None

    return _app


def read_fields(fields):
    def _app(i, e):
        out = []
        for f in fields:
            if f in i:
                out.append(i[f])
            else:
                return None, "{} not found".format(f)
        return out, None

    return _app


def write_field(f):
    def _app(i, e):
        if e is not None:
            return None, {f: e}
        else:
            return {f: i}, None

    return _app


def write_error_field(f):
    def _app(i, e):
        if e is not None:
            return i, {f: e}
        return i, e

    return _app


def dict_enforcer(i, e):
    if i is not None and not isinstance(i, dict):
        return None, "dict expected"
    return i, e


def apply_over_output(fun):
    def _app(input_dict: dict, output_dict: dict, error_dict: dict):
        (res, err) = fun(input_dict, output_dict, error_dict)
        if err is not None:
            error_dict.update(err)
        elif res is not None:
            output_dict.update(res)
        return input_dict, output_dict, error_dict

    return _app


def compose(*funcs):
    def _comp(a, b):
        def _app(*n):
            return b(*a(*n))

        return _app

    return reduce(_comp, funcs)
