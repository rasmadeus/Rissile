# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$24.06.2014 15:42:21$"


from PyQt4 import QtCore, QtGui


class Item:
    """
    Класс предоставляет интерфейс для организации иерархии свойств вида ключ: значение.
    """
    def __init__(self, name, owner=None):
        """
        :param name: идентификатор свойства.
        :type name: str.
        :param owner: владелей свойства.
        :type owner: Item.
        """
        def append_properties():
            self._name = name   # Идентификатор свойства.
            self._owner = owner # Владелец свойства.
            self._parts = []    # Составные части свойства.


        def add_part():
            """
            Метод добавляет self к составным частям владельца, если последний существует.
            """
            if owner is not None:
                owner._parts.append(self)


        append_properties()
        add_part()


    def clear_parts(self):
        """
        Метод удаляет все составные части объекта.
        """
        self._parts = []   

        
    def flags(self, column):
        """
        Первый столбец - идентификатор, не подлежит редактированию.
        Второй столбец редактировать дозволено в реализации по умолчанию.
        """
        if self.is_editable(column):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled
    
    def is_editable(self, column):
        return True if column == 1 else False


    def row(self):
        """
        self является составной частью своего владельца, если он есть.

        :return: индекс, под которым self следует в составе своего владельца.
        """
        if self._owner is None:
            return 0
        return self._owner._parts.index(self)


    def owner(self):
        """
        Владелец self.
        """
        return self._owner


    def parts_count(self):
        """
        Количество составных частей self.
        """
        return len(self._parts)


    def part(self, row):
        """
        Возвращает ссылку на свою часть.
        """
        return self._parts[row]


    def column_count(self):
        """
        Свойство описывается его идентификатором и значением. Поэтому возвращаем 2.
        """
        return 2
    

    def name(self):
        """
        Идентификатор свойства.
        """
        return self._name


    def show(self, column, role):
        """
        Функция предназначена для вызова из QAbstractItemModel, для отображения свойства на экране.
        Путём реализации соответствующих методов, вы можете настроить вид каждого конкретного свойства.
        """
        showman = {
            QtCore.Qt.DisplayRole: self._display_role,
            QtCore.Qt.FontRole: self._font_role
        }
        return showman.get(role, lambda column: QtCore.QVariant())(column)


    def delegate(self, parent=None):
        """
        Создавайте делегата здесь.
        """
        return QtGui.QItemDelegate(parent)        


    def _display_role(self, column):
        """
        Текстовое представление. В первом столбце всегда выводится идентификатор вершины.
        """
        return self._name if column == 0 else self._second_column_display_role()


    def _second_column_display_role(self):
        """
        Если вы хотите, чтобы во втором столбце представления выводились
        данные, отличные от представленных по умолчанию, перегружайте этот метод.
        """
        return self._value


    def _font_role(self, column):
        """
        :return: Шрифт текстового представления.
        :rtype: QFont()
        """
        font = QtGui.QFont()
        font.setPointSize(10)
        return font


class Value(Item):
    """
    Класс помимо идентификатора содержит значение, которое можно редактировать.
    """
    def __init__(self, name, owner=None):
        Item.__init__(self, name, owner)
        self._value = 0.0


    def value(self):
        """
        :return: self._value
        """
        return self._value


    def set_value(self, value):
        """
        В этом методе выполняйте установку значения.
        """
        pass


class ValueEditable(Value):
    """
    Класс позволяет редактировать значение.
    Всегда имеет владельца. Но владелец не всегда содржит self как составную часть.
    """
    def __init__(self, name, alias, owner):
        """
        :param alias: Параметр name используется как ключ для формирования структуры генерируемых значений, alias выводится на экран как расшифровка name.
        :type alias: str
        """
        Value.__init__(self, name, owner)
        self._alias = alias


    def usurp_owner(self):
        """
        Метод включает self в составные части владельца.
        """
        self._owner._parts.append(self)


    def set_value(self, value):
        """
        :type value: bool | str | int | float
        """
        self._value = value


    def _display_role(self, column):
        return self._alias if column == 0 else self._value


    def delegate(self, parent=None):
        """
        :return: делегата QDoubleSpinBox для редактирования значения.
        :rtype QtGui.QItemDelegate.
        """
        pass
    
