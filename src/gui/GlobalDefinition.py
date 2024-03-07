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
    WingNameString = BrandNameString =\
        DxfReferenceLayerName = TwoDDxfColorDesc = ThreeDDxfColorDesc = "^[a-zA-Z0-9_.\-\s\']*$"
    AirfoilsNameString = "(.|\s)*\S(.|\s)*"
    ParaTyp = "(.|\s)*\S(.|\s)*"
    ThreeDShapingPrintName = "^(Inter3D|Ovali3D|tesse3D|exteDXF|exteSTL)"
    DxfLayerName = "^(general|line-external|cutexternal|line-sewing|points|circles|triangles|square|text|reference|notes)"
    MarksTypesName = "^(typepoint|typepoint2|typepoint3|typevent|typetab|typejonc|typeref|type8|type9|type10)"
    TwoDDxfLayerNames = ThreeDDxfLayerNames = "^(A_lines_color|B_lines_color|C_lines_color|D_lines_color|E_lines_color|F_lines_color)"
    ThreeDDxfLayerNamesPlus = "^(Extrados|Vents|Intrados)"
    LinesCharLineForm = "^(r|c)"
    LinesCharLineLabel = LinesCharMatType = "[a-zA-Z0-9_.\-\']{0,15}$"     # 15 characters no whitespace
    LinesCharLoopType = "^(s|p)"

