import serial
import atexit

from . import base_input

class SerialInput(base_input.BaseInput):
    """Input device that reads bytes from a serial port."""

    def __init__(self, name="", port):
        """Creates a SerialInput that reads from the given port."""
        super().__init__(name)
        self.enabled = False

    def open(self):
        self.port = serial.Serial(port)
        atexit.register(self.close)
        self.enabled = True

    def close(self):
        self.enabled = False
        self.port.close()

    def read(self):
        if not self.enabled:
            return tuple()
        events = []
        while self.port.in_waiting > 0:
            byte = self.port.read().decode("utf-8")

            events.append({"input": "uart",
                           "type": "byte",
                           "byte": byte})

            events.append({"input": "uart",
                           "type": byte,
                           "byte": byte})

        return tuple(events)
