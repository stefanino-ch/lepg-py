 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

------------
Tuchspannung
------------
Im Fenster *Tuchspannung* editieren wir die Parameter aus dem 5. Abschnitt der lep Datei. 

.. image:: /images/proc/skinTension-de.png
   :width: 602
   :height: 286

Rohdaten::

	*************************************************************
	*           5. SKIN TENSION                                 *
	*************************************************************
	Extrados
	0.		0.	0.		0.
	7.5		1.3	10.		1.33
	15.		2.5	20.		2.5
	80.		2.5	80.		2.5
	90.		1.33	90.		1.33
	100.		0.0	100.		0.
	0.0114
	1000	1.0

Die Spannung von Ober- und Untersegel kann durch die Definition von zusätzlichen Verbreiterungen verändert werden. In der Basisversion können je 6 Punke definiert werden. Der Übergang zwischen den Punkten wird linear berechnet.

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S05_skintension_p.jpg

Obere Dist Eintrittskante
-------------------------
Distanz von der Eintrittskante in [% Flügeltiefe]

Obere Verbr
-----------
Grösse der Verbreiterung in [% Flügeltiefe]

Untere Dist Austrittskante
--------------------------
Distanz von der Austrittskante in [% Flügeltiefe]

Untere Verbr
------------
Grösse der Verbreiterung in [% Flügeltiefe]

Spann mini ribs
---------------
Hier geht es darum die Dehnung des Tuches zu korrigieren. 

.. image:: http://laboratoridenvol.com/leparagliding/lep2images/S05_Ripstop_elasticity.jpg

Im Zweifelsfall setze hier den Standardwert von **0.0114**

Anzahl Punkte und Koeff
-----------------------
Prinzipiell gibt es zwei verschiedene Interpretationen der beiden Werte. Beschrieben wird hier nur der empfohlene Anwendungsfall. 

Setze die Parameter auf die Werte:

**1000     1.0**

Die erste Zahl **"1000"** sagt dem Programm die maximal mögliche Präzision bei der Längenberechnung von Rippen und Panels zu benutzen. Typischerweise werden Werte besser 0.1 mm erreicht. 

Der zweite Wert beeinflusst noch einmal die Berechnung. Der Wert kann zwischen 0.0 und 1.0 verändert werden. 

"0.0" es werden keine Korrekturen berechnet, der erste Wert wird ausgehebelt. 

**"1.0"** es wird mit maximaler Genauigkeit gerechnet. 


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.5" target="_blank">Laboratori d'envol website</a>
