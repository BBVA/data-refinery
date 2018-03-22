import logging
import os

from click.testing import CliRunner

from datarefinery.cli.executor import run, validate


logger = logging.getLogger(__name__)


def test_run_metadata_not_exist():
    runner = CliRunner()
    result = runner.invoke(run, ['pathdontexisthere', '--etl', 'initial'])
    assert result.exit_code == 2
    assert 'Path "pathdontexisthere" does not exist.' in result.output


def test_run_without_etl_argument():
    runner = CliRunner()
    result = runner.invoke(run, [os.path.abspath('tests/cli/files/metadata.yaml'), '--etl'])
    assert result.exit_code == 2
    assert '--etl option requires an argument' in result.output


def test_run_without_etl_option():
    runner = CliRunner()
    result = runner.invoke(run, [os.path.abspath('tests/cli/files/metadata.yaml')])
    assert result.exit_code == 0
    assert 'You have to specify an etl to execute' in result.output


def test_run_without_metadata():
    runner = CliRunner()
    result = runner.invoke(run, ['--etl', 'initial'])
    assert result.exit_code == 2
    assert 'Missing argument "metadata_file".' in result.output


def test_run_extra_argument():
    runner = CliRunner()
    result = runner.invoke(run, [os.path.abspath('tests/cli/files/metadata.yaml'), '--etl', 'initial', 'extraArgument'])
    assert result.exit_code == 2
    assert 'Got unexpected extra argument' in result.output


def test_run():
    runner = CliRunner()
    result = runner.invoke(run, [os.path.abspath('tests/cli/files/metadata.yaml'), '--etl', 'initial'])
    assert result.exit_code == 0


def test_validate_without_metadata():
    runner = CliRunner()
    result = runner.invoke(validate)
    assert result.exit_code == 2
    assert 'Missing argument "metadata_file".' in result.output


def test_validate_extra_argument():
    runner = CliRunner()
    result = runner.invoke(validate, [os.path.abspath('tests/cli/files/metadata.yaml'), 'extraArgument'])
    assert result.exit_code == 2
    assert 'Got unexpected extra argument' in result.output


def test_validate():
    runner = CliRunner()
    result = runner.invoke(validate, [os.path.abspath('tests/cli/files/metadata.yaml')])
    assert result.exit_code == 0
    assert 'Your metadata file is correct :)' in result.output
