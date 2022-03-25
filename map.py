from graphics import *
from math import sqrt
from enum import Enum
from random import uniform, gauss


BACKGROUND_COLOUR = "black"
ORIGIN_X = 400
ORIGIN_Y = 300
STEP = 70
WIDTH = 800
HEIGHT = 600
DETECTION_FACTOR = 0.5
X_MAX = (WIDTH - ORIGIN_X) / STEP
X_MIN = - ORIGIN_X / STEP
Y_MAX = ORIGIN_Y / STEP
Y_MIN = (ORIGIN_Y - HEIGHT) / STEP
X_LIMIT = max([X_MAX, -X_MIN])
Y_LIMIT = max([Y_MAX, -Y_MIN])
PRECISION = 0.000_01
JUMP = 0.1
NUM_CONTOURS = 50
DEGREE = 6
COLOUR_CONSTANT = 256
COLOUR_MAX = 255


class JumpType(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Screen(GraphWin):
    def __init__(self, origin_x, origin_y, step, **kwargs):
        super().__init__(**kwargs)
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.step = step

    def draw_line(self, start_x, start_y, end_x, end_y, colour):
        start = Point(int(self.step * start_x) + self.origin_x,
                      -int(self.step * start_y) + self.origin_y)
        end = Point(int(self.step * end_x) + self.origin_x,
                    -int(self.step * end_y) + self.origin_y)
        line = Line(start, end)
        line.setOutline(colour)
        line.draw(self)


class Polynomial:
    def __init__(self, coefficients):
        """ Create a Polynomial object
        :param coefficients: a 2d array (list of lists) such that the
        [i][j] entry is the coefficient of x**j * y**i
        """
        self.coefficients = coefficients

    def apply(self, x, y):
        total = 0
        multiplier = 1
        for row in self.coefficients:
            full_multiplier = multiplier
            for entry in row:
                total += entry * full_multiplier
                full_multiplier *= x
            multiplier *= y
        return total

    def x_derivative(self):
        return Polynomial([[entry * (i + 1) for i, entry in enumerate(row[1:])]
                           for row in self.coefficients])

    def y_derivative(self):
        return Polynomial([[entry * (i + 1) for entry in row]
                           for i, row in enumerate(self.coefficients[1:])])

    def __str__(self):
        return str(self.coefficients)

    @classmethod
    def random(cls, degree):
        coefficients = []
        multiplier = 1
        for i in range(degree + 1):
            row = []
            full_multiplier = multiplier
            for j in range(degree + 1 - i):
                row.append(gauss(0, full_multiplier))
                full_multiplier /= (j+1)
            coefficients.append(row)
            multiplier /= (i+1)
        return cls(coefficients)


class Poly(Polynomial):
    def __init__(self, coefficients):
        super().__init__(coefficients)
        self.ddx = self.x_derivative()
        self.ddy = self.y_derivative()

    def newton_raphson(self, start_x, start_y, target_value, precision):
        while True:
            value = self.apply(start_x, start_y)
            ddx = self.ddx.apply(start_x, start_y)
            ddy = self.ddy.apply(start_x, start_y)
            square_norm = ddx * ddx + ddy * ddy
            new_x = (target_value - value) * ddx / square_norm + start_x
            new_y = (target_value - value) * ddy / square_norm + start_y
            if (new_x - start_x) ** 2 + (new_y - start_y) ** 2 < precision ** 2:
                break
            start_x = new_x
            start_y = new_y
        return new_x, new_y

    def jump(self, surface, start_x, start_y, jump_distance,
             jump_type, precision, colour):
        value = self.apply(start_x, start_y)
        ddx = self.ddx.apply(start_x, start_y)
        ddy = self.ddy.apply(start_x, start_y)
        norm = sqrt(ddx * ddx + ddy * ddy)
        multiplier = jump_distance / norm
        if jump_type == JumpType.LEFT:
            new_x, new_y = self.newton_raphson(start_x - ddy * multiplier,
                                               start_y + ddx * multiplier,
                                               value, precision)
        else:
            new_x, new_y = self.newton_raphson(start_x + ddy * multiplier,
                                               start_y - ddx * multiplier,
                                               value, precision)
        surface.draw_line(start_x, start_y, new_x, new_y, colour)
        return new_x, new_y

    def plot_contour(self, surface, x, y, jump_distance, precision,
                     x_limit, y_limit, colour):
        x_left, y_left = x, y
        x_right, y_right = x, y
        first_time = True
        left_in_bounds = True
        right_in_bounds = True
        while True:
            if left_in_bounds:
                x_left, y_left = self.jump(surface, x_left, y_left, jump_distance,
                                           JumpType.LEFT, precision, colour)
                if abs(x_left) > x_limit or abs(y_left) > y_limit:
                    if not right_in_bounds:
                        break
                    left_in_bounds = False
                if not first_time:
                    if ((x_left - x_right) ** 2 + (y_left - y_right) ** 2 <
                            jump_distance ** 2 * DETECTION_FACTOR):
                        surface.draw_line(x_left, y_left, x_right, y_right, colour)
                        break
            if right_in_bounds:
                x_right, y_right = self.jump(surface, x_right, y_right, jump_distance,
                                             JumpType.RIGHT, precision, colour)
                if abs(x_right) > x_limit or abs(y_right) > y_limit:
                    if not left_in_bounds:
                        break
                    right_in_bounds = False
                if not first_time:
                    if ((x_left - x_right) ** 2 + (y_left - y_right) ** 2 <
                            jump_distance ** 2 * DETECTION_FACTOR):
                        surface.draw_line(x_left, y_left, x_right, y_right, colour)
                        break
            first_time = False


def rainbow(index):
    index *= 6
    if index < 1:
        return color_rgb(int(COLOUR_CONSTANT*index), 0, 0)
    elif index < 2:
        index %= 1
        return color_rgb(COLOUR_MAX, int(COLOUR_CONSTANT*index), 0)
    elif index < 3:
        index %= 1
        return color_rgb(COLOUR_MAX-int(COLOUR_CONSTANT*index), COLOUR_MAX, 0)
    elif index < 4:
        index %= 1
        return color_rgb(0, COLOUR_MAX, int(COLOUR_CONSTANT*index))
    elif index < 5:
        index %= 1
        return color_rgb(0, COLOUR_MAX-int(COLOUR_CONSTANT*index), COLOUR_MAX)
    else:
        index %= 1
        return color_rgb(int(COLOUR_CONSTANT*index), 0, COLOUR_MAX)


def main():
    screen = Screen(ORIGIN_X, ORIGIN_Y, STEP, width=WIDTH, height=HEIGHT)
    screen.setBackground("black")
    points = []
    for _ in range(NUM_CONTOURS):
        points.append((uniform(X_MIN, X_MAX), uniform(Y_MIN, Y_MAX)))
    poly = Poly.random(DEGREE)
    values = []
    for i, point in enumerate(points):
        values.append((poly.apply(point[0], point[1]), i))
    values.sort()
    colour_indices = [None] * NUM_CONTOURS
    for i, value in enumerate(values):
        colour_indices[value[1]] = i / NUM_CONTOURS
    for point, colour_index in zip(points, colour_indices):
        poly.plot_contour(screen, point[0], point[1], JUMP, PRECISION,
                          X_LIMIT, Y_LIMIT, rainbow(colour_index))
    screen.getMouse()


if __name__ == "__main__":
    main()
