# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$08.07.2014 8:22:30$"



from rissile.rio.params.item import ValueForGenerator
from rissile.rio.params.test_params_generator import GeneratorTester


class TestValueGenerator(GeneratorTester):
    def _create_generator(self):
        from rissile.rio.params.params_generator import ParamsGenerator
        def create_range_value():
            value = ValueForGenerator('value', 'range generator', None)
            begin = value.part(0)
            begin.set_value(1)
            right_border = value.part(1)
            right_border.set_value(3)
            step = value.part(2)
            step.set_value(1)
            return value


        generator = ParamsGenerator('wo generator')
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
        from rissile.rio.params.item import Root
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
        
        
class TestRootRepeater(GeneratorTester):
    _number_of_params = 5
    _params = {'mass': 10, 'velocity': 20}
    
    def _create_generator(self):
        from rissile.rio.params.item import RootRepeater
        root_repeater = RootRepeater('root_repeater')
        root_repeater.set_value(self._number_of_params)
        root_repeater.restore_from_params(self._params)
        return root_repeater.generator()
    
    def _right_data(self):
        return ({'index': i, 'root_repeater': self._params} for i in range(self._number_of_params))
