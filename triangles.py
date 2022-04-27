from random import gauss, random, randint
from graphics import *

NUM_TRIANGLES = 1000
TRIANGLE_VERTICES = 3
TRIANGLE_SIZE = 80
WIDTH = 800
HEIGHT = 600
COLOUR_CONSTANT = 256
COLOUR_MAX = 255


def rand_rainbow():
    index = random()
    index *= 6
    if index < 1:
        return color_rgb(int(COLOUR_CONSTANT * index), 0, COLOUR_MAX - int(COLOUR_CONSTANT * index))
    elif index < 2:
        index %= 1
        return color_rgb(COLOUR_MAX, int(COLOUR_CONSTANT * index), 0)
    elif index < 3:
        index %= 1
        return color_rgb(COLOUR_MAX - int(COLOUR_CONSTANT * index), COLOUR_MAX, 0)
    elif index < 4:
        index %= 1
        return color_rgb(0, COLOUR_MAX, int(COLOUR_CONSTANT * index))
    elif index < 5:
        index %= 1
        return color_rgb(0, COLOUR_MAX - int(COLOUR_CONSTANT * index), COLOUR_MAX)
    else:
        index %= 1
        return color_rgb(int(COLOUR_CONSTANT * index), 0, COLOUR_MAX)


def draw_triangle(surface):
    startx = randint(0, WIDTH)
    starty = randint(0, HEIGHT)
    vertices = []
    for _ in range(TRIANGLE_VERTICES):
        vertices.append(Point(gauss(startx, TRIANGLE_SIZE), gauss(starty, TRIANGLE_SIZE)))
    triangle = Polygon(vertices)
    triangle.setFill(rand_rainbow())
    triangle.draw(surface)


def main():
    win = GraphWin(height=HEIGHT, width=WIDTH)
    for _ in range(NUM_TRIANGLES):
        draw_triangle(win)
    win.getMouse()


if __name__ == "__main__":
    main()