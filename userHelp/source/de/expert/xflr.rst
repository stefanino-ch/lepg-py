 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0
 
 .. _xflr_de:

---------------------------------
Datei für XFLR5-Analyse erstellen
---------------------------------
Wenn Sie diesen Abschnitt verwenden, wird er automatisch im Verzeichnis xflr5/ mit einer .xwimp-Datei und
Profilen im .dat-Format zur Verwendung in einer aerodynamischen Analyse mit dem Programm XFLR5. Die Einzelheiten, wie
sind hier erklärt: http://www.laboratoridenvol.com/info/lep2xflr5/lep2xflr5.html
Leider können wir mit XFLR5 weder Gleitschirme mit Profilrotationen im Z-Winkel modellieren, noch
Single-Skin Schirme. Für diese Art von Schirmen müssen CFD-Programme verwendet werden.

.. image:: /images/expert/xflr-de.png
   :width: 402
   :height: 287

Rohdaten::

 *******************************************************
 *       36. CREATE FILES FOR XFLR5 ANALYSIS
 *******************************************************
 1
 * Panel parameters
 10 chord nr
 5 per cell
 1 cosine distribution along chord
 0 uniform along span
 * Include billowed airfoils (more accuracy)
 0

Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.9" target="_blank">Laboratori d'envol website</a>

.. |manual_link| raw:: html

	<a href="http://www.laboratoridenvol.com/leparagliding/linesopt/lineopt.en.html" target="_blank">OPTIMIZE YOUR LINES IN LEPARAGLIDING</a>
