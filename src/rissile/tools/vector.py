# -*- coding: utf-8 -*-

__author__="K. Kulikov"
__date__ ="$Jun 06, 2014 10:30:15 AM$"


from rissile.tools import angles
from rissile.tools import assistants


class Vector:
    """
    Описывает векторные операции в пространстве 3D.
    Класс не имеет явного интерфейса для изменения
    компонентов вектора, однако поддерживает арифметические операции с
    присваиванием, функцию нормализацию и др. модифицирующие методы.
    """
    
    def __init__(self, x, y, z):
        """
        :param x, y, z: составляющие вектора.
        :type x, y, z: float.
        """
        self._x = x
        self._y = y
        self._z = z


    @staticmethod
    def X_UNIT():         
        return Vector(1.0, 0.0, 0.0)


    @staticmethod
    def Y_UNIT():
        return Vector(0.0, 1.0, 0.0)

    @staticmethod
    def Z_UNIT():
        return Vector(0.0, 0.0, 1.0)


    @staticmethod
    def ZERO():
        return Vector(0.0, 0.0, 0.0)


    def __str__(self):
        return '({x}, {y}, {z})'.format(x=self._x, y=self._y, z=self._z)


    def __call__(self):
        """
        :return: кортеж, составленный из элементов вектора.

        >>> vector = Vector(1.5, 4.8, -9.2)
        >>> print(vector())
        (1.5, 4.8, -9.2)
        """
        return (self._x, self._y, self._z)  


    def __add__(self, vector):
        """
        :return: сумму двух векторов.

        >>> vector0 = Vector(1.0, 2.0, 3.0)
        >>> vector1 = Vector(2.0, 4.0, -1.0)
        >>> vector2 = vector0 + vector1
        >>> print(vector2)
        (3.0, 6.0, 2.0)
        """
        return Vector(self._x + vector._x, self._y + vector._y, self._z + vector._z)


    def __sub__(self, vector):
       """
       :return: разность двух векторов.

       >>> vector0 = Vector(1.0, 2.0, 3.0)
       >>> vector1 = Vector(2.0, 4.0, -1.0)
       >>> vector2 = vector0 - vector1
       >>> print(vector2)
       (-1.0, -2.0, 4.0)
       """
       return Vector(self._x - vector._x, self._y - vector._y, self._z - vector._z)


    def __mul__(self, vector):
        """
        :return: произведение двух векторов.
        
        >>> vector0 = Vector(1.0, 2.0, 3.0)
        >>> vector1 = Vector(2.0, 4.0, -1.0)
        >>> vector2 = vector0 * vector1
        >>> print(vector2)
        (2.0, 8.0, -3.0)
        """
        return Vector(self._x * vector._x, self._y * vector._y, self._z * vector._z)


    def __div__(self, vector):
        """
        :return: вектор, полученный путём деления двух векторов.
        
        >>> vector0 = Vector(4.0, 2.0, 3.0)
        >>> vector1 = Vector(2.0, 1.0, 1.5)
        >>> vector2 = vector0 / vector1
        >>> print(vector2)
        (2.0, 2.0, 2.0)
        """
        return Vector(self._x / vector._x, self._y / vector._y, self._z / vector._z)


    def __neg__(self):
        """
        :return: вектор с противоположными компонентами.

        >>> vector0 = Vector(-1.0, 3.0, 1.5)
        >>> vector1 = -vector0
        >>> print(vector1)
        (1.0, -3.0, -1.5)
        """
        return Vector(-self._x, -self._y, -self._z)


    def __iadd__(self, vector):
        """
        Сложение с присваиванием.
        
        >>> vector0 = Vector(1.0, 3.0, -1.0)
        >>> vector0 += Vector(1.0, -3.0, 1.0)
        >>> print(vector0)
        (2.0, 0.0, 0.0)
        """
        self._x += vector._x
        self._y += vector._y
        self._z += vector._z
        return self


    def __isub__(self, vector):
        """
        Вычитание с присваиванием.
        
        >>> vector0 = Vector(1.0, 3.0, -1.0)
        >>> vector0 -= Vector(1.0, -3.0, 1.0)
        >>> print(vector0)
        (0.0, 6.0, -2.0)
        """
        self._x -= vector._x
        self._y -= vector._y
        self._z -= vector._z
        return self


    def __imul__(self, vector):
        """
        Умножение с присваиванием.
        
        >>> vector0 = Vector(1.0, 3.0, -1.0)
        >>> vector0 *= Vector(1.0, -3.0, 1.0)
        >>> print(vector0)
        (1.0, -9.0, -1.0)
        """
        self._x *= vector._x
        self._y *= vector._y
        self._z *= vector._z
        return self


    def __idiv__(self, vector):
        """
        Деление с присваиванием.
        
        >>> vector0 = Vector(1.0, 3.0, -1.0)
        >>> vector0 /= Vector(1.0, -3.0, 1.0)
        >>> print(vector0)
        (1.0, -1.0, -1.0)
        """
        self._x /= vector._x
        self._y /= vector._y
        self._z /= vector._z
        return self


    def __eq__(self, vector):
        """
        Сравнение текущего и переданного вектора на равенство.

        >>> vector0 = Vector(0.3333333333, 2.0, 5.6)
        >>> vector1 = Vector(1.0/3.0, 3.0 / 1.5, 6.0 - 0.4)
        >>> vector0 == vector1
        True
        """
        from rissile.tools.assistants import is_equals
        return is_equals(self._x, vector._x) and is_equals(self._y, vector._y) and is_equals(self._z, vector._z)


    def __getitem__(self, i):
        return self()[i]


    def x(self):
        return self._x


    def y(self):
        return self._y


    def z(self):
        return self._z


    def length_squared(self):
        """
        :return: длину вектора в квадрате.

        >>> vector = Vector(2.0, 0.0, 0.0)
        >>> vector.length_squared()
        4.0
        """
        return self._x ** 2 + self._y ** 2 + self._z ** 2


    def length(self):
        """
        :return: длину вектора.

        >>> vector = Vector(2.0, 2.0, 1.0)
        >>> vector.length()
        3.0
        """
        return self.length_squared() ** 0.5


    def distance(self, vector):
        """
        :return: растояние до другого вектора.

        >>> vector0 = Vector(4, 4, 3)
        >>> print(vector0.distance(Vector(2, 2, 2)))
        3.0
        """
        return (self - vector).length()


    def dot_product(self, vector):
        """
        :return: скалярное произведение двух векторов.

        >>> vector0 = Vector(1.0, 1.5, -1.0)
        >>> vector1 = Vector(2.0, 4.0, 3.0)
        >>> print(vector0.dot_product(vector1))
        5.0
        """
        return self._x * vector._x + self._y * vector._y + self._z * vector._z


    def radian_to(self, vector):
        """
        :return: угол между двумя векторами.
        
        >>> vector0 = Vector(1.0, 0.0, 0.0)
        >>> degrees = vector0.radian_to(Vector(0.0, 1.0, 0.0))
        >>> print(degrees.to_degree())
        90.0
        >>> vector1 = Vector(1.0, 1.0, 0.0)
        >>> degrees = vector1.radian_to(vector0)
        >>> print(degrees.to_degree())
        45.0
        """
        import math
        dot_product = self.dot_product(vector) / self.length() / vector.length()
        return angles.Radian(math.acos(dot_product))


    def normalize(self):
        """
        Метод выполняет операцию нормализации - приведение вектора к еденичной длине.

        >>> vector0 = Vector(2.0, 2.0, 2.0)
        >>> vector0.normalize()
        >>> vector0.length()
        1.0
        """
        length = self.length()
        if length > 0.0:
            self._x /= length
            self._y /= length
            self._z /= length


    def normalized(self):
        """
        :return: нормализованный вектор.

        >>> vector0 = Vector(6.0, 0.0, 0.0)
        >>> vector1 = vector0.normalized()
        >>> print(vector1)
        (1.0, 0.0, 0.0)
        """
        import copy
        result = copy.copy(self)
        result.normalize()
        return result


    def cross_product(self, vector):
        """
        Метод вычисляет векторное произведение двух векторов.
        Результирующий вектор является перпендекуляром к этим двум векторам.
        Данную функцию можно использовать, например чтобы расчитать нормаль к плоскости.
        Например, найдём нормаль к плоскости XY:

        >>> vector_x = Vector(1.0, 0.0, 0.0)
        >>> vector_y = Vector(0.0, 1.0, 0.0)
        >>> normal = vector_x.cross_product(vector_y)
        >>> print(normal)
        (0.0, 0.0, 1.0)

        Возвращаемый результат не нормализован. Это сделано по соображением эффективности.
        """
        return Vector(\
            self._y * vector._z - self._z * vector._y,\
            self._z * vector._x - self._x * vector._z,\
            self._x * vector._y - self._y * vector._x,\
            )


    def is_zero_length(self):
        """
        Функция проверяет, что длина вектора условно равна нулю.

        >>> vector0 = Vector(0.0000001, 0.0000001, 0.0000001)
        >>> vector0.is_zero_length()
        True
        """
        return assistants.about_zero(self.length())


    def reflect(self, normal):
        """
        Метод вычисляет "тень" вектора на плоскость, которая определяется нормалью к
        этой плоскости.
        """
        dot_product = 2.0 * self.dot_product(normal)
        return self - Vector(dot_product, dot_product, dot_product) * normal


    def is_equals(self, vector, tolerance=assistants.TOLERANCE_VALUE):
        """
        Метод проверяет на равенство текущий вектор со входным
        учитывая допустимую ошибку.

        >>> vector0 = Vector(3.0 - 2.7, 6.13 - 2.11, 5.6 - 7.12)
        >>> vector1 = Vector(0.3, 4.02, -1.52)
        >>> vector0.is_equals(vector1)
        True
        """
        return assistants.is_equals(self._x, vector._x, tolerance) and\
               assistants.is_equals(self._y, vector._y, tolerance) and\
               assistants.is_equals(self._z, vector._z, tolerance)


    def direction_equals(self, vector, toleranse_in_radian):
        """
        Проверяет сонаправленность текущего вектора с другим в пределах
        допустимого отклонения.

        >>> import math
        >>> vector0 = Vector(5.0, 0.0, 0.0)
        >>> vector1 = Vector(5.0, 0.1, 0.0)
        >>> vector2 = Vector(1.0, 0.5, 0.0)
        >>> tolerance = angles.Radian(math.pi / 90)
        >>> vector0.direction_equals(vector1, tolerance)
        True
        >>> vector0.direction_equals(vector2, tolerance)
        False
        """
        return assistants.is_equals(self.radian_to(vector)(), 0.0, toleranse_in_radian())


    def clone(self):
        return Vector(self._x, self._y, self._z)
    
