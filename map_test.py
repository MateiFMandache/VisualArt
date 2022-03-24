from map import *


def test():
    test_poly = Poly([
        [0, -3, 0, 1],
        [],
        [-1]
    ])
    print(test_poly.apply(10, 2))
    print(test_poly.x_derivative())
    print(test_poly.y_derivative())
    print(test_poly.apply(*test_poly.newton_raphson(1.12, 3.97, 1, 0.001)))
    screen = Screen(ORIGIN_X, ORIGIN_Y, STEP, width=WIDTH, height=HEIGHT)
    test_poly.plot_contour(screen, -0.3, -2.1, 0.1, 0.001, 4, 3)
    test_poly.plot_contour(screen, -0.3, -1.1, 0.1, 0.001, 4, 3)
    test_poly.plot_contour(screen, -0.3, -0.1, 0.1, 0.001, 4, 3)
    test_poly.plot_contour(screen, -0.3, -2.6, 0.1, 0.001, 4, 3)
    test_poly.plot_contour(screen, 2.3, -0.6, 0.1, 0.001, 4, 3)
    screen.getMouse()


if __name__ == "__main__":
    test()
