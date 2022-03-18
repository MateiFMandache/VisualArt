from graphics import *
from random import gauss, choices
from math import *

WIDTH = 800
HEIGHT = 600
STARTX = 400
STARTY = 300
STARTDIR = pi/2
SPEED = 3
STEERING = 0.3
TIME = 10000
STARTR = 0.5
STARTG = 0.5
STARTB = 0.5
COLOUR_CONSTANT = 256
COLOUR_CHANGING = 0.1
COLOUR_MIDDLE_BIAS = 0.001


def update_colour(initial, changing, middle_bias):
    initial = (initial + 0.5 * middle_bias) / (1 + middle_bias)
    increment = changing * initial * (1-initial)
    return choices([initial/(1 + increment),
                    (initial + increment)/(1 + increment)],
                   [1 - initial, initial])[0]


class Car:
    def __init__(self, surface, startx, starty, start_dir,
                 speed, steering, wrapx, wrapy, startr, startg, startb,
                 colour_changing, colour_middle_bias):
        """
        Sets up a car to start drawing
        :param surface: Surface to draw on
        :param startx: starting x position
        :param starty: starting y position
        :param start_dir: starting direction (angle)
        :param speed: how fast the car goes
        :param steering: amount of wobble in direction
        :param wrapx: x coordinate to wrap around at
        :param wrapy: y coordinate to wrap around at
        :param startr: start red component
        :param startg: start green component
        :param startb: start blue component
        :param colour_changing: how much the colour changes step by
        step
        :param colour_middle_bias: tendency of the colour to gravitate
        towards the middle
        """
        self.surface = surface
        self.x = startx
        self.y = starty
        self.dir = start_dir
        self.speed = speed
        self.steering = steering
        self.wrapx = wrapx
        self.wrapy = wrapy
        self.r = startr
        self.g = startg
        self.b = startb
        self.colour_changing = colour_changing
        self.colour_middle_bias = colour_middle_bias

    def drive(self):
        current = Point(int(self.x), int(self.y))
        self.x += self.speed * sin(self.dir)
        self.y -= self.speed * cos(self.dir)
        new = Point(int(self.x), int(self.y))
        trace = Line(current, new)
        trace.setOutline(color_rgb(int(COLOUR_CONSTANT * self.r),
                                   int(COLOUR_CONSTANT * self.g),
                                   int(COLOUR_CONSTANT * self.b)))
        trace.draw(win)
        self.r = update_colour(self.r, self.colour_changing, self.colour_middle_bias)
        self.g = update_colour(self.g, self.colour_changing, self.colour_middle_bias)
        self.b = update_colour(self.b, self.colour_changing, self.colour_middle_bias)
        self.dir += gauss(0, self.steering)
        self.x %= self.wrapx
        self.y %= self.wrapy


if __name__ == "__main__":

    win = GraphWin(width=WIDTH, height=HEIGHT)
    win.setBackground("black")
    car = Car(win, STARTX, STARTY, STARTDIR, SPEED, STEERING, WIDTH, HEIGHT,
              STARTR, STARTG, STARTB, COLOUR_CHANGING, COLOUR_MIDDLE_BIAS)
    for _ in range(TIME):
        car.drive()
    win.getMouse()
    win.close()
