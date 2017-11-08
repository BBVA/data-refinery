import json
import io
import csv


def from_json(i, o, e):
    """
    convert json to dict

    :param i:
    :param o:
    :param e:
    :return:
    """
    return json.loads(i), o, e


def to_json(i, o, e):
    """
    convert dict to json

    :param i:
    :param o:
    :param e:
    :return:
    """
    return i, json.dumps(o), e


def _list_to_csv(l):
    """
    Util function to overcome the use of files by in-memory io buffer

    :param l:
    :return:
    """
    io_file = io.StringIO()
    writer = csv.writer(io_file, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(l)
    return io_file.getvalue()


def _csv_to_list(csv_input):
    """
    Util function to overcome the use of files by in-memory io buffer

    :param csv_input:
    :return:
    """
    io_file = io.StringIO(csv_input)
    return next(csv.reader(io_file, delimiter=','))


def csv_to_map(fields):
    """
    Convert csv to dict

    :param fields:
    :return:
    """
    def _app(current_tuple, o={}, e={}):
        csv_list = _csv_to_list(current_tuple)
        if len(csv_list) != len(fields):
            e.update({"input": f"unexpected number of fields {len(csv_list)} obtained {len(fields)} expected"})
            return None, o, e
        return {k: v for (k, v) in zip(fields, csv_list)}, o, e
    return _app


def map_to_csv(fields):
    """
    Convert dict to csv

    :param fields:
    :return:
    """
    def _app(i, current_tuple={}, e={}):
        csv_list = []
        for f in fields:
            if f in current_tuple:
                csv_list.append(current_tuple[f])
            else:
                e.update({"output": f"expected field {f} not found"})
                return i, None, e
        return i, _list_to_csv(csv_list), e
    return _app
