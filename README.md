yamleins - Yaml-based Configuration Validation
==============================================

A dataclass that handles reading YAML files into
a configuration object. It also handles writing the configuration
object back to a YAML file.

Addtionally, it handles
* YAML templates to define default values, range, type, docstrong
* Simple calculations
* Physical units

Exmaple for a template file:


    blue_time:
        type: float
        default: 20us
        unit: s
        doc: Duration of the blue time
        range: [1 ns, 1s]

    num_blue_time:
        type: int
        default: 128
        unit: None
        doc: Number of blue times
        range: [1, 1000]

    white_time:
        type: float
        default: 1ms
        unit: s
        doc: Duration of a single white time frame
        range: [1 ns, 1s]


Example of a configuration file:

    blue_time: 20us
    num_blue_time: 128
    white_time: num_blue_time * blue_time

Create a configuration object:

    config = YamlConfig.create('template.yaml')

Then  load a configuration file:

    config.load('config.yaml')

The configuration object can be used like a dictionary:

        print(config['blue_time'])

or

        print(config.blue_time)

