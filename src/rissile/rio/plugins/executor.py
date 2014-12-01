# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$Nov 24, 2014 10:54:30 PM$"

from PyQt4 import QtCore


from PyQt4.QtCore import QThread
class _ProcessGenerator(QThread):
    """
    """
    finished_after_all_work = QtCore.pyqtSignal()
    def __init__(self, plugin, 
                 generator, parent):
        QThread.__init__(self, parent)
        self._plugin = plugin
        self._generator = generator
        
    def run(self):
        from multiprocessing import Pool, cpu_count
        self._pool = Pool(processes=cpu_count())
        self._pool.map(self._plugin(), self._generator)
        self._pool.close()
        self._pool.join()
        self.finished_after_all_work.emit()
    
    def stop(self):
        self._pool.terminate()
        self._pool.join()
        

class Executor(QtCore.QObject):
    """
    """
    start_running = QtCore.pyqtSignal()
    stop_running = QtCore.pyqtSignal()
    
    def __init__(self, log, generator, parent):
        QtCore.QObject.__init__(self, parent)
        self._log = log
        self._generator = generator
        self._plugin = None
        self._process = None
        
    def set_plugin(self, plugin):
        self._plugin = plugin
        
    def run(self):
        if self._has_active_plugin():
            self._try_start_new_process()
        else:
            self._say_that_plugin_was_not_set()
    
    def stop(self):
        if self._has_active_process():
            self._process.terminate()
            self._say_that_process_was_broken()
            self._process.wait()
            self._process = None
            self.stop_running.emit()
        
    def _process_ended_after_full_work(self):
        self.stop_running.emit()
        self._say_that_process_finished()
        self._process = None
        
    def _try_start_new_process(self):
        if self._has_active_process():
            self._say_that_process_is_running()
        else:
            self._say_that_process_started()
            self.start_running.emit()
            self._process = _ProcessGenerator(self._plugin.Plugin, self._generator(), self)
            self._process.finished_after_all_work.connect(self._process_ended_after_full_work)
            self._process.start()
        
    def _has_active_plugin(self):
        return self._plugin is not None
    
    def _has_active_process(self):
        return self._process is not None
    
    def _say_that_plugin_was_not_set(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'Any plugin wasn\'t set.')
        self._log.write_important_info(important_info)
    
    def _say_that_process_started(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'The process started.')
        self._log.write_important_info(important_info)
        
    def _say_that_process_is_running(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'The process is running now.')
        self._log.write_important_info(important_info)
        
    def _say_that_process_finished(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'All work was done.')
        self._log.write_important_info(important_info)
    
    def _say_that_process_was_broken(self):
        important_info = QtCore.QCoreApplication.translate('rio', 'The process was broken by you.')
        self._log.write_important_info(important_info)
    

        
        
        
        
