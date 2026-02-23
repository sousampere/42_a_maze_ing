#!/usr/bin/python3


class ParsingError(Exception):
    pass


def add_config(config: dict[str: any], key: str, value: str, type: object, line: int) -> dict[str: any]:
    """ Adding configuration line to the config dictionnary """
    # Integer
    if type is int:
        try:
            config[key] = int(value)
        except Exception:
            raise ParsingError(f'Could not parse config at line {line}: invalid int "{value}".')

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
            raise ParsingError(f'Could not parse config at line {line}: invalid coordinates "{value}".')
        
    # Boolean
    if type is bool:
        if (value.lower().strip() == 'true'):
            config[key] = True
        elif (value.lower().strip() == 'false'):
            config[key] = False
        else:
            raise ParsingError(f'Could not parse config at line {line}: invalid boolean "{value}".')
    return config

def get_parsed_config(config_path: str = '../config.txt') -> dict[str: str|int]:
    with open(config_path, 'r') as f:

        # Ignore comments
        raw_config = []
        for line in f:
            raw_config.append(line.split('#')[0])

        # Parsing configuration
        config = {}
        current_line = 0
        for line in raw_config:
            current_line += 1
            if (line.startswith('WIDTH=')
                or line.startswith('HEIGHT=')):
                config = add_config(config=config,
                           key=line.split('=')[0],
                           value=line.split('=')[1],
                           type=int,
                           line=current_line)
            if (line.startswith('ENTRY=')
                or line.startswith('EXIT=')):
                config = add_config(config=config,
                           key=line.split('=')[0],
                           value=line.split('=')[1],
                           type=tuple,
                           line=current_line)
            if (line.startswith('OUTPUT_FILE=')
                or line.startswith('SEED=')):
                config = add_config(config=config,
                           key=line.split('=')[0],
                           value=line.split('=')[1],
                           type=str,
                           line=current_line)
            if (line.startswith('PERFECT=')):
                config = add_config(config=config,
                           key=line.split('=')[0],
                           value=line.split('=')[1],
                           type=bool,
                           line=current_line)

    # Verifying if all mandatory configurations are present
    print(config)
    mandatory_configurations = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'ENTRY']
    for parameter in mandatory_configurations:
        if parameter not in config.keys():
            raise ParsingError(f'Missing {parameter} parameter in your configuration file')

    return config

if __name__ == '__main__':
    conf = get_parsed_config('/home/gtourdia/Documents/42_a_maze_ing/config.txt')