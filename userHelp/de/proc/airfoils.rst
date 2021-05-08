 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

------
Zellen
------
Im Fenster Zellen editieren wir die Parameter aus dem 2. Abschnitt der lep Datei. 

.. image:: /images/proc/airfoils-de.png
   :width: 602
   :height: 225
   
Rohdaten::

	**************************************************************
	*             2. AIRFOILS       	                     *
	**************************************************************
	* Airfoil name, intake in, intake out, open , disp. rrw
	1	gnua.txt	1.6	6.3	1	0	1	15	
	2	gnua.txt	1.6	6.3	1	0	1	15
	3	gnua.txt	1.6	6.3	1	0	1	15
	4	gnua.txt	1.6	6.3	1	0	1	15
	5	gnua.txt	1.6	6.3	1	0	1	15
	6	gnua.txt	1.6	6.3	1	0	1	15
	7	gnua.txt	1.6	6.3	1	0	1	15
	8	gnua.txt	1.6	6.3	1	0	1	15
	9	gnua.txt	1.6	6.3	1	0	1	15
	10	gnua.txt	1.6	6.3	1	0	1	15
	11	gnua.txt	1.6	6.3	1	0	1	15
	12	gnua.txt	1.6	6.3	0	0	1	15
	13	gnua.txt	1.6	6.3	0	0	1	15
	14	gnuat.txt	0.0	6.3	0	0	1	1

Name
----
Der Name der Datei welche das Rippenprofil definiert. Bevor der Prozessor gestartet werden kann muss diese Datei in demselben Verzeichnis wie der Prozessor gespeichert werden. 

Start Öffnung
-------------
Position an der die Einlassöffnung startet. Wird angegeben in [% Flügeltiefe].

Ende Öffnung
------------
Position an der die Einlassöffnung endet. Wird angegeben in [% Flügeltiefe].

Offen/ geschl.
--------------
Ein Wert von 0 oder 1 der definiert ob eine offene oder geschlossene Zelle links der Rippe erstellt werden soll. 

**"0"** geschlossene Zelle

**"1"** offene Zelle
 
vert Verstz
-----------
Vertikaler Versatz einer Rippe in [cm]. Die Idee ist die Position von unbelasteten Rippen (ohne Aufhängepunkte) zu kontrollieren. 
Der Wert ist normalerweise 0.

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S02_delta_displacement.jpg
   :width: 532
   :height: 375

Rel Gewicht
-----------
Definiert die relative Belastung im Verhältnis zur Last. 
Der Wert ist normalerweise 1.

rrw
---
Abhängig vom Flügeltyp gibt es hier zwei verschiedene Bedeutungen. 

Single skin Flügel
''''''''''''''''''
**"0"** Die Dreiecke der Aufhängungen werden nicht rotiert, sondern nur seitlich geneigt wie mit dem winkel "beta" im Fenster Geometrie definiert.

**"1"** Die Dreiecke der Aufhängungen werden automatisch abhängig vom Flügelprofil rotiert. 

Double skin Flügel
''''''''''''''''''
Wenn der Wert grösser als 1 ist dann definiert er die Länge der Mini-Ribs. Dies ist nur bei nicht "ss" Flügeln möglich. Die Angabe der Länge erfolgt in [% Flügeltiefe].

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S02_minicab-minirib.jpg
   :width: 294
   :height: 416

Nach Rippen Nr sortieren
------------------------
Mit der Schaltfläche **Nach Rippen Nr sortieren** können die Zeilen neu angeordnet werden. Wenn das gemacht werden soll kannst Du die neuen Rippen Nummern in der ersten Spalte einsetzten und anschliessend mit der Schaltfläche die Tabelle neu sortieren. 

**BEACHTE** die Zeilen müssen die Flügeldefinition von der Mitte nach aussen definieren?


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.2" target="_blank">Laboratori d'envol website</a>

