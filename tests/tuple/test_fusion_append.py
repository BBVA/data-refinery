from datarefinery.TupleOperations import fusion_append, wrap


def greet_person_and_world(x):
    return {"greet_person": " ".join(x), "greet_world": "{} world".format(x[0])}


def test_empty():
    inp = None
    op = fusion_append(
        fields=["greet", "who"],
        error_field="tfus",
        etl_func=wrap(greet_person_and_world)
    )

    (res, err) = op(inp)

    assert res is None
    assert err == {"tfus": "no input provided"}


def test_some_working():
    inp = {"greet": "hello", "who": "Tom"}
    op = fusion_append(
        fields=["greet", "who"],
        error_field="tfus",
        etl_func=wrap(greet_person_and_world)
    )

    (res, err) = op(inp)

    assert res == {'greet_person': 'hello Tom', 'greet_world': 'hello world'}
    assert err is None


def test_some_fields_missing():
    inp = {"greet": "hello"}
    op = fusion_append(
        fields=["greet", "who"],
        error_field="tfus",
        etl_func=wrap(greet_person_and_world)
    )

    (res, err) = op(inp)

    assert res is None
    assert err == {"tfus": "who not found"}
