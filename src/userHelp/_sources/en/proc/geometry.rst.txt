 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

--------
Geometry
--------
The Geometry window defines the second part of the first section in the lep file. 

.. image:: /images/proc/geometry-en.png
   :width: 458
   :height: 171
   
Raw data::

	* Rib geometric parameters
	* Rib	x-rib	  y-LE	  y-TE	    xp	      z	         beta	   RP	      Washin
	 1     24.37      0.18    309.24     24.36      0.46      2.16     33.33      0.00
	 2     72.86      1.60    308.49     72.71      4.08      6.48     33.33      0.00
	 3    120.88      4.44    307.00    120.18     11.21     10.59     33.33      0.00
	 4    168.18      8.68    304.79    166.31     21.64     14.90     33.33      0.00
	 5    214.54     14.30    301.85    210.67     35.08     18.81     33.33      0.00
	 6    259.73     21.30    298.21    252.79     51.40     23.70     33.33      0.00
	 7    303.50     29.77    293.87    292.02     70.79     28.88     33.33      0.00
	 8    345.46     41.26    288.87    327.84     92.61     33.84     33.33      0.00
	 9    385.16     56.00    283.16    359.89    116.02     38.37     33.33      0.00
	10    422.21     73.45    276.64    387.92    140.23     44.11     33.33      0.00
	11    456.31     93.04    269.45    410.61    165.64     52.52     33.33      0.00
	12    487.22    114.20    261.78    427.78    191.33     59.97     33.33      0.00
	13    514.81    136.38    253.80    438.47    216.67     74.82     33.33      0.00
	14    539.00    159.09    245.71    441.90    240.55     88.56     33.33      0.00

These parameters can not be defined without a previous drawing, preferably in a file of computer aided design CAD, in which the desired plan is drawn to an appropriate scale, form lobe in elevation, and inclination of the ribs. This drawing is one of the most basic and important design (pre-process).

It would be possible to generate this drawing by a geometric preprocessor to read basic data from the wing desired number of cells, separation, size, shape, edge and trailing by a few parameters defined to create elliptical shapes. This pre-processor has been implemented. If you want to go this way you will find the data edit and processing functionality in lepg under Pre-Prosessor. However doing the wing outline with the help of a CAD application will give you much more degrees of freedom in your design. b

There is a limitation of not being able to define airfoils in the center of symmetry. To remedy this situation can be defined a virtual central cell's with almost zero thickness. 

The graphic below provides an overview about the individual parameters

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S01_Definition.jpg
   :width: 400
   :height: 594
   
The 2nd last column defines the percentage to be taken into account if washing proportional to the chord (**"1"**) is selected in the Basic data window. 

The last column defines the torsion angle for each single rib. You have to specify these values if you select **Alpha mode** **"0"** in the Basic data window. 

The button **Sort by Rib Number** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the rib numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen. 

**ATTENTION** you have to order the lines in a way that the wing is defined from the middle to the tip. 


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.1" target="_blank">Laboratori d'envol website</a>