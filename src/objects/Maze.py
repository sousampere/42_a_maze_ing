#!/usr/bin/python3


from src.parsing import Config


class Maze():
    def __init__(self, config: Config):
        print(config.width)