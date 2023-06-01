 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

-----------------
Airfoil thickness
-----------------
Coefficients of amplification or reduction of the thickness of the cells. 
Normally defined as "1.0", or "0.0" in the wingtip.

.. image:: /images/proc/airfoilThickness-en.png
   :width: 350
   :height: 286
   
Raw data::

	*******************************************************
	*       30. AIRFOIL THICKNESS MODIFICATION
	*******************************************************
	1
	1    1.0
	2    1.0
	3    1.0
	4    1.0
	5    1.0
	6    1.0
	7    1.0
	8    1.0
	9    1.0
	10   1.0
	11   1.0
	12   1.0
	13   1.0
	14   0.0

Type
----
*Airfoil thickness* is an **optional section**. 

If you do not want to define/ use these parameters set the Type to **None**.

Rib num
-------
Rib num for which the coefficient is defined.

The lines are configured automatically and based on **Number of Ribs** in the *Basic data** window. 

Coef
----
Coefficient describing the thickness modification

**0.0**: thickness equals 0 (typical for wingtip)

**1.0**: thickness equally to definition in profile file

**>1**: increased thickness compared to the definition in the profile file


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.30" target="_blank">Laboratori d'envol website</a>
