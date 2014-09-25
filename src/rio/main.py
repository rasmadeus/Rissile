# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$23.06.2014 9:03:52$"


from PyQt4 import QtGui, QtCore
from rio import view
import sys
from rio.rissile_model_factory import RissileModels

def create_test_rissile_models(rissile_models):
    from stone.stone import FlyingStone
    rissile_models.create_group('test models', QtCore.QObject().tr('Test models'))
    rissile_models.append('test models', QtCore.QObject().tr('Stone'), FlyingStone)
    rissile_models.append('test models', QtCore.QObject().tr('Stone two'), FlyingStone)

def main():
    rio = QtGui.QApplication(sys.argv)
    rissile_models = RissileModels()
    create_test_rissile_models(rissile_models)
    firstFace = view.View(rissile_models)
    firstFace.show()
    sys.exit(rio.exec_())

    
if __name__ == "__main__":
    main()