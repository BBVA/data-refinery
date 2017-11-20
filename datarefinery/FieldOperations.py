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

import datetime

from collections import OrderedDict
from typing import Callable, TypeVar, Tuple, Optional, List, Union
from datarefinery.tuple.TupleOperations import compose

T = TypeVar('T')
U = TypeVar('U')


def _fixed_input(return_value: U, error_text: str = "") \
        -> Callable[[T], Tuple[Optional[U], Optional[str]]]:
    """

    Return a function that gives the value or the error supplied as parameter.

    :param return_value: Any
    :param error_text: str
    :return: Callable
    """
    def _value(x, e=None):
        return return_value, None

    def _error(x, e=None):
        return None, error_text

    if return_value is not None:
        return _value
    else:
        return _error


def type_enforcer(enforcer_function: Callable[[T], U]) -> \
        Callable[[T], Tuple[Optional[U], Optional[str]]]:
    """

    Return a function that cast from one type to another.

    :param enforcer_function: Callable
    :return: Callable
    """

    def _app(x: T, e: str=None) -> Tuple[Optional[U], Optional[str]]:
        if x is None:
            return None, None
        try:
            return enforcer_function(x), None
        except Exception as e:
            return None, "can't cast {} to enforced type {}".format(x, e)

    if enforcer_function is None:
        return _fixed_input(None, "a enforcer function is required")
    return _app


def min_max_normalization(min_value: float, max_value: float) -> \
        Callable[[float], Tuple[Optional[float], Optional[str]]]:
    """

    Return a function that apply a Rescaling normalization.
    Rescaling normalization - Normalization based on the mininum and maximum value of the given value.
    It's like rescale the value

    :param min_value: float
    :param max_value: float
    :return: Callable
    """

    def _app(x: float, e: str=None) -> Tuple[Optional[float], Optional[str]]:
        if x is None:
            return None, None
        return (x - min_value) / (max_value - min_value), None

    if min_value is None:
        return _fixed_input(None, "Min value required")
    if max_value is None:
        return _fixed_input(None, "Max value required")
    if max_value <= min_value:
        return _fixed_input(None, "Min > Max")
    return _app


def std_score_normalization(average: float, std_deviation: float) -> \
        Callable[[float], Tuple[Optional[float], Optional[str]]]:
    """

    Return a function that apply a Standardization normalization.
    Standardization normalization - Normalization based on the average and standard deviation of the given values.

    :param average: float
    :param std_deviation: float
    :return: Callable[[float], Tuple[Optional[float], Optional[str]]]
    """

    def _app(x: float, e: str=None) -> Tuple[Optional[float], Optional[str]]:
        if x is None:
            return None, None
        return (x - average) / std_deviation, None

    if average is None:
        return _fixed_input(None, "average is required")
    if std_deviation is None:
        return _fixed_input(None, "std deviation is required")
    if std_deviation == 0:
        return _fixed_input(None, "std deviation must be != 0")
    return _app


def buckets_grouping(*buckets: float) -> \
        Callable[[float], Tuple[Optional[int], Optional[str]]]:
    """

    Return a function that gives the index of the value using a group interval by provided input.

    :param buckets: float
    :return: Callable
    """

    def _app(x: float, e=None) -> Tuple[Optional[int], Optional[str]]:
        if x is None:
            return None, None
        for (lower, upper, index) in intervals:
            if lower is None and x <= upper:
                return index, None
            elif upper is None and lower < x:
                return index, None
            elif lower is not None and upper is not None and lower < x <= upper:
                return index, None
        return None, "bucket not found for {}".format(x)

    size = len(buckets)
    if size <= 0 or any([x is None for x in buckets]):
        return _fixed_input(None, "buckets not provided")
    intervals = list(zip([None] + list(buckets), list(buckets) + [None], range(1, len(buckets) + 2)))
    return _app


