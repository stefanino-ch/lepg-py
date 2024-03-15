 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0
 
 .. _Lines_characteristics_de:

---------------------
Leinen-Eigenschaften
---------------------
Im Fenster *Leinen-Eigenschaften* definieren wir die speziellen eigenschaften der Trag- und Bremsleinen:

.. image:: /images/proc/lineCharacteristics-de.png
   :width: 764
   :height: 330

Rohdaten::

    *******************************************************
    *       34. LINES CHARACTERISTICS TABLE
    *******************************************************
    1
    6
    1  c  5.0   2.0  Riser    1000 daN  u_dyneem    10.0   g   p 12. cm  7
    2  c  1.90  3.0  Line275   275 daN  s_dyneem    2.26   g   s 12. cm  1
    3  c  1.40    Line160   160 daN  s_dyneem    1.34   g   s 10. cm  3
    4  c  1.15    Line120   120 daN  s_dyneem    1.00   g   s 10. cm  5
    5  c  0.80    Line100U  100 daN  u_dyneem    0.43   g   p 8.  cm  2
    6  c  2.00    Line200B  200 daN  s_dynemm    3.10   g   s 12. cm  6


Individuelle Definition der Eigenschaften von bis zu 50 verschiedenen Linientypen.

**Leinentyp** Diese Nummer wird verwendet für die Zuweisung der Eigenschaften zu den individuellen Leinen.

**Leinenform** r oder c (r=rectangular-> rechteckiger oder c=circular-> runder Querschnitt)

**Leinendurchmesser** in [mm]

**B-Diam** Nur anwendbar wenn Leinenform r verwendet wird, sonst leer lassen

**Leinenname** z.B. "Riser", "PPSL275", "DC60",... max 15 Zeichen, KEINE LEERSCHLÄGE

**Bruchlast** in [daN]

**Materialtyp** "dyneema", "aramid", "polyester", ... max 15 Zeichen, KEINE LEERSCHLÄGE

**Gewicht/m** Leinengewicht in [g] pro Meter

**Loop Typ** s oder p (s=sewed-> genähter der p=spliced-> gespleisster Loop)

**Loop Länge** Total Länge des Loop [cm]

**CAD Farbe** Nummer der CAD Farbe. Funktioniert nur wenn Code 1341 in Abschnitt 37 (Spezielle Parameter) aktiviert wurde.

Sortieren
---------
Mit der Schaltfläche **Sortieren** können die Zeilen neu angeordnet werden. Wenn das gemacht werden soll kannst Du die neuen Nummern in der ersten Spalte einsetzten und anschliessend mit der Schaltfläche die Tabelle neu sortieren. 


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.9" target="_blank">Laboratori d'envol website</a>

.. |manual_link| raw:: html

	<a href="http://www.laboratoridenvol.com/leparagliding/linesopt/lineopt.en.html" target="_blank">OPTIMIZE YOUR LINES IN LEPARAGLIDING</a>
