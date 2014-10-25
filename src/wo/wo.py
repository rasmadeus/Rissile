# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$18.10.2014 20:39:34$"

class WorldObject:
    """    
    """
    def __init__(self, id, alias):
        self._id = id
        self._alias = alias        

    def id(self):
        return self._id
    
    def alias(self):
        return self._alias

    def default_state(self):
        pass
    
    def run(self):
        pass
    
    def call(self, out_agent):
        pass