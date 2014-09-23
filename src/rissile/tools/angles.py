# -*- coding: utf-8 -*-
"""
Чтобы очистить код, работающий с
угловыми сущностями, от
магической константы вида 57.3,
в проекте Rissile используются классы
Radian и Degree.
"""


__author__="K. Kulikov"
__date__ ="$Jun 06, 2014 10:30:15 AM$"


import math


class PhysicalValue:
    """
    Модуль описывает физическую величину.
    Пример использования приведён на базе классов Radian и Degree.
    """


    def __init__(self, value):
        self._value = float(value)


    def __call__(self):
        return self._value


    def __str__(self):
        return '{value}'.format(value=self._value)


    def __add__(self, angle):
        """
        :return: cумму self и angle
        :rtype: 

        >>> radian = Radian(math.pi / 2)
        >>> radian = radian + Radian(math.pi / 2)
        >>> print(radian)
        3.14159265359
        >>> degree = Degree(90.0)
        >>> degree = degree + Radian(math.pi / 2).to_degree()
        >>> print(degree)
        180.0
        """
        return self.__class__(self._value + angle._value)


    def __sub__(self, angle):
        """
        Разность двух углов.

        >>> angle0 = Degree(180.0)
        >>> angle1 = Degree(180.0)
        >>> angle2 = angle0 + angle1
        >>> print(angle2)
        360.0
        """
        return self.__class__(self._value - angle._value)


    def __mul__(self, k):
        """
        Правостороннее умножение.
        
        :return: угол, равный self умноженному на k.
        :rtype: Degree | Radian

        >>> angle0 = Degree(60.0)
        >>> angle1 = angle0 * 2.5
        >>> print(angle1)
        150.0
        """
        return self.__class__(self._value * k)


    def __rmul__(self, k):
        """
        Левостороннее умножение.

        >>> angle0 = Degree(60.0)
        >>> angle1 = 2.5 * angle0
        >>> print(angle1)
        150.0
        """
        return self * k


    def __div__(self, k):
        """
        :return: частное self и k.
        :rtype: Degree | Radian

        >>> angle0 = Radian(math.pi)
        >>> angle1 = angle0 / 4
        >>> print(angle1)
        0.785398163397
        """
        return self.__class__(self._value / k)


    def __neg__(self):
        """
        :return: угол, противоположный self.
        :rtype: Degree | Radian

        >>> angle0 = Degree(45.0)
        >>> angle1 = - angle0
        >>> print(angle1)
        -45.0
        """
        return self.__class__(-self._value)


    def __iadd__(self, angle):
        """
        Сложение с присваиванием.

        >>> angle0 = Radian(math.pi / 2)
        >>> angle0 += angle0
        >>> print(angle0)
        3.14159265359
        """
        self._value += angle._value
        return self


    def __isub__(self, angle):
        """
        Вычитание с присваиванием.

        >>> import math
        >>> angle0 = Radian(math.pi)
        >>> angle0 -= Radian(math.pi)
        >>> print(angle0)
        0.0
        """
        self._value -= angle._value
        return self


    def __imul__(self, k):
        """
        Заменить значение текущего вектора
        его произведением с коэффициентом.

        >>> angle0 = Degree(30.0)
        >>> angle0 *= 3.0
        >>> print(angle0)
        90.0
        """
        self._value *= k
        return self


    def __idiv__(self, k):
        """
        Заменить значение текущего вектора
        его частным с к.

        >>> angle0 = Degree(90.0)
        >>> angle0 /= 2.0
        >>> print(angle0)
        45.0
        """
        self._value /= k
        return self


class Radian(PhysicalValue):
    """
    Возвращает текущее значение в
    размерности радиан.

    >>> radian = Radian(math.pi)
    >>> radian.degrees()
    180.0
    >>> radian.cos()
    -1.0
    """
    def __init__(self, value):
        PhysicalValue.__init__(self, value)


    def degrees(self):
        """
        >>> radian = Radian(math.pi / 4)
        >>> radian.degrees()
        45.0
        """
        return 180.0 / math.pi * self._value


    def to_degree(self):
        """
        >>> radian = Radian(math.pi / 2)
        >>> radian.to_degree()()
        90.0
        """
        return Degree(self.degrees())


    @staticmethod
    def from_degrees(value):
        """
        >>> radian = Radian.from_degrees(180)
        >>> radian()
        3.141592653589793
        """
        return Degree(value).to_radian()


    def sin(self):
        return math.sin(self._value)


    def cos(self):
        return math.cos(self._value)


    def tan(self):
        return math.tan(self._value) 


class Degree(PhysicalValue):
    """
    Возвращает текущее значение в
    размерности градус.

    >>> degrees = Degree(180.0)
    >>> degrees.radians()
    3.141592653589793
    >>> degrees.cos()
    -1.0
    >>> degrees.tan()
    -1.2246467991473532e-16
    """


    def __init__(self, value):
        PhysicalValue.__init__(self, value)


    def radians(self):
        """
        >>> degree = Degree(90)
        >>> degree.radians()
        1.5707963267948966
        """
        return self._value / 180 * math.pi


    def to_radian(self):
        """
        >>> degree = Degree(45)
        >>> degree.to_radian()()
        0.7853981633974483
        """
        return Radian(self.radians())


    @staticmethod
    def from_radians(value):
        """
        >>> degree = Degree.from_radians(math.pi / 4)
        >>> degree()
        45.0
        """
        return Radian(value).to_degree()


    def sin(self):
        return self.to_radian().sin()


    def cos(self):
        return self.to_radian().cos()


    def tan(self):
        return self.to_radian().tan()
