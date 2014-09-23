# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$03.07.2014 8:57:02$"


import unittest
from rissile.wo.world_object import WorldObject
from rissile.tools.assistants import is_equals


class TestWorldObjectStepping(unittest.TestCase):
    def setUp(self):
        def create_objects():
            self.terra = WorldObject('terra', 0.2)
            self.missile = WorldObject('missile', 0.3, self.terra)
            self.aircraft = WorldObject('aircraft', 0.4, self.terra)
            self.bomb = WorldObject('bomb', 0.1, self.aircraft)
            self.rocket = WorldObject('rocket', 0.5, self.aircraft)
            self.objects = (self.terra, self.missile, self.aircraft, self.bomb, self.rocket)


        def prepare_objects():
            self.terra.init()
            self.terra.prepare_for_stepping()

        create_objects()
        prepare_objects()


    def test_min_step(self):
        self.assertEquals(self.terra.min_step(), 0.1)


    def test_frequency_rate(self):
        self.assertEquals(2, self.terra._frequency_rate)
        self.assertEquals(3, self.missile._frequency_rate)
        self.assertEquals(4, self.aircraft._frequency_rate)
        self.assertEquals(1, self.bomb._frequency_rate)
        self.assertEquals(5, self.rocket._frequency_rate)


    def test_time(self):
        ticks_count = 10
        right_time = {
            'terra':    (0.0, 0.2, 0.2, 0.4, 0.4, 0.6, 0.6, 0.8, 0.8, 1.0),
            'missile':  (0.0, 0.0, 0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 0.9, 0.9),
            'aircraft': (0.0, 0.0, 0.0, 0.4, 0.4, 0.4, 0.4, 0.8, 0.8, 0.8),
            'bomb':     (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
            'rocket':   (0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0)
        }
        for tick in range(ticks_count):
            self.terra.do_step()
            for object in self.objects:\
                self.assertTrue(\
                    is_equals(\
                        object.time(),\
                        right_time[object.id()][tick]\
                    )\
                )
           

    def test_call_out_agent(self):
        ticks_count = 10


        right_time = {
            'terra':    (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
            'missile':  (0.0, 0.3, 0.6, 0.9),
            'aircraft': (0.0, 0.4, 0.8),
            'bomb':     (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
            'rocket':   (0.0, 0.5, 1.0)
        }

        
        def out_agent(id, buffer):
            right_ticks = right_time[id]
            ticks = buffer['t,c']
            n_ticks = len(ticks)
            for tick in range(n_ticks):
                self.assertTrue(\
                    is_equals(\
                        ticks[tick],\
                        right_ticks[tick]\
                    )\
                )


        for tick in range(ticks_count):
            self.terra.do_step()
        for object in self.objects:
            object.call_out_agent(out_agent)