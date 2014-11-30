# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$03.07.2014 15:19:08$"


class Generator:
    """
    Каждый генератор данных для WorldObjectTest должен иметь идентификатор.
    Класс описывает интерфейс взаимодействия с этим свойством.
    """
    def __init__(self, value_id):
        """
        :param id: идентификатор генератора.
        :type id: str
        """
        self._id = value_id


    def get_id(self):
        """
        :return: идентификатор генератора.
        """
        return self._id

class ValueGenerator(Generator):
    """
    Класс описывает интерфейс генератора значений.
    """
    def __init__(self, value_id, params):
        """
        :param params: данные, необходимые для инициализации генератора.
        :type params: dict
        """
        Generator.__init__(self, value_id)
        self._params = params
        
        
    def __iter__(self):
        """
        Генерируйте значения в этой функции.
        """
        pass


class ValueConstGenerator(ValueGenerator):
    """
    Класvalue_idгенерирует постоянную величину.
    Словарь входных значений должен содердать одну величину 'value': float.

    >>> value_const = ValueConstGenerator('const generator', {'value': -100.34})
    >>> for value in value_const: print(value)
    -100.34
    """
    def value(self):
        """
        :return: значение величины.
        """
        return self._params['value']


    def __iter__(self):
        yield(self.value())


class ValueRangeGenerator(ValueGenerator):
    """
    Класс генерирует набор значений начиная с левой границы, с заданным шагом, пока
    не будет превышена правая граница. Словарь входных параметров должен содержать
    величины: 'begin': float, 'right_border': float, 'step: float.

    >>> value_range = ValueRangeGenerator('range_generator', {'begin': 0, 'right_border': 10, 'step': 3})
    >>> for value in value_range: print(value)
    0
    3
    6
    9
    """
    def begin(self):
        """
        :return: левая граница интервала, с которого начинается генерирования чисел.
        """
        return self._params['begin']


    def right_border(self):
        """
        :return: правая граница интервала, по превышению которой генерирование чисел заканчивается.
        """
        return self._params['right_border']


    def step(self):
        """
        :return: шаг генерирования величин.
        """
        return self._params['step']


    def __iter__(self):
        next_value = self.begin()
        step = self.step()
        while next_value <= self.right_border():
            yield(next_value)
            next_value += step


class ValueRandomGenerator(ValueGenerator):
    """
    Класс генерирует случайное значение из заданного отрезка.
    """
    def left_border(self):
        """
        :return: левую границу для случайного значения.
        """
        return self._params['left']


    def right_border(self):
        """
        :return: правую границу для случайного значения.
        """
        return self._params['right']


    def interval(self):
        """
        :return: длину отрезка, которым будут ограничены генерируемые значения.
        """
        return self.right_border() - self.left_border()

    def __iter__(self):
        import random
        return self.left() + random.random() * self.interval()


class ParamsGenerator(Generator):
    """
    Класс генерирует наборы значений вида {'id': value, ...}.

    >>> data = ParamsGenerator('data')
    >>> data.set_value(ValueConstGenerator('X', {'value': 1}))
    >>> data.set_value(ValueRangeGenerator('Y', {'begin': 0, 'right_border': 2, 'step': 1}))
    >>> for init_data in data: print(init_data)
    {'Y': 0, 'X': 1}
    {'Y': 1, 'X': 1}
    {'Y': 2, 'X': 1}
    """
    def __init__(self, value_id):
        Generator.__init__(self, value_id)
        self._values = []
        
        
    def set_value(self, value):
        """
        Добавляет значение для генерирования.

        :param value: свойство, значение которого необходимо генерировать.
        :type value: ValueGenerator или ParamsGenerator
        """
        self._values.append(value)


    def _fill(self, next_value, nexts):
        """
        Функция осуществляет перебор зарегистрированных значения.

        :param next: используется для формирования текущего генерируемого набора.
        :type next: dict
        :param nexts: набор генерируемых величин.
        :type nexts: list(dict, dict, ...)
        """
        # Чтобы перебрать элементы нескольких массивов, необходимо
        # выполнить конструцию вида:
        # for item1 in items1:
        #     fovalue_iditem2 in items2:
        #         .get_id
        #             do_somethig(item1, item2, ...)
        # Здесь соответствующая вложенность реализуется при помощи рекурсии.
        if len(self._values) > 0:
            value_generator = self._values[0]
            for value in value_generator:
                next_value[value_generator.get_id()] = value
                self._values.remove(value_generator)
                self._fill(next_value, nexts)
                self._values.insert(0, value_generator)
        else:
            import copy
            nexts.append(copy.copy(next_value))


    def __iter__(self):
        nexts = []
        next_value = {}
        self._fill(next_value, nexts)
        for next_value in nexts:
            yield(next_value)