 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------------------------
Colors lower sail: old style
----------------------------
If you want to use different colors in the lower sail you can configure the settings in this window.

*Colors lower sail* does use the same definitions as *Colors upper sail*. 
:ref:`A programming example you can find here<extrados_colors_en>`

.. image:: /images/proc/intradosColors-en.png
   :width: 403
   :height: 286

Raw data::

	*****************************************************
	*	16. Intrados colors
	*****************************************************
	3
	1   1
	1   40.1   0.
	2   1
	1   20.15   0.
	3   1
	1   0.0   0.

Number of configs
-----------------
Colors lower sail is an **optional section**. 

If you do not want to define/ use these parameters set the **Number of configs** value to **0**.

Rib num
-------
The rib number for which you define the color marks.

Dist TE
-------
Distance from Trailing edge in [% chord] of the mark.

Sort by Order Num
-----------------
The button **Sort by Order Num** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen. 


---------------------------------------
Colors upper sail: Type 2 (since V3.24)
---------------------------------------
.. image:: /images/proc/extradosColors-t2-en.png
   :width: 403
   :height: 286

Raw data::

	*****************************************************
	*	16. Intrados colors
	*****************************************************
    -2
    3
    2    1
    1    40.1    20.15    10.  0.
    3    1
    1    20.15    0.00    10.  0.
    4    3
    1    0.0     15.0    10.  0.
    2    15.0    30.0    10.  0.
    3    50.0    60.0    10.  0.

Example:
 - Panels 2,3,4 with cuts
 - Panel 2 and 3 with 1 cut each
 - Panel 4 with 3 cuts

Number of configs
-----------------
Colors lower sail is an **optional section**.

If you do not want to define/ use these parameters set the **Number of configs** value to **0**.

Rib num
-------
The rib number for which you define the color marks.

Dist TE
-------
Left side of the cell: distance of the mark from Trailing edge in [% chord].

Dist TE right
-------------
Right side of the cell: distance of the mark from Trailing edge in [% chord].

Seam
----
Seam width in [mm].

Sort by Order Num
-----------------
The button **Sort by Order Num** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen.

**Note:** When the wing has an odd number of panels (center panel of nonzero width),
the cut to the left of the center panel (panel 1) is defined exactly on the wing's axis of symmetry,
for make symmetrical designs possible.



A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.16" target="_blank">Laboratori d'envol website</a>
