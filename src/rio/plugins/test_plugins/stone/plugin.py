# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$25.10.2014 19:26:18$"

NAME = 'Stone'
SHORT_DESCRIPTION = 'This is the simple model of flying stone.'

from rio import plugins

class Plugin(plugins.plugins.Plugin):
    """    
    """
    def get_default_state(self):
        return {
            'angle_yaw': 0.0,
            'angle_pitch': 45.0,
            'vx0': 10,
            'vy0': 10,
            'vz0': 0
        }
        