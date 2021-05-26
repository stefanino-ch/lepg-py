 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

---------
Glue vent
---------
This window allows to automatically "glue" the air inlets (vents) into the panels of upper or lower sail or to make them standalone. 

The vents include sewing edges. 

The skin tension in the vent is linear and automatically corresponds to that defined at the points corresponding for upper and lower sail.

.. image:: /images/proc/glueVent-en.png
   :width: 350
   :height: 286
   
Raw data::

	*******************************************************
	*       26. GLUE VENTS
	*******************************************************
	1
	1   0
	2   0
	3   0
	4   0
	5   0
	6   0
	7   0
	8   0
	9   0
	10  0
	11   
	12  -2
	13  -1
	14  -1

Type
----
*Glue vent* is an **optional section**. 

If you do not want to define/ use these parameters set the Type to **Defaults**.

If **Type** is set to **User defined** lepg will create autmatically the needed configuration lines depending on number of cells and ribs configured in the *Basic data* window. 

Airfoil num
-----------
Number of the airfoil (cell) configured on this line. 

Vent param
----------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S26.jpg
   :width: 462
   :height: 653

**1** glue the vent to the upper sail (normally used in single skin paragliders)

**0** do not glue the vent anywhere (open air inlet). It is drawn apart to define with CAD special air intakes (circles, ellipses, ...)

**-1** glue the vent to the lower sail (usually means, closed cell)

**-2** diagonal vent 100% open on left, glued to lower sail

**-3** diagonal vent 100% open on right, glued to lower sail


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.26" target="_blank">Laboratori d'envol website</a>
