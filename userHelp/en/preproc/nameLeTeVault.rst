 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

Pre-Processor data
==================

In the window Pre-Processor data the parameters out of the first three
sections of the pre-processor input file can be edited.

.. image:: /images/preproc/nameLeTeVault1.png
   :width: 621
   :height: 322


Leading edge definition
-----------------------

Raw date::

	**********************************
	* 1. Leading edge parameters
	**********************************
	1
	a1= 641.92
	b1= 194.02
	x1= 340
	x2= 490
	xm= 527
	c0= 28
	ex1= 2.8
	c02= 12
	ex2= 4.0  

Currently there's only one type of leading edge definition possible. Therefore
thy **Type** column has been removed from the GUI. Lepg will take care about
the correct setup in the background.

The leading edge is defined by an ellipse of semiaxis a1 and b1 (red),
centered at the point (0.0).

**Xm** is half span.

In versions 1.4 and earlier it is only possible to modify the ellipses with a
parabolic correction (degree 2). Now it is possible to make two corrections
with a generic curve of degree N.

The first correction begins at the point x1 and allows a deflection c01, with
a variation of degree ex1.

The second correction begins at the point x2 > x1 and allows a deflection
c02, with a variation of degree ex2.

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/lete-1.5.jpg
   :width: 600
   :height: 357

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/1_LE.jpg

Trailing edge definition
------------------------

Raw data::

	**********************************
	* 2. Trailing edge parameters
	**********************************
	1
	a1= 643.28
	b1= 140.5
	x1= 180
	xm= 527
	c0= -8.9
	y0= 88.06
	exp= 1.5 

Currently there's only one type of trailing edge definition possible. Therefore
thy **Type** column has been removed from the GUI. Lepg will take care about
the correct setup in the background.

The trailing edge is defined by an ellipse of semiaxis a1 and b1 (green),
centered at the point (0,y0).

**Xm** is half span.

In versions 1.4 and earlier it is only possible to modify the ellipses with
a parabolic correction (degree 2). Now it is possible to make correction with
a generic curve of degree N.

The correction begins at the point x1 and allows a deflection c0, with a
variation of degree exp.

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/lete-1.5.jpg
   :width: 600
   :height: 357

Vault Type 1
------------

Vault type 1 example (see window image on top of the page)::

	**********************************
	* 3. Vault
	**********************************
	1
	a1= 414.2901
	b1= 237.4300
	x1= 265.3489
	c1= 28.22 

The shape of the vault is an ellipse of semiaxis a1 (horizontal) and b1
(vertical), but with a modification with a "cosine type function", from point
x1 of the horizontal axis. Half of the span is increased by an amount c1::
  
	for all y in [0,b1]:  
	If x < x1 then:  x=a1*sqrt(1-((y*y)/(b1*b1)))  
	If x >= x1 then: x=a1*sqrt(1-((y*y)/(b1*b1)))+c1*(1-cos(((y1-y)/y1)*0.5*pi)  
  
Verification::
	for y=0 x=a1*sqrt(1-((y*y)/(b1*b1)))+c1*1
	for y=y1 x=a1*sqrt(1-((y*y)/(b1*b1)))+c1*0
	where y1=b1*sqrt(1-((x1*x1)/(a1*a1)))

Attached drawing explains:  

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/20121005_3_vault.jpg
   :width: 355
   :height: 588

Vault Type 2
------------

.. image:: /images/preproc/nameLeTeVault2.png
   :width: 621
   :height: 322

Vault type 2 example::

	**********************************
	* 3. Vault
	**********************************
	2
	741.33	10.13
	372	12.72
	288.41	24.74
	112.185   37.41

Type 2: vault using four tangent circles. In four rows indicate radious and
angle (deg)::

	741.33	10.13

Radius (cm) and angular sector (deg) rotated by the first circle::

	372	12.72  

Radius (cm) and angular sector (deg) rotated by the second circle::

	288.41	24.74  

Radius (cm) and angular sector (deg) rotated by the third circle::  

	112.185   37.41  

Radius (cm) and angular sector (deg) rotated by the fourth circle.  


.. image:: http://laboratoridenvol.com/leparagliding/pre/images/2_1.jpg

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/2_2.jpg

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/2_3.jpg

.. image:: http://laboratoridenvol.com/leparagliding/pre/images/2_4.jpg

A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/pre.en.html#2" target="_blank">Laboratori d'envol website</a>