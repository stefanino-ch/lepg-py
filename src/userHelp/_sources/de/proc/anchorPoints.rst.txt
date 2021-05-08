 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

--------------
Aufhängepunkte
--------------
Im Fenster Zellen editieren wir die Parameter aus dem 3. Abschnitt der lep Datei. 

.. image:: /images/proc/anchorPoints-de.png
   :width: 602
   :height: 225
   
Rohdaten::

	*************************************************************
	*            3. ANCHOR POINTS                               *
	*************************************************************
	* Airf  Anch  A    B      C    D    E    F
	1       4     8.5   27.5  53   77   0    0
	2       4     8.5   27.5  53   77   0    0
	3       4     8.5   27.5  53   77   0    0
	4       4     8.5   27.5  53   77   0    0
	5       4     8.5   27.5  53   77   0    0
	6       4     8.5   27.5  53   77   0    0
	7       4     8.5   27.5  53   77   0    0
	8       4     8.5   27.5  53   77   0    0
	9       4     8.5   27.5  53   77   0    0
	10      4     8.5   27.5  53   77   0    0
	11      4     8.6   27.5  53   77   0    100
	12      3     9.0   40.0  75   0    0    100
	13      0     0     0     0    0    0    100
	14      4     0.0   30    60   90   0    0

Rippen Nr
---------
Rippennummer für die auf der Zeile die Aufhängepunkte definiert werden.

Anz Auf
-------
Anzahl der Aufhängepunkte (A...E) die während dem Berechnen berücksichtigt werden müssen. Die Bremsleinen müssen nicht mit eingerechnet werden. 

Pos A
-----
Position des Aufhängepunktes der A-Leinen [% Flügeltiefe].
0 eingeben wenn der Aufhängepunkt nicht verwendet werden soll. 

Pos B
-----
Position des Aufhängepunktes der B-Leinen [% Flügeltiefe].
0 eingeben wenn der Aufhängepunkt nicht verwendet werden soll. 

Pos C
-----
Position des Aufhängepunktes der C-Leinen [% Flügeltiefe].
0 eingeben wenn der Aufhängepunkt nicht verwendet werden soll. 

Pos D
-----
Position des Aufhängepunktes der D-Leinen [% Flügeltiefe].
0 eingeben wenn der Aufhängepunkt nicht verwendet werden soll. 

Pos E
-----
Position des Aufhängepunktes der E-Leinen [% Flügeltiefe].
0 eingeben wenn der Aufhängepunkt nicht verwendet werden soll. 

Bremsleinen
-----------
Position of the brake lines anchor point in [% chord].
0 eingeben wenn keine Bremsleinen vorhanden sind. 

Nach Rippen Nr sortieren
------------------------
Mit der Schaltfläche **Nach Rippen Nr sortieren** können die Zeilen neu angeordnet werden. Wenn das gemacht werden soll kannst Du die neuen Rippen Nummern in der ersten Spalte einsetzten und anschliessend mit der Schaltfläche die Tabelle neu sortieren. 

**BEACHTE** die Zeilen müssen die Flügeldefinition von der Mitte nach aussen definieren.


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.3" target="_blank">Laboratori d'envol website</a>
