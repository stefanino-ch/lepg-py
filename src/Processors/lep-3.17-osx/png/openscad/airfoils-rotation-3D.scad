// Airfoils rotation in tree-axes test
// Laboratori d'envol - Pere Casellas
// 20210814
// Load external airfoil chord = 280 cm in file gnuLAB3.dxf

//////////////////////////////////////////////////////
// PARAMETERS
//////////////////////////////////////////////////////
// Rotation angles
// Rotation around axis parallel to X
washin=20.0;
washin_pos=50;
// Rotation around axis Y
beta=90.0;
// Rotation around axis parallel to Z
rotz=35.0;
rotz_pos=50.0;

// Calculed parameters
pX=280*washin_pos/100;
echo(pX);
pZ=280*rotz_pos/100;

////////////////////////////////////////////////////
// Set visibility parameters
vis_ini=1;  // view initial airfoil (grey)
vis_rX=1;  // view washin airfoil (red)
vis_rY1=1; // view Y-local rotated airfoil (yellow)
vis_rY2=1;  // view Y-global rotated airfoil (green)
vis_rZ1=1;  // view Z-local rotated airfoil (orange)
vis_rZ2=1;  // view Z-global rotated airfoil (blue), still not available
////////////////////////////////////////////////////

// Draw initial airfoil (grey)
if (vis_ini==1) {
    
color ([0.9,0.9,0.9]) {
translate([0,0,0])    
rotate ([0,0,0])
rotate ([90,0,90]) 
linear_extrude(height = 1, center = false, convexity = 10)
   import (file = "gnuLAB3.dxf", layer = "air");
}   
}

// Draw washin airfoil (red)
if (vis_rX==1) {
    
color ([1,0,0]) {
translate([0,pX*(1-cos(washin)),pX*sin(washin)])    
rotate ([-washin,0,0])
rotate ([90,0,90]) 
linear_extrude(height = 1.0, center = false, convexity = 10)
   import (file = "gnuLAB3.dxf", layer = "air");
}   
}

// Draw airfoil rotated around global Y (green)
if (vis_rY1==1) {
    
color ([0,1,0]) {
rotate ([0,beta,0])
translate([0,pX*(1-cos(washin)),pX*sin(washin)])    
rotate ([-washin,0,0])
rotate ([90,0,90]) 
linear_extrude(height = 1.0, center = false, convexity = 10)
   import (file = "gnuLAB3.dxf", layer = "air");
}   
}

// Draw airfoil rotated around local Y (yellow)
if (vis_rY2==1) {
    
color ([1,1,0]) {
translate([0,pX*(1-cos(washin)),pX*sin(washin)])    
rotate ([-washin,0,0])
rotate ([90,0,90]) 
rotate ([beta,0,0])
linear_extrude(height = 1.0, center = false, convexity = 10)
   import (file = "gnuLAB3.dxf", layer = "air");
}   
}

// Draw airfoil rotated around local Z (orange)
if (vis_rZ1==1) {
    
color ([0.9,0.6,0]) {
rotate ([0,beta,0])
translate([0,pX*(1-cos(washin)),pX*sin(washin)])    
rotate ([-washin,0,0])
rotate ([90,0,90]) 
translate ([pZ*(1-cos(rotz)),0,pZ*sin(rotz)])
rotate ([0,rotz,0])
linear_extrude(height = 1.0, center = false, convexity = 10)
   import (file = "gnuLAB3.dxf", layer = "air");
}   
}

// Draw airfoil rotated around global Z (blue)
if (vis_rZ2==1) {
    
color ([0.2,0.0,1]) {
rotate ([0,beta,0])
translate([0,pX*(1-cos(washin)),pX*sin(washin)])  
translate ([pZ*sin(rotz),pZ*(1-cos(rotz)),0])
rotate ([0,0,rotz])  
rotate ([-washin,0,0])
rotate ([90,0,90]) 
linear_extrude(height = 1.0, center = false, convexity = 10)
   import (file = "gnuLAB3.dxf", layer = "air");
}   
}


