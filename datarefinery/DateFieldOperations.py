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

from datetime import datetime, timedelta
from itertools import takewhile
from functools import reduce


def date_parser(date_formats: list):
    def _app(x: str, e=None):
        if x is None:
            return None, "Date can't be None: {}".format(x)
        if date_formats is None:
            return None, "Date formats can't be None"
        for current_format in date_formats:
            try:
                d = datetime.strptime(x, current_format)
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
                d = datetime.strptime(x, current_format).time()
                if d is not None:
                    return d, None
            except ValueError:
                continue
        return None, "Can not parse time {}".format(x)

    return _app


def explode_date(date: datetime, e=None):
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


def explode_time(time: datetime.time, e=None):
    if time is not None:
        return {
                   "hour": time.hour,
                   "minute": time.minute,
                   "second": time.second
               }, e
    else:
        return None, e


def _date_iterator(start, advance):
    current = {
        "year": start.year,
        "month": start.month,
        "day": start.day,
        "hour": start.hour,
        "minute": start.minute,
        "second": start.second
    }
    yield datetime(**current)
    while True:
        current = advance(current)
        yield datetime(**current)


def year_iterator(start):
    def _year_step(current):
        current["year"] += 1
        return current
    return _date_iterator(start, _year_step)


def month_iterator(start):
    def _month_step(current):
        current["month"] += 1
        return current
    return _date_iterator(start, _month_step)


def _time_iter(start, step):
    current = start
    yield current
    while True:
        current = current + step
        yield current


def day_iterator(start):
    delta = timedelta(days=1)
    return _time_iter(start, delta)


def hour_iterator(start):
    delta = timedelta(seconds=3600)
    return _time_iter(start, delta)


def minute_iterator(start):
    delta = timedelta(seconds=60)
    return _time_iter(start, delta)


def second_iterator(start):
    delta = timedelta(seconds=1)
    return _time_iter(start, delta)


def years_between(start):
    def _app(end, err=None):
        if end is None:
            return None, "no date provided"
        return end.year - start.year, err
    return _app


def months_between(start):
    year_counter = years_between(start)

    def _app(end, err=None):
        if end is None:
            return None, "no date provided"
        (years, err2) = year_counter(end)
        if err2 is not None:
            return None, err2
        return years*12 + (end.month - start.month), err
    return _app


def _count_steps(start, generator_fun):
    def _app(end, err=None):
        if end is None:
            return None, "no date provided"
        ite = generator_fun(start)
        total = map(lambda x: 1, takewhile(lambda d: d < end, ite))
        return reduce(lambda a, b: a + b, total), err
    return _app


def days_between(start):
    return _count_steps(start, day_iterator)


def hours_between(start):
    return _count_steps(start, hour_iterator)


def minutes_between(start):
    return _count_steps(start, minute_iterator)


def seconds_between(start):
    return _count_steps(start, second_iterator)
