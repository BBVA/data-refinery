from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import keep, substitution, fusion, append, filter_tuple, wrap, change, \
    keep_regexp, fusion_append


def test_keep_empty():
    operation = Tr(keep(["hello"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_keep():
    operation = Tr(keep(["hello"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == "Tom"
    assert transformed_error is not None
    assert transformed_error == {}


def test_keep_some_fields():
    operation = Tr(keep(["hello"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom", "greet": "hello"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert "greet" in transformed_input
    assert transformed_input["greet"] == "hello"
    assert transformed_output is not None
    assert "greet" not in transformed_output
    assert "hello" in transformed_output
    assert transformed_output["hello"] == "Tom"
    assert transformed_error is not None
    assert transformed_error == {}


def test_substitution_empty():
    operation = Tr(substitution(["hello"], etl_func=lambda i, e: (len(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_substitution():
    operation = Tr(substitution(["hello"], etl_func=lambda i, e: (len(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == 5
    assert transformed_error is not None
    assert transformed_error == {}


def test_substitution_func():
    operation = Tr(substitution(["hello"], etl_func=wrap(lambda i: len(i)))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "hello" in transformed_output
    assert transformed_output["hello"] == 5
    assert transformed_error is not None
    assert transformed_error == {}


def test_substitution_some_fields():
    operation = Tr(substitution(["hello"], etl_func=lambda i, e: (len(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom", "greet": "hello"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert "greet" in transformed_input
    assert transformed_input["greet"] == "hello"
    assert transformed_output is not None
    assert "greet" not in transformed_output
    assert "hello" in transformed_output
    assert transformed_output["hello"] == 3
    assert transformed_error is not None
    assert transformed_error == {}


def test_substitution_some_fields_some_values():
    operation = Tr(substitution(["hello", "greet"], etl_func=lambda i, e: (len(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "Tom", "greet": "hello"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "Tom"
    assert "greet" in transformed_input
    assert transformed_input["greet"] == "hello"
    assert transformed_output is not None
    assert "greet" in transformed_output
    assert transformed_output["greet"] == 5
    assert "hello" in transformed_output
    assert transformed_output["hello"] == 3
    assert transformed_error is not None
    assert transformed_error == {}


def test_fusion_empty():
    operation = Tr(fusion(fields=["a", "b"], target_field="greet", etl_func=lambda i, e: (" ".join(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_fusion():
    operation = Tr(fusion(fields=["a", "b"], target_field="greet", etl_func=lambda i, e: (" ".join(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello", "b": "world"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "b" in transformed_input
    assert transformed_input["b"] == "world"
    assert transformed_output is not None
    assert "greet" in transformed_output
    assert transformed_output["greet"] == "hello world"
    assert "a" not in transformed_output
    assert "b" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_fusion_func():
    operation = Tr(fusion(fields=["a", "b"], target_field="greet", etl_func=wrap(lambda i: " ".join(i)))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello", "b": "world"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "b" in transformed_input
    assert transformed_input["b"] == "world"
    assert transformed_output is not None
    assert "greet" in transformed_output
    assert transformed_output["greet"] == "hello world"
    assert "a" not in transformed_output
    assert "b" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_fusion_some_fields():
    operation = Tr(fusion(fields=["a", "b"], target_field="greet", etl_func=lambda i, e: (" ".join(i), None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello", "b": "mad", "c": "world"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "b" in transformed_input
    assert transformed_input["b"] == "mad"
    assert "c" in transformed_input
    assert transformed_input["c"] == "world"
    assert transformed_output is not None
    assert "greet" in transformed_output
    assert transformed_output["greet"] == "hello mad"
    assert "a" not in transformed_output
    assert "b" not in transformed_output
    assert "c" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_append_empty():
    operation = Tr(append(fields=["hello"], etl_func=lambda i, e: ({"head": i[0], "tail": i[1:]}, None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_append():
    operation = Tr(append(fields=["hello"], etl_func=lambda i, e: ({"head": i[0], "tail": i[1:]}, None))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "head" in transformed_output
    assert transformed_output["head"] == "w"
    assert "tail" in transformed_output
    assert transformed_output["tail"] == "orld"
    assert "hello" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_append_func():
    operation = Tr(append(fields=["hello"], etl_func=wrap(lambda i: ({"head": i[0], "tail": i[1:]})))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"hello": "world"})
    assert transformed_input is not None
    assert "hello" in transformed_input
    assert transformed_input["hello"] == "world"
    assert transformed_output is not None
    assert "head" in transformed_output
    assert transformed_output["head"] == "w"
    assert "tail" in transformed_output
    assert transformed_output["tail"] == "orld"
    assert "hello" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_append_some_fields():
    operation = Tr(append(fields=["a"], etl_func=wrap(lambda i: ({"head": i[0], "tail": i[1:]})))) \
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello", "b": "mad", "c": "world"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "b" in transformed_input
    assert transformed_input["b"] == "mad"
    assert "c" in transformed_input
    assert transformed_input["c"] == "world"
    assert transformed_output is not None
    assert "head" in transformed_output
    assert transformed_output["head"] == "h"
    assert "tail" in transformed_output
    assert transformed_output["tail"] == "ello"
    assert "a" not in transformed_output
    assert "b" not in transformed_output
    assert "c" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_filter_positive():
    operation = Tr(filter_tuple(fields=["a"], etl_func=wrap(lambda i: i == "hello"))).then(keep(fields=["b"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello", "b": "world"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "b" in transformed_input
    assert transformed_input["b"] == "world"
    assert "a" not in transformed_output
    assert "b" in transformed_output
    assert transformed_output["b"] == "world"
    assert transformed_error is not None
    assert transformed_error == {}


def test_filter_negative():
    operation = Tr(filter_tuple(fields=["a"], etl_func=wrap(lambda i: i != "hello"))).then(keep(fields=["b"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello", "b": "world"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "b" in transformed_input
    assert transformed_input["b"] == "world"
    assert transformed_output is None
    assert transformed_error is not None
    assert transformed_error == {}


def test_filter_none_value():
    operation = Tr(filter_tuple(fields=["a"], etl_func=wrap(lambda i: i != "hello"))).then(keep(fields=["b"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"b": "world"})
    assert transformed_input is not None
    assert "b" in transformed_input
    assert transformed_input["b"] == "world"
    assert transformed_output is None
    assert transformed_error is not None
    assert transformed_error == {'a': 'a not found'}


def test_filter_none_value_with_err():
    def _filter_with_err(i, e):
        if i is None:
            return None, e
        return None, "There is a nasty error"
    operation = Tr(filter_tuple(fields=["b"], etl_func=_filter_with_err)).then(keep(fields=["b"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"b": "world"})
    assert transformed_input is not None
    assert "b" in transformed_input
    assert transformed_input["b"] == "world"
    assert transformed_output is None
    assert transformed_error is not None
    assert transformed_error["b"] == "There is a nasty error"


def test_change():
    operation = Tr(substitution(["a"], etl_func=wrap(lambda x: x.upper())))\
        .then(change(fields=["a"], etl_func=wrap(lambda x: f"{x}!!!")))\
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"a": "hello"})
    assert transformed_input is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert transformed_output is not None
    assert "a" in transformed_output
    assert transformed_output["a"] == "HELLO!!!"
    assert transformed_error is not None
    assert transformed_error == {}


def test_keep_regexp():
    operation = Tr(keep_regexp(regexp="a_?.*")).apply()
    input_tuple = {"a": "hello", "a_1": "world", "b": "no keep"}
    (transformed_input, transformed_output, transformed_error) = operation(input_tuple)
    assert transformed_input is not None
    assert transformed_output is not None
    assert transformed_error is not None
    assert "a" in transformed_input
    assert transformed_input["a"] == "hello"
    assert "a_1" in transformed_input
    assert transformed_input["a_1"] == "world"
    assert "b" in transformed_input
    assert transformed_input["b"] == "no keep"
    assert "a" in transformed_output
    assert transformed_output["a"] == "hello"
    assert "a_1" in transformed_output
    assert transformed_output["a_1"] == "world"
    assert "b" not in transformed_output
    assert transformed_error is not None
    assert transformed_error == {}


def test_fusion_append():
    operation = Tr(fusion_append(
        fields=["greet", "who"], error_field="tfus",
        etl_func=wrap(lambda x: {"greet_person": " ".join(x), "greet_world": f"{x[0]} world"}))
    )\
        .apply()
    (transformed_input, transformed_output, transformed_error) = operation({"greet": "hello", "who": "Tom"})
    assert transformed_input is not None
    assert "greet" in transformed_input
    assert transformed_input["greet"] == "hello"
    assert "who" in transformed_input
    assert transformed_input["who"] == "Tom"
    assert transformed_output is not None
    assert "greet_person" in transformed_output
    assert transformed_output["greet_person"] == "hello Tom"
    assert "greet_world" in transformed_output
    assert transformed_output["greet_world"] == "hello world"
    assert transformed_error is not None
    assert transformed_error == {}
