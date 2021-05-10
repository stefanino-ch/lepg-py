 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------------
New skin tension
----------------
In the New skin tension window you can define the parameters from the 31st section of the lep file.
New skin tension does follow the same definitions as the original skin tension with the exception you can define more than 6 configuration lines. 

.. image:: /images/proc/newSkinTension-en.png
   :width: 602
   :height: 286
   
Raw data::

	*******************************************************
	*       31. NEW SKIN TENSION MODULE
	*******************************************************
	1
	1
	* Skin tension group number "1" from rib 1 to 14, 6 points, type "1"
	1      	1	14	6	1
	1	0.		0.1	0.		0.
	2	7.5		1.3	10.		1.33
	3	15.		2.5	20.		2.5
	4	80.		2.5	80.		2.5
	5	90.		1.33	90.		1.33
	6	100.		0.0	100.		0.1

The tension of the top surface and lower surface panels is achieved by creating tapers in the panels. The program allows you to define "over-wides" in 6 points along the edge of the panels. The transition between basis points of overwide is linear. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S05_skintension_p.jpg

Number of groups
----------------
In a group you can bundle the settings for a group of ribs. For all ribs within the same group the same settings apply. 
New skin tension is an optional section. If you do not want to define/ use these parameters set the Number of Groups value to 0.

First rib
---------
Here you define the number of the first rib in the group for which the settings apply. 

Last rib
--------
Here you define the number of the last rib in the group for which the settings apply. 

Type
----
The only available calculation type at the moment is 1. 

Top dist LE
-----------
Distance from Leading Edge in [% chord]

Top widening
------------
Over widening in [% chord]

Bott dist TE
------------
Distance from Trailing Edge in [% chord]

Bott widening
-------------
Over widening in [% chord]

Strain mini ribs
----------------
New skin tension uses the same settings for Strain mini ribs as the original section does. Therefore you must define the correct values in the Skin Tension window!

The background here is to deal with the extension of the canvas. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S05_Ripstop_elasticity.jpg

In case of doubt put the default value of **0.0114**

Num Points and Coeff
--------------------
New skin tension uses the same settings for Num Points and Cooeff as the original section does. Therefore you must define the correct values in the Skin Tension window!

There are two different inperpretations of these parameters. Recommended for all designs is the setup described below. 

Set the parameters of the line to the values:

**1000     1.0**

First number **"1000"** is only a convention than signifies force the program to use maximal precision, reformating panels to achieve accuraccy better than 0.1 mm (lengths differences beetween rib and panels located at left and right).

Second number is a coefficient between 0.0 and 1.0 that sets the intensity of the correction. If coefficient is set to "0.0" then no correction applies. If the coefficient is set to **"1.0"** the accuracy is maximal, aprox < 0.01 mm.

Sort by Order Num
-----------------
The button **Sort by Order Num** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen. 

A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.31" target="_blank">Laboratori d'envol website</a>
