'''
Created on 26.12.2019

@author: User
'''

from PyQt5.QtCore import QObject

class Singleton(type(QObject), type):
    def __init__(cls, name, bases, dict):  # @NoSelf @ReservedAssignment
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):  # @NoSelf
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance