from etlfunc.Tr import Tr
from etlfunc.tuple.TupleOperations import keep
from etlfunc.tuple.Formats import from_json, to_json, csv_to_map, map_to_csv


def test_reader_json_empty():
    operation = Tr(keep(fields=["who"])).reader(from_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_reader_json_some_working():
    operation = Tr(keep(fields=["who"])).reader(from_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation('{"who": "anciano"}')
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert "who" in transformed_output
    assert transformed_output["who"] == "anciano"
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_json_empty():
    operation = Tr(keep(fields=["who"])).then(to_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_json_some_working():
    operation = Tr(keep(fields=["who"])).then(to_json).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"who": "anciano"})
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert transformed_output == '{"who": "anciano"}'
    assert transformed_error is not None
    assert transformed_error == {}


def test_reader_csv_empty():
    operation = Tr(keep(fields=["who"])).reader(csv_to_map(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_reader_csv_some_working():
    operation = Tr(keep(fields=["who"])).reader(csv_to_map(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation('"anciano"\r\n')
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert "who" in transformed_output
    assert transformed_output["who"] == "anciano"
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_csv_empty():
    operation = Tr(keep(fields=["who"])).then(map_to_csv(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation(None)
    assert transformed_input is None
    assert transformed_output is not None
    assert transformed_output == {}
    assert transformed_error is not None
    assert transformed_error == {}


def test_writer_csv_some_working():
    operation = Tr(keep(fields=["who"])).then(map_to_csv(["who"])).apply()
    (transformed_input, transformed_output, transformed_error) = operation({"who": "anciano"})
    assert transformed_input is not None
    assert "who" in transformed_input
    assert transformed_input["who"] == "anciano"
    assert transformed_output is not None
    assert transformed_output == '"anciano"\r\n'
    assert transformed_error is not None
    assert transformed_error == {}