class ValueFloatEditable(ValueEditable):
    def delegate(self, parent=None):
        class Delegate(QtGui.QItemDelegate):
            def __init__(self, parent=parent):
                QtGui.QItemDelegate.__init__(self, parent)


            def createEditor(self, parent, option, index):
                editor = QtGui.QDoubleSpinBox(parent)
                editor.setDecimals(10)
                editor.setMinimum(-1000000.0)
                editor.setMaximum(1000000.0)
                return editor


            def setEditorData(self, editor, index):
                editor.setValue(float(index.data().toString()))


            def setModelData(self, editor, model, index):
                model.setData(index, editor.value())

        return Delegate(parent)
    
class ValueRepeater(ValueEditable):
    def _font_role(self, column):
        font = ValueEditable._font_role(self, column)
        if column == 0:
            font.setBold(True)
        return font
    
    def delegate(self, parent=None):
        class Delegate(QtGui.QItemDelegate):
            def __init__(self, parent=parent):
                QtGui.QItemDelegate.__init__(self, parent)


            def createEditor(self, parent, option, index):
                editor = QtGui.QSpinBox(parent)
                editor.setMinimum(1)
                editor.setMaximum(1000000.0)
                return editor


            def setEditorData(self, editor, index):
                editor.setValue(int(index.data().toString()))


            def setModelData(self, editor, model, index):
                model.setData(index, editor.value())


        return Delegate(parent)


class ValueForGenerator(Value):
    """
    Класс-контейнер, организует интерфейс для редактирования исходных данных генераторов
    из пакета rissile.wo.data_generator
    """
    def __init__(self, get_id, item_type, owner):
        class Data:
            def __init__(self, owner):
                self._parts = self._create_parts(owner)
                self._generator = self._create_generator()


            def _create_parts(self, owner):
                return None


            def _create_generator(self):
                return None


            def name(self):
                return None


            def usurp_owner(self):
                for part in self._parts:
                    part.usurp_owner()


        class DataForConstGenerator(Data):
            def name(self):
                return QtCore.QCoreApplication.translate('rio', 'const value')


            def _create_parts(self, owner):
                return (
                    ValueFloatEditable('value', QtCore.QCoreApplication.translate('rio', 'value'), owner),
                )


            def _create_generator(self):
                from rissile.rio.params.params_generator import ValueConstGenerator
                return ValueConstGenerator


        class DataForRangeGenerator(Data):
            def name(self):
                return QtCore.QCoreApplication.translate('rio', 'interval')


            def _create_parts(self, owner):
                return (
                    ValueFloatEditable('begin', QtCore.QCoreApplication.translate('rio', 'start value'), owner),
                    ValueFloatEditable('right_border', QtCore.QCoreApplication.translate('rio', 'right border'), owner), 
                    ValueFloatEditable('step', QtCore.QCoreApplication.translate('rio', 'step'), owner)
                )


            def _create_generator(self):
                from rissile.rio.params.params_generator import ValueRangeGenerator
                return ValueRangeGenerator


        class DataForRandomGenerator(Data):
            def name(self):
                return QtCore.QCoreApplication.translate('rio', 'random value')


            def _create_parts(self, owner):
                return (
                    ValueFloatEditable('left_border', QtCore.QCoreApplication.translate('rio', 'left border'), owner),
                    ValueFloatEditable('right_border', QtCore.QCoreApplication.translate('rio', 'right border'), owner)
                )


            def _create_generator(self):
                from rissile.rio.params.params_generator import ValueRandomGenerator
                return ValueRandomGenerator


        def create_types():
            self._types = {
                'const generator': DataForConstGenerator(self),
                'range generator': DataForRangeGenerator(self),
                'random generator': DataForRandomGenerator(self)
            }


        Value.__init__(self, get_id, owner)
        create_types()
        self.change_type(item_type)


    def change_type(self, type_item):
        """
        Метод меняет части self в зависимости от типа.
        """
        self.clear_parts()
        self._type = type_item
        self._types[type_item].usurp_owner()


    def set_value(self, value):
        """
        Метод изменяет тип контейнера в части задания исходных данных для генератора.

        :param value: Идентификатор частей генератора - 'const generator' | 'random generator' | 'range generator'.
        :type value: QVarinat(QString())
        """
        self._value = str(value.toString())
        self.change_type(self._value)


    def _display_role(self, column):
        return self._name if column == 0 else self._types[self._type].name()


    def fill(self, wo_init_data_generator):
        """
        Метод заполняет переданный генератор значением, соответствующему self.

        :value wo_init_data_generator: Генератор значений для WorldObjectTest.
        :type wo_init_data_generator: rissile.wo._data_generator.WorldObjectTestDataGenerator
        """
        def params():
            """
            :return: параметры для инициализации генератора.
            :rtype: dict
            """
            params = {}
            for part in self._parts:
                params[part._name] = part._value
            return params

        generator_maker = self._types[self._type]._create_generator()
        wo_init_data_generator.set_value(generator_maker(self._name, params()))


    def delegate(self, parent=None):
        """
        :return: делагат QComboBox для редактирования значения.
        :rtype: QtGui.QItemDelegate
        """
        class Delegate(QtGui.QItemDelegate):
            def __init__(self, types, parent=parent):
                QtGui.QItemDelegate.__init__(self, parent)
                self._types = types


            def createEditor(self, parent, option, index):
                editor = QtGui.QComboBox(parent)
                for key, item in self._types.iteritems():
                    editor.addItem(item.name(), key)
                return editor


            def setEditorData(self, editor, index):
                key = index.internalPointer()._value
                for i in range(editor.count()):
                    item_data = editor.itemData(i)
                    if item_data == key:
                        editor.setCurrentIndex(i)
                        return


            def setModelData(self, editor, model, index):
                model.setData(index, QtCore.QVariant(editor.itemData(editor.currentIndex())))


        return Delegate(self._types, parent)


