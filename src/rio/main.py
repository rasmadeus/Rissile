# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$23.06.2014 9:03:52$"


from PyQt4 import QtGui
from rio import view
import sys

def main():
    rio = QtGui.QApplication(sys.argv)
    firstFace = view.View()
    firstFace.show()
    sys.exit(rio.exec_())

    
if __name__ == "__main__":
    main()