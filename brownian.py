from graphics import *
from random import choice
from enum import Enum
from sys import argv


WIDTH = 700
HEIGHT = 700
START_X = WIDTH // 2
START_Y = HEIGHT // 2
DEFAULT_STEPS = 100_000
DEFAULT_COLOUR = "black"
DEFAULT_BACKGROUND = "gray"


class Direction(Enum):
    RIGHT = "RIGHT"
    UP = "UP"
    LEFT = "LEFT"
    DOWN = "DOWN"


def main():
    win = GraphWin(width=WIDTH, height=HEIGHT)

    x = START_X
    y = START_Y
    colour = DEFAULT_COLOUR
    bg_colour = DEFAULT_BACKGROUND
    steps = DEFAULT_STEPS

    if len(argv) > 1:
        colour = argv[1]
    if len(argv) > 2:
        bg_colour = argv[2]
    if len(argv) > 3:
        steps = int(argv[3])
    win.setBackground(bg_colour)

    directions = [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN]
    for _ in range(steps):
        win.plot(x, y, colour)
        direction = choice(directions)
        if direction == Direction.RIGHT:
            x = x + 1
        if direction == Direction.UP:
            y = y - 1
        if direction == Direction.LEFT:
            x = x - 1
        if direction == Direction.DOWN:
            y = y + 1

    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()
