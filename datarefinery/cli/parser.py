import yaml
from cerberus import Validator


SCHEMA = \
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


v = Validator(SCHEMA)


def load_yml(yml_path):
    with open(yml_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            raise exception


def validate_data(document):
    return v.validate(document)


def parser_errors(document):
    v.validate(document)
    return v.errors
