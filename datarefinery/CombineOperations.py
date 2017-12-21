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


def parallel(*tupleOperations):
    # inp, err
    # todas las tuple Operations reciben el mismo input y error
    # luego combinamos todos los outputs y errors
    # se devuelve el output combinado y el error
    # map y reduce, pringada
    def _no_operations(inp, err=None):
        if err is None:
            err = {}
        if inp is None:
            inp = {}
        return inp, err

    def _no_affect(inp, err):
        i = copy.deepcopy(inp)
        e = copy.deepcopy(err)
        return i, e

    def _apply(inp, err):
        def _reductor(acc, re):
            (i, e) = acc
            (o, er) = re
            i.update(o)
            e.update(er)
            return i, e
        inmutable = map(lambda x: compose(_no_affect, x), tupleOperations)
        results = map(lambda x: x(inp, err), inmutable)
        return reduce(_reductor, results, ({}, {}))

    some_params = any(map(lambda x: x is not None, tupleOperations))
    if tupleOperations is not None and some_params:
        return compose(_no_operations, _apply)
    return _no_operations


def secuential(*tupleOperations):
    # inp, err
    # la primera operacion recibe el inp
    # cada operacion recibe como input el output de la anterior
    # devolvemos el output y el error de la ultima
    # con our compose
    def _no_operations(inp, err=None):
        if err is None:
            err = {}
        if inp is None:
            inp = {}
        return inp, err

    def _no_affect(inp, err):
        i = copy.deepcopy(inp)
        e = copy.deepcopy(err)
        return i, e

    def _apply(inp, err=None):
        for operation in tupleOperations:
            inp, err = operation(inp, err)
        return inp, err

    some_params = any(map(lambda x: x is not None, tupleOperations))
    if tupleOperations is not None and some_params:
        return compose(_no_operations, _no_affect, _apply)
    return _no_operations
