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

from functools import reduce
from typing import Tuple, Callable, List, Optional, Any

from datarefinery.tuple.TupleDSL import compose, use_input, read_field, write_field, apply_over_output, read_match, \
    read_fields, write_error_field, dict_enforcer, use_output


def wrap(func: Callable[[Any], Any]) \
        -> Callable[[Any], Tuple[Optional[Any], Optional[str]]]:
    def _app(i, err):
        try:
            if i is not None:
                return func(i), None
            return i, err
        except Exception as e:
            return None, e

    return _app


def keep(fields) -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    operations = [compose(use_input(), read_field(f), write_field(f)) for f in fields]
    return reduce(compose, map(apply_over_output, operations))


def keep_regexp(regexp) -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    return apply_over_output(compose(use_input(), read_match(regexp), dict_enforcer))


def substitution(fields: List[str], etl_func: Callable[[Any], Tuple[Optional[Any], Optional[str]]]) \
        -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    operations = [compose(use_input(), read_field(f), etl_func, write_field(f)) for f in fields]
    return reduce(compose, map(apply_over_output, operations))


def fusion(fields: List[str], target_field: str, etl_func: Callable[[Any], Tuple[Optional[Any], Optional[str]]]) \
        -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    return apply_over_output(compose(use_input(), read_fields(fields), etl_func, write_field(target_field)))


def fusion_append(fields: List[str], error_field: str, etl_func: Callable[[Any], Tuple[Optional[Any],
                                                                                       Optional[str]]]) \
        -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    return apply_over_output(compose(use_input(), read_fields(fields),
                                     etl_func, dict_enforcer, write_error_field(error_field)))


def append(fields: List[str], etl_func: Callable[[Any], Tuple[Optional[Any], Optional[str]]]) \
        -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    operations = [compose(use_input(), read_field(f), etl_func, dict_enforcer, write_error_field(f))
                  for f in fields]
    return reduce(compose, map(apply_over_output, operations))


def filter_tuple(fields: List[str], etl_func: Callable[[Any], Tuple[Optional[Any], Optional[str]]]):
    operations = [compose(use_input(), read_field(f), etl_func, write_error_field(f)) for f in fields]

    def _app(input_dict: dict, output_dict: dict, error_dict: dict):
        for f in operations:
            (res, err) = f(input_dict, output_dict, error_dict)

            if err is not None:
                error_dict.update(err)

            if (res is not None and res is False) or (res is None):
                return input_dict, None, error_dict
        return input_dict, output_dict, error_dict

    return _app


def change(fields: List[str], etl_func: Callable[[Any], Tuple[Optional[Any], Optional[str]]]) \
        -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
    operations = [compose(use_output(), read_field(f), etl_func, write_field(f)) for f in fields]
    return reduce(compose, map(apply_over_output, operations))


def alternative(*alternatives):
    def reduction(
            a: Callable[[dict, dict, dict], Tuple[dict, dict, dict]],
            b: Callable[[dict, dict, dict], Tuple[dict, dict, dict]]
    ) -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
        def _app(input_dict: dict, output_dict: dict, error_dict: dict):
            (inp, res, err) = a(input_dict, output_dict, {})
            if len(err) == 0:
                return inp, res, error_dict
            return b(input_dict, output_dict, error_dict)

        return _app

    if len(alternatives) == 1:
        return alternatives[0]
    return reduce(reduction, alternatives)


def recover():
    # TODO
    pass


def chain():
    # TODO
    pass
