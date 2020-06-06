import curses
import atexit
import string


class KeypadInput:
    """Input device that reads keystrokes from the keyboard in a terminal
    window. Works on posix (Linux/MacOS) platforms only."""

    def __init__(self):
        """Creates a KeypadInput that receives keystrokes from the current
        window."""

        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        atexit.register(self.close)
        self.scr.addstr(1, 1, "Vibrance: Keypad Input")
        self.scr.refresh()

    def close(self):
        """Resets the terminal state."""
        self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __iter__(self):
        return self

    def __next__(self):
        key = self.scr.getkey()
        events = []

        if key in string.ascii_letters:
            key_type = "letter"
        elif key in string.digits:
            key_type = "number"
        elif key in string.punctuation:
            key_type = "symbol"
        else:
            key_type = "special"

        events.append({"input": "keypad",
                       "type": "keydown",
                       "key": key})

        events.append({"input": "keypad",
                       "type": key_type,
                       "key": key})

        events.append({"input": "keypad",
                       "type": f"key_{key}",
                       "key": key})

        return tuple(events)
