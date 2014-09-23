# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$25.06.2014 8:30:39$"


import stone
from PyQt4 import QtCore
from rio.params.item import Root


class Model(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self._root = Root('root', None)


    def restore_from_params(self, params):
        """
        Строит иерархию self в соответствии с params.

        :params: набор свойств для радактирования.
        :type params: dict(str: int | bool | float | dict)
        """
        self._root.restore_from_params(params)
        self.reset()


    def generator(self):
        """
        :return: генератор исходных данных, в соответствии с иерархией self.
        """
        return self._root.generator()


    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        return index.internalPointer().show(index.column(), role)


    def flags(self, index):
        if not index.isValid(): return 0
        return index.internalPointer().flags(index.column())


    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent): return QtCore.QModelIndex()
        parent_item = parent.internalPointer() if parent.isValid() else self._root
        child_item = parent_item.part(row)
        return QtCore.QModelIndex() if child_item == 0 else self.createIndex(row, column, child_item)


    def parent(self, index):
        if not index.isValid(): return 0
        child_item = index.internalPointer()
        parent_item = child_item.owner()
        if parent_item is self._root: return QtCore.QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)


    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0: return 0
        parent_item = parent.internalPointer() if parent.isValid() else self._root
        return parent_item.parts_count()


    def columnCount(self, parent=QtCore.QModelIndex()):
        item = parent.internalPointer() if parent.isValid() else self._root
        return item.column_count()


    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return (u'id', u'value')[section]
        return QtCore.QVariant()


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid() or role != QtCore.Qt.EditRole: return False
        item = index.internalPointer()
        self.beginRemoveRows(index, 0, item.parts_count())
        item.set_value(value)
        self.endRemoveRows()
        return True