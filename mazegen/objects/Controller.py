from mazegen.parsing import Config
from pynput import keyboard  # type: ignore[import-untyped]
from itertools import cycle
from typing import Any


class Controller:
    def __init__(self, config: Config) -> None:
        """Initiliazes the controller's values

        Args:
            config (Config): the current verified and parsed config

        Returns: None
        """
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.speed = 0.1
        self.colors = [
            "\033[0;31m",
            "\033[1;32m",
            "\033[1;33m",
            "\033[1;35m",
            "\033[0;34m",
            "\033[0;36m",
        ]
        self.enable_path = config.show_path
        self.color_cycle = cycle(self.colors)
        self.color = self.colors[5]
        self.stop = False
        self.pause = False
        return None

    def _on_press(self, key: Any) -> None:
        """Key controller, executes an action
        each time a certain keyboard key is pressed

        Keys accepted are '+', '-', 'c', 'r', 'p' and 's'

        Args:
            key (Any): the key pressed, sent by the listener

        Returns: None
        """
        try:
            if key.char == "+":
                self.speed = max(0.03, self.speed - 0.01)
            elif key.char == "-":
                self.speed = min(0.8, self.speed + 0.01)
            elif key.char == "c":
                self.color = next(self.color_cycle)
            elif key.char == "r":
                self.stop = True
            elif key.char == "p":
                self.pause = True
            elif key.char == "s":
                if self.enable_path is False:
                    self.enable_path = True
                else:
                    self.enable_path = False
        except AttributeError:
            pass
        return None

    def start_listener(self) -> None:
        """Starts the listener that will listen to stdin

        Returns: None
        """
        self.listener.start()
        return None

    def stop_listener(self) -> None:
        """Stops the listener

        Returns: None
        """
        self.listener.stop()
        return None
