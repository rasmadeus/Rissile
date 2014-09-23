# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$08.07.2014 8:22:30$"


import unittest
from rio.params.item import ValueForGenerator
from rio.params.item import Root
from rissile.wo.data_generator import WorldObjectInitDataGenerator
from rissile.wo.test_data_generator import GeneratorTester


class TestValueGenerator(GeneratorTester):
    def _create_generator(self):
        def create_range_value():
            value = ValueForGenerator('value', 'range generator', None)
            begin = value.part(0)
            begin.set_value(1)
            right_border = value.part(1)
            right_border.set_value(3)
            step = value.part(2)
            step.set_value(1)
            return value


        generator = WorldObjectInitDataGenerator('wo generator')
        create_range_value().fill(generator)
        return generator


    def _right_data(self):
        return (
            {'value': 1},
            {'value': 2},
            {'value': 3}
        )


class TestRootGenerator(GeneratorTester):
    def _create_generator(self):
        terra = Root('terra', None)
        ValueForGenerator('aircraft', 'const generator', terra)
        missile = Root('missile', terra)
        engine = ValueForGenerator('engine', 'range generator', missile)
        engine.part(1).set_value(1)
        engine.part(2).set_value(1)
        fighting_part = ValueForGenerator('fighting part', 'range generator', missile)
        fighting_part.part(1).set_value(1)
        fighting_part.part(2).set_value(1)
        return terra.generator()


    def _right_data(self):
        return (
            {'aircraft': 0.0, 'missile':{'engine': 0.0, 'fighting part': 0.0}},
            {'aircraft': 0.0, 'missile':{'engine': 0.0, 'fighting part': 1.0}},
            {'aircraft': 0.0, 'missile':{'engine': 1.0, 'fighting part': 0.0}},
            {'aircraft': 0.0, 'missile':{'engine': 1.0, 'fighting part': 1.0}},
        )