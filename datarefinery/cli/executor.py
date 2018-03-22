import inspect
import logging
import os
import pkgutil
import sys

import click

import datarefinery
from datarefinery.cli.parser import load_yml, validate_data, parser_errors
from datarefinery.tuple.tupledsl import compose

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def _populate_globals(package):
    """
    Function to populate all functions from package

    """
    func_globals = {}
    for finder, mname, ispackage \
            in pkgutil.walk_packages(path=package.__path__,
                                     prefix=package.__name__+'.',
                                     onerror=lambda x: None):
        if not ispackage:
            module = finder.find_module(mname).load_module()
            functions = inspect.getmembers(module, predicate=inspect.isfunction)
            func_globals.update({k: v for k, v in functions if not k.startswith('_')})
    return func_globals


def _execution_stdin(operation):
    """
    Function to execute the transformation and see the results

    """
    total = 0
    processed = 0
    filtered = 0
    failed = 0

    # stdin_text = click.get_text_stream('stdin')
    # stdout_binary = click.get_binary_stream('stdout')

    for event in sys.stdin:
        if event == '':
            continue
        (res, err) = operation(event)
        total += 1
        if err is not None and len(err) > 0:
            failed += 1
            logger.error("{}".format(err))
        elif res is not None:
            processed += 1
            print("{}".format(res))
        else:
            filtered += 1
        if total % 100 == 0:
            logger.error("total:{} failed:{} processed:{} filtered:{}".format(total, failed, processed, filtered))

    logger.info("total:{} failed:{} processed:{} filtered:{}".format(total, failed, processed, filtered))


class EtlExecutor:
    """
    Define your transformation class

    """
    def __init__(self, filename):
        self.METADATA = filename
        self.IMPORTS = _populate_globals(datarefinery)
        (self.ETLS, err) = self._get_operations()
        if err is None:
            click.echo(err)

    def execute_etl(self, name):
        operation = self.ETLS[name]()
        _execution_stdin(operation)

    def _get_operations(self):
        """
        Returns a dictionary with all transformations defined on metadata_file.
        :return: a tuple, the dictionary and error
        """
        etl_globals = self.IMPORTS
        etl_locals = {}
        etl_operations = {}

        data = load_yml(self.METADATA)
        is_valid = validate_data(data)

        if is_valid:
            for etl in data['etls']:
                if etl.get('transformations').get('helpers') is not None:
                    path_helpers = os.path.abspath(etl['transformations']['helpers'])
                    helpers = compile(open(path_helpers).read(), self.METADATA, 'exec')
                    # Populate local functions with definitions on helpers section
                    exec(helpers, etl_globals, etl_locals)

                operation = eval(etl['transformations']['operation'], etl_globals, etl_locals)

                if etl.get('dependencies') is None:
                    # avoid late binding
                    def getop(operation=operation):
                        return operation
                else:
                    def getop(etl=etl, etl_operations=etl_operations, operation=operation):
                        deps = [etl_operations[name]() for name in etl['dependencies']]
                        return compose(*deps, operation)

                etl_operations[etl["name"]] = getop

            error = None
        else:
            error = "Your metadata file is not valid: {}".format(parser_errors(data))

        return etl_operations, error


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Cli for data-refinery to transform your data"""
    ...


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('metadata_file', type=click.Path(exists=True))
def validate(metadata_file):
    """Command for validate your metadata file"""
    data = load_yml(metadata_file)
    if type(data) is str:
        logger.error("YAMLError: {}".format(data))
    elif validate_data(data):
        print("Your metadata file is correct :)")
    else:
        logger.error("SchemaError: your metadata file is incorrect. "
                     "Please, fix the next errors: {}".format(parser_errors(data)))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('metadata_file', type=click.Path(exists=True))
@click.option('-e', '--etl', metavar='<str>', help='name of the etl to execute')
# @click.argument('data_file', type=click.File('wb'))
def run(etl, metadata_file):
    """Command to execute your transformation"""
    executor = EtlExecutor(metadata_file)
    if etl:
        executor.execute_etl(etl)
    else:
        print("You have to specify an etl to execute: {}".format([key for key in executor.ETLS.keys()]))
