"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""


class BackgroundColorDefinition:
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


class BackgroundHighlight:
    BackgroundHighlightActive = 150
    BackgroundHighlightInactive = 100


class Regex:
    WingNameString = BrandNameString = "^[a-zA-Z0-9_.\-\s\']*$"

    ParaTyp = "(.|\s)*\S(.|\s)*"


class ValidationValues:
    MaxNumCells = MaxNumRibs = 100
    WingSpanMax_cm = 20000
    HalfWingSpanMax_cm = WingSpanMax_cm/ 2
    WingChordMax_cm = 10000
    WingZMax_cm = 5000



    class PreProc:
        cZeroOneMax = cZeroTwoMax = 100
        exOneMax = exTwoMax = 100

        cZeroMin = -10
        cZeroMax = 10

        yZeroMin = 0
        yZeroMax = 100

        expMin = 0
        expMax = 10

        cOneMin = 0
        cOneMax = 100

        aMax_deg = 120

    class Proc:
        # Basic data
        ScaleMin = 0
        ScaleMax = 50

        AlphaMaxTipMin = AlphaMaxCentMin = -10
        AlphaMaxTipMax = AlphaMaxCentMax = 10

        RibVerticalAngleMin_deg = -105  # Beta
        RibVerticalAngleMax_deg = 105   # Beta

        RibRotationPointMin_chord = 0
        RibRotationPointMax_chord = 100

        WashinMin = RotZColMin = -45
        WashinMax = RotZColMax = 45