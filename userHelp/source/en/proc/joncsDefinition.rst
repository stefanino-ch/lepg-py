 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------------
Joncs definition
----------------
In the window *Joncs definition* you control the creation of pockets used to place nylon rods on the ribs.

.. image:: /images/proc/joncsDefinition-en.png
   :width: 736
   :height: 308
   
Raw data::

	*******************************************************
	*       21. JONCS DEFINITION (NYLON RODS)
	*******************************************************
	2                     
	2                     
	1 1                   
	2                     
	1 1 15                
	5.5  10.   1.5   2.0
	5.   11.   2.2   2.0
	0.0  9.35  6.3  9.35
	2   16 19             
	5.   9.    2.5   2.0
	5.   12    3.    2.0
	0.0  9.35  6.3  9.35
	2 2                   
	2                     
	1 1 15                
	20. 2.  30. -2.0 3.0  
	0.0  9.35  6.3  9.35  
	2 16 20               
	40. 4.  30. -3.2 0.0  
	0.0  9.35  6.3  9.35  

Number of blocs
---------------
Nose mylars is an **optional section**. 

If you do not want to define/ use these parameters set the **Number of blocs** value to **0**.

A bloc bundles either type 1 or type 2 rods.

Whithin a bloc you can define several groups of parameters, each group does define one pocket.

**Type 1** rods
---------------
Type 1 rods are the typical wing nose rods. 

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S21.jpg
   :width: 462
   :height: 642

   Type 1 rods definition

+-----------+----------+------------+------------+---------+---------+------------+------------+---------+---------+---------+---------+---------+---------+
| First rib | Last rib | Param A    | Param B    | Param C | Param D | Param F    | Param G    | Param H | Param I | S1      | S2      | S3      | S4      |
+-----------+----------+------------+------------+---------+---------+------------+------------+---------+---------+---------+---------+---------+---------+
| rib num   | rib num  | xeini [1]_ | xefin [1]_ | ye [2]_ | n [3]_  | xicni [1]_ | xifin [1]_ | yi [2]_ | n [3]_  | S1 [4]_ | S2 [4]_ | S3 [4]_ | S4 [4]_ |
+-----------+----------+------------+------------+---------+---------+------------+------------+---------+---------+---------+---------+---------+---------+

.. [1] in [% chord]
.. [2] in [% chord]
.. [3] n is the power of the deflection formula y = k*x^n
.. [4] in [mm]

**Type 2** rods
---------------
Type 2 rods can be placed on the rib wherever you want.

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S21-jtype2.jpeg
   :width: 462
   :height: 458

   Type 2 rods definition

+-----------+----------+--------------+--------------+------------+------------+------------------+----+---------+---------+---------+
| First rib | Last rib | Param A      | Param B      | Param C    | Param D    | Param E          | S1 | S2      | S3      | S4      |
+-----------+----------+--------------+--------------+------------+------------+------------------+----+---------+---------+---------+
| rib num   | rib num  | x-start [1]_ | y-start [2]_ | x-end [1]_ | y-end [2]_ | deflection f [2] | 0  | S2 [4]_ | S3 [4]_ | S4 [4]_ |
+-----------+----------+--------------+--------------+------------+------------+------------------+----+---------+---------+---------+

Sort by Order Num
-----------------
The button **Sort by Order Num** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen. 

A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.21" target="_blank">Laboratori d'envol website</a>
