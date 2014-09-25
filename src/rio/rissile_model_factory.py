# -*- coding: utf-8 -*-

__author__="K. Kulikov"
__date__ ="$24.09.2014 17:42:40$"

from PyQt4 import QtGui

class Aliasable:
    def __init__(self, alias):
        self._alias = alias
        
    def alias(self):
        return self._alias
    
    
class RissileModelMaker(Aliasable):
    def __init__(self, alias, maker):
        Aliasable.__init__(self, alias)
        self._maker = maker
        
    def maker(self):
        return self._maker
    
    
class RissileModelGroup(Aliasable):
    def __init__(self, alias):
        Aliasable.__init__(self, alias)
        self._group = []
        
    def append(self, model_name_alias, model_maker):
        self._group.append(RissileModelMaker(model_name_alias, model_maker))        
        
    def fill_actions(self, actions):
        for rissile_model_maker in self._group:
            action = QtGui.QAction(rissile_model_maker.alias(), actions)
            action.setData(rissile_model_maker.maker())
            actions.addAction(action)  
        
        
class RissileModels:
    def __init__(self):
        self._models_maker = {}
        
    def create_group(self, group_key, group_alias):
        self._models_maker[group_key] = RissileModelGroup(group_alias)
        
    def append(self, group_key, model_name_alias, model_maker):
        if group_key in self._models_maker:
            self._models_maker[group_key].append(model_name_alias, model_maker)
            
    def fill_menu(self, menu, action_processor):
        for models_maker in self._models_maker.values():
            submenu = menu.addMenu(models_maker.alias())
            actions = QtGui.QActionGroup(submenu)
            actions.triggered.connect(action_processor)
            models_maker.fill_actions(actions)
            submenu.addActions(actions.actions())
            
            