class ValidationValues:
    MaxNumCells = MaxNumRibs = 100
    WingSpanMax_cm = 20000
    HalfWingSpanMax_cm = WingSpanMax_cm/ 2

    WingChordMax_cm = 10000

    WingChordMin_perc = 0
    WingChordMax_perc = 100

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
        # Globals
        MinDxfColorNum = 0
        MaxDxfColorNum = 255

        # 1: Basic data
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

        # 2: Airfoils
        DisplacementMin_cm = 0
        DisplacementMax_cm = 100

        RelativeWeightMin = 0
        RelativeWeightMax = 100

        # 3: Anchors
        NumAnchorsMin = 2   # At least two anchors are needed to get a flying wing
        NumAnchorsMax = 5   # There are five anchors for the main lines (plus one for the brakes

        AnchorsNumMin = 1   # Anchors are numbered from 1 to
        AnchorsNumMax = 6   # this includes the brake anchor as well

        # 4: Rib Holes
        RibHolesOpt1Min = 0
        RibHolesOpt1Max = 50

        # 5: Skin tension
        StrainMiniRibsMin = 0
        StrainMiniRibsMax = 1
        NumPointsMin = 0
        NumPointsMax = 1000
        SkinTensionCoefMin = 0
        SkinTensionCoefMax = 1
        SkinTensionAddWidthMin = 0
        SkinTensionAddWidthMax = 100

        # 6: Sewing Allowances
        MinSewingAllowance_mm = 0
        MaxSewingAllowance_mm = 100

        # 7: Sewing Marcage
        MinMarksSpacing_cm = 0
        MaxMarksSpacing_cm = 50
        MinMarksPointRadius_cm = 0
        MaxMarksPointRadius_cm = 50
        MinMarksDisplacement_cm = 0
        MaxMarksDisplacement_cm = 50

        # 8: Global AoA
        FinesseMin_deg = 0
        FinesseMax_deg = 45
        RisersBasicLengthMin_cm = 0
        RisersBasicLengthMax_cm = 100
        LinesBasicLengthMin_cm = 0
        LinesBasicLengthMax_cm = 1500
        KarabinersSeparationMin_cm = 0
        KarabinersSeparationMax_cm = 100

        # 9: Lines
        LinesControlParamMin = 0
        LinesControlParamMax = 3
        NumLineLevelsMin = 0
        NumLineLevelsMax = 4
        LineOrderNumMin = 0
        LineOrderNumMax = 50

        # 10: Brakes
        BrakeLengthMin_cm = 0
        BrakeLengthMax_cm = LinesBasicLengthMax_cm + 2
        NumBrakeLevelsMin = 0
        NumBrakeLevelsMax = 4
        BrakeOrderNumMin = 0
        BrakeOrderNumMax = 50
        BrakeSParamMin = 0
        BrakeSParamMax = 100
        BrakeDeltaLengthMin_cm = -100
        BrakeDeltaLengthMax_cm = 100

        # 11: Ramification
        RamificationLengthMin_cm = 0
        RamificationLengthMax_cm = LinesBasicLengthMax_cm

        # 15/ 16 Colors
        MaxNumColorLines = 100

        # 17: Additional Rib Points
        MaxNumAddRibPointLines = 100

        # 18: Elastic lines correction
        MinInFlightLoad_kg = 0
        MaxInFlightLoad_kg = 250
        LoadDistrMin_perc = 0
        LoadDistrMax_perc = 0
        LineDeformationMin = 0
        LineDeformationMax = 1

        # 20: Marks types
        MinMarksForm_num = 1
        MaxMarksForm_num = 3
        MinMarksFormParam = 0
        MaxMarksFormParam = 100

        # 21: Joncs
        MaxJoncsDefinitions = 50
        MinJoncsDeflectionPower = 0
        MaxJoncsDeflectionPower = 10
        MinJoncsSParam_mm = 0
        MaxJoncsSParam_mm = 1000

        # 24: 2D DXF Layer names
        # 25: 3D DXF Layer names

        # 26: Glue vents
        MinGlueVentParamNum = -6
        MaxGlueVentParamNum = 6

        # 27: Special wingtip
        MinSpecWingtipAngle_deg = -60
        MaxSpecWingtipAngle_deg = 60

        # 28: Calage variation
        MinCalageVarAngle_deg = -45
        MaxCalageVarAngle_deg = 45
        MinCalageVarCalcSteps_num = 0
        MaxCalageVarCalcSteps_num = 30

        # 29: 3D shaping
        Min3DShapingDepth_coef = -1
        Max3DShapingDepth_coef = 1

        # 30: Airfoil Thickness
        MinAirfoilThickness_coef = 0
        MaxAirfoilThickness_coef = 10

        # 32: Parts Separation
        MinPartsSep_coef = 0
        MaxParsSep_coef = 3

        # 33: Detailed Risers
        DetRisersMinLength_cm = 0
        DetRisersMaxLength_cm = 100

        # 34: Lines Characteristics
        LinesCharTypeMax_num = 99
        LinesCharMinDiam = 0.1
        LinesCharMaxDiam = 10
        LinesCharMinBreakStr = 1
        LinesCharMaxBreakStr = 10000
        LinesCharMinWeightPerM = 0.01
        LinesCharMaxWeightPerM = 100
        LinesCharMinLoopLength_cm = 0.0
        LinesCharMaxLoopLength_cm = 100

        # 35: SOLVE EQUILIBRIUM EQUATIONS
        SolveEquEqu_g_min = 9.05
        SolveEquEqu_g_max = 10
        SolveEquEqu_ro_min = 1
        SolveEquEqu_ro_max = 1.5
        SolveEquEqu_mu_min = 10
        SolveEquEqu_mu_max = 30
        SolveEquEqu_V_min = 5
        SolveEquEqu_V_max = 20
        SolveEquEqu_cl_min = 0
        SolveEquEqu_cl_max = 2
        SolveEquEqu_cle_min = 0
        SolveEquEqu_cle_max = 2
        SolveEquEqu_Cd_min = 0
        SolveEquEqu_Cd_max = 2
        SolveEquEqu_cde_min = 0
        SolveEquEqu_cde_max = 2
        SolveEquEqu_cm_min = 0
        SolveEquEqu_cm_max = 2
        SolveEquEqu_Spilot_min = 0.2
        SolveEquEqu_Spilot_max = 2
        SolveEquEqu_Cdpilot_min = 0
        SolveEquEqu_Cdpilot_max = 2
        SolveEquEqu_Mw_min = 0
        SolveEquEqu_Mw_max = 10
        SolveEquEqu_Mp_min = 50
        SolveEquEqu_Mp_max = 250
        SolveEquEqu_Pmc_min = 0
        SolveEquEqu_Pmc_max = 1
        SolveEquEqu_Mql_min = 0
        SolveEquEqu_Mql_max = 500
        SolveEquEqu_Ycp_min = 0
        SolveEquEqu_Ycp_max = 5000      # Keep in sync with ValidationValues.WingZMax_cm
        SolveEquEqu_Zcp_min = 0
        SolveEquEqu_Zcp_max = 5000      # Keep in sync with ValidationValues.WingZMax_cm
