from graphics import *
from math import sin, cos, pi, sqrt

WIDTH = 800
HEIGHT = 600
SEEDS = 1000
RADIUS = 3
AREA = 45
ANGLE = pi * (1 + sqrt(5))


class Screen(GraphWin):
    def draw_circle(self, x, y, radius):
        point = Point(self.width//2 + x, self.height//2 - y)
        circle = Circle(point, radius)
        circle.setOutline("black")
        circle.draw(self)


def main():
    screen = Screen(width=WIDTH, height=HEIGHT)
    for i in range(SEEDS):
        r = sqrt(AREA * i)
        theta = ANGLE * i
        screen.draw_circle(r * cos(theta), r*sin(theta), RADIUS)
    screen.getMouse()


if __name__ == "__main__":
    main()
