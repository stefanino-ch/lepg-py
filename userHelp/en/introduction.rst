 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0

********************
Introduction to lepg
********************

Lepg is a graphical front end to the calculation programm lep written originally by Pere Casellas. The goal of Lepg is to provide an easy as possible GUI allowing 
to edit the data needed for wing calculation. 

The workflow: 

 .. image:: /images/workflow-en.png

Lepg does help editing the data and does take care about formatting the data in the files needed to run lep. But still some backround knowledge about the lep data is needed. 

Der farbige Hintergrund in den Eingabefelder zeigt das Resultat der Werte Prüfung welche im Hintergrund läuft:

.. image:: /images/input-validation-en.png

- grün: die Werte liegen innerhalb des definierten Wertebereiches
- gelb: lepg kann nicht mit Sicherheit feststellen dass der Wert gültig ist. In obigem Bild wurde ein Flügel-Massstab von 1:99 eingegeben. Dieser Wert liegt ausserhalb des Bereiches welcher für die Werteprüfung festgelegt wurde, kann aber in Spezialfällen trotzdem sinn machen.
- rot: hier ist definitiv etwas falsch

Nicht immer müssen in den Fenstern alle Parameter ausgefüllt werden:

.. image:: /images/num-of-params-en.png

grey fields indicate unused input fields depending on the currently selected parameter type.

The Online help does try to cover the most important topics. If you want or need to know it in all details you must have a look at Peres website |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/pre.en.html#2" target="_blank">Laboratori d'envol</a>