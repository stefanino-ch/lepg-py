 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

---------------
3D DXF Optionen
---------------
Hier definierst Du die Farben der Linien in den DXF Zeichnungen. 

.. image:: /images/proc/threeDDxf-de.png
   :width: 350
   :height: 331

Rohdaten::

	*******************************************************
	*       25. GENERAL 3D DXF OPTIONS
	*******************************************************
	1
	A_lines_color   1         red
	B_lines_color   8         grey
	C_lines_color   8         grey
	D_lines_color   8         grey
	E_lines_color   8         grey
	F_lines_color   30        orange
	Extrados        1     5   blue
	Vents           0     1   red
	Intrados        0     3   green

Type
----
*3D DXF Optionen* ist eine **optionale Konfiguration**. 

Wenn Du diese Werte nicht speziell definieren willst, dann setze **Typ** auf **Standard**. 

Linienname
----------
Die Namen sind fix definiert und müssen genau so eingegeben werden. 

* A_lines_color
* B_lines_color
* C_lines_color
* D_lines_color
* E_lines_color
* F_lines_color
* Extrados [1]_
* Vents [2]_
* Intrados [3]_

.. [1] Einstellungen für die Panels des Obersegels

.. [2] Einstellungen für die Einlassöffnungen

.. [3] Einstellungen für die Panels des Untersegels

Farbcode
--------
Standard Farbnummer für CAD Systeme:
1=rot, 2=gelb, 3=grün, 4=cyan, 5=blau, 6=magenta, 7=weiss, 8=dunkelgrau, 9= grau,... bis 255

Es wird empfohlen nur 2-stellige Farbnummern zu verwenden. 

Farbname
--------
Deine eigene Beschreibung der gewählten Farbe. 


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.25" target="_blank">Laboratori d'envol website</a>
