from datarefinery.tuple.TupleDSL import compose, read_field, write_field, apply_over_output, read_match, \
    read_fields, write_error_field, dict_enforcer
from functools import reduce


def wrap(func):
    def _app(i, err):
        try:
            if i is not None:
                return func(i), None
            return i, err
        except Exception as e:
            return None, e

    return _app


def keep(fields):
    operations = [compose(read_field(f), write_field(f)) for f in fields]
    return reduce(compose, operations)


def keep_regexp(regexp):
    return compose(read_match(regexp), dict_enforcer, write_error_field(regexp))


def substitution(fields, etl_func):
    operations = [compose(read_field(f), etl_func, write_field(f)) for f in fields]
    return reduce(compose, operations)


def fusion(fields, target_field, etl_func):
    """
    TODO: dict based better than list based please

    :param fields:
    :param target_field:
    :param etl_func:
    :return:
    """
    return compose(read_fields(fields), etl_func, write_field(target_field))


def fusion_append(fields, error_field, etl_func):
    """
    TODO: dict based better than list based please

    :param fields:
    :param error_field:
    :param etl_func:
    :return:
    """
    return compose(read_fields(fields),
                   etl_func, dict_enforcer, write_error_field(error_field))


def append(fields, etl_func):
    operations = [compose(read_field(f), etl_func, dict_enforcer, write_error_field(f))
                  for f in fields]
    return reduce(compose, operations)


def filter_tuple(fields, etl_func):
    operations = [compose(read_field(f), etl_func, write_error_field(f)) for f in fields]

    def _app(input_dict: dict, output_dict: dict, error_dict: dict):
        for f in operations:
            (res, err) = f(input_dict, output_dict, error_dict)

            if err is not None:
                error_dict.update(err)

            if (res is not None and res is False) or (res is None):
                return input_dict, None, error_dict
        return input_dict, output_dict, error_dict

    return _app


def alternative(*alternatives):
    def reduction(a, b):
        def _app(input_dict, error_dict=None):
            if error_dict is None:
                error_dict = {}
            (res, err) = a(input_dict, error_dict)
            if len(err) == 0:
                return res, error_dict
            return b(input_dict, error_dict)

        return _app

    if len(alternatives) == 1:
        return alternatives[0]
    return reduce(reduction, alternatives)
