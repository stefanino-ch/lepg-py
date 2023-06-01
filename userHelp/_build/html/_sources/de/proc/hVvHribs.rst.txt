 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

--------------
Diagonalrippen
--------------
Der Abschnitt *Diagonalrippen* ist sehr warscheinlich derjenige welcher die meisten und komplexesten Parameter beinhaltet. 

Es gibt 6 verschiedene Typen von Diagonalrippen, für jeden Typ sind die Parameterdefinitionen immer ein wenig anders. 

**WICHTIG**

   Einstellige Typ Nummern (x: 1...6) verwenden absolute Masse in [cm] und werden skaliert mit Flügel-Massstab.

   Zweistellige Typ Nummern (xx: 11...16) verwenden die Massangaben in [% Profiltiefe]

**WICHTIG**

   NICHT ein- und zweistellige Typ Nummern in derselben Konfiguration verwenden. Hier gilt entweder oder!

.. image:: /images/proc/hVvHribs-de.png
   :width: 736
   :height: 286
   
Rohdaten::

	***************************************************
	*	12. H V and VH ribs
	***************************************************
	12
	80  150
	1   1  0  1  1  1  6.0  0  0  0
	2   1  0  2  1  2  6.0  0  0  0
	3   1  0  3  1  3  6.0  0  0  0
	4   1  0  4  1  4  6.0  0  0  0
	5   1  4  1  5  1  6.0  0  0  0
	6   1  4  2  5  2  6.0  0  0  0
	7   1  4  3  5  3  6.0  0  0  0
	8   1  4  4  5  4  6.0  0  0  0
	9   1  8  1  9  1  6.0  0  0  0
	10  1  8  2  9  2  6.0  0  0  0
	11  1  8  3  9  3  6.0  0  0  0
	12  6  8  4  9  4  6.0  0  0  0  11  12

Zchn Distanz horiz/ vert
------------------------
Mit diesen Werten steuert man die Distanz zwischen den einzelnen Rippen in Feld 2-4 auf dem Plan. 
Die Distanz wird multipliziert mit dem Zeichnungsmasstab. Wenn z.B. ein Wert von 80.0 cm und ein Zeichnungsmasstab von 1.5 wird die totale Distanz 80* 1.5 betragen. 

.. image:: /images/proc/hVvHribsSpacing.png
   :width: 370
   :height: 380

Anz Konfigurationen
-------------------
*Diagonalrippen* ist eine **optionale Konfiguration**.

Wenn Du keine Diagonalrippen verwenden willst da setze die **Anz Konfigurationen** auf **0**.

Typ 1/ 11: Horizontales Band zwischen Rippe i1 und Rippe i2
-----------------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib1_p.jpg

+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib      | Param A    | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  |Param I   |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 1/ 11   | Rippe i1     | Ebene [1]_ | Rippe i2     | Ebene [1]_   | Breite [2]_  | 0            | 0            | 0            | 0        | 0        |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [1]

    Hier referenziert man auf die Ebenen der Aufhängepunkte Ebene 1= Aufh Pt A, Ebene 2= Aufh Pt B, ….

.. [2]

    Typ x: Breite in [cm]

    Typ xx: Breite in [% Flügeltiefe]


Typ 2/ 12: Partielle, diagonale V-Rippe zentriert in Rippe i
------------------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib2_p.jpg

+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib      | Param A    | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  |Param I   |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 2/ 12   | Mittl Rippe  | Ebene [1]_ | links [3]_   | rechts [4]_  | r- [5]_      | r+ [6]_      | Höhe [7]_    | beta [8]_    | 0        | 0        |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [3] links

   "0": die linke Diagonalrippe wird nicht berechnet

   "1": die linke Diagonalrippe wird berechnet und auf der Zeichnung gezeigt

.. [4] rechts

   "0": die rechte Diagonalrippe wird nicht berechnet

   "1": die rechte Diagonalrippe wird berechnet und auf der Zeichnung gezeigt

.. [5] untere Rippenbreite

    Typ x: Breite in [cm]

    Typ xx: Breite in [% Flügeltiefe]

.. [6] obere Rippenbreite

    Typ x: Breite in [cm]

    Typ xx: Breite in [% Flügeltiefe]
   
.. [7]

   Typ x: Höhe in [cm]

   Typ xx: Höhe in [% Profiltiefe]

.. [8] beta

   Der Winkel des oberen Abschlusses

Type 3/ 13: Volle, diagonale V-Rippe zentriert in Rippe i
---------------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib3_p.jpg

