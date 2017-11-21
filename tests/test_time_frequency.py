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

from datetime import datetime
from datarefinery.DateFieldOperations import year_iterator, month_iterator, day_iterator
from datarefinery.DateFieldOperations import hour_iterator, minute_iterator, second_iterator
from itertools import islice


def test_year_iterator():
    ite = year_iterator(datetime(1970, 1, 1))
    five_years = list(islice(ite, 5))
    assert len(five_years) == 5
    zero = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1, five_years),
        None
    )
    assert zero is not None
    one = next(
        filter(lambda d: d.year == 1971 and d.month == 1 and d.day == 1, five_years),
        None
    )
    assert one is not None
    two = next(
        filter(lambda d: d.year == 1972 and d.month == 1 and d.day == 1, five_years),
        None
    )
    assert two is not None
    three = next(
        filter(lambda d: d.year == 1973 and d.month == 1 and d.day == 1, five_years),
        None
    )
    assert three is not None
    four = next(
        filter(lambda d: d.year == 1974 and d.month == 1 and d.day == 1, five_years),
        None
    )
    assert four is not None
    five = next(
        filter(lambda d: d.year == 1975 and d.month == 1 and d.day == 1, five_years),
        None
    )
    assert five is None


def test_month_iterator():
    ite = month_iterator(datetime(1970, 1, 1))
    five_months = list(islice(ite, 5))
    assert len(five_months) == 5
    zero = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1, five_months),
        None
    )
    assert zero is not None
    one = next(
        filter(lambda d: d.year == 1970 and d.month == 2 and d.day == 1, five_months),
        None
    )
    assert one is not None
    two = next(
        filter(lambda d: d.year == 1970 and d.month == 3 and d.day == 1, five_months),
        None
    )
    assert two is not None
    three = next(
        filter(lambda d: d.year == 1970 and d.month == 4 and d.day == 1, five_months),
        None
    )
    assert three is not None
    four = next(
        filter(lambda d: d.year == 1970 and d.month == 5 and d.day == 1, five_months),
        None
    )
    assert four is not None
    five = next(
        filter(lambda d: d.year == 1970 and d.month == 6 and d.day == 1, five_months),
        None
    )
    assert five is None


def test_day_iterator():
    ite = day_iterator(datetime(1970, 1, 1))
    five_days = list(islice(ite, 5))
    assert len(five_days) == 5
    zero = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1, five_days),
        None
    )
    assert zero is not None
    one = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 2, five_days),
        None
    )
    assert one is not None
    two = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 3, five_days),
        None
    )
    assert two is not None
    three = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 4, five_days),
        None
    )
    assert three is not None
    four = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 5, five_days),
        None
    )
    assert four is not None
    five = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 6, five_days),
        None
    )
    assert five is None


def test_hour_iterator():
    ite = hour_iterator(datetime(1970, 1, 1))
    five_hours = list(islice(ite, 5))
    assert len(five_hours) == 5
    zero = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0, five_hours),
        None
    )
    assert zero is not None
    one = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 1, five_hours),
        None
    )
    assert one is not None
    two = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 2, five_hours),
        None
    )
    assert two is not None
    three = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 3, five_hours),
        None
    )
    assert three is not None
    four = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 4, five_hours),
        None
    )
    assert four is not None
    five = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 5, five_hours),
        None
    )
    assert five is None


def test_minute_iterator():
    ite = minute_iterator(datetime(1970, 1, 1))
    five_minutes = list(islice(ite, 5))
    assert len(five_minutes) == 5
    zero = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0 and d.minute == 0,
               five_minutes),
        None
    )
    assert zero is not None
    one = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0 and d.minute == 1,
               five_minutes),
        None
    )
    assert one is not None
    two = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0 and d.minute == 2,
               five_minutes),
        None
    )
    assert two is not None
    three = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0 and d.minute == 3,
               five_minutes),
        None
    )
    assert three is not None
    four = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0 and d.minute == 4,
               five_minutes),
        None
    )
    assert four is not None
    five = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1 and d.hour == 0 and d.minute == 5,
               five_minutes),
        None
    )
    assert five is None


def test_second_iterator():
    ite = second_iterator(datetime(1970, 1, 1))
    five_seconds = list(islice(ite, 5))
    assert len(five_seconds) == 5
    zero = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1
               and d.hour == 0 and d.minute == 0 and d.second == 0,
               five_seconds),
        None
    )
    assert zero is not None
    one = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1
               and d.hour == 0 and d.minute == 0 and d.second == 1,
               five_seconds),
        None
    )
    assert one is not None
    two = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1
               and d.hour == 0 and d.minute == 0 and d.second == 2,
               five_seconds),
        None
    )
    assert two is not None
    three = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1
               and d.hour == 0 and d.minute == 0 and d.second == 3,
               five_seconds),
        None
    )
    assert three is not None
    four = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1
               and d.hour == 0 and d.minute == 0 and d.second == 4,
               five_seconds),
        None
    )
    assert four is not None
    five = next(
        filter(lambda d: d.year == 1970 and d.month == 1 and d.day == 1
               and d.hour == 0 and d.minute == 0 and d.second == 5,
               five_seconds),
        None
    )
    assert five is None
