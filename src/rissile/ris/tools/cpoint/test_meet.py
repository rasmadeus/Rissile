# -*- coding: utf-8 -*-

__author__="K. Kulikov"
__date__ ="$01.07.2014 13:35:12$"

import unittest
from rissile.ris.tools.cpoint import meet
from rissile.ris.tools.vector import Vector

class TestMissile(meet.Missile):
    def v_average(self):
        return 1000

    def k_v_average(self):
        """
        :return: матрицу коэффициентов поверхности, аппроксимирующей среднюю скорость
        в зависимости от наклонной дальности и высоты.

        Матрица должна содержать хотя бы один элемент ((value, ), )
        """
        return (\
            (949.149, 109.152, -37.017, 0.0),\
            (-174.643, 93.017, 2.847, -22.78),\
            (-144.271, -56.949, 109.152, 36.068),\
            (198.372, -57.898, -103.457, -5.695)\
        )

    def start_engine_time(self):
        return 2


    def half_of_R(self):
        return 27500


    def unknown_R(self):
        return 22500


    def half_of_H(self):
        return 10000


class TestMeet(unittest.TestCase):

    def setUp(self):
        self._i = 0
        self._right_data = (
            (54.11, 53.33, 52.55, 51.78, 51.0, 50.24, 49.47, 48.71, 47.96, 47.21, 46.46, 45.72, 44.98, 44.25, 43.53, 42.81, 42.10, 41.39, 40.69, 39.99, 39.30),
            (42.94, 42.33, 41.72, 41.11, 40.5, 39.88, 39.26, 38.64, 38.02, 37.40, 36.77, 36.14, 35.51, 34.87, 34.24, 33.59, 32.95, 32.31, 31.66, 31.00, 30.35)
        )


    def t(self):
        return self._right_data[0][self._i]


    def x(self):
        return self._right_data[1][self._i]


    def next(self):
        self._i += 1


    def test_meet(self):
        """
        Повторим вариант для предложенной ракеты.
        """
        def outer(meet_pos):
            print('t={t}, x={x}'.format(t=meet_pos.time(), x=meet_pos.pos().x() / 1000))


        def comparator(meet_pos):
            from rissile.ris.tools.assistants import is_equals
            tolerance = 0.005
            self.assertTrue(is_equals(self.t(), meet_pos.time(), tolerance))
            self.assertTrue(is_equals(self.x(), meet_pos.pos().x() / 1000, tolerance))
            self.next()


        manager = meet.MeetManager(TestMissile(), Vector(70000, 20000, 0), Vector(-500, 0, 0), Vector(1000, 0, 0))
        manager.meeting_point(21, comparator)
        
            