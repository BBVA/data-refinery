from etlfunc.FieldOperations import add_column_prefix


def test_empty():
    operation = add_column_prefix("no")
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_some_working():
    operation = add_column_prefix("no")
    (res, err) = operation({"hello": "goodbye"})
    assert res is not None
    assert "no_hello" in res
    assert res["no_hello"] == "goodbye"
    assert err is None