+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib      | Param A    | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  |Param I   |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 3/ 13   | Mittl Rippe  | Ebene [1]_ | links [3]_   | rechts [4]_  | r- [5]_      | r+ [6]_      | 0            | 0            | 0        | 0        |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+


Typ 4/ 14: Diagonal-horizontal Rippe zwischen Rippe i-1 to i+2
--------------------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_Minirib4_p.jpg

+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib      | Param A    | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  |Param I   |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 4/ 14   | Rippe i1     | Ebene [1]_ | links [3]_   | rechts [4]_  | r- [5]_      | r+ [6]_      | Höhe [7]_    | beta [8]_    | 0        | 0        |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+


Typ 5/ 15: Volle, kontinuerliche Diagonalrippe zentriert in Rippe i
-------------------------------------------------------------------
.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_VRF-p.p.jpg

   Volle, kontinuerliche Diagonalrippe mit parabolischen Öffnungen (Höhe < 100%)

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_VRF-e.p.jpg

   Volle, kontinuerliche Diagonalrippe mit elliptischen Öffnungen (Höhe < 100%)

+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib      | Param A    | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  |Param I   |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 5/ 15   | Rippe i1     | Ebene [1]_ | links [3]_   | rechts [4]_  | alpha1       | alpha2       | Höhe [9]_    | r [10]_      | 0        | 0        |
|         |              |            |              |              | Eintritts K  | Austritts K  |              |              |          |          |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [9]

   Höhe < 100[%]: parabolische Öffnung
   
   Höhe > 100[%]: elliptische Öffnung
   
.. [10]

   Typ x: in [cm]

   Typ xx: in [% Profiltiefe]

**WICHTIG**
   Wenn Rippen dieses Typs definiert werden muss folgendes beachtet werden:

   * Die Anzahl Aufhängepunkte der Rippe "i" und von denjenigen zur linken und rechten Seite muss identisch sein. Dies auch wenn dort keine Leinen befestigt werden sollen (virtuelle Aufhängepunkte)

   * Wenn Du Typ 5 Rippen definierst, dann musst Du für jeden Aufhängepunkt eine Konfigurationszeile schreiben

   Beispiel für 4 Aufhängepunkte::

	5       5 1     1 1    60.0    60.0    80.     7.
	5       5 2     1 1    60.0    60.0    80.     7.
	5       5 3     1 1    60.0    60.0    80.     7.
	5       5 4     1 1    60.0    60.0    80.     7.

Typ 6/ 16: Universelle Diagonalrippe zwischen Rippe i und Rippe i+1
-------------------------------------------------------------------
Typ 6/16 ist eine universelle Diagonalrippe mit einer trapezform zwischen Rippe i und Rippe i+1. 
Die Rippe ist komplett konfigurierbar in der Grösse und Position. 
Ursprüngliche wurde das Design gemacht für die Entwiklung von Hochleistungsflügeln der CCC Klasse welche 4-5 Zellen ohne Aufhängepunkte haben. 
Dieser Typ kann auch für einfachste Flügel verwendet werden und die Diagonalrippen von oben ersetzen. Es handelt sich hier um eine universelle Definition welche nicht zwingend an die Position der Aufhängepunkte gebunden ist. 

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S12_V-ribtype6.p.jpg

+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| Type    | Ini Rib      | Param A    | Param B      | Param C      | Param D      | Param E      | Param F      | Param G      | Param H  |Param I   |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+
| 6/ 16   | rib i        | pos [11]_  | height [12]_ | r+ [13]_     | r- [14]_     | rib i+1      | pos [11]_    | height [12]_ | r+ [13]_ | r- [14]_ |
+---------+--------------+------------+--------------+--------------+--------------+--------------+--------------+--------------+----------+----------+

.. [11]

   Typ x: in [cm]

   Typ xx: in [% Flügeltiefe]

.. [12]

   [% Profiltiefe]

.. [13]

   Typ x: in [cm]

   Typ xx: in [% Flügeltiefe]

.. [14]

   Typ x: in [cm]

   Typ xx: in [% Flügeltiefe]

Sortieren
---------
Mit der Schaltfläche **Sortieren** können die Zeilen neu angeordnet werden. Wenn das gemacht werden soll kannst Du die neuen Nummern in der ersten Spalte einsetzten und anschliessend mit der Schaltfläche die Tabelle neu sortieren. 


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.12" target="_blank">Laboratori d'envol website</a>
