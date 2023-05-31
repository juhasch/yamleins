"""Test the Validator class"""
from yamleins import Validator
from pytest import raises


def test_instance():
    """Test that Validator is an instance of dict"""
    schema = dict(type='float', default=1.0, unit='s', doc='Test', range=[0.0, 1.0])
    validator = Validator('param', schema)
    assert isinstance(validator, Validator)


def test_fields():
    """Test that Validator has the correct fields"""
    p = dict(type='float', default=1.0, unit='s', doc='Test', range=[0.0, 1.0])
    validator = Validator('param', p)
    for field in validator.fields:
        assert field in validator.schema


def test_valid_schema():
    schema = {'type': 'int', 'default': 0, 'unit': 'kg', 'doc': 'test doc', 'range': [0, 100]}
    validator = Validator('param', schema)
    assert validator.type == int
    assert validator.default == 0
    assert validator.unit == 'kg'
    assert validator.doc == 'test doc'
    assert validator.range == [0, 100]


def test_invalid_schema():
    schema = {'type': 'int', 'default': 0, 'doc': 'test doc', 'range': [0, 100]}
    with raises(KeyError):
        validator = Validator('param', schema)


def test_invalid_unit():
    schema = {'type': 'int', 'default': 0, 'unit': 'foobar', 'doc': 'test doc', 'range': [0, 100]}
    with raises(ValueError):
        validator = Validator('param', schema)
