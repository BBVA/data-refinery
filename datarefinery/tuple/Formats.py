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
import io
import csv
from datarefinery.tuple.TupleDSL import fixed_input


def from_json(i, e=None):
    try:
        return json.loads(i), e
    except Exception as err:
        return None, "Can't parse"


def to_json(i, e=None):
    if e is not None:
        return None, e
    return json.dumps(i), e


def _list_to_csv(l):
    """
    Util function to overcome the use of files by in-memory io buffer

    :param l:
    :return:
    """
    io_file = io.StringIO()
    writer = csv.writer(io_file, quoting=csv.QUOTE_NONNUMERIC, lineterminator='')
    writer.writerow(l)
    return io_file.getvalue()


def _csv_to_list(csv_input):
    """
    Util function to overcome the use of files by in-memory io buffer

    :param csv_input:
    :return:
    """
    io_file = io.StringIO(csv_input)
    return next(csv.reader(io_file, delimiter=','))


def csv_to_map(fields):
    """
    Convert csv to dict

    :param fields:
    :return:
    """
    def _app(current_tuple, e=None):
        if current_tuple is None or len(current_tuple) == 0:
            return None, "no input"
        csv_list = _csv_to_list(current_tuple)
        if len(csv_list) != len(fields):
            e = {"input": "unexpected number of fields {} obtained {} expected".format(len(csv_list), len(fields))}
            return None, e
        return {k: v for (k, v) in zip(fields, csv_list)}, e
    if fields is None or len(fields) == 0:
        return fixed_input(None, "no fields provided, cannot proceed without order")
    return _app


def map_to_csv(fields):
    """
    Convert dict to csv

    :param fields:
    :return:
    """
    def _app(current_tuple, e=None):
        if e is not None:
            return None, e
        csv_list = []
        for f in fields:
            if f in current_tuple:
                csv_list.append(current_tuple[f])
            else:
                e.update({"output": "expected field {} not found".format(f)})
                return None, e
        return _list_to_csv(csv_list), e
    if fields is None or len(fields) == 0:
        return fixed_input(None, "no fields provided, cannot proceed without order")
    return _app
