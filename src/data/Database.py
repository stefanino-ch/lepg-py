'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging

from PyQt5.QtSql import QSqlDatabase
from Singleton.Singleton import Singleton

class Database(QSqlDatabase, metaclass=Singleton):
    '''
    :class: Used to establish the connection to the internal database. 
        Implemented in a way that there is only one connection to the database opened at a time. 
    '''
    db = None

    def __init__(self, parent=None): # @UnusedVariable
        '''
        Constructor
        '''
        super().__init__()
        
    def openConnection(self):
        '''
        :metho: Opens a new connection if there is no one in place yet.
        '''
        if self.db is None:
            # open database
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName("lepgModel.sqlite")
            if not self.db.open():
                logging.error(self.__className+ '.__init__ cannot open db')
