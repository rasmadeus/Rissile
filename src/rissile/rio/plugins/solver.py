# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$Nov 24, 2014 10:54:30 PM$"

from PyQt4 import QtCore


class _PluginSolver(QtCore.QThread):
    """
    """
    finished_after_all_work = QtCore.pyqtSignal()
    
    def __init__(self, plugin_class, initial_states, parent):
        QtCore.QThread.__init__(self, parent)
        self._plugin_class = plugin_class
        self._initial_states = initial_states
        
    def run(self):
        from multiprocessing import Pool, cpu_count
        self._pool = Pool(processes=cpu_count())
        self._pool.map(self._plugin_class(), self._initial_states)
        self._pool.close()
        self._pool.join()
        self.finished_after_all_work.emit()
    
    def stop(self):
        self._pool.close()
        self._pool.terminate()
        self._pool.join()
        

class PluginExecutor(QtCore.QObject):
    """
    """
    start_running = QtCore.pyqtSignal()
    stop_running = QtCore.pyqtSignal()
    
    def __init__(self, log, generator, parent):
        QtCore.QObject.__init__(self, parent)
        self._log = log
        self._generator = generator
        self._plugin_module = None
        self._plugin_solver = None
        
    def set_plugin_module(self, plugin_module):
        self._plugin_module = plugin_module
        
    def run(self):        
        if self._has_active_plugin():
            self._try_start_plugin_solving()
        else:
            self._say_that_plugin_was_not_set()
    
    def stop(self):
        if self._plugin_solver_is_active():
            self._plugin_solver.stop()
            self._plugin_solver = None
            self._say_that_process_was_broken()
            self.stop_running.emit()
        
    def _plugin_solver_have_done_all_work(self):
        self.stop_running.emit()
        self._say_that_process_finished()
        self._plugin_solver = None
        
    def _try_start_plugin_solving(self):
        if self._plugin_solver_is_active():
            self._say_that_process_is_running()
        else:
            self._start_plugin_solving()
        
    def _start_plugin_solving(self):
        self._say_that_process_started()
        self.start_running.emit()
        self._plugin_solver = _PluginSolver(self._plugin_module.Plugin, self._generator(), self)
        self._plugin_solver.finished_after_all_work.connect(self._plugin_solver_have_done_all_work)
        self._plugin_solver.start()
        
    def _has_active_plugin(self):
        return self._plugin_module is not None
    
    def _plugin_solver_is_active(self):
        return self._plugin_solver is not None
    
    def _say_that_plugin_was_not_set(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'Any plugin wasn\'t set.')
        self._log.important_info(important_info)
    
    def _say_that_process_started(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'The process started.')
        self._log.important_info(important_info)
        
    def _say_that_process_is_running(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'The process is running now.')
        self._log.important_info(important_info)
        
    def _say_that_process_finished(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'All work was done.')
        self._log.important_info(important_info)
    
    def _say_that_process_was_broken(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'The process was broken by you.')
        self._log.important_info(important_info)

        
        
        
        
