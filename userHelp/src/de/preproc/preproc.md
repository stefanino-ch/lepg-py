Author: Stefan Feuz; http://www.laboratoridenvol.com
Copyright: General Public License GNU GPL 3.0

# Preprocessor Parameter

Die Beschreibungen hier fassen nur die wichtigsten Themen zuammen. Eine detaillierte Beschreibung findest Du auf [Laboratori d'envol website](http://laboratoridenvol.com/leparagliding/pre.en.html)  

# Beispieldatei
	**********************************  
	LEPARAGLIDING  
	GEOMETRY PRE-PROCESSOR     v1.5  
	**********************************  
	gnuA2  
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
	**********************************  
	* 3. Vault  
	**********************************  
	2  
	741.33	10.13  
	372	12.72  
	288.41	24.74  
	112.185   37.41  
	**********************************  
	* 4. Cells distribution  
	**********************************  
	3  
	0.2  
	33  

# Dateibeschreibung

## Header
	**********************************  
	LEPARAGLIDING  
	GEOMETRY PRE-PROCESSOR     v1.5  
	**********************************  
The file header will be generated automatically by lepg.

## Design Name
	gnuA2  
The name of the design  

## Definition Eintrittskante
	1  
Leading edge type 1  

	a1= 641.92  
	b1= 194.02  
	x1= 340  
	x2= 490  
	xm= 527  
	c0= 28  
	ex1= 2.8  
	c02= 12  
	ex2= 4.0  
The leading edge is defined by an ellipse of semiaxis a1 and b1 (red), centered at the point (0.0).  

Xm is half span.  

In versions 1.4 and earlier it is only possible to modify the ellipses with a parabolic correction (degree 2). Now it is possible to make two corrections with a generic curve of degree N.  

The first correction begins at the point x1 and allows a deflection c01, with a variation of degree ex1.  

The second correction begins at the point x2 > x1 and allows a deflection c02, with a variation of degree ex2.  
<img src="http://laboratoridenvol.com/leparagliding/pre/images/lete-1.5.jpg" width="600" height="357">  
![](http://laboratoridenvol.com/leparagliding/pre/images/1_LE.jpg)

## Definition Austrittskante
	1

Trailing edge type 1

	a1= 643.28  
	b1= 140.5  
	x1= 180  
	xm= 527  
	c0= -8.9  
	y0= 88.06  
	exp= 1.5  

The trailing edge is defined by an ellipse of semiaxis a1 and b1 (green), centered at the point (0,y0).  

Xm is half span.  

In versions 1.4 and earlier it is only possible to modify the ellipses with a parabolic correction (degree 2). Now it is possible to make correction with a generic curve of degree N.  

The correction begins at the point x1 and allows a deflection c0, with a variation of degree exp.  

<img src="http://laboratoridenvol.com/leparagliding/pre/images/lete-1.5.jpg" width="600" height="357">  
![](http://laboratoridenvol.com/leparagliding/pre/images/1_TE.jpg)

## Krümmung
### Vault Typ 1
	1  
Type 1: vault using ellipse and cosinus modification, indicate parameters a1, b1.  

	a1= 414.2901  

semiaxis a  

	b1= 237.4300  

semiaxis b  

	x1= 265.3489  

point where start ellipse modification  

	c1= 28.22  

increased half span  

The shape of the vault is an ellipse of semiaxis a1 (horizontal) and b1 (vertical), but with a modification with a "cosine type function", from point x1 of the horizontal axis. Half of the span is increased by an amount c1.  
  
	for all y in [0,b1]:  
	If x < x1 then:  x=a1*sqrt(1-((y*y)/(b1*b1)))  
	If x >= x1 then: x=a1*sqrt(1-((y*y)/(b1*b1)))+c1*(1-cos(((y1-y)/y1)*0.5*pi)  
  
Verification: 
	for y=0 x=a1*sqrt(1-((y*y)/(b1*b1)))+c1*1
	for y=y1 x=a1*sqrt(1-((y*y)/(b1*b1)))+c1*0
	where y1=b1*sqrt(1-((x1*x1)/(a1*a1)))

Attached drawing explains:  

<img src="http://laboratoridenvol.com/leparagliding/pre/images/20121005_3_vault.jpg" width="355" height="588">
### Vault Typ 2
	2  

Type 2: vault using four tangent circles. In four rows indicate radious and angle (deg).

	741.33	10.13

radius (cm) and angular sector (deg) rotated by the first circle  

	372	12.72  

radius (cm) and angular sector (deg) rotated by the second circle  

	288.41	24.74  

radius (cm) and angular sector (deg) rotated by the third circle  

	112.185   37.41  

radius (cm) and angular sector (deg) rotated by the fourth circle  

![](http://laboratoridenvol.com/leparagliding/pre/images/2_1.jpg)
![](http://laboratoridenvol.com/leparagliding/pre/images/2_2.jpg)
![](http://laboratoridenvol.com/leparagliding/pre/images/2_3.jpg)
![](http://laboratoridenvol.com/leparagliding/pre/images/2_4.jpg)

## Zellenverteilung
	3

"3" indicates cell width proportional to chord  

"4" we use explicit width of each cell with automatic adjustement, if the sum not match the span.  

	0.2

Coefficient between "0.0" and "1.0". If coefficient is "0" then cell width is estrictly proportional to the chord, using iterative calculus. If coefficient is set to "1.0", then cell width is uniform. Use intermediate values as you need.  

	33  

The total cell number.  

![](http://laboratoridenvol.com/leparagliding/pre/images/3_1.jpg)
![](http://laboratoridenvol.com/leparagliding/pre/images/3_2.jpg)
![](http://laboratoridenvol.com/leparagliding/pre/images/3_3.jpg)
![](http://laboratoridenvol.com/leparagliding/pre/images/3_4.jpg)
