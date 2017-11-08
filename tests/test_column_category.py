from etlfunc.FieldOperations import column_category


def test_empty():
    operator = column_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operator = column_category(None)
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_all_empty():
    operator = column_category(None)
    (res, err) = operator(None)
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_simple():
    operator = column_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator("niño")
    assert res is not None
    assert err is None
    assert res == {"bebé": 0, "niño": 1, "joven": 0, "adulto": 0, "anciano": 0}


def test_zero_categories():
    operator = column_category([])
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_different_category():
    operator = column_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator("buzo")
    assert res is None
    assert err is not None
    assert err == "value buzo not found on categories"
