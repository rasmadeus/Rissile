# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$03.07.2014 16:30:50$"


import unittest
from rissile.wo.data_generator import WorldObjectInitDataGenerator, ValueConstGenerator, ValueRangeGenerator


@unittest.SkipTest
class GeneratorTester(unittest.TestCase):
    def test_generator(self):
        right_data = self._right_data()
        i = 0
        for value in self._create_generator():
            self.assertEquals(value, right_data[i])
            i += 1


    def _create_generator(self):
        pass


    def _right_data(self):
        pass


class TestDataGenerator(GeneratorTester):
    def _create_generator(self):
        def create_generator_of_value():
            gen = WorldObjectInitDataGenerator('value generator')
            gen.set_value(ValueRangeGenerator('X', {'begin': 0, 'right_border': 1, 'step': 1}))
            gen.set_value(ValueRangeGenerator('H', {'begin': 0, 'right_border': 10, 'step': 2}))
            return gen


        def create_generator_of_wo_init_data():
            gen = WorldObjectInitDataGenerator('wo generator')
            gen.set_value(ValueConstGenerator('V', {'value': 0}))
            gen.set_value(ValueConstGenerator('m', {'value': 2}))
            gen.set_value(create_generator_of_value())
            return gen


        return create_generator_of_wo_init_data()


    def _right_data(self):
        return (
                {'V': 0, 'm': 2, 'value generator': {'X': 0, 'H': 0}},
                {'V': 0, 'm': 2, 'value generator': {'X': 0, 'H': 2}},
                {'V': 0, 'm': 2, 'value generator': {'X': 0, 'H': 4}},
                {'V': 0, 'm': 2, 'value generator': {'X': 0, 'H': 6}},
                {'V': 0, 'm': 2, 'value generator': {'X': 0, 'H': 8}},
                {'V': 0, 'm': 2, 'value generator': {'X': 0, 'H': 10}},
                {'V': 0, 'm': 2, 'value generator': {'X': 1, 'H': 0}},
                {'V': 0, 'm': 2, 'value generator': {'X': 1, 'H': 2}},
                {'V': 0, 'm': 2, 'value generator': {'X': 1, 'H': 4}},
                {'V': 0, 'm': 2, 'value generator': {'X': 1, 'H': 6}},
                {'V': 0, 'm': 2, 'value generator': {'X': 1, 'H': 8}},
                {'V': 0, 'm': 2, 'value generator': {'X': 1, 'H': 10}}
            )