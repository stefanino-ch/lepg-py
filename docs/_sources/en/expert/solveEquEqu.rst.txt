 .. Author: Stefan Feuz; http://www.laboratoridenvol.com

 .. Copyright: General Public License GNU GPL 3.0
 
 .. _SolveEquEqu_en:

---------------------------
Solve Equilibrium Equations
---------------------------
Definition of the initial basic parameters used to solve the longitudinal equilibrium of the paraglider.
This section is informative and is used by the designer, to study the values of the forces involved in the
balance of the wing, the flight speed, the angles, and the glide coefficient.
To find realistic values, it is necessary to do the study simultaneously with the XFLR5 program or CFD
programs, and perform several iterations until satisfactory values are obtained. Currently, it is not yet
possible to fully automate this calculation. The designer must apply his criteria according to the type of
wing under study.

.. image:: /images/expert/solveEquEqu-en.png
   :width: 402
   :height: 346
   
Raw data::

   *******************************************************
   *       35. SOLVE EQUILIBRIUM EQUATIONS
   *******************************************************
   1
   g        9.807  m/s2 gravity of Earth
   ro       1.225  kg/m3 air mass density
   mu       18.46  muPa·s air dynamic viscosity (microPascals)
   V        12.4   m/s  estimated flow speed
   Alpha    9.45    deg  estimated wing angle of attact at trim speed
   Cl       0.67913       wing lift coefficient
   cle      1.0         lift correction coefficient
   Cd	    0.03790     wing drag coefficient
   cde      1.1        drag correction coefficient
   Cm       0.0         wing moment coefficient
   Spilot	0.438  m2   pilot+harness frontal surface
   Cdpilot  0.6         pilot+harness drag coefficient
   Mw       4.0    kg   wing mass
   Mp       70   kg   pilot mass included harness and instruments
   Pmc      0.2    m    pilot mass center below main karabiners
   Mql      8.0    g    one quick link mass (riser-lines)
   Ycp      0.575  m   y-coordinate center of pressure
   Zcp      0.395  m   z-coordinate center of pressure


**g** Gravity of Earth (9.80665 m/s2 standard gravity)

**ro** Air mas density kg/m3

**mu** Air dynamic viscosity microPascals·s

**V** Estimated initial flow speed m/s, used for first Cl, Cd, Cm values

**Alpha** Estimated ideal angle of attack deg. Max glide ratio according wing aerodynamic analysis

**Cl** Wing lift coefficient, obtained by analysis with individual profiles, XFLR5, or CFD

**Cle** Multiplier coefficient of Cl, to consider non-modeled geometries, use 1.0 in case of doubt

**Cd** Wing drag coefficient, obtained by analysis with individual profiles, XFLR5, or CFD

**Cde** Multiplier coefficient of Cd, to consider non-modeled geometries, use 1.15 in case of doubt. If
the Cd data comes from CFD this coefficient can be very close to 1.0. Currently studying how this
Leparagliding 3.20V Notes and changes over previous versions 9
coefficient affects the results. Probably by adjusting through Cde the expected GR, the rest of the
parameters will be very close to reality.

**Cm** Wing moment coefficient, obtained by analysis with individual profiles XFLR5, or CFD

**Spilot** Pilot + harness frontal surface (m2)

**Cdpilot** Pilot+harness drag coefficient (depends on the type of harness, especially if have fairings)

**Mw** Wing mass (kg) without lines and risers

**Mp** Pilot+harness+instruments mass (kg)

**Pmc** Pilot+harness mass center distance from main carabiners (m)

**Mql** Mass of one quicklink used to connect riser with lines (kg)

**Ycp** Y-coordinate of center of pressure (m), obtained by analysis with individual profiles, XFLR5,
or CFD

**Zcp** Z-coordinate of center of pressure (m), obtained by analysis with individual profiles, XFLR5, or
CFD

Remember that the axes used in LEparagliding are:

* Origin (0,0,0)= at the nose of the central profile section.

* X-axis horizontal and in the span direction

* Y-axis along the central chord

* Z-axis perpendicular to the XY plane and pointing down (not coincides with gravity axis)


A more detailed description you can find here |pere_link|.

.. |pere_link| raw:: html

	<a href="http://laboratoridenvol.com/leparagliding/manual.en.html#6.9" target="_blank">Laboratori d'envol website</a>

.. |manual_link| raw:: html

	<a href="http://www.laboratoridenvol.com/leparagliding/linesopt/lineopt.en.html" target="_blank">OPTIMIZE YOUR LINES IN LEPARAGLIDING</a>
