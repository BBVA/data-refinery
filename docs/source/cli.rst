Command Line Interface
======================

The data-refinery CLI provides direct use of transformations on your data. These transformations must be described on
a YAML file.

YAML schema
-----------

.. code-block:: yaml

    {
        'etls':
            {
                'type': 'list',
                'minlength': 1,
                'required': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'dependencies': {
                            'type': 'list',
                            'required': False,
                            'schema': {
                                'type': 'string',
                                'empty': False
                            }
                        },
                        'name': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        },
                        'transformations': {
                            'required': True,
                            'type': 'dict',
                            'schema': {
                                'operation': {
                                    'type': 'string',
                                    'required': True,
                                    'empty': False
                                },
                                'helpers': {
                                    'type': 'string',
                                    'required': False,
                                    'empty': False
                                }
                            }
                        }
                    }
                }
            }
    }

For example:

.. code-block:: yaml

    etls:
    - name: final
      transformations:
        helpers: /path/to/helpers.py
        operation: |
          parallel(keep(['feat1']), substitution(['feat2'], wrap(x2)))
      dependencies:
        - initial
    - name: initial
      transformations:
        operation: |
          sequential(from_json, keep_regexp(".*"))

Help
~~~~

To get help when using the data-refinery CLI, you can simply add help to the end of the command.

.. code-block:: bash

    data-refinery --help

There are two subcommands:

  - run
  - validate

For both, it's necessary add as argument a metadata_file. This file is the YAML where your transformations are.

Validate
~~~~~~~~
Command for validate your metadata file.

Usage:

.. code-block:: bash

    data-refinery validate metadata.yaml

The output will be an OK or the error on your YAML file.

Run
~~~
Command to execute your transformation.

Usage:

.. code-block:: bash

    cat joined.json | data-refinery run metadata.yaml --etl initial

The output will be your data transformed.