class Root(Item):
    """
    Класс является главой иерархии для Root или ValueForGenerator.
    """
    def _font_role(self, column):
        """
        :return: жирный шрифт, установленный по умолчанию.
        :rtype: QFont()
        """
        font = Item._font_role(self, column)
        font.setBold(True)
        return font
    
    def _second_column_display_role(self):
        """
        Значение контейнера не подлежит редактированию,
        поэтому возвращается пустая строка. Однако здесь можно,
        вывести краткий комментарий по назначению self.
        """
        return ''


    def restore_from_params(self, params):
        """
        Метод выстраивает иерархию с вершиной self в соответствии с данными params.

        :param params: Иерархичная структура, которую будет повторять self.
        :type params: dict
        """
        self.clear_parts()        
        for get_id, value in params.iteritems():
            if isinstance(value, dict):
                part = Root(get_id, self)
                part.restore_from_params(value)
            else:
                item = ValueForGenerator(get_id, 'const generator', self)
                item.part(0).set_value(value)
                
    def is_editable(self, column):
        return False
                
    def generator(self):
        """
        :return: генератор исходных данных, в соответствии с иерархией self.
        :rtype: rissile.wo.data_generator.ParamsGenerator
        """
        from rissile.rio.params.params_generator import ParamsGenerator
        wo_init_data_generator = ParamsGenerator(self._name)
        for part in self._parts:
            part.fill(wo_init_data_generator)
        return wo_init_data_generator


    def fill(self, wo_init_data_generator):
        """
        :param wo_init_data_generator: Генератор, к которому нужно добавить значения для генерирования, соответствующие self.
        :type wo_init_data_generator: rissile.wo.data_generator.ParamsGenerator
        """
        wo_init_data_generator.set_value(self.generator())
        
        
class RootRepeater(Item):
    
    def __init__(self, name, owner=None):
        Item.__init__(self, name, owner)
        self._repeater = ValueRepeater('number of params', QtCore.QCoreApplication.translate('rio', 'Number of params'), self)
        self._root = Root(name, self)            
       
    def restore_from_params(self, params):
        self._root.restore_from_params(params)        
        
    def set_value(self, value):
        self._repeater.set_value(value)    
        
    def value(self):
        return self._repeater.value()    
        
    def generator(self):
        from rissile.rio.params.params_generator import ParamsGenerator
        from rissile.rio.params.params_generator import ValueRangeGenerator
        wo_init_data_generator = ParamsGenerator(self._name)
        value_range_generator = ValueRangeGenerator('index', {'begin': 0, 'right_border': self._repeater.value() , 'step': 1})
        wo_init_data_generator.set_value(value_range_generator)
        wo_init_data_generator.set_value(self._root.generator())
        return wo_init_data_generator