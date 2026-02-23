#!/usr/bin/python3

# Avoir les 4 directions

class CellException(Exception):
    pass


class CellDirectionException(CellException):
    pass


class Cell():
    """ Cell object that compose a Maze """
    def __init__(self,
                 north: int = 0,
                 east: int = 0,
                 south: int = 0,
                 west: int = 0) -> None:

        # Setting direction values
        if self.validate_direction(north):
            self._north = north
        if self.validate_direction(east):
            self._east = east
        if self.validate_direction(south):
            self._south = south
        if self.validate_direction(west):
            self._west = west
        return None

    @staticmethod
    def validate_direction(direction: int) -> bool:
        """ Validate the value for a cell's direction (0 or 1) """
        if (direction == 0 or direction == 1):
            return True
        raise CellDirectionException(f'Invalid direction {direction}. '
                                     'Must be 1 or 0.')

    def get_direction(self, direction: str) -> int:
        """ Return the value of the given direction for the cell """
        available_directions = {
            'north': self._north,
            'east': self._east,
            'south': self._south,
            'west': self.west
            }
        if (direction not in available_directions.keys()):
            raise CellDirectionException(f'Invalid direction. '
                                         'Must be a direction in '
                                         f'{available_directions.keys()}')
        return available_directions[direction]

    def directions(self) -> dict[str: int]:
        """ Returns all the directions values of a cell """
        return {
            'north': self._north,
            'east': self._east,
            'south': self._south,
            'west': self.west
            }

    def set_direction(self, direction: str, value: int) -> None:
        """ Set the value for the given direction for the cell """
        available_directions = {
            'north': self._north,
            'east': self._east,
            'south': self._south,
            'west': self.west
            }
        if (direction not in available_directions.keys()):
            raise CellDirectionException(f'Invalid direction. '
                                         'Must be a direction in '
                                         f'{available_directions.keys()}')
        if (self.validate_direction(value)):
            if (direction == 'north'):
                self._north = value
            if (direction == 'east'):
                self._east = value
            if (direction == 'south'):
                self._south = value
            if (direction == 'west'):
                self._west = value

        return available_directions[direction]