def linear_category(categories: List[T]) -> \
        Callable[[T], Tuple[Optional[int], Optional[str]]]:
    """

    Return a function that gives a categorization value.
    This categorization is a substitution the given value by a numeric representation in the category supplied.

    :param categories: List
    :return: Callable
    """

    def _app(x: T, e: str=None) -> Tuple[Optional[int], Optional[str]]:
        if x is None:
            return None, None
        if x not in category_map:
            return None, "value {} not found on categories".format(x)
        return category_map[x], None

    if categories is None or len(categories) == 0:
        return _fixed_input(None, "no categories supplied")
    category_map = {value: i+1 for (i, value) in enumerate(categories)}

    return _app


def column_category(categories: List[T]) -> \
        Callable[[T], Tuple[Optional[dict], Optional[str]]]:
    """

    Return a function that gives a categorization value vectorized (see: one hot vector).
    This categorization is a substitution the given value by a vector with all categories and 1 in the category
    supplied.

    :param categories: list
    :return: Optional[str]
    """
    def _app(x: T, e: str=None) -> Tuple[Optional[dict], Optional[str]]:
        if x is None:
            return None, None
        if x not in categories:
            return None, "value {} not found on categories".format(x)
        category_map = OrderedDict([(category, 0) if category != x else (category, 1) for category in categories])
        return category_map, None

    if categories is None or len(categories) == 0:
        return _fixed_input(None, "no categories supplied")
    return _app


def add_column_prefix(prefix):
    def _app(x, e=None):
        if x is not None:
            return {"{}_{}".format(prefix, k): v for (k, v) in x.items()}, None
        return None, e
    return _app


def explode(prefix: str):
    """
    given an array of objects de-normalized into fields
    """
    def _app(i, e):
        if i is not None:
            return {k: v for (k, v) in iter_fields(i)}, None
        return i, e

    def iter_fields(event_field: Union[dict, list]):
        if type(event_field) is dict:
            for key, val in event_field.items():
                yield (key, val)
        elif type(event_field) is list:
            for i, value in enumerate(event_field):
                for key, val in value.items():
                    if not i == 0:
                        yield ("{}_{}".format(key, i), val)
                    else:
                        yield (key, val)

    return compose(_app, add_column_prefix(prefix))


def replace_if(func, replacement):
    def _app(i, e):
        if func(i):
            return replacement(i), e
        return i, e

    return _app


def date_parser(date_formats: list):
    def _app(x: str, e=None):
        if x is None:
            return None, "Date can't be None: {}".format(x)
        if date_formats is None:
            return None, "Date formats can't be None"
        for current_format in date_formats:
            try:
                d = datetime.datetime.strptime(x, current_format)
                if d is not None:
                    return d, None
            except ValueError:
                continue
        return None, "Can not parse date {}".format(x)

    return _app


def time_parser(formats: list):
    def _app(x: str, e=None):
        if x is None:
            return None, "Time can't be None: {}".format(x)
        if formats is None:
            return None, "Time formats can't be None"
        for current_format in formats:
            try:
                d = datetime.datetime.strptime(x, current_format).time()
                if d is not None:
                    return d, None
            except ValueError:
                continue
        return None, "Can not parse time {}".format(x)

    return _app


def explode_date(date: datetime.datetime, e):
    if date is not None:
        return {
                   "year": date.year,
                   "month": date.month,
                   "day": date.day,
                   "hour": date.hour,
                   "minute": date.minute,
                   "second": date.second
               }, e
    else:
        return None, e


def explode_time(time: datetime.time, e):
    if time is not None:
        return {
                   "hour": time.hour,
                   "minute": time.minute,
                   "second": time.second
               }, e
    else:
        return None, e


def remove_columns(*columns_to_remove: str):
    def _app(i, e):
        if i is not None:
            out = {k: v for k, v in i.items() if k not in columns_to_remove}
            if len(out) == 0:
                return i, "No remain columns"
            else:
                return out, None
        else:
            return i, e
    return _app


def match_dict(dictionary):
    def _app(x, e=None):
        if dictionary is None:
            return None, "You need a dict for matching"
        if x in dictionary:
            return dictionary[x], None
        return None, "{} not found on dictionary".format(x)
    return _app


def replace_if_else(fn_cond, fn_then, fn_else=lambda x: x):
    def _app(i, e):
        if fn_cond(i):
            return fn_then(i), e
        else:
            return fn_else(i), e

    return _app
