 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

----------
Planmarken
----------
In diesem Fenster können die Symbole in den DXF Dateien definiert werden. Es stehen verschiedene Formen 
zur Verfügung (Punkte, Kreise, Dreiecke, ....).

Hilfreich können eigene Symboldefinitionen sein wenn zum Beispiel Laser Plotter für das Ausschneiden 
der Einzelteile verwendet werden. 

Leparagliding kreiert zwei verschiedene Plantypen, einen für die verwendung mit normalen Druckern (print), 
und einen andern für die Verwendung mit Schneideplottern (laser). 

.. image:: /images/proc/marksTypes-de.png
   :width: 603
   :height: 286

Rohdaten::

	******************************************************
	*       20. Marks types
	******************************************************
	10
	typepoint   1  0.25  1.2     2  0.3  1.2
	typepoint2  1  0.25  1.2     2  0.2  1.2
	typepoint3  1  0.25  1.2     2  0.2  1.2
	typevent    1  10.   0.0     2  2.0  0.0
	typetab     1  10.   0.0     3  2.0  0.0
	typejonc    1  10.   0.0     2  2.0  0.0
	typeref     1  5.    1.      1  2.0  0.0
	type8       1  0.2   4.0     1  0.0  4.0
	type9       1  0.25  1.2     2  0.2  1.2
	type10      1  0.25  1.2     2  0.2  1.2

Anzahl Konfigurationen
----------------------
*Planmarken* ist eine **optionale Konfiguration**. 

Wenn Du keine speziellen Planmarken definieren willst setze den Wert von **Anzahl Konfigurationen** auf **0**.


  |

+-----------------+------------------------------+------------------------+-----------------------------+
| Markierungstyp  | **Print**                    | **Print**              | **Print**                   |
|                 | Form 1                       | Form 1 1. Wert         | Form 1 2. Wert              |
+-----------------+------------------------------+------------------------+-----------------------------+
| typepoint [1]_  | 1=Kreis/ Kreuz               |  Kreisradius  [mm]     | Offset [mm]                 |
|                 | 2=Kreis                      |                        |                             |
+-----------------+------------------------------+------------------------+-----------------------------+
| typepoint2 [2]_ | 1                            | 0.25                   | 1.2                         |
+-----------------+------------------------------+------------------------+-----------------------------+
| typepoint3 [2]_ | 1                            | 0.25                   | 1.2                         |
+-----------------+------------------------------+------------------------+-----------------------------+
| typevent        | 1=zwei grüne Punkte          | Punktdistanz oder      | Offset [mm]                 |
|                 | 2=Segment                    | Segment-Länge [mm]     |                             |
|                 | 3=Doppel-Segment             |                        |                             |
+-----------------+------------------------------+------------------------+-----------------------------+
| typetab         | 1=Drei orange Punkte         | Punktdistanz oder      | offset [mm]                 |
|                 | 2=Drei orange "full control" | Dreiecks-Höhe [mm]     |                             |
|                 | 3=Dreieck                    |                        |                             |
+-----------------+------------------------------+------------------------+-----------------------------+
| typejonc   [2]_ | 1                            | 10.                    | 0.0                         |
+-----------------+------------------------------+------------------------+-----------------------------+
| typeref    [2]_ | 1                            | 5.0                    | 0.0                         |
+-----------------+------------------------------+------------------------+-----------------------------+
| type8 [3]_      | 1                            | [6]_ Pos römische Nr   | [6]_ Vertikaler Offset [mm] |
|                 |                              | 0.0 ganz links         | zur Basislinie              |
|                 |                              | 1.0 ganz rechts        |                             |
|                 |                              | empfohlen 0.2 or 0.5   |                             |
+-----------------+------------------------------+------------------------+-----------------------------+
| type9 [4]_      | 1                            | 0.0                    | Zahlengrösse [cm]           |
|                 |                              |                        | Ein-Austrittskante          |
|                 |                              |                        | Rippen, Panels Eintrittsk.  |
+-----------------+------------------------------+------------------------+-----------------------------+
| type10 [5]_     | 1                            | 0.0                    | Zahlengrösse [cm]           |
|                 |                              |                        | Diagonalrippen              |
+-----------------+------------------------------+------------------------+-----------------------------+

  |

+-----------------+------------------------------+-----------------------------------+---------------------------------+
| Markierungstyp  | **Laser**                    | **Laser**                         | **Laser**                       |
|                 | Form 2                       | Form 2 1. Wert                    | Form 2 2. Wert                  |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typepoint [1]_  | 1=Punkt                      |  Kreisradius [mm]                 | Offset [mm]                     |
|                 | 2=Kreis                      |                                   |                                 |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typepoint2 [2]_ | 2                            | 0.2                               | 1.2                             |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typepoint3 [2]_ | 2                            | 0.2                               | 1.2                             |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typevent        | 1=zwei grüne Punkte          | Punktdistanz oder                 | Offset [mm]                     |
|                 | 2=Segment                    | Segment-Länge [mm]                |                                 |
|                 | 3=Doppel-Segment             |                                   |                                 |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typetab         | 1=Drei orange Punkte         | Punktdistanz oder                 | Offset [mm]                     |
|                 | 2=Drei orange "full control" | Dreiecks-Höhe [mm]                |                                 |
|                 | 3=Dreieck                    |                                   |                                 |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typejonc   [2]_ | 2                            | 2.0                               | 0.0                             |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| typeref    [2]_ | 1                            | 2.0                               | 0.0                             |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| type8 [3]_      | 1                            | 0.0                               | [6]_ Dist zwischen Punkten der  |
|                 |                              |                                   | römischen Nr [mm]. (Beeinflusst |
|                 |                              |                                   | die Zahlengrösse).              |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| type9 [4]_      | 1                            | [6]_ Dist zwischen Punkten der    | [6]_ Dist zwischen Punkten der  |
|                 |                              | römischen Nr [mm]. (Beeinflusst   | römischen Nr [mm]. (Beeinflusst |
|                 |                              | die Zahlengrösse). Für **Stäbchen | die Zahlengrösse). Für          |
|                 |                              | Eintrittskante**                  | **Rippen**                      |
+-----------------+------------------------------+-----------------------------------+---------------------------------+
| type10 [5]_     | 1                            | 0.0                               | [6]_ Dist zwischen Punkten der  |
|                 |                              |                                   | römischen Nr [mm]. (Beeinflusst |
|                 |                              |                                   | die Zahlengrösse). Für          |
|                 |                              |                                   | **Diagonalrippen**              |
+-----------------+------------------------------+-----------------------------------+---------------------------------+

.. [1] typepoint allgemein verwendete Markierung

.. [2] noch nicht fertig implementiert, verwende die angegebenen Standard-Werte

.. [3] römische Nummern in Panels welche mit 3D Shaping definiert werden

.. [4] Nummerngrösse und Grösse der römischen Nummern in den Rippen

.. [5] Nummerngrösse in Diagonalrippen

.. [6] gilt für print and laser Version

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S20.jpg
   :width: 462
   :height: 660

   Typen 1,2,3,4,5,8,9,10 sind nun vollständig implementiert

.. figure:: http://laboratoridenvol.com/leparagliding/lep2images/S20-romanop-position.p.png
   :width: 462
   :height: 435

   Type8 Definition


Eine detaillierte Beschreibung in englisch findest Du auf der |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.20" target="_blank">Laboratori d'envol website</a>
