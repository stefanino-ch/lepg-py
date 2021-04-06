'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtSql import QSqlDatabase
from Singleton.Singleton import Singleton

class Database(QSqlDatabase, metaclass=Singleton):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
    def openConnection(self):
                # open database
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("lepgModel.sqlite")
        if not self.db.open():
            logging.error(self.__className+ '.__init__ cannot open db')
