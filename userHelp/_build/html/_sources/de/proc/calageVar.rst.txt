 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------------
Calage variation
----------------
*Calage* ist ein französisches Wort welches das System beschreibt wie in lep Pilotenposition und 
Winkel definiert werden. 
Es gibt keine exakte Übersetzung des Wortes *Calage* ins Deutsche, darum verwenden wir weiterhin
den französischen Begriff. 

Vom geometrischen Standpunkt aus ist *Calage* die Distand in % Flügeltiefe von der Eintrittskante bis zur 
Senkrechten von der Pilotenposition auf die Profilsehne. 

Ein kleiner Calage Wert bedeutet dass der Pilot näher zur Eintrittskante ist, die Fluggeschwindigkeit steigt. 
Wird die Calage nach hinten verschoben wird der Flügel langsamer. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S08_calage_p.jpg

Der Calage Wert beeinfluss auch den Angele of Attack. Aber Angle of Attack ist ein schwieriger Wert in der Definition
und schwierig zu bestimmen. Es ist einfacher die Calage zu bestimmen, der Flügel balanciert sich im Flug 
automatisch aus. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S28a.jpg
   :width: 462
   :height: 464

Im *Calage Variation* Fenster haben wir die Möglichkeit eine Studienberechnung zu definieren welche
den Einfluss einer Winkelveränderung des Flügels auf die Leinenlänge und die Calage Position zeight. 
Die hier definierten Parameter sind nur zu Studienzwecken und haben keinen Einfluss auf die Leinen- oder 
Flügelgeometrie selbst. 

.. image:: /images/proc/calageVar-en.png
   :width: 405
   :height: 233

Rohdaten::

	*******************************************************
	*       28. PARAMETERS FOR CALAGE VARIATION
	*******************************************************
	1
	3
	10. 30.35  60  0  0  0
	-4 4 5 10

Über Winkel und Anzahl Schritte
-------------------------------
lep berechnet total vier verschiedene Fälle welche weiter unten erklärt werden. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S28b.jpg
   :width: 462
   :height: 424

Typ
---
*Calage Variation* ist eine **optionale Konfiguration**.

Wenn Du keine speziellen Konfigurationen machen möchtest, dann setze den Wert von **Typ** auf **keine**.

Anzahl Aufhängepunkte
---------------------
Die Anzahl der Aufhängepunkte für die die Parameter berechnet werden sollen. (1...6)

Pos. A....F
--------------
Die Position der Aufhängepunkte in [% Flügeltiefe]. Da es sich hier um eine reine Studienberechnung
handelt müssen die Punkte nicht exakt mit dem richtigen Flügel übereinstimmen. 

Speed System Variation
----------------------
Die Parameter *Max neg Winkel* und *Anz neg Schritte* definieren die Kalkulation für eine 
Speed System Variation. 

Es werden zwei verschiedene Fälle berechnet: 

a) die ersten Gurten werden verändert, der Drehpunkt ist im letzten Aufhängepunkt

b) die letzten Gurten werden verändert, der Drehpunkt ist im ersten Aufhängepunkt

Max neg Winkel
''''''''''''''
Hier wird der maximale negative Winkel für die Studie definiert. Berechnet werden im Anschluss 
Winkel zwischen dem eingegebenen Wert und 0.

Num neg Schritte
''''''''''''''''
Die Anzahl Schritte welche berechnet werden sollen. Ein neg Winkel von -4 und 4 Schritte ergeben am Schluss eine Berechnung pro Grad.

Trimm System Variation
----------------------
Die Parameter *Max pos Winkel* und *Anz pos Schritte* definieren die Kalkulation für eine 
Trimm System Variation. 

Es werden zwei verschiedene Fälle berechnet: 

c) die letzten Gurten werden verändert, der Drehpunkt ist im ersten Aufhängepunkt

d) die ersten Gurten werden verändert, der Drehpunkt ist im letzten Aufhängepunkt

Max pos Winkel
''''''''''''''
Hier wird der maximale positive Winkel für die Studie definiert. Berechnet werden im Anschluss 
Winkel zwischen dem eingegebenen Wert und 0.

Num neg Schritte
''''''''''''''''
Die Anzahl Schritte welche berechnet werden sollen. 
Ein positiver Winkel von 5 und 10 Schritte ergeben am Schluss eine Berechnung in .5 Grad Schritten. 

Berechnete Parameter::

	 7. CALAGE AND RISERS VARIATIONS WITH ANGLE

	 a) Speed system pivot in last riser:
	 -------------------------------------------
	 i   alpha       A       B       C  Calage
	 1   -0.00    0.00    0.00    0.00   31.00
	 2   -1.00   -2.68   -1.60    0.00   26.90
	 3   -2.00   -5.36   -3.20    0.00   22.83
	 4   -3.00   -8.04   -4.80    0.00   18.80
	 5   -4.00  -10.70   -6.39    0.00   14.86

	 b) Speed system pivot in first riser:
	 -------------------------------------------
	 i   alpha       A       B       C  Calage
	 1   -0.00    0.00    0.00    0.00   31.00
	 2   -1.00    0.00    1.10    2.67   26.89
	 3   -2.00    0.00    2.20    5.34   22.78
	 4   -3.00    0.00    3.29    8.00   18.66
	 5   -4.00    0.00    4.39   10.65   14.54

	 c) Trimer system pivot in first riser:
	 -------------------------------------------
	 i   alpha       A       B       C  Calage
	 1    0.00    0.00    0.00    0.00   31.00
	 2    0.50    0.00   -0.55   -1.34   33.05
	 3    1.00    0.00   -1.10   -2.68   35.10
	 4    1.50    0.00   -1.65   -4.02   37.15
	 5    2.00    0.00   -2.19   -5.36   39.20
	 6    2.50    0.00   -2.74   -6.71   41.24
	 7    3.00    0.00   -3.29   -8.05   43.28
	 8    3.50    0.00   -3.84   -9.40   45.32
	 9    4.00    0.00   -4.39  -10.74   47.36
	10    4.50    0.00   -4.93  -12.09   49.39
	11    5.00    0.00   -5.48  -13.44   51.42

	 d) Trimer system pivot in last riser:
	 -------------------------------------------
	 i   alpha       A       B       C  Calage
	 1    0.00    0.00    0.00    0.00   31.00
	 2    0.50    1.34    0.80    0.00   33.05
	 3    1.00    2.69    1.60    0.00   35.11
	 4    1.50    4.03    2.40    0.00   37.17
	 5    2.00    5.38    3.20    0.00   39.23
	 6    2.50    6.73    4.00    0.00   41.29
	 7    3.00    8.07    4.80    0.00   43.35
	 8    3.50    9.42    5.59    0.00   45.41
	 9    4.00   10.77    6.39    0.00   47.47
	10    4.50   12.12    7.19    0.00   49.53
	11    5.00   13.47    7.99    0.00   51.58


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.28" target="_blank">Laboratori d'envol website</a>
