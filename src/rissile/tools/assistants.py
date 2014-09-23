# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$Jun 06, 2014 10:30:15 AM$"


TOLERANCE_VALUE = 1e-3
EPSILON = 1e-6


def about_zero(value, tolerance=TOLERANCE_VALUE):
    """
    :return: истину, если переданное значение лежит в окрестности нуля.

    >>> first_angle = 3.0 - 2.7
    >>> second_angle = 0.3
    >>> print(first_angle)
    0.3
    >>> print(second_angle)
    0.3
    >>> first_angle == second_angle
    False
    >>> about_zero(first_angle - second_angle)
    True
    """
    import math
    return math.fabs(value) <= tolerance


def is_equals(first, second, tolerance=TOLERANCE_VALUE):
    """
    :return: истину, если два числа равны с заданной точностью.

    >>> is_equals(3.0 - 2.7, 0.3, 0.00001)
    True
    """
    return about_zero(first - second, tolerance)
