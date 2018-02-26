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

from datarefinery.tuple_operations import substitution
from datarefinery.field_operations import replace_if


def test_some_working():
    def _if_part(x):
        return x == 0

    def _fun_part(x):
        return x+1

    inp = {"a": 0}
    operation = substitution(["a"], replace_if(_if_part, _fun_part))
    (res, err) = operation(inp)
    assert inp is not None
    assert res is not None
    assert "a" in res
    assert res["a"] == 1
    assert err is None


def test_empty():
    def _if_part(x):
        return x == 0

    def _fun_part(x):
        return x+1

    operation = substitution(["a"], replace_if(_if_part, _fun_part))
    (res, err) = operation(None)
    assert res is None
    assert err == {'a': 'a not found'}
