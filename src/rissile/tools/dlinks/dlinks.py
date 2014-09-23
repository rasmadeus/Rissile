# -*- coding: utf-8 -*-
__author__="K. Kulikov"
__date__ ="$Jun 06, 2014 10:30:15 AM$"


"""
В модуле приведена реализация типовых динамичеких
звеньев, которые используются для построения
систем автоматического управления.
множитель: y = k * x,
производная: y = p,
интеграл: y = 1 / p,
где p - оператор Лапласса.
"""


class Link:
    """
    Класс описывает базовый интерфейс типовых
    динамических звеньев.
    """

    def __init__(self, step):
        self._step = step

    def __call__(self, in_value):
        pass

    def reset(self):
        pass

    def set_step(self, step):
        self._step = step

    def step(self):
        return self._step


class Gainer(Link):
    """
    Динамическое звено усилитель: y = k * x.
    """

    def __init__(self, step, k):
        Link.__init__(self, step)
        self._k = k        

    def set_k(self, k):
        self._k = k

    def k(self):
        return self._k

    def __call__(self, in_value):
        return self._k * in_value


class LinkPreValueKeep:
    """
    Интерфейс для динамических звеньев,
    которые в своей реализации используют информацию
    о входе, пришедшем на предыдущем шаге счёта.
    """

    def __init__(self, step):
        Link.__init__(self, step)
        self._prev = 0

    def reset(self):
        self._reset()
        self._prev = 0

    def __call__(self, in_value):
        result = self._out(in_value)
        self._prev = in_value
        return result

    def _reset(self):
        pass

    def _out(self, in_value):
        pass


class Derivative(LinkPreValueKeep):
    """
    Динамическое звено производная: y = p.
    """

    def _out(self, in_value):
        return (in_value - self._prev) / self._step


class Integral(LinkPreValueKeep):
    """
    Динамическое звено интеграл: y = 1 / p.
    """

    def __init__(self, step):
        LinkPreValueKeep.__init__(self, step)
        self._summ = 0


    def _reset(self):
        self._summ = 0


    def _out(self, in_value):
        self._summ += 0.5 * (self._prev + in_value) * self._step
        return self._summ
        

    

