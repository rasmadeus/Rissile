# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$Jun 06, 2014 10:30:15 AM$"


from rissile.tools.quaternion import Quaternion
from rissile.tools.vector import Vector
from rissile.tools.assistants import about_zero


class WorldObject:
    """
    Класс предоставляет интерфейс для численного расчёта предметной модели.
    Порядок работы с объектом рекомендуется выполнять следующим образом:

    >>> obj = WorldObject('obj', 0.001)           # Создание объекта.
    >>> obj.init({'H, м': 1000})                  # Устанавливаем начальное состояние объекта.
    >>> obj.prepare_for_stepping()                # Подготавливаем объект к счёту.
    >>> for tick in range(1000): obj.do_step()    # Выполнить расчёт состояний объекта.
    >>> obj.call_out_agent(lambda id, buffer: id) # Обработаем массив свойств, описывающих состояние объекта.
    'obj'
    >>> obj.time()
    1.0
    """
    def __init__(self, id, step, owner=None):
        """
        Инициализация общих для всех объектов параметров.

        :param id: идентификатор объекта.
        :type id: str
        :param step: шаг интегрирования объекта.
        :type step: float
        :param owner: владелец объекта.
        :type owner: WorldObject
        """
        self._id = id
        self._step = step
        self._owner = owner
        self._parts = []
        self._origin_state = {}
        self._fill_origin_state()
        if owner is not None:
            owner._parts.append(self)


    def run(self):
        """

        """
        while self._is_alive_and_kicking():
            self.do_step();

    
    def _fill_origin_state(self):
        pass


    def _is_alive_and_kicking(self):
        """
        :return: условие окончания счёта модели.
        :return type: bool
        """
        return True 


    def init(self, params=None):
        """
        Функция приводит объект в начальное состояние.
        Вызывать её следует до начала счёта.

        :param params: словарь со значениями.
        :type params: dict(str: value)
        """
        def init_values():
            """
            Функция производит инициализацию атрибутов, необходимых для
            расчёта времени и сохранения состояний объекта.
            """
            self._step_count = 0  # Не было совершено ни одного такта счёта.
            self._buffer = {}     # Забуферизованные состояния объекта отсутствуют.
            self._init_buffer()
            self._save_state()    # После инициализации, сохраним начальное состояние объекта.


        def init_params():
            """
            Функция производит разбор входных параметров.
            """
            if params is not None:
                self._init(params)


        def init_parts():
            """
            Функция инициализирует составные части self.
            """
            for part in self._parts:
                part.init(None if params is None else params.get(part._id))


        def init_origin_state():
            self._origin_state = params
            
            
        init_origin_state()
        init_params()
        init_parts()
        init_values()


    def prepare_for_stepping(self):
        """
        Функция подготавливает объект к счёту. Должна быть вызвана до начала счёта.
        """
        self._set_frequency_rate(self.min_step())


    def time(self):
        """
        Время соответствующее текущему состоянию объекта.
        """
        return self._step * self._step_count


    def id(self):
        """
        :return: идентификатор объекта.
        """
        return self._id
    

    def do_step(self):
        """
        Функция расчитывает состояние объекта на следующий такт.
        """
        def do_parts_step():
            """
            Функция просчитывает состояние частей self.
            """
            for part in self._parts:
                part.do_step()


        def try_do_step():
            """
            Функция производит расчёт состояния объекта на текущий момент времени, если настало очередь делать это.
            """
            if self.is_time_do_step():
                self._do_step()
                self._step_count += 1
                self._missed_steps_count = 1
                self._save_state()
            else:
                self._missed_steps_count += 1


        do_parts_step()
        try_do_step()


    def call_out_agent(self, out_agent):
        """
        :return: результат работы out_agent(идентификатор объекта, буферизованные данные)
        :param out_agent: функция обработчик буферизованных состояний объекта.
        :type out_agent: function(str, dict)
        """
        return out_agent(self._id, self._buffer)


    def origin_state(self):
        return self._origin_state


    def min_step(self):
        """
        :return: минимум из шагов счёта self и его частей.
        """
        min_step = self._step
        for part in self._parts:
            part_min_step = part.min_step()
            if part_min_step < min_step:
                min_step = part_min_step
        return min_step


    def step(self):
        """
        :return: шаг счёта объекта.
        """
        return self._step


    def is_time_do_step(self):
        """
        :return: признак необходимости счёта объекта.
        """
        return self._frequency_rate == self._missed_steps_count


    def serialize(self):
        """
        :return: словарь с сериализованным self.
        """
        params = {}
        self._serialize(params)
        for part in self._parts:
            params[part.id()] = part.serialize()
        return params


    def _set_frequency_rate(self, min_step):
        """
        Функция выполняет подготовку объекта к синхронному счёту.

        :param min_step: минимум из шагов счёта self и его частей.
        """
        self._frequency_rate = int(self._step / min_step + 0.5)
        self._missed_steps_count = 1
        for part in self._parts:
            part._set_frequency_rate(min_step)


    def _add_id_to_buffer(self, id):
        """
        Добавляет к буферу, хранящему состояние объекта новый свойство.

        :param id: идентификатор свойства.
        :type id: str
        """
        self._buffer[id] = []


    def _save_value(self, id, value):
        """
        Функция буферизует переданное значение.

        :param id: идентификатор свойства. Должен быть добавлен в функции _init_buffer.
        :type id: str
        :param value: значение свойства на текущий момент времени.
        """
        self._buffer[id].append(value)


    def _init_buffer(self):
        """
        В этом методе произведите инициализацию свойсв буфера при
        помощи функции _add_id_to_buffer
        """
        self._add_id_to_buffer('t,c')


    def _save_state(self):
        """
        В этом методе выполните буферизацию состояния объекта при
        помощи функции _save_value.
        """
        self._save_value('t,c', self.time())


    def _init(self):
        """
        В этом методе выполняйте инициализацию параметров, уникальных для self.
        """
        pass


    def _do_step(self):
        """
        Изменяйте состояние объекта в этой функции.
        """
        pass


    def _serialize(self, params):
        """
        Выполняйте сериализацию объекта в этой функции.

        :param params: структура, подлежащая сериализации.
        :type params: dict(str: float | int | bool | str)
        """
        pass