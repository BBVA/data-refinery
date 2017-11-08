from etlfunc.FieldOperations import linear_category


def test_empty():
    operator = linear_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator(None)
    assert res is None
    assert err is None


def test_empty_definition():
    operator = linear_category(None)
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_all_empty():
    operator = linear_category(None)
    (res, err) = operator(None)
    assert res is None
    assert err is not None
    assert err == "no categories supplied"


def test_simple():
    operator = linear_category(["bebé", "niño", "joven", "adulto", "anciano"])
    (res, err) = operator("niño")
    assert res is not None
    assert res == 2
    assert err is None


def test_zero_categories():
    operator = linear_category([])
    (res, err) = operator("niño")
    assert res is None
    assert err is not None
    assert err == "no categories supplied"
