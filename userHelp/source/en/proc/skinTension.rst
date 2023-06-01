 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

------------
Skin tension
------------
In the *Skin tension* window you can define the parameters from the 5th section of the lep file.

.. image:: /images/proc/skinTension-en.png
   :width: 602
   :height: 286
   
Raw data::

	*************************************************************
	*           5. SKIN TENSION                                 *
	*************************************************************
	Extrados
	0.		0.	0.		0.
	7.5		1.3	10.		1.33
	15.		2.5	20.		2.5
	80.		2.5	80.		2.5
	90.		1.33	90.		1.33
	100.		0.0	100.		0.
	0.0114
	1000	1.0

The tension of the top surface and lower surface panels is achieved by creating tapers in the panels. The program allows you to define "over-wides" in 6 points along the edge of the panels. The transition between basis points of overwide is linear. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S05_skintension_p.jpg

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
The background here is to deal with the extension of the canvas. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S05_Ripstop_elasticity.jpg

In case of doubt put the default value of **0.0114**

Num Points and Coeff
--------------------
There are two different inperpretations of these parameters. Recommended for all designs is the setup described below. 

Set the parameters of the line to the values:

**1000     1.0**

First number **"1000"** is only a convention than signifies force the program to use maximal precision, reformating panels to achieve accuraccy better than 0.1 mm (lengths differences beetween rib and panels located at left and right).

Second number is a coefficient between 0.0 and 1.0 that sets the intensity of the correction. If coefficient is set to "0.0" then no correction applies. If the coefficient is set to **"1.0"** the accuracy is maximal, aprox < 0.01 mm.


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.5" target="_blank">Laboratori d'envol website</a>
