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

# Example of integration with pandas
import pandas as pd
from datarefinery.TupleOperations import fusion, wrap


def pandas_dataframe_operator(df, operation):
    if df is None or operation is None:
        return None, None
    raw_df = pd.DataFrame(df.apply(operation, axis=1), columns=["res"])

    raw_df['ok'] = raw_df["res"].apply(lambda x: x[0])
    raw_df['ko'] = raw_df["res"].apply(lambda x: x[1])

    raw_df = pd.concat([df, raw_df[['ok', 'ko']]], axis=1)

    ok_filter = raw_df["ok"].apply(lambda x: x is not None)
    ok_df = raw_df[ok_filter]
    ok_df = pd.DataFrame(ok_df["ok"].apply(pd.Series))
    ko_df = raw_df[~ok_filter]
    ko_df = pd.concat([ko_df, pd.DataFrame(ko_df["ko"].apply(pd.Series))], axis=1)
    del ko_df['ok']
    del ko_df['ko']

    return ok_df, ko_df


def test_empty():
    (res, err) = pandas_dataframe_operator(None, None)

    assert res is None
    assert err is None


def test_some():
    greet = ["hello", "hi", "greetings"]
    people = ["Tom", "Alex", "Unihorn"]

    df = pd.DataFrame.from_dict({'greet': greet, 'people': people})
    operation = fusion(["greet", "people"], "salute", wrap(lambda x: x[0] + " " + x[1]))

    (res, err) = pandas_dataframe_operator(df, operation)
    assert res is not None
    assert isinstance(res, pd.DataFrame)
    assert err is not None
    assert isinstance(err, pd.DataFrame)
    assert res['salute'].tolist() == ['hello Tom', 'hi Alex', 'greetings Unihorn']


def test_some_error():
    greet = ["hello", "hi", "greetings"]
    people = ["Tom", "Alex", "Unihorn"]

    df = pd.DataFrame.from_dict({'greet': greet, 'people': people})
    operation = fusion(["gredo", "people"], "salute", wrap(lambda x: x[0] + " " + x[1]))

    (res, err) = pandas_dataframe_operator(df, operation)
    assert res is not None
    assert isinstance(res, pd.DataFrame)
    assert err is not None
    assert isinstance(err, pd.DataFrame)
    assert err['salute'].tolist() == ['gredo not found', 'gredo not found', 'gredo not found']
