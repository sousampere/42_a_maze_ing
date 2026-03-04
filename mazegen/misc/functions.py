
from .constants import Colors
import sys
from typing import Any


def printerr(*args: Any) -> None:
    """Prints a red message"""
    sys.stderr.write(f"{Colors.RED}")
    sys.stderr.write(str(*args))
    sys.stderr.write(f'{Colors.END}\n')


def debug(*args: Any) -> None:
    """Prints a blue message"""
    sys.stderr.write(f"{Colors.BLUE}")
    sys.stderr.write(str(*args))
    sys.stderr.write(f'{Colors.END}\n')
