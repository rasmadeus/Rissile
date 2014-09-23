# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$04.07.2014 9:14:59$"


"""
Модуль stone содержит пример работы с библиотекой wo.
"""


from rissile.tools.angles import Radian
from rissile.wo.world_object import WorldObject

class FlyingStone(WorldObject):
    """
    Класс реализует модель полёта камня на Земле с нулевой высоты
    без учёта сопротивления воздуха в плоскости XY. Данный пример ознакомит пользователя
    с принципами работы с библиотекой wo.
    """
    def __init__(self):
        WorldObject.__init__(self, 'flying_stone', 0.001)


    def _init(self):
        """
        Для расчёта траектории полёта камня нам нужно знать
        его массу, угол бросания камня и начальную скорость.
        """
        self._mass = self._origin_state['mass']
        self._angle = Radian.from_degrees(self._origin_state['angle'])
        self._V0 = self._origin_state['V0']
        self._time = 0
        self._X = 0
        self._Y = 0
        self._V = 0


    def _fill_origin_state(self):
        self._origin_state['mass'] = 100
        self._origin_state['angle'] = 45
        self._origin_state['V0'] = 123


    def _init_buffer(self):
        """
        Будем контролировать следующие параметры состояния полёта камня:
        координаты X, Y, время полёта и скорость.
        """
        self._add_id_to_buffer('t,c')
        self._add_id_to_buffer('X,м')
        self._add_id_to_buffer('Y,м')
        self._add_id_to_buffer('V,м/c')


    def _save_state(self):
        """
        Соответственно все параметры объекты, которые мы хотим контролировать,
        необходимо буферизовать на каждом такте счёта.
        Следите за сигнатурой контролируемых объектов, которую вы определили в
        функции _init_buffer.
        """
        self._save_value('t,c', self._time)
        self._save_value('X,м', self._X)
        self._save_value('Y,м', self._Y)
        self._save_value('V,м/c', self._V)


    def _serialize(self, params):
        """
        Все параметры, по которым можно будет восстановить начальное состояние объекта,
        сохраним в структуре params.

        :param params: структура, содержащая начальное состояние объекта.
        :type params: dict(str: float | int | bool | str)
        """
        params['mass'] = self._mass
        params['angle'] = self._angle.to_degree()()
        params['V0'] = self._V0


    def _is_alive_and_kicking(self):
        return self._Y >= 0

    def _do_step(self):
        pass