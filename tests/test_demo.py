from etlfunc.tuple.TupleOperations import keep
from etlfunc.Tr import Tr


def test_demo():
    keep_people = Tr(keep(["who"])).apply()
    (inp, res, err) = keep_people({"greet": "hello", "who": "world"})
    assert res == {'who': 'world'}
