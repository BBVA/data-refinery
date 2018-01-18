from datarefinery.TupleOperations import keep


def test_empty():
    inp = None
    op = keep(["field1"])
    (res, err) = op(inp)

    assert res is None
    assert err == {'field1': 'field1 not found'}


def test_some_value():
    inp = {"field1": True}
    op = keep(["field1"])
    (res, err) = op(inp)

    assert res == {"field1": True}
    assert err is None


def test_field_not_found():
    inp = {"field1": True}
    op = keep(["missing"])
    (res, err) = op(inp)

    assert res is None
    assert err == {'missing': 'missing not found'}


def test_multiple_fields():
    inp = {"field1": True, "field2": True, "field3": True, "field4": True}
    op = keep(["field1", "field2", "field3"])
    (res, err) = op(inp)

    assert err is None
    assert res == {"field1": True, "field2": True, "field3": True}
