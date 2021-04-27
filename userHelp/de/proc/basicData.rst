 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

**********
Basisdaten
**********

Im Fenster Basisdaten wird ein Teil der Parameter aus dem ersten Abschnitt der Datendatei editiert. 

.. image:: /images/proc/basicData-de.png
   :width: 375
   :height: 258
 
Rohdaten::

  **************************************************************
  *             1. GEOMETRY                                    *
  **************************************************************
  * Brand name
  "LABORATORI D'ENVOL"
  * Wing name
  "gnu-A+test-3.10"
  * Drawing scale
  1.
  * Wing scale 
  1.
  * Number of cells
	  27
  * Number of ribs
	  28
  
Ein Zeichnungsmasstab von 1 bedeutet dass die Zeichnung im Masstab 1:1 ausgegeben werden. 

Mit dem Flügelmasstab kann das gesamte Design verkleinert oder vergrössert werden ohne dass 
man die einzelnen Parameter anpassen muss. Ein Flügelmasstab von 1 bedeutet dass das Desing 
mit den Originalwerten wie in lepg angegeben übernommen wird. 
  
Zwischen Anzahl Zellen und Rippen gibt es eine direkte Beziehung. Bei Werten welche so nicht sein können, werden die Eingabefelder rot umrandet. 
 
.. image:: /images/proc/basicDataError-de.png
   :width: 375
   :height: 258

Abhängig von der hier konfigurierten Anzahl Rippen gibt es weitere Fenster welche angepasst werden, z.B. Geometrie und Ankerpunkte. 


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.1" target="_blank">Laboratori d'envol website</a>
