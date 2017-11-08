from etlfunc.FieldOperations import std_score_normalization


def test_empty():
    operation = std_score_normalization(55, 100)
    (res, err) = operation(None)
    assert res is None
    assert err is None


def test_all_empty():
    operation = std_score_normalization(None, None)
    (res, err) = operation(None)
    assert res is None
    assert err is not None
    assert err == "average is required"


def test_empty_definition():
    operation = std_score_normalization(None, None)
    (res, err) = operation(50)
    assert res is None
    assert err is not None
    assert err == "average is required"


def test_some_working():
    operation = std_score_normalization(79, 8)
    (res, err) = operation(85)
    assert res is not None
    assert res == 0.75
    assert err is None


def test_some_working_2():
    operation = std_score_normalization(70, 5)
    (res, err) = operation(74)
    assert res is not None
    assert res == 0.8
    assert err is None


def test_zero_deviation():
    operation = std_score_normalization(70, 0)
    (res, err) = operation(74)
    assert res is None
    assert err is not None
    assert err == "std deviation must be != 0"
