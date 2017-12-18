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


def parallel(*tupleOperations):
    # inp, err
    # todas las tuple Operations reciben el mismo input y error
    # luego combinamos todos los outputs y errors
    # se devuelve el output combinado y el error
    # map y reduce, pringada
    def _apply(inp, err):
        out = copy.deepcopy(inp)  # input inmutable? si no, out = inp
        for operation in tupleOperations:
            pout, perr = operation(inp, err)
            out.update(pout)
            err.update(perr)
        return out, err
    return _apply


def secuential(*tupleOperations):
    # inp, err
    # la primera operacion recibe el inp
    # cada operacion recibe como input el output de la anterior
    # devolvemos el output y el error de la ultima
    # con our compose
    def _apply(inp, err):
        for operation in tupleOperations:
            inp, err = operation(inp, err)
        return inp, err
    return _apply
