 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

--------------
2D DXF options
--------------
With the *2D DXF* options you define the colors for the different lines in the final drawings.

.. image:: /images/proc/twoDDxf-en.png
   :width: 350
   :height: 286

Raw data::

	*******************************************************
	*       24. GENERAL 2D DXF OPTIONS
	*******************************************************
	1
	A_lines_color   1     red
	B_lines_color   30    orange
	C_lines_color   3     green
	D_lines_color   4     cyan
	E_lines_color   6     magenta
	F_lines_color   5     blue

Type
----
*2D DXF options* is an **optional section**. 

If you do not want to define/ use these parameters set the Type to **Defaults**.

Line name
---------
The line names are fix and must be entered as shown below. 

* A_lines_color
* B_lines_color
* C_lines_color
* D_lines_color
* E_lines_color
* F_lines_color

Color code
----------
Usual color index numbers for CAD systems:
1= red, 2=yellow, 3=green, 4=cyan, 5=blue, 6=magenta 7=white 8=dark grey 9= grey,... up to 255 depending on your color palette. 

It is preferable not to use colors with more than two digits.

Color name
----------
A free description of the color you have setup. 


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.24" target="_blank">Laboratori d'envol website</a>
