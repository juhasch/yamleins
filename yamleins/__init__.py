"""ValidatedConfig"""

__version__: str = '0.1.0'

from dataclasses import dataclass
from typing import Dict, Any
import yaml
from PhysicalQuantities.unit import findunit
from PhysicalQuantities.transform import transform_line
from PhysicalQuantities import isphysicalquantity
from PhysicalQuantities import q as pq


class Validator:
    fields = ['type', 'default', 'unit', 'doc', 'range']
    schema: Dict[str, Any]
    name: str

    def __init__(self, name: str, schema: dict):
        self.name = name
        self.schema = schema
        self.check_schema()
        self.check_units()
        # convert...
        self.schema['type'] = eval(self.schema['type'])
        statement = transform_line(str(self.schema['default']))
        self.schema['default'] = eval(statement, dict(pq=pq))
        low = transform_line(str(self.schema['range'][0]))
        high = transform_line(str(self.schema['range'][1]))
        self.schema['range'] = [eval(low, dict(pq=pq)), eval(high, dict(pq=pq))]

    def check_schema(self):
        """Check if schema is valid"""
        if not all(field in self.schema for field in self.fields):
            raise KeyError(f'[{self.name}]: A field is missing in schema.')

    def check_units(self):
        """Check if value is valid unit"""
        if 'unit' in self.schema:
            value = self.schema['unit']
            if value not in ['', 'None'] and not findunit(value):
                raise ValueError(f'[{self.name}]: Unit {value} not found.')

    def verify(self, value):
        """Verify if value is valid

        Parameters
        ----------
        value
            Value to be verified
        """
        low = self.schema['range'][0]
        high = self.schema['range'][1]
        if not low <= value <= high:
            raise ValueError(f'[{self.name}]: Value {value} is not in range {self.schema["range"]}')
        if isphysicalquantity(value):
            value = value.value
        if not isinstance(value, self.schema['type']):
            raise TypeError(f'[{self.name}]: Value {value} is not of type {self.schema["type"]}')

    def __getattr__(self, item):
        return self.schema[item]


@dataclass
class YamlConfig:
    _parameters: Dict[str, 'Validator']  # Dict of parameters read from template yaml file
    _values: Dict[str, 'Any'] = None

    def __post_init__(self):
        self._values = dict()

    @staticmethod
    def create(yaml_str: str):
        """Create Config from template yaml string

        Parameters
        ----------
        yaml_str
            String containing YAML file
        """
        yaml_dict = yaml.safe_load(yaml_str)
        parameter_dict = dict()
        # Now populate the parameter_dict with the values from the yaml_dict
        for key, value in yaml_dict.items():
            parameter_dict[key] = Validator(key, value)
        return YamlConfig(parameter_dict)

    def load(self, yaml_str: str, keep_units: bool = True):
        """Load Config from YAML string

        Parameters
        ----------
        yaml_str
            String containing YAML file
        keep_units
            If True, keep the units in the values
        """
        config_dict = yaml.safe_load(yaml_str)
        for key, value in config_dict.items():
            if key in self._parameters:
                # Does the value have a unit...
                statement = transform_line(str(value))
                _value = eval(statement, self._values, dict(pq=pq))
                self._parameters[key].verify(_value)
                self._values[key] = _value
                self._values.pop('__builtins__', None)
            else:
                raise KeyError(f'Key {key} not found in parameters.')
        # Fill in default values
        for key, value in self._parameters.items():
            if key not in self._values:
                if value.default is None:
                    raise ValueError(f'[{key}]: No default value given.')
                statement = transform_line(str(value.default))
                _value = eval(statement, self._values, dict(pq=pq))
                self._values[key] = _value
                self._values.pop('__builtins__', None)
        # Remove units if requested
        if not keep_units:
            for key, value in self._values.items():
                if isphysicalquantity(value):
                    self._values[key] = value.base.value

    def __getitem__(self, item):
        return self._values[item]

    def __getattr__(self, item):
        return self._values[item]

    def __dict__(self):
        return self._values

#    def __dir__(self):
#        print('dir')
#        return list(self._values.keys())

    @property
    def yaml(self) -> str:
        """Export class as YAML string

        Returns
        -------
        YAML string
        """
        values = dict()
        for key, value in self._values.items():
            if isphysicalquantity(value):
                value = str(value)
            values[key] = value
        return yaml.dump(values)

    def __repr__(self):
        return f'YamlConfig({self._values})'


if __name__ == '__main__':
    a = """
        blue_time:
            type: float
            default: 20us
            unit: s
            doc: Duration of a single chirp
            range: [1 ns, 1s]

        num_blue_time:
            type: int
            default: 128
            unit: None
            doc: Number of fast time chirps
            range: [1, 1000]

        white_time:
            type: float
            default: 1ms
            unit: s
            doc: Duration of a single slow time frame
            range: [1 ns, 1s]
            
        bandwidth:
            type: float
            default: 1GHz
            unit: Hz
            doc: Bandwidth of the chirp
            range: [1 Hz, 10GHz]
    """
    b = """
        blue_time: 11us
        num_blue_time: 128
        white_time: num_blue_time * blue_time
    """
    r = YamlConfig.create(a)
    r.load(b)
    print(r.yaml)

    r.load(b, keep_units=False)
    print(r.yaml)
