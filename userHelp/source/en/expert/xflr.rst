 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0
 
 .. _xflr_en:

------------------------------
Create File for XFLR5 analysis
------------------------------
If you use this section, it will automatically be created in xflr5/ directory with a .xwimp file and
profiles in .dat format to use in an aerodynamic analysis with the XFLR5 program. The details of how
to do it are explained here: http://www.laboratoridenvol.com/info/lep2xflr5/lep2xflr5.html
Unfortunately with XFLR5 we cannot model paragliders with profile rotations in the Z angle, nor
single skin paragliders. CFD programs must be used for this type of paraglider.

.. image:: /images/expert/xflr-en.png
   :width: 402
   :height: 287
   
Raw data::

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

A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.9" target="_blank">Laboratori d'envol website</a>

.. |manual_link| raw:: html

	<a href="http://www.laboratoridenvol.com/leparagliding/linesopt/lineopt.en.html" target="_blank">OPTIMIZE YOUR LINES IN LEPARAGLIDING</a>
