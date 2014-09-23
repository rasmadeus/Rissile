# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$Jun 06, 2014 10:30:15 AM$"

"""
Модуль quaternion
=================
"""


from rissile.tools.angles import Radian, Degree
from rissile.tools.vector import Vector
from rissile.tools import assistants
import math


class Quaternion:
    """
    Реализация кватерниона выполнена по материалам:
    http://www.ogre3d.org 
    http://www.cprogramming.com/tutorial/3d/quaternions.html
    http://www.gamedev.net/page/resources/_/reference/programming/math-and-physics/
    http://www.j3d.org/
    """


    @staticmethod
    def ZERO():
        return Quaternion(0.0, 0.0, 0.0, 0.0)


    @staticmethod
    def IDENTITY():
        return Quaternion(1.0, 0.0, 0.0, 0.0)


    @staticmethod
    def from_axis_and_angle(axis, angle):
        """
        Функция конструирует нормализованный кватерниона из оси и угла.

        >>> q0 = Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Radian(math.pi / 2))
        >>> print(q0)
        (0.707106781187, 0.707106781187, 0.0, 0.0)
        >>> q1 = Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Degree(90.0))
        >>> print(q1)
        (0.707106781187, 0.707106781187, 0.0, 0.0)
        """
        a = (angle if isinstance(angle, Radian) else angle.to_radian()) / 2
        s = a.sin()
        c = a.cos()
        vector = axis.normalized()
        return Quaternion(c, s * vector.x(), s * vector.y(), s * vector.z()).normalized()


    @staticmethod
    def around_x(angle):        
        return Quaternion.from_axis_and_angle(Vector.X_UNIT(), angle)


    @staticmethod
    def around_y(angle):
        return Quaternion.from_axis_and_angle(Vector.Y_UNIT(), angle)


    @staticmethod
    def around_z(angle):
        return Quaternion.from_axis_and_angle(Vector.Z_UNIT(), angle)      


    def __init__(self, w, x, y, z):
        self._w = w
        self._x = x
        self._y = y
        self._z = z


    def __str__(self):
        return '({w}, {x}, {y}, {z})'.format(w=self._w, x=self._x, y=self._y, z=self._z)


    def __call__(self):
        return (self._w, self._x, self._y, self._z)


    def __getitem__(self, i):
        return self()[i]


    def vector(self):
        return Vector(self._x, self._y, self._z)


    def scalar(self):
        return self._w


    def length_squared(self):
        """
        :return: квадратичную длину кватерниона.

        >>> q0 = Quaternion(1.0, 2.0, 0.0, -1.0)
        >>> print(q0.length_squared())
        6.0
        """
        return self._w ** 2 + self._x ** 2 + self._y ** 2 + self._z ** 2


    def length(self):
        """
        :return: длину кватерниона.

        >>> q0 = Quaternion(4.0, 2.0, 2.0, 1.0)
        >>> print(q0.length())
        5.0
        """
        return self.length_squared() ** 0.5


    def normalize(self):
        """
        Производит приведение кватерниона к еденичной длине.

        >>> q0 = Quaternion(6.0, 0.0, 0.0, 0.0)
        >>> q0.length()
        6.0
        >>> q0.normalize()
        >>> q0.length()
        1.0
        """
        length = self.length()
        if length >= 0:
            self._w /= length
            self._x /= length
            self._y /= length
            self._z /= length            


    def normalized(self):
        """
        :return: копию текущего нормализованного кватерниона.

        >>> q0 = Quaternion(6.0, 0.0, 0.0, 0.0)
        >>> q1 = q0.normalized()
        >>> print(q1)
        (1.0, 0.0, 0.0, 0.0)
        """
        import copy
        res = copy.copy(self)
        res.normalize()
        return res    


    def conjugate(self):
        """
        :return: кватернион, сопряжённый по отношению к текущему.

        >>> q0 = Quaternion(1.5, 0.7, 0.3, -1.3)
        >>> q1 = q0.conjugate()
        >>> print(q1)
        (1.5, -0.7, -0.3, 1.3)
        """
        return Quaternion(self._w, -self._x, -self._y, -self._z)


    def __neg__(self):
        """
        :return: кватернион, с векторной и скалярной компонентами,
        противоположными текущему.

        >>> q0 = Quaternion(-1.0, 1.0, 0.0, 1.0)
        >>> q1 = -q0
        >>> print(q1)
        (1.0, -1.0, -0.0, -1.0)
        """
        return Quaternion(-self._w, -self._x, -self._y, -self._z)


    def __add__(self, q):
        """
        :return: кватернион, полученный путем покомпонентного сложения
        текущего и переданного кватернионов.

        >>> q0 = Quaternion(2.0, -1.0, 1.0, 4.0)
        >>> q1 = Quaternion(-1.0, 3.0, 2.0, -1.0)
        >>> q2 = q0 + q1
        >>> print(q2)
        (1.0, 2.0, 3.0, 3.0)
        """
        return Quaternion(self._w + q._w, self._x + q._x, self._y + q._y, self._z + q._z)


    def __sub__(self, q):
        """
        :return: кватернион, полученный путём покомпонетного вычитания
        текущего и переданного кватернионов.
        
        >>> q0 = Quaternion(4.0, 3.0, -1.0, 4.0)
        >>> q1 = Quaternion(-1.0, 3.0, 1.0, 2.0)
        >>> q2 = q0 - q1
        >>> print(q2)
        (5.0, 0.0, -2.0, 2.0)
        """
        return Quaternion(self._w - q._w, self._x - q._x, self._y - q._y, self._z - q._z)


    def __rmul__(self, k):
        """
        Левостороннее умножение текущего кватерниона на коэффициент.

        >>> q0 = Quaternion(2.0, -1.0, 3.0, 4.0)
        >>> q1 = 2.0 * q0
        >>> print(q1)
        (4.0, -2.0, 6.0, 8.0)
        """
        return Quaternion(
            self._w * k,\
            self._x * k,\
            self._y * k,\
            self._z * k\
        )


    def __mul__(self, q):
        """
        :return: кватернион, полученный путём умножения кватернионов текущего и переданного.
        Смысл данного умножения - получить суммированный поворот.
        Данная операция не обладает свойством коммутативности, то есть q0 * q1 != q1 * q0.

        >>> q0 = Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Radian(math.pi / 2))
        >>> q1 = Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Radian(math.pi))
        >>> q0 = q0 * q0
        >>> print(q0)
        (2.22044604925e-16, 1.0, 0.0, 0.0)
        >>> print(q1)
        (6.12323399574e-17, 1.0, 0.0, 0.0)

        Если же переданный аргумент является коэффициентом, тогда возвращается
        кватернион, составленный из компонентов текущего, умноженного на коэффициент.

        >>> q0 = Quaternion(2.0, 3.0, 1.0, -1.0)
        >>> q1 = q0 * 5
        >>> print(q1)
        (10.0, 15.0, 5.0, -5.0)

        :param q: Коэффициент или кватернион.
        :type q: Quaternion или float
        :returns: Quaternion
        """
        def q_is_quaternion():
            return Quaternion(\
                self._w * q._w - self._x * q._x - self._y * q._y - self._z * q._z,\
                self._w * q._x + self._x * q._w + self._y * q._z - self._z * q._y,\
                self._w * q._y + self._y * q._w + self._z * q._x - self._x * q._z,\
                self._w * q._z + self._z * q._w + self._x * q._y - self._y * q._x\
            )
        
        return q_is_quaternion() if isinstance(q, Quaternion) else q * self


    def __iadd__(self, q):
        """
        Суммирует текущий кватернион с переданным покомпонетно.

        >>> q0 = Quaternion(3.7, -1.4, 2.0, 7.1)
        >>> q1 = Quaternion(-1.2, 4.5, 1.3, -1.1)
        >>> q0 += q1
        >>> print(q0)
        (2.5, 3.1, 3.3, 6.0)
        """
        self._w += q._w
        self._x += q._x
        self._y += q._y
        self._z += q._z
        return self


    def __isub__(self, q):
        """
        Отнимает от текущего кватерниона переданный кватернион покомпонетно.

        >>> q0 = Quaternion(4.5, -1.4, 3.1, -4.5)
        >>> q1 = Quaternion(3.6, 1.2, 3.1, 2.7)
        >>> q0 -= q1
        >>> print(q0)
        (0.9, -2.6, 0.0, -7.2)
        """
        self._w -= q._w
        self._x -= q._x
        self._y -= q._y
        self._z -= q._z
        return self


    def __imul__(self, q):
        """
        Умножает текущий кватернион на переданный.

        >>> q0 = Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Radian(math.pi / 2))
        >>> q0 *= q0
        >>> print(q0)
        (2.22044604925e-16, 1.0, 0.0, 0.0)
        """
        rotated = self * q
        self._w = rotated._w
        self._x = rotated._x
        self._y = rotated._y
        self._z = rotated._z
        return self


    def __eq__(self, q):
        """
        :return: истинность равенства текущего и переданного кватернионов.

        >>> q0 = Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Radian(math.pi / 2))
        >>> q1 =Quaternion.from_axis_and_angle(Vector(1.0, 0.0, 0.0), Degree(90.000000001))
        >>> q0 == q1
        True
        """
        from rissile.tools.assistants import is_equals
        return is_equals(self._w, q._w) and is_equals(self._x, q._x) and is_equals(self._y, q._y) and is_equals(self._z, q._z)


    def rotated_vector(self, vector):
        """
        :return: вектор, повёрнутый на углы, соответствующие данному кватерниону.
        Ниже приведён пример поворота вектора (1, 0, 0) вокруг оси Z.

        >>> q0 = Quaternion.from_axis_and_angle(Vector(0.0, 0.0, 1.0), Radian(math.pi / 2))
        >>> vector = q0.rotated_vector(Vector(1.0, 0.0, 0.0))
        >>> print(vector)
        (2.22044604925e-16, 1.0, 0.0)
        """
        q0 = Quaternion(0, vector.x(), vector.y(), vector.z())
        return (self * q0 * self.conjugate()).vector()        


    def roll(self, reproject_axis=True):
        """
        :return: локальный угол курса текущего кватерниона.
        :return type: Radian

        >>> q0 = Quaternion.around_z(Degree(47.0))
        >>> roll = q0.roll()
        >>> print(roll.to_degree())
        47.0
        """
        if reproject_axis:
            y = 2.0 * self._y
            z = 2.0 * self._z
            wz = z * self._w
            xy = y * self._x
            yy = y * self._y
            zz = z * self._z
            return Radian(math.atan2(xy + wz, 1.0 - yy - zz))
        else:
            first = 2.0 * (self._x * self._y + self._w * self._z)
            second = self._w ** 2 + self._x ** 2 - self._y ** 2 - self._z ** 2
            return Radian(math.atan2(first, second))


    def pitch(self, reproject_axis=True):
        """
        :return: локальный угол тангажа текущего кватерниона.
        :return type: Radian
        
        >>> q0 = Quaternion.around_x(Degree(53.0))
        >>> pitch = q0.pitch()
        >>> print(pitch.to_degree())
        53.0
        """
        if reproject_axis:
            x = 2.0 * self._x
            z = 2.0 * self._z
            wx = x * self._w
            xx = x * self._x
            yz = z * self._y
            zz = z * self._z
            return Radian(math.atan2(yz + wx, 1.0 - xx - zz))
        else:
            first = 2.0 * (self._y * self._z + self._w * self._x)
            second = self._w ** 2 - self._x ** 2 - self._y ** 2 + self._z ** 2
            return Radian(math.atan2(first, second)) 


    def yaw(self, reproject_axis=True):
        """
        :return локальный угол крена текущего кватерниона.
        :return type: Radian
        
        >>> q0 = Quaternion.around_y(Degree(-30.0))
        >>> yaw = q0.yaw()
        >>> print(yaw.to_degree())
        -30.0
        """
        if reproject_axis:
            x = 2.0 * self._x
            y = 2.0 * self._y
            z = 2.0 * self._z
            wy = y * self._w
            xx = x * self._x
            xz = z * self._x
            yy = y * self._y
            return Radian(math.atan2(xz + wy, 1.0 - xx - yy))
        else:
            return Radian(math.asin(-2.0 * (self._x * self._z - self._w * self._y)))


    def dot(self, q):
        """
        Возвращает скалярное произведение текущего и
        переданного кватернионов.

        >>> q0 = Quaternion(4.0, 2.5, -2.0, 2.0)
        >>> q1 = Quaternion(1.0, 2.0, -1.5, 0.5)
        >>> dot = q0.dot(q1)
        >>> print(dot)
        13.0
        """
        return self._w * q._w + self._x * q._x + self._y * q._y + self._z * q._z


    def slerp(self, factor, dest, shortest_path = False):
        """
        Сферическая линейная интерполяция между двумя кватернионами.
        Операция не обладает свойствами коммутативности, то есть
        slerp(first_quaternion, 0.25, second_quaternion) != slerp(second_quaternion, 0.75, first_quaternion).
        Это особенно важно учитывать в ряде задач, например при рассчёте инверсной кинематики.

        :param factor: указывает на шаг интерполяции между двумя кватернионами, принадлежит отрезку [0; 1].
        :type factor: float
        :param dest: кватернион, к которому будет выполняться интерполяция.
        :type dest: Quaternion

        >>> q0 = Quaternion.around_x(Degree(0.0))
        >>> q1 = Quaternion.around_x(Degree(90.0))
        >>> q2 = q0.slerp(0.0, q1)
        >>> q3 = q0.slerp(0.5, q1)
        >>> q4 = q0.slerp(1.0, q1)
        >>> print(q0)
        (1.0, 0.0, 0.0, 0.0)
        >>> print(q1)
        (0.707106781187, 0.707106781187, 0.0, 0.0)
        >>> print(q2)
        (1.0, 0.0, 0.0, 0.0)
        >>> print(q3)
        (0.923879532511, 0.382683432365, 0.0, 0.0)
        >>> print(q4)
        (0.707106781187, 0.707106781187, 0.0, 0.0)
        """
        cos = self.dot(dest)
        if cos < 0.0 and shortest_path:
            cos *= -1
            res = -dest
        else:
            res = dest
        if math.fabs(cos) < (1.0 - assistants.TOLERANCE_VALUE):
            sin = (1 - cos ** 2) ** 0.5
            angle = Radian(math.atan2(sin, cos))
            coeff0 = (angle * (1.0 - factor)).sin() / sin
            coeff1 = (angle * factor).sin() / sin
            return self * coeff0 + res * coeff1
        else:
            res = self * (1.0 - factor) + res * factor
            res.normalise()
            return res


    def clone(self):
        return Quaternion(self._w, self._x, self._y, self._z)
