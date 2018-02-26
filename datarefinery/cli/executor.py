import pkgutil
import inspect

import click

from datarefinery.cli.parser import load_yml, validate_data, parser_errors

IMPORTS = {}


def __populate_globals():
    for finder, mname, ispackage in pkgutil.iter_modules(['datarefinery']):
        if not ispackage:
            module = finder.find_module(mname).load_module()
            functions = inspect.getmembers(module, predicate=inspect.isfunction)
            IMPORTS.update({k: v for k, v in functions if not k.startswith('_')})
    return IMPORTS.copy()


def __get_operations(metadata):
    etl_locals = {}
    etl_globals = __populate_globals()
    etl_operations = {}

    data = load_yml(metadata)
    validation = validate_data(data)

    if validation:
        for etl in data['etls']:
            ops = []
            if etl.get('transformations').get('helpers') is not None:
                helpers = compile(open(etl['transformations']['helpers']).read(), metadata, 'exec')
                # Populate local functions with definitions on helpers section
                exec(helpers, etl_globals, etl_locals)
            if etl.get('dependencies') is not None:
                for dependency in etl['dependencies']:
                    ops.append(etl_operations[dependency])
            operation = eval(etl['transformations']['operation'], etl_globals, etl_locals)
            if len(ops) != 0:
                for op in ops:
                    # final operation
                    ...
            etl_operations[etl['name']] = operation
        error = ""
    else:
        error = "metadata file is not valid: {}".format(parser_errors(data))
    return etl_operations, error


@click.command()
@click.option('--etl', help='etl for execution')
@click.argument('metadata')
def cli(metadata, etl):
    (operations, err) = __get_operations(metadata)
