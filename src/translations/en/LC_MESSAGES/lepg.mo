��    H      \  a   �            !  
   )     4  
   A     L     `     v     �     �     �     �     �     �               '     :     O     d     w     �     �     �     �     �     �                ,     B     X     n     �     �     �     �     �     �     	     	     2	     H	     ]	     p	     �	     �	     �	     �	     �	     �	     �	     
     
     )
     5
     H
     X
     h
     z
     �
     �
     �
     �
     �
     �
  
   �
  #   �
          )     @     Z  �  q     /  
   A     L  
   Y     d  A   w  *   �      �       6   $  6   [  <   �  <   �            -     N     e  *   u  !   �     �  $   �  )        1     O  "   g     �     �     �     �     �          2     P     m     �     �  !   �     �     �  �     #   �     �  F   �  &   /  ?   V  -   �  !   �  #   �     
     (  V   E  J   �  -   �  )     I   ?  
   �     �     �  -   �     �  �   	  0   �  #   �  .     /   :     j  =   �  8   �  #   �     "     >           (       9      =      H   2   C      /          A           <   4       D       B   '           :             -                 .      ?       ;              !   @   5         *          &                ,   3                   1         %       G      "       
   	   )              #       >          6   E       8   F   7   +          $       0    Displac Intake End Intake Start Open-close PreProc-CellNumDesc PreProc-DistrCoefDesc PreProc-LE-Type-Desc PreProc-LE-a1-Desc PreProc-LE-b1-Desc PreProc-LE-c01-Desc PreProc-LE-c02-Desc PreProc-LE-ex1-Desc PreProc-LE-ex2-Desc PreProc-LE-x1-Desc PreProc-LE-x2-Desc PreProc-LE-xm-Desc PreProc-NumCellsDesc PreProc-TE-Type-Desc PreProc-TE-a1-Desc PreProc-TE-b1-Desc PreProc-TE-c0-Desc PreProc-TE-exp-Desc PreProc-TE-x1-Desc PreProc-TE-xm-Desc PreProc-TE-y0-Desc PreProc-Vault-a1-Desc PreProc-Vault-b1-Desc PreProc-Vault-c1-Desc PreProc-Vault-r1-Desc PreProc-Vault-r2-Desc PreProc-Vault-r3-Desc PreProc-Vault-r4-Desc PreProc-Vault-ra1-Desc PreProc-Vault-ra2-Desc PreProc-Vault-ra3-Desc PreProc-Vault-ra4-Desc PreProc-Vault-x1-Desc PreProc-WidthDesc PreProc-WingNameDesc Proc-AirfoilNameDesc Proc-AlphaMaxCentDesc Proc-AlphaMaxTipDesc Proc-AlphaModeDesc Proc-BrandNameDesc Proc-DisplacDesc Proc-DrawScaleDesc Proc-IntakeEnDesc Proc-IntakeStartDesc Proc-NumCellsDesc Proc-NumRibsDesc Proc-OpenCloseDesc Proc-ParaParamDesc Proc-ParaTypeDesc Proc-RPDesc Proc-RelWeightDesc Proc-RibNumDesc Proc-WashinDesc Proc-WingNameDesc Proc-WingScaleDesc Proc-betaDesc Proc-rrwDesc Proc-xpDesc Proc-xribDesc Proc-yLEDesc Proc-yTEDesc Proc-zDesc edit_preProc_cellsDistr_description edit_preProc_data_description open_preProc_file_desc save_preProc_file_as_desc save_preProc_file_desc Project-Id-Version: lepg-py
PO-Revision-Date: 2021-05-07 10:10+0200
Last-Translator: Stefan Feuz
Language-Team: Stefan
Language: en
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
X-Generator: Poedit 2.4.3
Plural-Forms: nplurals=2; plural=(n != 1);
X-Poedit-Basepath: ../../..
X-Poedit-SourceCharset: UTF-8
X-Poedit-SearchPath-0: .
X-Poedit-SearchPathExcluded-0: userHelp
 vert Displacement Intake end Intake start Open close Number of the cell Coefficient which will reduce the cell width
towards the wing tip Currently there's only LE type 1 available Leading Edge horizontal semiaxis Leading Edge vertical semiaxis Leading Edge deflection coefficient 
for 1st curvature Leading Edge deflection coefficient 
for 2nd curvature Leading Edge deflection variation Degree  
for 1st curvature Leading Edge deflection variation Degree  
for 2nd curvature 1st curvature start leading edge 2nd curvature start leading edge Leading Edge half span Number of cells Currently there's only TE type 1 available Trailing Edge horizontal semiaxis Trailing Edge vertical semiaxis Trailing edge deflection coefficient Trailing Edge deflection variation Degree Curvature start trailing edge Trailing Edge half span Trailing edge wing chord reduction Semiaxis a (horizontal) Semiaxis b (vertical) Wing curvature point (vertical) Radius of 1st angular section Radius of 2nd angular section Radius of 3rd angular section Radius of 4th angular section Angle of 1st angular section Angle of 2nd angular section Angle of 3rd angular section Angle of 4th angular section Wing curvature point (horizontal) Width of the cell in cm The name of the wing Name of the file in which defines the profile of the rib.
This file must be saved prior the processing in the same
folder where the processor is saved. Washing angle in the
center airfoil Washing angle of the tip 0: manual Definition
1: proportional to chord
2: automatic center->tip Brand Name or the Name of the designer Vertical displacement of the rib in [cm]
Usually the value is 0 The drawing scale used during plan generation End of the air inlet in [% chord] Start of the air inlet in [% chord] Number of cells in the design Number of ribs in the design Defines the form of the cell left of the rib
"0" indicates closed-cell 
"1" open cell) 0: triangles in TE will be rotated 
1: triangles in TE will not be rotated ds: double skin
ss: single skin
pc: parachute Rotation point of the ribs
for the washin Relative weight of the chord, in relation to the load 
Value is usually 1 Rib number Washing angle of the rib The name of the wing Can be used to scale the whole desing at once Lateral angle of the rib Single Skin wings:
"0" Triangles will not be rotated
"1" Triangles will be rotated corresponding to profile
Double Skin Wings:
Value > 1 => Lenght of mini ribs in [% chord] Distance on x-axis
of the wing in its final form Distance on x-axis
of the flat wing Position on y-axis of the
leading edge (depth) Position on y-axis of the
trailing edge (depth) Position on z-axis 
(height) Opens the edit window for the cell distribution configuration Opens the window to edit name, LE, TE and vault settings Opens a datafile from local storage Saves data under a new name Saves data to local file 