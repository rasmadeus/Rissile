# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$23.06.2014 9:03:52$"


def main():
    from PyQt4 import QtGui
    from rissile.rio.view import View
    import sys

    rio_app = QtGui.QApplication(sys.argv)
    firstFace = View()
    firstFace.show()
    sys.exit(rio_app.exec_())

    
if __name__ == "__main__":
    main()