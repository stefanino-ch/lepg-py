 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------
Mark types
----------
This window allows the user to choose different types of marking elements in DXF files (one-dimensional 
points, minicircles, triangles, segments, ...). 

This is especially useful for laser cutting plotters, and the ability to adapt marking to manufacturer 
preferences. 

Remember that leparagliding generates two types of plans, some for use with conventional printers 
("print" version), and others for professional use with computerized cutting plotters ("laser" version).

.. image:: /images/proc/marksTypes-en.png
   :width: 603
   :height: 286
   
Raw data::

	******************************************************
	*       20. Marks types
	******************************************************
	10
	typepoint   1  0.25  1.2     2  0.3  1.2
	typepoint2  1  0.25  1.2     2  0.2  1.2
	typepoint3  1  0.25  1.2     2  0.2  1.2
	typevent    1  10.   0.0     2  2.0  0.0
	typetab     1  10.   0.0     3  2.0  0.0
	typejonc    1  10.   0.0     2  2.0  0.0
	typeref     1  5.    1.      1  2.0  0.0
	type8       1  0.2   4.0     1  0.0  4.0
	type9       1  0.25  1.2     2  0.2  1.2
	type10      1  0.25  1.2     2  0.2  1.2

Number of marks
---------------
*Mark types* is an **optional section**.

If you do not want to define/ use these parameters set the **Number of configs** value to **0**.

  |

+-----------------+----------------------------+----------------------------+----------------------------+
| Marks type      | **Print**                  | **Print**                  | **Print**                  |
|                 | Form 1                     | Form 1 1st param           | Form 1 2nd param           |
+-----------------+----------------------------+----------------------------+----------------------------+
| typepoint [1]_  | 1=constructed point        |  radius of minicircle [mm] | offset [mm]                |
|                 | 2=minicircle               |                            |                            |
+-----------------+----------------------------+----------------------------+----------------------------+
| typepoint2 [2]_ | 1                          | 0.25                       | 1.2                        |
+-----------------+----------------------------+----------------------------+----------------------------+
| typepoint3 [2]_ | 1                          | 0.25                       | 1.2                        |
+-----------------+----------------------------+----------------------------+----------------------------+
| typevent        | 1=two green points         | points separation or       | offset [mm]                |
|                 | 2=segment                  | segment [mm]               |                            |
|                 | 3=double segment           |                            |                            |
+-----------------+----------------------------+----------------------------+----------------------------+
| typetab         | 1=tree orange points       | points separation or       | offset [mm]                |
|                 | 2=tree orange full control | segment [mm]               |                            |
|                 | 3=triangle                 |                            |                            |
+-----------------+----------------------------+----------------------------+----------------------------+
| typejonc   [2]_ | 1                          | 10.                        | 0.0                        |
+-----------------+----------------------------+----------------------------+----------------------------+
| typeref    [2]_ | 1                          | 5.0                        | 0.0                        |
+-----------------+----------------------------+----------------------------+----------------------------+
| type8 [3]_      | 1                          | [6]_ pos of roman number   | [6]_ vertical offset [mm]  |
|                 |                            | 0.0 totally left           | ref baseline               |
|                 |                            | 1.0 totally right          |                            |
|                 |                            | normal 0.2 or 0.5          |                            |
+-----------------+----------------------------+----------------------------+----------------------------+
| type9 [4]_      | 1                          | 0.0                        | numbers size [cm]          |
|                 |                            |                            | leading/ trailing edge     |
|                 |                            |                            | ribs, trailing edge panels |
+-----------------+----------------------------+----------------------------+----------------------------+
| type10 [5]_     | 1                          | 0.0                        | numbers size [cm]          |
|                 |                            |                            | diagonal ribs              |
+-----------------+----------------------------+----------------------------+----------------------------+

  |

+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| Marks type      | **Laser**                  | **Laser**                         | **Laser**                         |
|                 | Form 2                     | Form 2 1st param                  | Form 2 2nd param                  |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typepoint [1]_  | 1=unidimensional           |  radius of minicircle [mm]        | offset [mm]                       |
|                 | 2=minicircle               |                                   |                                   |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typepoint2 [2]_ | 2                          | 0.2                               | 1.2                               |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typepoint3 [2]_ | 2                          | 0.2                               | 1.2                               |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typevent        | 1=two green points         | points separation or              | offset [mm]                       |
|                 | 2=segment                  | segment [mm]                      |                                   |
|                 | 3=double segment           |                                   |                                   |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typetab         | 1=tree orange points       | points separation or              | offset [mm]                       |
|                 | 2=tree orange full control | triangle height [mm]              |                                   |
|                 | 3=triangle                 |                                   |                                   |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typejonc   [2]_ | 2                          | 2.0                               | 0.0                               |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| typeref    [2]_ | 1                          | 2.0                               | 0.0                               |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| type8 [3]_      | 1                          | 0.0                               | [6]_ offset between dots of       |
|                 |                            |                                   | roman numeral [mm]. (global size  |
|                 |                            |                                   | of the roman numerals)            |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| type9 [4]_      | 1                          | [6]_ offset in mm between dots of | [6]_ offset in mm between dots of |
|                 |                            | roman numeral [mm](global size    | roman numeral [mm](global size    |
|                 |                            | of the roman numerals)            | of the roman numerals)            |
|                 |                            | in **rod pockets**                | in **ribs**                       |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+
| type10 [5]_     | 1                          | 0.0                               | [6]_ offset in mm between dots of |
|                 |                            |                                   | roman numeral [mm](global size    |
|                 |                            |                                   | of the roman numerals)            |
|                 |                            |                                   | in **diagonal ribs**              |
+-----------------+----------------------------+-----------------------------------+-----------------------------------+

.. [1] typepoint  is the point for general use

.. [2] still not used, set defaults

.. [3] romano numbering in panels generated using 3D shaping

.. [4] general numbers size, and roman marks size in ribs

.. [5] general numbers size in diagonal ribs

.. [6] print and laser

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S20.jpg
   :width: 462
   :height: 660

   Types 1,2,3,4,5,8,9,10 now fully functional

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S20-romanop-position.p.png
   :width: 462
   :height: 435
   
   Type8 marks parameters interpretation


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.20" target="_blank">Laboratori d'envol website</a>
