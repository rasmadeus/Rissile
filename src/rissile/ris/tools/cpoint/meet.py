# -*- coding: utf-8 -*-

__author__="K. Kulikov"
__date__ ="$01.07.2014 11:53:27$"

"""
Автор алгоритмов: Судейко О. Е.

Все нижеследующие комментарии частично были переписаны со старой реализации,
а частично написаны прораммистом. Поэтому нуждаются в редакционной правке со
стороны эксперта.
"""

def radar_tracking_radius_of_the_earth():
    """
    :return: радиолокационный радиус Земли в метрах.
    """
    return 8487000


def radar_tracking_diameter_of_the_earth():
    """
    :return: радиолакационный диаметр Земли в метрах.
    """
    return 16974000


from rissile.ris.tools.vector import Vector
class MeetPos:
    """
    Решает задачу пролонгации движения цели - расчитывает точку встречи с целью.
    """
    def __init__(self, t_begin, t_end, pos, V):
        """
        :param t_begin: время начала пролонгации.
        :param t_end: время конца пролонгации.
        :param pos: позиция цели.
        :item_type param: Vector
        :param V: скорость цели.
        :item_type V: Vector
        """
        def init_t():
            """
            Заполним выходную структуру временем конца пролонгации.
            """
            self._t = t_end


        def init_pos():
            """
            Вычислим новую позицию цели.
            """
            dt = t_end - t_begin
            self._pos = pos + Vector(dt, dt, dt) * V


        def init_h():
            """
            Произведём вычисление высоты и поправим позицию цели в части y.
            """
            def change_y(h, y):
                self._H = h
                self._pos = Vector(self._pos.x(), y, self._pos.z())


            dh = self._pos.length_squared() / radar_tracking_diameter_of_the_earth()
            self._H = self._pos.y() + dh
            if self._H < 0: change_y(0, -dh)
            if self._H > 20000 and (self._pos.y() + dh) < 20000: change_y(20000, self._H - dh)


        def init_r():
            """
            Зыполним выходную структура дальностью.
            """
            self._R = self._pos.length()


        def init_vr():
            """
            Заполним выходную структуру скоростью изменения дальности.
            """
            Vr = 0
            Vr = Vr + self._pos.x() * V.x() / self._R
            Vr = Vr + self._pos.y() * V.y() / self._R
            Vr = Vr + self._pos.z() * V.z() / self._R
            self.Vr = Vr

        init_t()
        init_pos()
        init_h()
        init_r()
        init_vr()


    def pos(self):
        """
        :return: точку встречи.
        """
        return self._pos


    def time(self):
        """
        :return: время полёта в точку встречи.
        """
        return self._t


    def R(self):
        """
        :return: наклонная дальность до точки встречи.
        """
        return self._R


    def H(self):
        """
        :return: высота точки встречи.
        """
        return self._H


    def meeting_time(self, V):
        """
        :return: время встречи.
        :param V: модуль средней скороти ракеты.
        """
        return self._R / (V - self.Vr)


class Missile:
    """
    Класс описывает свойства ракеты, необходимые для расчёта точки встречи.
    """
    def v_average(self):
        """
        :return: среднюю скорость ракеты.
        """
        pass

    def k_v_average(self):
        """
        :return: матрицу коэффициентов поверхности, аппроксимирующей среднюю скорость.
        """
        pass

    def start_engine_time(self):
        """
        :return: время старта ракеты.
        """
        pass


    def half_of_R(self):
        """
        :return: полувину дальности полёта ракеты
        """
        pass


    def unknown_R(self):
        """
        :return: непонятно что, но прослеживается связь с наклонной дальностью.
        """
        pass


    def half_of_H(self):
        """
        :return: половину потолка по высоте.
        """
        pass


    def flight_time(self, meet_pos):
        """
        :param R: наклонная дальность
        :param H: высота
        :return: время полёта ракеты в точку (R, H)
        """
        def flight_v_average(r, h):
            """
            :return: среднюю скорость ракеты при полёте в точку (R, H)
            """
            av = self.k_v_average()
            V = 0
            for ir in range(len(av)):
                for ih in range(len(av[0])):
                    V += av[ir][ih] * (h ** ih) * (r ** ir)
            return V


        def range_value(value):
            value = 1 if value - 1 > 0 else value
            value = -1 if value + 1 < 0 else value
            return value


        r = range_value((meet_pos.R() - self.half_of_R()) / self.unknown_R())
        h = range_value((meet_pos.H() - self.half_of_H()) / self.half_of_H())
        return meet_pos.R() /flight_v_average(r, h) + self.start_engine_time()


    def find_meeting_point(self, pos_target, V_target, t0=0, accuracy=0.2):
        """
        :return: парметры точки встречи.
        :param pos_target: позиция цели.
        :param V_target: скорость цели.
        :accuracy: точность вычисления точки встречи.
        """
        def first_approach_time():
            return MeetPos(t0, t0, pos_target, V_target).meeting_time(self.v_average())


        def position(time):
            return MeetPos(t0, time, pos_target, V_target)


        def time_meet(t1, t2, t3):
            """
            Расчёт времени встречи.
            """
            return t2 + 1 / (1 / (t1 - t2) + 1 / (t3 - t2))


        def number_of_approach():
            """
            :return: количество приближений.
            """
            return 5


        import math
        t1 = first_approach_time()
        for _ in range(number_of_approach()):
            meet_pos = position(t0 + t1)
            t2 = self.flight_time(meet_pos)
            if math.fabs(t2 - t1) < accuracy: return meet_pos
            meet_pos = position(t0 + t2)
            t3 = self.flight_time(meet_pos)
            meet_pos = position(t0 + (t2 + t3) / 2)
            if math.fabs(t3 - t2) < accuracy: return meet_pos
            t_meet = t0 + time_meet(t1, t2, t3)
        meet_pos = position(t_meet)
        return meet_pos


class MeetManager:
    """
    Класс предоставляет интерфейс для расчёта точки встречи с целью.
    """
    def __init__(self, missile, start_target_pos, V_target, step):
        """
        :item_type start_target_pos: Vector
        :item_type V_target: Vector
        :param step: шаг изменения по координатам.
        :item_type step: Vector
        """
        self._missile = missile
        self._start_target_pos = start_target_pos
        self._V_target = V_target
        self._step = step


    def meeting_point(self, n_step, f):
        """
        :param f: функция для обратного вызова.
        :type f: function(MeetPos)
        """
        for i in range(n_step):
            target_pos = self._start_target_pos - self._step * Vector(i, i, i)
            f(self._missile.find_meeting_point(target_pos, self._V_target))