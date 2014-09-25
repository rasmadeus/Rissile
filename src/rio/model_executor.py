# -*- coding: utf-8 -*-

__author__="K. Kulikov"
__date__ ="$24.09.2014 17:52:35$"

class RissileModelExecutor:
    def __init__(self, logger):
        self._logger = logger    
    
    def set_model_creator(self, model_creator):
        self._model_creator = model_creator
        
    def set_generator(self, generator):
        self._generator = generator
        
    def start(self):
        pass
    
    def stop(self):
        pass