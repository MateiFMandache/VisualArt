from random import gauss, randrange
from graphics import *

WIDTH = 800
HEIGHT = 600
NUM_MOUNTAINS = 30
BACKGROUND_RED = 60
BACKGROUND_GREEN = 130
BACKGROUND_BLUE = 205
FOREGROUND_RED = 0
FOREGROUND_GREEN = 130
FOREGROUND_BLUE = 0
CHANGEABILITY = 100
OFFSET = 5
FACTOR_BASE = 0.9
BACKGROUND_COLOUR = color_rgb(BACKGROUND_RED, BACKGROUND_GREEN, BACKGROUND_BLUE)


def get_factor(index):
    return FACTOR_BASE ** index


def start_level(index):
    factor = get_factor(index)
    return randrange(int(factor*HEIGHT/2), int(factor*HEIGHT))


def get_colour(index):
    factor = get_factor(index)
    return color_rgb(
        int(BACKGROUND_RED + factor * (FOREGROUND_RED - BACKGROUND_RED)),
        int(BACKGROUND_GREEN + factor * (FOREGROUND_GREEN - BACKGROUND_GREEN)),
        int(BACKGROUND_BLUE + factor * (FOREGROUND_BLUE - BACKGROUND_BLUE))
    )


def change(index):
    return gauss(0, CHANGEABILITY / (index + OFFSET))


def draw_mountain(view, index, coverage, lines_to_redraw, width, height):
    colour = get_colour(index)
    level = start_level(index)
    point2 = Point(0, level)
    if level < (sight_base := coverage[0]):
        coverage[0] = level
        vertical_fill = Line(Point(0, sight_base-1), point2)
        vertical_fill.setOutline(colour)
        vertical_fill.draw(view)
    for i in range(width):
        point1 = point2
        level += change(index)
        if level < 0:
            level = - level
        if level > height:
            level = 2 * height - level
        point2 = Point(i+1, int(level))
        if int(level) < (sight_base := coverage[i+1]):
            coverage[i+1] = int(level)
            vertical_fill = Line(Point(i+1, sight_base), point2)
            vertical_fill.setOutline(colour)
            vertical_fill.draw(view)
            if (redraw_line := lines_to_redraw[i]) is not None:
                redraw_line.draw(view)
            line = Line(point1, point2)
            line.setOutline("black")
            line.draw(view)
            lines_to_redraw[i] = Line(point1, point2)
            lines_to_redraw[i].setOutline("black")


def main():
    coverage = [HEIGHT + 1] * (WIDTH + 1)
    lines_to_redraw = [None] * WIDTH
    view = GraphWin(width=WIDTH, height=HEIGHT)
    view.setBackground(BACKGROUND_COLOUR)
    for i in range(NUM_MOUNTAINS):
        draw_mountain(view, i, coverage, lines_to_redraw, WIDTH, HEIGHT)
    view.getMouse()


if __name__ == "__main__":
    main()
