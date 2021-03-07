.. _howto-install_de:

Author: Stefan Feuz; http://www.laboratoridenvol.com

Copyright: General Public License GNU GPL 3.0

***********
Nahtzugaben
***********

Eine detaillierte Beschreibung findest Du auf der |pere_link|.

Beispiel::

	*************************************************************
	*           6. SEWING ALLOWANCES                            *
	*************************************************************
	15	25	25	upper panels (mm)
	15	25	25	lower panels (mm)
	15	ribs (mm)
	15	vribs (mm)
	
Detailbeschreibung
******************

Header::

	*************************************************************
	*           6. SEWING ALLOWANCES                            *
	************************************************************* 
   
Der Header wird automatisch von lepg erzeugt.

Die Nahtmarkierungen werden auf 4 Zeilen definiert. 


Zeile 1: Nahtzugaben für die oberen Panels::

	15	25	25	upper panels (mm)

* Parameter 1 Seitliche Nahtzugabe

* Parameter 2 Nahtzugabe für die Eintrittskante

* Parameter 3 Nahtzugabe für die Austrittskante
	
Zeile 2: Nahtzugaben für die unteren Panels::

	15	25	25	lower panels (mm)

* Parameter 1: Seitliche Nahtzugabe

* Parameter 2: Nahtzugabe für die Eintrittskante

* Parameter 3: Nahtzugabe für die Austrittskante
	
Zeile 3: Nahtzugaben für die Rippen::

	15	ribs (mm)

Zeile 4: Nahtzugaben für V-Rippen::

	15	vribs (mm)


.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.6" target="_blank">Laboratori d'envol website</a>
