 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

-------------
Diagonal ribs
-------------
The *Diagonal ribs* is maybe the one with the most complex parameter set.

There are 6 different types of Diagonal ribs, each of the types with it's own set of parameters.

**IMPORTANT**

   single digit types (x: 1...6) do use absolut measurings in [cm] which will be scaled with the scaling factor of the wing

   double digit types (xx: 11...16) are set in [% of the profile chord]

**IMPORTANT**

   DO NOT merge single or double digit types withing the same configuration. Use just either one!

.. image:: /images/proc/hVvHribs-en.png
   :width: 736
   :height: 286
   
Raw data::

	***************************************************
	*	12. H V and VH ribs
	***************************************************
	12
	80  150
	1   1  0  1  1  1  6.0  0  0  0
	2   1  0  2  1  2  6.0  0  0  0
	3   1  0  3  1  3  6.0  0  0  0
	4   1  0  4  1  4  6.0  0  0  0
	5   1  4  1  5  1  6.0  0  0  0
	6   1  4  2  5  2  6.0  0  0  0
	7   1  4  3  5  3  6.0  0  0  0
	8   1  4  4  5  4  6.0  0  0  0
	9   1  8  1  9  1  6.0  0  0  0
	10  1  8  2  9  2  6.0  0  0  0
	11  1  8  3  9  3  6.0  0  0  0
	12  6  8  4  9  4  6.0  0  0  0  11  12

x and y Spacing
---------------
X and y Spacing" is the horizontal/ vertical separation distance between V-ribs drawn in box 2-4. The distance in cm will be multiplied by the scale of the drawing. So if "x-spacing" = 80.0 cm and "drawing scale" = 1.5 total distance is 80.0 x 1.5

.. image:: /images/proc/hVvHribsSpacing.png
   :width: 370
   :height: 380

Number of configs
-----------------
*Diagonal ribs* is an **optional section**. 

If you do not want to define/ use these parameters set the **Number of configs** value to **0**.

Type 1/ 11: Horizontal strap between rib i1 and rib i2
------------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib1_p.jpg

+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib | Param A  | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  | Param I  |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 1/ 11   | from rib| row [1]_ | to rib       | row [1]_     | width [2]_   | 0            | 0            | 0            | 0        | 0        |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [1]

    here anchor rows are used again: row 1=A, row 2=B, ….

.. [2]

    type x: strap witdh in [cm]

    type xx: strap witdh in [% chord]


Type 2/ 12: Diagonal partial V-rib centered in rib i
----------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib2_p.jpg

+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib | Param A  | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  | Param I  |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 2/ 12   | rib     | row [1]_ | left [3]_    | right [4]_   | r- [5]_      | r+ [6]_      | height [7]_  | beta [8]_    | 0        | 0        |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [3] left

   "0": no left diagonal rib will be created

   "1": a digonal rib to the left will be created

.. [4] right

   "0": no right diagonal rib will be created

   "1": a digonal rib to the right will be created

.. [5] lower rib width

   type 1: in [cm]

   type 2: in [% chord]

.. [6] upper rib width

   type x: in [cm]

   type xx: in [% chord]
   
.. [7]

   type x: in [cm]

   type xx: in [% chord]

.. [8] beta

   angle of the upper end 

Type 3/ 13: Diagonal full V-rib centered in rib i
-------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib3_p.jpg

+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib | Param A  | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  | Param I  |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 3/13    | rib     | row [1]_ | left [3]_    | right [4]_   | r- [5]_      | r+ [6]_      | 0            | 0            | 0        | 0        |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+


Type 4/ 14: "VH-rib" between rib i-1 to i+2
-------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib4_p.jpg

+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib | Param A  | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  | Param I  |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 4/ 14   | rib     | row [1]_ | left [3]_    | right [4]_   | r- [5]_      | r+ [6]_      | height [7]_  | beta [8]_    | 0        | 0        |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

Type 5/ 15: full continous VH-rib centered in rib i
---------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_VRF-p.p.jpg

   Full continous V-ribs type 5 using parabolic holes (if height < 100%)

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_VRF-e.p.jpg

   Full continous V-ribs type 5 using elliptical holes (if heigth > 100%)

+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib | Param A  | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  | Param I  |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 5/ 15   | rib     | row [1]_ | left [3]_    | right [4]_   | alpha1 (LE)  | alpha2 (TE)  | height [9]_  | r [10]_      | 0        | 0        |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [9]

   height < 100[%]: parabolic hole
   
   height > 100[%]: elliptical hole
   
.. [10]

   type x: in [cm]

   type xx: in [% chord]
   
**IMPORTANT**
   When using type 5/ 15 ribs keep in mind the following:

   * The number of anchorages on the rib "i" must be equal to the number of anchors on the right and left, even if they are not used (they can be virtual, ie without lines)

   * To define the Type 5 rib, use a number of lines equal to the number of anchors. 

   Example for 4 anchor points::

	5       5 1     1 1    60.0    60.0    80.     7.
	5       5 2     1 1    60.0    60.0    80.     7.
	5       5 3     1 1    60.0    60.0    80.     7.
	5       5 4     1 1    60.0    60.0    80.     7.

Type 6/ 16: general diagonal "VH-rib" between rib i and rib i+1
---------------------------------------------------------------

Type 6/ 16 is a general diagonal. It's very simple. A trapezoidal diagonal ranging from rib number i to rib number i+1. But the rib is totally configurable in size and position. It has been designed to develop competition paragliders CCC types, which need to jump between 4 and 5 cells without lines. But it can also serve to design simplest paragliders, and replacing some of the types of diagonals described above. It is also very useful to define transverse horizontal strips located in all parts of the wing (the tapes have not necessarily coincide with the anchor points).

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_V-ribtype6.p.jpg

+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib | Param A  | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  | Param I  |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 6/ 16   | rib i   | pos [11]_| height [12]_ | r+ [13]_     | r- [14]_     | rib i+1      | pos [11]_    | height [12]_ | r+ [13]_ | r- [14]_ |
+---------+---------+----------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [11]

   type x: in [cm]

   type xx: in [% chord]

.. [12]

   [% chord]

.. [13]

   type x: in [cm]

   type xx: in [% chord]

.. [14]

   type x: in [cm]

   type xx: in [% chord]

Sort by Order Num
-----------------
The button **Sort by Order Num** can be used to rearrange the definition lines. If for whatever reasons you will rearrange the lines, just define the numbering in an ascending order and press the Order button afterwards. Lepg will reorder the lines according to the numbering you've choosen. 

A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.12" target="_blank">Laboratori d'envol website</a>
