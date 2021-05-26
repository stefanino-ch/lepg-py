 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------------
Einlassöffnungen
----------------
Hier kann die Form der Einlassöffnungen definiert werden. Zusätzlich besteht die Möglickeit zu definieren ob und zu welchem Panel die Verschlussstücke verbunden werden. 

Für die Verschlussstücke wird der Nähsaum automatisch berechnet wo notwendig. 

Die Segelspannung folgt automatisch den Parametern definiert *Tuchspannung*.

.. image:: /images/proc/glueVent-de.png
   :width: 350
   :height: 286
   
Rohdaten::

	*******************************************************
	*       26. GLUE VENTS
	*******************************************************
	1
	1   0
	2   0
	3   0
	4   0
	5   0
	6   0
	7   0
	8   0
	9   0
	10  0
	11   
	12  -2
	13  -1
	14  -1

Typ
----
*Einlassöffnungen* ist eine **optionale Konfiguration**.

Wenn die Standard Parameter verwendet werden sollen dann setze **Typ** auf **Standard**.

Wenn **Typ** auf **Benutzerdefiniert** gesetzt wird, dann generiert lepg automatisch die notwendigen Konfigurationszeilen basierend auf den Einstellungen für Anzahl Zellen und Rippen aus dem Fenster *Basisdaten*.

Zellen Nr
---------
Nummer der Zelle für welche die Konfiguratioszeile gilt.

Einl Parameter
--------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S26.jpg
   :width: 492
   :height: 653
   
**1** Verschlussstück ist Teil des Obersegels (Typisch bei Single Skin Flügeln)

**0** Verschlussstück ist nicht verbunden (offene Zelle, ober wenn spezielle Einlassöffnungen z.B. mit einem CAD kreiert werden sollen)

**-1** Verschlussstück ist Teil des Untersegels (normalerweise bei geschl Zellen)

**-2** diagonale Öffnung, links 100% offen, Verschlussstück ist Teil des Untersegels

**-3** diagonale Öffnung, rechts 100% offen, Verschlussstück ist Teil des Untersegels


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.26" target="_blank">Laboratori d'envol website</a>
