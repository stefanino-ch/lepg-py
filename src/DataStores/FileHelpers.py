'''
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
'''
import logging
import re

class FileHelpers(object):
    '''
    classdocs
    '''
    # TODO :doc
    
    __className = 'FileHelpers'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def remTabSpace(self, line):
        '''
        :method: Deletes all leaing and trailing edges from a string
        :param Line: The string to be cleaned
        :returns: cleaned string 
        '''
        #logging.debug(self.__className+'.remTabSpace')
        value = re.sub(r'^\s+|\s+$', '', line ) 
        return value
    
    def remTabSpaceQuot(self, line):
        '''
        :method: Removes from a string all leading, trailing spaces tabs and quotations
        :param Line: The string to be cleaned
        :returns: cleaned string 
        '''
        #logging.debug(self.__className+'.remTabSpaceQuot')
        line = self.remTabSpace(line)
        line = re.sub(r'^\"+|\"+$', '', line )
        return line
    
    def splitLine(self, line):
        '''
        :method: Splits lines with multiple values into a list of values delimiters could be spaces and tabs
        :param line: The line to be split
        :returns: a list of values 
        '''
        #logging.debug(self.__className+'.splitLine')
        line = self.remTabSpace(line) # remove leadind and trailing waste
        values = re.split(r'[\t\s]\s*', line)
        return values
    
    def chkNum(self, val, ret=0):
        '''
        :method: Checks if a value is integer, float or a string containing a numerical value
        :param val: The value to check
        :param ret: Optional parameter defining what must be returned if val is not numerical
        :returns: If val is numerical: val, else  0 or ret 
        '''
        if isinstance(val, int) or isinstance(val, float):
            return val
        elif val.isnumeric():
            return val
        else:
            return ret
        
    def chkStr(self, val, ret='x'):
        '''
        :method: Checks if a value is string and the lentth is > 0
        :param val: The value to check
        :param ret: Optional parameter defining what must be returned if val is not string or empty
        :returns: If val is non empty string: val, else  x or ret 
        '''
        if isinstance(val, str) and len(val)>0:
            return val
        else:
            return ret