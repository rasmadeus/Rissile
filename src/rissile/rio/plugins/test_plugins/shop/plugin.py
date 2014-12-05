# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$25.10.2014 19:25:52$"


NAME = 'Shop'
SHORT_DESCRIPTION = 'This is imitation a simple shop\'s activity'

from rissile.rio.plugins import plugins

class Plugin(plugins.Plugin):
    """
    """
    def _run(self):
        print('I am a shop')