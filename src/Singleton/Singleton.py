'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''

from PyQt5.QtCore import QObject

class Singleton(type(QObject), type):
    '''
    :class: Parent class used to build the individial singletons across the program. 
    '''
    def __init__(cls, name, bases, dict):  # @NoSelf @ReservedAssignment
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):  # @NoSelf
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance