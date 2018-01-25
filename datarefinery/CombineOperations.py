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

import copy
from functools import reduce

from datarefinery.tuple.TupleDSL import compose


def parallel(*tuple_operations):
    def _no_operations(inp=None, err=None):
        return None, "No operations to perform"

    def _no_affect(inp, err=None):
        if inp is not None:
            i = copy.deepcopy(inp)
        else:
            i = None
        if err is not None:
            e = copy.deepcopy(err)
        else:
            e = None
        return i, e

    def _apply(inp, err=None):
        def _reducer(acc, re):
            (i, e) = acc
            (o, er) = re
            if o is not None and i is not None:
                i.update(o)
            elif o is not None:
                i = o
            if er is not None and e is not None:
                e.update(er)
            elif er is not None:
                e = er
            return i, e
        immutable = map(lambda x: compose(_no_affect, x), tuple_operations)
        results = map(lambda x: x(inp, err), immutable)
        return reduce(_reducer, results, (None, None))

    some_params = any(map(lambda x: x is not None, tuple_operations))
    if tuple_operations is not None and some_params:
        return _apply
    return _no_operations


def sequential(*tuple_operations):
    def _no_operations(inp=None, err=None):
        return None, "No operations to perform"

    def _no_affect(inp, err=None):
        if inp is not None:
            i = copy.deepcopy(inp)
        else:
            i = None
        if err is not None:
            e = copy.deepcopy(err)
        else:
            e = None
        return i, e

    some_params = any(map(lambda x: x is not None, tuple_operations))
    if tuple_operations is not None and some_params:
        return compose(_no_affect, reduce(compose, tuple_operations))
    return _no_operations
