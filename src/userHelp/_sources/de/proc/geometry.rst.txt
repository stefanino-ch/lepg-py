 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

---------------
Flügelgeometrie
---------------
Im Fenster Geometrie wird der zweite Teil der Daten aus dem ersten Abschnitt der lep Datei definiert. 

.. image:: /images/proc/geometry-en.png
   :width: 458
   :height: 171
   
Rohdaten::

	* Rib geometric parameters
	* Rib	x-rib	  y-LE	  y-TE	    xp	      z	         beta	   RP	      Washin
	 1     24.37      0.18    309.24     24.36      0.46      2.16     33.33      0.00
	 2     72.86      1.60    308.49     72.71      4.08      6.48     33.33      0.00
	 3    120.88      4.44    307.00    120.18     11.21     10.59     33.33      0.00
	 4    168.18      8.68    304.79    166.31     21.64     14.90     33.33      0.00
	 5    214.54     14.30    301.85    210.67     35.08     18.81     33.33      0.00
	 6    259.73     21.30    298.21    252.79     51.40     23.70     33.33      0.00
	 7    303.50     29.77    293.87    292.02     70.79     28.88     33.33      0.00
	 8    345.46     41.26    288.87    327.84     92.61     33.84     33.33      0.00
	 9    385.16     56.00    283.16    359.89    116.02     38.37     33.33      0.00
	10    422.21     73.45    276.64    387.92    140.23     44.11     33.33      0.00
	11    456.31     93.04    269.45    410.61    165.64     52.52     33.33      0.00
	12    487.22    114.20    261.78    427.78    191.33     59.97     33.33      0.00
	13    514.81    136.38    253.80    438.47    216.67     74.82     33.33      0.00
	14    539.00    159.09    245.71    441.90    240.55     88.56     33.33      0.00

Diese Parameter können nur mit der Hilfe einer zusätzlichen Geometrischen Betrachtung (am besten mit Hilfe eines CAD Programmes) erzeugt werden. 

Als Alternative können die Parameter auch mit dem Pre-Prozessor auf Basis von wenigen Parametern berechnet und anschliessend in den Prozessor Teil importiert werden. Beachte: der Pre-Prozessor ist ein mögliches Hilfsmittel welches für einfache Flügelgeometrien nutzbar ist, für ausgefeilte Designs musst Du den Weg über ein CAD Programm nehmen. 

Es gibt eine Beschränkung dass keine Zellen genau in der Mitte des Flügels definiert werden können. Für eine gerade Anzahl Zellen kann die mittlere Zelle mit einer Breite von 0.0 definiert werden.

Das Bild zeigt genau welcher Parameter welchem Mass entspricht. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S01_Definition.jpg
   :width: 400
   :height: 594

Die zweitletzte Spalte definiert den Prozentanteil welcher die Flügeltiefe auf die Verwindung hat. Dieser Parameter wird nur ausgewertet wenn der **Alpha mode** im Basisdaten Fenster auf **"1"** gesetzt ist. 

Die letzte Spalte definiert die Flügelverwindung für jede einzelne Rippe. Dieser Wert muss gesetzt werden wenn der  **Alpha mode** im Basisdaten Fenster auf **"0"** gesetzt ist.

Mit der Schaltfläche **Nach Rippen Nr sortieren** können die Zeilen neu angeordnet werden. Wenn das gemacht werden soll kannst Du die neuen Rippen Nummern in der ersten Spalte einsetzten und anschliessend mit der Schaltfläche die Tabelle neu sortieren. 

**BEACHTE** die Zeilen müssen die Flügeldefinition von der Mitte nach aussen definieren?


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.1" target="_blank">Laboratori d'envol website</a>

