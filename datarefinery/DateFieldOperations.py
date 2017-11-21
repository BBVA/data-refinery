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


def explode_date(date: datetime, e):
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


def _date_iterator(start, advance):
    current = {
        "year": start.year,
        "month": start.month,
        "day": start.day,
        "hour": start.hour,
        "minute": start.minute,
        "second": start.second,
        "microsecond": start.microsecond
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
