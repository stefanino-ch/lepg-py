"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""


class ColorDefinition:
    """
    :class: holds all special color definitions used across the GUI
    """
    valNotUsed = '#A4C4CF'
    ''':attr: Background color for cells not used.'''

    valAcceptable = '#c4df9b'
    ''':attr: Background color for cells containing acceptable values.'''

    valIntermediate = '#fff79a'
    ''':attr: Background color for cells containing values where it is not a 100% if they are ok.'''

    valInvalid = '#f6989d'
    ''':attr: Background color for cells containing invalid values.'''
