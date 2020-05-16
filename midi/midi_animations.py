import time

from . import *

PALETTE = (
    "000000", # black
    "FFFFFF", # white
    "FF0000", # red
    "00FF00", # green
    "0000FF", # blue
    "FFFF00", # yellow
    "00FFFF", # cyan
    "FF00FF", # magenta
    "FF8000", # orange
    "8000FF", # purple
    "0080FF", # light blue
    "FF0080", # pink
)

PORTS = list(range(9001, 9007))

api = Interface("cloud.itsw.es")

@api.onOctave(-2)
def cycle(msg):
    i = msg.note % 12

    api.color((9001, 9004), PALETTE[i])
    api.color((9002, 9003, 9005, 9006), "000")
    api.wait(0.5)

    api.color((9002, 9005), PALETTE[i])
    api.color((9001, 9003, 9004, 9006), "000")
    api.wait(0.5)

    api.color((9003, 9006), PALETTE[i])
    api.color((9001, 9002, 9004, 9005), "000")
    api.wait(0.5)

    api.color((9002, 9005), PALETTE[i])
    api.color((9001, 9003, 9004, 9006), "000")
    api.update()

@api.onOctave(-1)
def expand(msg):
    i = msg.note % 12

    api.add(9002, PALETTE[i])
    api.color((9001, 9003, 9004, 9005, 9006), "000")
    api.wait(0.5)

    api.color((9001, 9003, 9005), PALETTE[i])
    api.color((9002, 9004, 9006), "000")
    api.wait(0.5)

    api.color((9004, 9006), PALETTE[i])
    api.color((9001, 9002, 9003, 9005), "000")
    api.update()

@api.onOctave(0)
def chase(msg):
    i = msg.note % 12
    for port in (9003, 9002, 9001, 9004, 9005, 9006):
        api.color(port, PALETTE[i])
        api.color([p for p in PORTS if p != port], "000")
        api.wait(0.1)
    api.update()

@api.onOctave(1)
def back_and_forth(msg):
    i = msg.note % 12
    for j in range(8):
        if j % 2 == 0:
            api.color((9001, 9002, 9003), PALETTE[i])
            api.color((9004, 9005, 9006), "000")
        else:
            api.color((9004, 9005, 9006), PALETTE[i])
            api.color((9001, 9002, 9003), "000")
        api.wait(0.2)
    api.update()


@api.onNote(127)
def clear(msg):
    api.color(PORTS, "000")
    api.update()

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

api.run()
