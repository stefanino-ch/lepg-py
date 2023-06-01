 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

---------
Rib holes
---------
In the *Rib holes* window you can define the parameters from the 4th section of the lep file.

.. image:: /images/proc/ribHoles-en.png
   :width: 603
   :height: 286
   
Raw data::

	*************************************************************
	*          4. AIRFOIL HOLES                                 *
	*************************************************************
	2 
	1	
	12 	
	9	
	1 14.59	2.79	2.735	6.72	0.	0.	0.	0.
	1 22.18	2.61	2.375	6.72	0.	0.	0.	0.	
	1 33.36	1.64	2.5	5.9	0.	0.	0.	0.
	1 40.32	1.46	2.4	5.8	0.	0.	0.	0.
	1 47.41	1.34	2.23	5.7	0.	0.	0.	0.
	1 59.17	1.27	1.84	3.4	0.	0.	0.	0.
	1 65.23	1.33	1.7	3.2	0.	0.	0.	0.
	1 71.21	1.18	1.6	3.0	0.	0.	0.	0.
	1 81.87	0.89	1.6	1.6	0.	0.	0.	0.
	13
	13
	3
	1 23.5	2.5	6.5	6.5	0.	0.	0.	0.
	1 55.0	1.92	4.3	4.3	0.	0.	0.	0.
	1 81.	1.1	1.7	1.7	0.	0.	0.	0.

Number of configurations
------------------------
In a configuration you can bundle the settings for a group of ribs. For all ribs within the same configuration the same settings apply. 

Initial rib
'''''''''''
The number of the first rib for which the configuration applies. 

Final rib
'''''''''
The number of the last rib for which the configuration applies. 

Number of configuration lines
-----------------------------
Within a configuration you can define several configuration lines. Basically each line defines one rib hole. 

Order Num
'''''''''
A number only used by Lepg allowing to reorder the lines during edit. 

Light type
''''''''''
The type of rib hole defined in this line: 

**"1"** ellipse or circle

**"2"** ellipse or circle with center strip

**"3"** triangle

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S04_Hole1_p.jpg

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S04_Hole2_p.jpg

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S04_Hole3_p.jpg

Hor dist
''''''''
The horizontal distance from the LE to the rib hole in [% chord].

Vert dist
'''''''''
The vertical distance from the chord line to the rib hole in [% chord].

Hor axis
''''''''
The lengt of the horizontal axis of the hole in [% chord]. Basically the width. 

Vert axis
'''''''''
The lengt of the vertical axis of the hole in [% chord]. Basically the height. 

Rot angle
'''''''''
The angle of which the hole shall be rotated in [deg].

Opt
'''
For type **"1"** holes set this value 0

For type **"2"** holes this value defines the width of the strip in [cm]

For type **"3"** holes the radius of the corners in [cm]

Sort by Order Num
-----------------
The button **Sort by Order Num** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen. 


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.4" target="_blank">Laboratori d'envol website</a>
