# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$25.10.2014 19:26:18$"

NAME = 'Stone'
SHORT_DESCRIPTION = 'This is the simple model of flying stone.'

from rissile.rio.plugins import plugins

class Plugin(plugins.Plugin):
    """    
    """    
    def __init__(self):
        self._states = {'time,sec':[], 'x,m':[], 'y,m':[], 'vx,m/sec':[], 'vy,m/sec':[]}
        self._x = 0.0
        self._y = 0.0
        self._t = 0.0
        self._step = 0.01
        self._g = 9.81
        self.set_initial(self.get_default_state())
        self._save_current_state()

        
    def get_default_state(self):
        return {
            'v0x': 10.0,
            'v0y': 10.0,
        }
        
    def set_initial(self, state):
        self._vx = state['v0x']
        self._vy = state['v0y']
  
        
    def print_state(self):
        print('t={t}; x={x}; y={y}; vx={vx}; vy={vy}'.format(t=self._t, x=self._x, y=self._y, vx=self._vx, vy=self._vy))

    def _update_time(self):
        self._t += self._step

    def _update_vy(self):
        self._vy -= self._g * self._step
        
    def _update_x(self):
        self._x += self._vx * self._step
        
    def _update_y(self):
        self._y += self._vy * self._step - self._g * self._step * self._step / 2        
    
    def must_live_until(self):
        return self._y >= 0.0
    
    def _save_current_state(self):
        self._states['time,sec'].append(self._t)
        self._states['x,m'].append(self._x)
        self._states['y,m'].append(self._y)
        self._states['vx,m/sec'].append(self._vx)
        self._states['vy,m/sec'].append(self._vy)

    
    def save_states(self):
        from random import randrange
        from time import gmtime, strftime
        out_dir_path = 'c:\\Users\\Kulikov\\Documents\\temp\\1\\'
        file_name = strftime("%H_%M_%S", gmtime(randrange(1000))) + '.txt'
        path_to_file = out_dir_path + file_name
        with open(path_to_file, 'w') as out_file:
            for key in self._states.keys():
                out_file.write(key+'\t')
            out_file.write('\n')
            size = len(self._states['time,sec'])
            for i in range(size):
                for key in self._states.keys():
                    out_file.write(str(self._states[key][i]) + '\t')
                out_file.write('\n')
                
    
    def _run(self):
        self._update_time()
        self._update_vy()
        self._update_x()
        self._update_y()
        self._save_current_state()
    
        
    def run(self):
        plugins.Plugin.run(self)
        try:
            self.save_states()
        except Exception as e:
            print(e)
    

        