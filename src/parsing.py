#!/usr/bin/python3


import string

from pydantic import BaseModel, Field, model_validator
import random
from typing import Any


class ParsingError(Exception):
    """ Parsing Error """
    pass


class ConfigError(Exception):
    """ Configuration Error """
    pass


class Config(BaseModel):
    """ Config object, containing the configuration data """
    width: int = Field(ge=2)
    height: int = Field(ge=2)
    entry_coords: dict[str, int]
    exit_coords: dict[str, int]
    output_file: str
    perfect: bool
    seed: str
    display_ft_pattern: bool

    @model_validator(mode='after')
    def validation(self) -> "Config":
        # Verify that there is no space in the output_file name
        if ' ' in self.output_file:
            raise ConfigError(f'Invalid file name: {self.output_file}')

        # Verify that the Entry/Exit is inside the Maze
        if self.entry_coords['x'] < 0 or self.entry_coords['y'] < 0:
            raise ConfigError(f'Invalid entry coords: {self.entry_coords}. '
                              f'Please use at least a 2x2 Maze.')
        if self.exit_coords['x'] < 0 or self.exit_coords['y'] < 0:
            raise ConfigError(f'Invalid exit coords: {self.exit_coords}. '
                              f'Please use at least a 2x2 Maze.')
        if self.exit_coords['x'] >= self.width or self.exit_coords['y'] >= \
                self.height:
            raise ConfigError(f'Invalid exit coords: {self.exit_coords}. '
                              f'Outside the maze\'s range.')
        if self.entry_coords['x'] >= self.width or self.entry_coords['y'] >= \
                self.height:
            raise ConfigError(f'Invalid exit coords: {self.exit_coords}. '
                              f'Outside the maze\'s range.')
        if self.entry_coords['x'] == self.exit_coords['x']\
           and self.entry_coords['y'] == self.exit_coords['y']:
            raise ConfigError('Invalid entry and exit coords: '
                              'cannot be the same')

        # Initialize seed
        random.seed(self.seed)
        return self


def add_config(config: dict[str, Any], key: str, value: str, type: object,
               line: int) -> dict[str, Any]:
    """ Adding configuration line to the config dictionnary """
    # Integer
    if type is int:
        try:
            config[key] = int(value)
        except Exception:
            raise ParsingError(f'Could not parse config at line {line}: '
                               f'invalid int "{value}".')

    # String
    if type is str:
        config[key] = value.strip()

    # Tuple (coordinates)
    if type is tuple:
        try:
            coords = []
            for coord in value.split(','):
                coords.append(int(coord))
            config[key] = tuple(coords)
        except Exception:
            raise ParsingError(f'Could not parse config at line {line}: '
                               f'invalid coordinates "{value}".')

    # Boolean
    if type is bool:
        if (value.lower().strip() == 'true'):
            config[key] = True
        elif (value.lower().strip() == 'false'):
            config[key] = False
        else:
            raise ParsingError(f'Could not parse config at line {line}: '
                               f'invalid boolean "{value}".')

    # Return the new config dictionnary, containing the parsed line
    return config


def get_parsed_config(config_path: str = '../config.txt') -> Config:
    """ Returns parsed the configuration (Config Object) from a given
    config_file path. """
    with open(config_path, 'r') as f:

        # Ignore comments
        raw_config = []
        for line in f:
            raw_config.append(line.split('#')[0])

        # Parsing configuration
        config: dict[str, Any] = {}
        current_line = 0
        for line in raw_config:
            current_line += 1

            # Integer
            if (line.startswith('WIDTH=')
                    or line.startswith('HEIGHT=')):
                config = add_config(config=config,
                                    key=line.split('=')[0],
                                    value=line.split('=')[1],
                                    type=int,
                                    line=current_line)

            # Tuple / Coordinate
            if (line.startswith('ENTRY=')
                    or line.startswith('EXIT=')):
                config = add_config(config=config,
                                    key=line.split('=')[0],
                                    value=line.split('=')[1],
                                    type=tuple,
                                    line=current_line)

            # String
            if (line.startswith('OUTPUT_FILE=')
                    or line.startswith('SEED=')
                    or line.startswith('DEFAULT_COLOR=')):
                config = add_config(config=config,
                                    key=line.split('=')[0],
                                    value=line.split('=')[1],
                                    type=str,
                                    line=current_line)

            # Bool
            if (line.startswith('PERFECT=')
                    or line.startswith('DISPLAY_FT_PATTERN=')):
                config = add_config(config=config,
                                    key=line.split('=')[0],
                                    value=line.split('=')[1],
                                    type=bool,
                                    line=current_line)

    # Verifying if all mandatory configurations are present
    mandatory_configurations = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                                'OUTPUT_FILE', 'ENTRY']
    for parameter in mandatory_configurations:
        if parameter not in config.keys():
            raise ParsingError(f'Missing {parameter} parameter in your'
                               'configuration file')

    # Verify that the configuration Entry and Exit have both x and y coords
    if len(config['ENTRY']) != 2:
        raise ParsingError('Invalid Entry format. '
                           'Please refer to: "ENTRY=x,y"')
    if len(config['EXIT']) != 2:
        raise ParsingError('Invalid Exit format. Please refer to: "EXIT=x,y"')
    config['ENTRY'] = {'x': config['ENTRY'][0], 'y': config['ENTRY'][1]}
    config['EXIT'] = {'x': config['EXIT'][0], 'y': config['EXIT'][1]}

    # Use random seed if the seed is not specified
    if 'SEED' not in config.keys():
        seed = ''.join(random.choices(string.ascii_lowercase +
                                      string.digits, k=5))
        config['SEED'] = seed

    if 'DISPLAY_FT_PATTERN' not in config.keys():
        config['DISPLAY_FT_PATTERN'] = True
    if 'DEFAULT_COLOR' not in config.keys():
        config['DEFAULT_COLOR'] = True

    # Create and return the Config object
    return Config(
        width=config['WIDTH'],
        height=config['HEIGHT'],
        entry_coords=config['ENTRY'],
        exit_coords=config['EXIT'],
        output_file=config['OUTPUT_FILE'],
        perfect=config['PERFECT'],
        seed=config['SEED'],
        display_ft_pattern=config['DISPLAY_FT_PATTERN']
        )


if __name__ == '__main__':
    conf = get_parsed_config('/home/gtourdia/Documents/'
                             '42_a_maze_ing/config.txt')
    print(conf)
    print(random.random())
