#!/usr/bin/python3

import argparse
from typing import Any


def get_args() -> dict[str, Any]:
    """ Get arguments using argparse:
     One single arg corresponding to the config path """
    parser = argparse.ArgumentParser(
        prog='a-maze-ing',
        description='A-maze-ing program made by lbonnet & gtourdia.',
        epilog='Made with terror by DISØRDER++'
    )
    parser.add_argument(
        'config_path',
        nargs='?',
        help='Configuration file path.',
        default='./config.txt'
    )
    args = parser.parse_args()

    return {'config': args.config_path}
