 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

-----------
Bremsleinen
-----------
Im Fenster *Bremsleinen* können die Parameter aus dem 10. Abschnitt der lep Datei bearbeitet werden, die Bremsleinen.

.. image:: /images/proc/brakes-de.png
   :width: 838
   :height: 395
   
Rohdaten::

 ***************************************************
 *       10. BRAKES
 ***************************************************
 270
 8
 4	1 1	2 1	3 1	4 1	6 2	- 6 2 3 5
 4	1 1	2 1	3 1	4 2	6 4	- 6 2 3 5
 4	1 1	2 1	3 2	4 3	6 6	- 6 2 3 5
 4	1 1	2 1	3 2	4 4	6 8	- 6 2 3 5
 4	1 1	2 2	3 3	4 5	6 10	- 6 2 3 5
 4	1 1	2 2	3 3	4 6	6 12	- 6 2 3 5
 4	1 1	2 2	3 4	4 7	6 14	- 6 2 3 5
 4	1 1	2 2	3 4	4 8	6 16	- 6 2 3 5
 * Brake distribution
 0	25	55	70	100
 0 	0	0	0	0

Die Definition der Bremsleinen erfolgt nach demselben Schema wie für die Hauptleinen. 

:ref:`Mehr zur Konfiguration der Hauptleinen findest Du hier.<Lines_configuration_de>`

Was Du sonst noch wissen musst
------------------------------
Die Hauptbremsleine ist fix Ebene 1 zugeordnet.

Die Hauptleinen können nur an die Aufhängepunkte der Rippen verbunden werden. 
Die Bremsleinen können auch zwischen den Rippen platziert werden. 
Dazu definierts Du die Rippennummer mit einer Kommastelle. 

Beispiel: 8.4 bedeutet dass die Bremsleine zwischen Rippe 8 und 9, auf 40% der Distanz zwischen den Rippen platziert werden soll. 

Verlängerung der Bremsleinen
----------------------------
Wenn notwendig können die Bremsleinen verlängert werden. Dazu können mit 5 Eckpunkten Verlängerungszonen entlang des Schirmes definiert werden. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S10_Brake_distribution_p.jpg

s 1, 2, 3, 4, 5
'''''''''''''''
Die Position des Eckpunktes entlang des Flügels ausgehend von der Flügelmitte. Definiert wird die Distanz in [% Flügelspannweite].

d 1, 2, 3, 4, 5
'''''''''''''''
Die Verlängerung der Bremsleinen für diesen Punkt.

Leinentypen
-----------
Mit der Version 3.23 wurde die Möglichkeit eingeführt individuelle Leineneigenschaften zu definieren. Das passiert im
Fenster **Leinen Eigenschaften**. Die Typen Nummer welche dort definiert wird, kann im Anschluss hier den individuellen
Leinen-Pfaden zugeordnet werden.

Werden im Fenster **Leinen bearbeiten** keine Typen-Nummern eingetragen, dann wird eine automatische Zuordnung gemacht:

* Ebene 1-> Typ 1

* Ebene 2-> Typ 2

* ...

Sortieren
---------
Mit der Schaltfläche **Sortieren** können die Zeilen neu angeordnet werden. Wenn das gemacht werden soll kannst Du die neuen Nummern in der ersten Spalte einsetzten und anschliessend mit der Schaltfläche die Tabelle neu sortieren. 


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.10" target="_blank">Laboratori d'envol website</a>
