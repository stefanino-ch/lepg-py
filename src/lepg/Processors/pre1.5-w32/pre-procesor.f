c***************************************************************
c      LE PARAGLIDING (PRE-PROCESSOR OPTIONAL MODULE)
c      Pere Casellas 2010-2018
c      Laboratori d'envol
c      http://www.laboratoridenvol.com
c      pere AT laboratoridenvol DOT com
c      Version 1.0: 2013-06-16 "Kemerovo"
c      Version 1.1: 2013-06-24 "Kemerovo"
c      Version 1.2: 2015-09-05 "Gurzuf"
c      Version 1.3: 2016-04-17 "Utah"
c      Version 1.4: 2016-08-22
c      Version 1.5: 2018-12-07
c      FORTRAN g95 (GNU/Linux)
c      GNU General Public License 3.0 (http://www.gnu.org)
c***************************************************************

       program preprocessor

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      1. VARIABLE NAMES
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      wname wing name
c      nomp  parameter name
c      a1    parameter (horizontal axis ellipse)
c      b1    parameter (vertical axis ellipse)
c      x1    paramener (change of analytical curve)
c      xm    half span
c      c0    parameter parabola adjustement
c      xk    parameter
c      span  wing span
c      jcontrol integer
c      b11
c      sepx, sepy
c      tetha angle in radians
c      xq, yq point in analytical curve
c      xp, yp next point in analytical curve
c      xq1(k), yq1(k)
c      xp1(k), yp1(k) leading edge in a vector
c      xle(k) 
c      yle(k)  leading edge in a vector K=1 to kmax1
c      chordmax
c      xq2(k), yq2(k)
c      xp2(k), yp2(k) trailing edge in a vector
c      xted(k) 
c      yted(k)  leading edge in a vector K=1 to kmax2
c      ivault vault type
c      xlong
c      xlongg accumuled vault length
c      theta1
c      theta2
c      xq3(k), yq3(k)
c      xp3(k), yp3(k) vault in a vector
c      y1
c      dy
c      c1
c      kmax3 max points vault
c      xvault(k)
c      yvault(k)
c      xscale parameter vault length adjustement
c      ra1, ... ra4 radius
c      alp1 ... alp4 angles
c      o1x ... o4x
c      o1y ... o4y centers
c      angle
c      xtras
c      nribs
c      ncells
c      xm1, bm1, xm2, bm2 interpolation values
c
c      atrapz() Cell surface
c      area wing surface flat

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      2. VARIABLES TYPE DECLARATION
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       real rib(0:100,100)

       character*50 wname, bname, nomair(100)
       character*50 xtext, nomp
       character*2 atp      

       real theta
      
       real xsob(10),ysob(10)
   
       real farea,parea,fspan,pspan,faratio,paratio,flattening  

       real area

       real atrapz(0:100)
      
       integer linecolor, pointcolor, txtcolor

       integer evenodd nribss ncells

       integer nte nle nva

       integer npce, npc1e(100), npc2e(20), npc3e(100,20)
       integer npci, npc1i(100), npc2i(20), npc3i(100,20)
       real xpc1e(100,20), xpc2e(100,20), xpc1i(100,20), xpc2i(100,20)

       real xle(100,20), xleinc(100,20), xpc3e(100,20), ypc3e(100,20)
       real xli(100,20), xliinc(100,20), xpc3i(100,20), ypc3i(100,20)

       real  xextra(100), xrade(100), xintra(100), xradi(100)

       real xarp(10), yarp(10)

       real hdist(100), hangle(100)

       real xq1(500),yq1(500),xp1(500),yp1(500)
       real xq2(500),yq2(500),xp2(500),yp2(500)
       real xq3(500),yq3(500),xp3(500),yp3(500)

       real xled(300), xted(300), yled(300), yted(300)
       real xvault(500), yvault(500)

       real xtri(50),ytri(50)

       real csus(10,10), cdis(10,10)

       real aload(100,10), xload(500), xlide(500), xlifi(500)
       real lvcx(300,30), lvcy(300,30),rvcx(300,30),rvcy(300,30)

       real anccont(100,10)

       real bd(10,10)

       real le_(3000,2), te_(3000,2), va_(3000,2)

       real xexp, xex1, xex2, x1, x2, c0, c01, c02

c      real pi

       pi=4.*atan(1.)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      3. INIT
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       write (*,*)
       write (*,*) "LABORATORI D'ENVOL PARAGLIDING"
       write (*,*)
       write (*,*) "GEOMETRY PRE-PROCESSOR"
       write (*,*) "Version 1.5 ""Baldiri"" (2018-12-07)"
       write (*,*) "Pere Casellas"
       write (*,*) "pere@laboratoridenvol.com"
       write (*,*) "GNU General Public License 3.0 http://www.gnu.org"
       write (*,*)

       open(unit=20,file='geometry.dxf')
       open(unit=22,file='pre-data.txt')
       open(unit=23,file='geometry-out.txt')
       open(unit=24,file='ltv.txt')
     
       
       write (*,*) "Auxiliar geometry matrix for use with", 
     + " LEparagliding 2.81"
       write (*,*)
       write (*,*) "Rib	x-rib      y-LE       y-TE   	xp	z",
     + "	beta      RP        Washin"
       write (*,*) 
       
       call dxfinit(20)

       
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     GEOMETRY PRE-PROCESSOR
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      1. Leading edge
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       a1=613.4546
c       b1=181.03
c       x1=392.116
c       xm=575.5
c       xk=0.000911648946

       
       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) 
       read (22,*) wname
       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) ilead
       read (22,*) nomp, a1
       read (22,*) nomp, b1
       read (22,*) nomp, x1
       read (22,*) nomp, x2
       read (22,*) nomp, xm
       read (22,*) nomp, c01
       read (22,*) nomp, xex1
       read (22,*) nomp, c02
       read (22,*) nomp, xex2

c       xk=c0/((xm-x1)**2.)
       xk1=c01/((xm-x1)**xex1) ! New definition using xexp-parabola
       xk2=c02/((xm-x2)**xex2)

       span=xm*2.

       jcontrol=0
       k=0
       b11=b1

       sepx=0.
       sepy=b1

       do tetha=0,pi/2-0.01,0.01

       xq=a1*sin(tetha)
       yq=b1*cos(tetha)
       xp=a1*sin(tetha+0.01)
       yp=b1*cos(tetha+0.01)
       
c      Leading edge definition if x < x1
       if (xq.lt.x1.and.jcontrol.eq.0) then

       k=k+1

       xq1(k)=xq
       yq1(k)=yq
       xp1(k)=xp
       yp1(k)=yp

       xled(k)=xq
       yled(k)=yq

       end if

c      Leading edge definition if x >= x1
       if (xq.ge.x1.and.jcontrol.lt.2) then

       k=k+1

       jcontrol=1

       xq=a1*sin(tetha)
       yq=b1*cos(tetha)
       xp=a1*sin(tetha+0.01)
       yp=b1*cos(tetha+0.01)

c      Redefine xp yp if last segment
       if (xq.lt.xm.and.xp.ge.xm) then
       xp=xm
       yp=b1*cos(asin(xp/a1))
       jcontrol=2
       end if

c      Simple correction
       if (xq.ge.x1.and.xq.lt.x2) then
       yq=yq-(xk1*(xq-x1)**xex1)
       yp=yp-(xk1*(xp-x1)**xex1)
       end if

c      Double correction
       if (xq.ge.x2) then
       yq=yq-(xk1*(xq-x1)**xex1)-(xk2*(xq-x2)**xex2)
       yp=yp-(xk1*(xp-x1)**xex1)-(xk2*(xp-x2)**xex2)
       end if

       xq1(k)=xq
       yq1(k)=yq
       xp1(k)=xp
       yp1(k)=yp

       xled(k)=xq
       yled(k)=yq
       xled(k+1)=xp
       yled(k+1)=yp

       end if

       kmax1=k

       end do

c      Leading edge

       write (24,*) "Leading edge coordinates:"
       write (24,*) kmax1+1

       nle=kmax1+1

       do k=1,kmax1

       call line(xq1(k)+sepx,-yq1(k)+sepy,xp1(k)+sepx,-yp1(k)+sepy,1)
       call line(-xq1(k)+sepx,-yq1(k)+sepy,-xp1(k)+sepx,-yp1(k)+sepy,1)

c      Write leding edge coordinates
       write (24,'(I3,3x,F10.4,3x,F10.4)') k,xq1(k)+sepx,-yq1(k)+sepy
   
c      Set variable le_   
       le_(k,1)=xq1(k)+sepx
       le_(k,2)=-yq1(k)+sepy

       end do

c      Last coordinate
       write (24,'(I3,3x,F10.4,3x,F10.4)') 
     + kmax1+1,xp1(kmax1)+sepx,-yp1(kmax1)+sepy

c      Set variable le_
       k=nle   
       le_(k,1)=xp1(k-1)+sepx
       le_(k,2)=-yp1(k-1)+sepy

       chordmax=b1 !def provisional

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      2. Trailing edge
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       a1=674.8918
c       b1=129.7418
c       x1=392.116
c       xm=575.5
c       xk=0.000110735
c       y0=40.05091

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) itrail
       read (22,*) nomp, a1
       read (22,*) nomp, b1
       read (22,*) nomp, x1
       read (22,*) nomp, xm
       read (22,*) nomp, c0
       read (22,*) nomp, y0
       read (22,*) nomp, xexp

c       xk=c0/((xm-x1)**2.)
       xk=c0/((xm-x1)**xexp) ! New definition using xexp-parabola


       chordmax=chordmax+b1-y0

       jcontrol=0
       k=0

       sepx=0.
       sepy=sepy

       do tetha=0,(pi/2.)-0.01,0.01

       xq=a1*sin(tetha)
       yq=-b1*cos(tetha)+y0
       xp=a1*sin(tetha+0.01)
       yp=-b1*cos(tetha+0.01)+y0
       
c      Trailing edge definition if x < x1
       if (xq.lt.x1.and.jcontrol.eq.0) then

       k=k+1

       xq2(k)=xq
       yq2(k)=yq
       xp2(k)=xp
       yp2(k)=yp

       xted(k)=xq
       yted(k)=yq

       end if

c      Trailing edge definition if x >= x1
       if (xq.ge.x1.and.jcontrol.lt.2) then

       k=k+1

c      when xq ge x1 jcontrol=1
       jcontrol=1

       xq=a1*sin(tetha)
       yq=-b1*cos(tetha)+y0
       xp=a1*sin(tetha+0.01)
       yp=-b1*cos(tetha+0.01)+y0

       if (xq.lt.xm.and.xp.ge.xm) then
       xp=xm
       yp=-b1*cos(asin(xp/a1))+y0
       jcontrol=2
       end if

       yq=yq-xk*(xq-x1)**xexp
       yp=yp-xk*(xp-x1)**xexp

       xq2(k)=xq
       yq2(k)=yq
       xp2(k)=xp
       yp2(k)=yp

       xted(k)=xq
       yted(k)=yq
       xted(k+1)=xp
       yted(k+1)=yp

       end if

       kmax2=k

       end do 

c      Trailing edge

       write (24,*) "Trailing edge coordinates:"
       write (24,*) kmax2+1

       nte=kmax2+1

       do k=1,kmax2

       call line(xq2(k)+sepx,-yq2(k)+sepy,xp2(k)+sepx,-yp2(k)+sepy,1)
       call line(-xq2(k)+sepx,-yq2(k)+sepy,-xp2(k)+sepx,-yp2(k)+sepy,1)

c      Write leding edge coordinates
       write (24,'(I3,3x,F10.4,3x,F10.4)') k,xq2(k)+sepx,-yq2(k)+sepy

c      Set variable te_   
       te_(k,1)=xq2(k)+sepx
       te_(k,2)=-yq2(k)+sepy

       end do

c      Last coordinate
       write (24,'(I3,3x,F10.4,3x,F10.4)') 
     + kmax2+1,xp2(kmax2)+sepx,-yp2(kmax2)+sepy

c      Set variable le_
       k=nte   
       te_(k,1)=xp2(k-1)+sepx
       te_(k,2)=-yp2(k-1)+sepy


c     Draw Tips

      call line(xp1(kmax1)+sepx,-yp1(kmax1)+sepy,
     + xp2(kmax2)+sepx,-yp2(kmax2)+sepy,1)

      call line(-xp1(kmax1)+sepx,-yp1(kmax1)+sepy,
     + -xp2(kmax2)+sepx,-yp2(kmax2)+sepy,1)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      3. Vault
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       pi=4.*atan(1.)

c       a1=447.6874
c       b1=253.0156
c       x1=307.6115
c       c1=24.7969

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) ivault

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vault type 1 (ellipse - cosinus modification)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ivault.eq.1) then

       read (22,*) nomp, a1
       read (22,*) nomp, b1
       read (22,*) nomp, x1
       read (22,*) nomp, c1

       xlong=0.
       xlongg=0.
       jcontrol=0
       k=0

       sepx=0.
       sepy=-400.

c      Main vault in 300 points max
       do i=0,299

       theta1=(2.*atan(1.))*float(i)/300.

       xq=a1*sin(theta1)

       yq=b1*sqrt(1.-(xq*xq/(a1*a1)))

       theta2=(2.*atan(1.))*float(i+1)/300.

       xp=a1*sin(theta2)

       if (xp.ge.x1) then
       xp=x1
       end if

       yp=b1*sqrt(1.-(xp*xp/(a1*a1)))

       if (xq.lt.x1) then

       k=k+1

       xq3(k)=xq
       yq3(k)=yq
       xp3(k)=xp
       yp3(k)=yp

       end if

c      Modification zone

       if (xq.ge.x1.and.jcontrol.eq.0) then
 
       y1=b1*sqrt(1.-(x1*x1/(a1*a1)))

c      Define modification zone in 100 steps

       do j=0,99

       dy=y1/100.

       yq=y1-dy*float(j)

       yp=yq-dy

       xq=a1*sqrt(1-(yq*yq/(b1*b1)))+
     + c1*(1-(cos((y1-yq)*pi/(1.*y1))+1)*0.5)

       xp=a1*sqrt(1-(yp*yp/(b1*b1)))+
     + c1*(1-(cos((y1-yp)*pi/(1.*y1))+1)*0.5)

       k=k+1

       xq3(k)=xq
       yq3(k)=yq
       xp3(k)=xp
       yp3(k)=yp

       end do

       jcontrol=1

       end if

       end do

       kmax3=k

c      Define vault vectors

       do k=1,kmax3

       xvault(k)=xq3(k)
       yvault(k)=yq3(k)
       xvault(k+1)=xp3(k)
       yvault(k+1)=yp3(k)

       xlongg=xlongg+sqrt((xvault(k)-xvault(k+1))**2.+
     + (yvault(k)-yvault(k+1))**2.)

       end do

       if (abs(yvault(kmax3+1)).lt.0.0001) then
       yvault(kmax3+1)=0.0
       end if

c      Redefine vault to adjust length

       xscale=xm/xlongg

       xlongg=0.

       do k=1,kmax3
       xvault(k)=xvault(K)*xscale
       yvault(k)=yvault(k)*xscale
       end do
       xvault(kmax3+1)=xvault(kmax3+1)*xscale
       yvault(kmax3+1)=yvault(kmax3+1)*xscale

c      Virtual point kmax3+2
       xvault(kmax3+2)=xvault(kmax3+1)+(xvault(kmax3+1)-xvault(kmax3))
       yvault(kmax3+2)=yvault(kmax3+1)+(yvault(kmax3+1)-yvault(kmax3))

       b1=yvault(1)

c      Calculate vault lenght
       do k=1,kmax3
       xlongg=xlongg+sqrt((xvault(k)-xvault(k+1))**2.+
     + (yvault(k)-yvault(k+1))**2.)
       end do

c      Redefine q p

       do k=1,kmax3+1
       xq3(k)=xvault(k)
       yq3(k)=yvault(k)
       xp3(k)=xvault(k+1)
       yp3(k)=yvault(k+1)
       end do
    
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vault type 2 (4 successive tangent circles)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ivault.eq.2) then

       sepx=0.
       sepy=-400.

       xlongg=0.
       xlonggg=0.

c      Read data     
       read (22,*) ra1, alp1
       read (22,*) ra2, alp2
       read (22,*) ra3, alp3
       read (22,*) ra4, alp4

c      Circles centers
       o1x=0.
       o2x=o1x+(ra1-ra2)*sin(alp1*pi/180.)
       o3x=o2x+(ra2-ra3)*sin((alp1+alp2)*pi/180.)
       o4x=o3x+(ra3-ra4)*sin((alp1+alp2+alp3)*pi/180.)

       o1y=-400.
       o2y=o1y+(ra1-ra2)*cos(alp1*pi/180.)
       o3y=o2y+(ra2-ra3)*cos((alp1+alp2)*pi/180.)
       o4y=o3y+(ra3-ra4)*cos((alp1+alp2+alp3)*pi/180.)

       k=0

c      First circle

       do angle=0.,alp1-(alp1/99.),alp1/99.

       k=k+1

       xq3(k)=o1x+ra1*sin(pi*angle/180.)
       yq3(k)=o1y+ra1*cos(pi*angle/180.)
       xp3(k)=o1x+ra1*sin(pi*(angle+(alp1/99.))/180.)
       yp3(k)=o1y+ra1*cos(pi*(angle+(alp1/99.))/180.)

c       write (*,*) "1 ",k,angle,xq3(k),yq3(k)

       end do

c      Second circle

c       k=k-1

       do angle=alp1,alp1+alp2-(alp2/99.),alp2/99.

       k=k+1

       xq3(k)=o2x+ra2*sin(pi*angle/180.)
       yq3(k)=o2y+ra2*cos(pi*angle/180.)
       xp3(k)=o2x+ra2*sin(pi*(angle+(alp2/99.))/180.)
       yp3(k)=o2y+ra2*cos(pi*(angle+(alp2/99.))/180.)

c       write (*,*) "2 ",k,angle,xq3(k),yq3(k)

       end do

c      Third circle

c       k=k-1

       do angle=alp1+alp2,alp1+alp2+alp3-(alp3/99.),alp3/99.

       k=k+1

       xq3(k)=o3x+ra3*sin(pi*angle/180.)
       yq3(k)=o3y+ra3*cos(pi*angle/180.)
       xp3(k)=o3x+ra3*sin(pi*(angle+(alp3/99.))/180.)
       yp3(k)=o3y+ra3*cos(pi*(angle+(alp3/99.))/180.)

c       write (*,*) "3 ",k,angle,xq3(k),yq3(k)


       end do

c      Fourth circle

c       k=k-1

       do angle=alp1+alp2+alp3,alp1+alp2+alp3+alp4-(alp4/99.),alp4/99.

       k=k+1

       xq3(k)=o4x+ra4*sin(pi*angle/180.)
       yq3(k)=o4y+ra4*cos(pi*angle/180.)
       xp3(k)=o4x+ra4*sin(pi*(angle+(alp4/99.))/180.)
       yp3(k)=o4y+ra4*cos(pi*(angle+(alp4/99.))/180.)

c       write (*,*) "4 ",k,angle,xq3(k),yq3(k)

       end do

       kmax3=k

c      Define vault vectors

       do k=1,kmax3

       xvault(k)=xq3(k)
       yvault(k)=yq3(k)
       xvault(k+1)=xp3(k)
       yvault(k+1)=yp3(k)

       xlongg=xlongg+sqrt((xvault(k)-xvault(k+1))**2.+
     + (yvault(k)-yvault(k+1))**2.)

       end do

c      Redefine vault to adjust length

c       write (*,*) "xm, xlongg ", xm, xlongg

       xscale=xm/xlongg

       xlongg=0.

       do k=1,kmax3
       xvault(k)=xvault(K)*xscale
       yvault(k)=yvault(k)*xscale
       end do
       xvault(kmax3+1)=xvault(kmax3+1)*xscale
       yvault(kmax3+1)=yvault(kmax3+1)*xscale

c      Virtual point kmax3+2
       xvault(kmax3+2)=xvault(kmax3+1)+(xvault(kmax3+1)-xvault(kmax3))
       yvault(kmax3+2)=yvault(kmax3+1)+(yvault(kmax3+1)-yvault(kmax3))

       do k=1,kmax3+2
c       write (*,*) kmax3,k,xvault(k),yvault(k)
       end do

c      Calculate vault lenght
       do k=1,kmax3
       xlongg=xlongg+sqrt((xvault(k)-xvault(k+1))**2.+
     + (yvault(k)-yvault(k+1))**2.)
       end do

c       write (*,*) "xlong final ", xlongg

c      Translate vault equivalent to type 1

       xtras=yvault(kmax3+1)
       b1=yvault(1)-yvault(kmax3+1)

       do k=1,kmax3+1
       xvault(k)=xvault(k)
       yvault(k)=yvault(k)-xtras
       end do
       xvault(kmax3+2)=xvault(kmax3+1)+(xvault(kmax3+1)-xvault(kmax3))
       yvault(kmax3+2)=yvault(kmax3+1)+(yvault(kmax3+1)-yvault(kmax3))
c     + -xtras

c      Redefine q p

       do k=1,kmax3+1
       xq3(k)=xvault(k)
       yq3(k)=yvault(k)
       xp3(k)=xvault(k+1)
       yp3(k)=yvault(k+1)

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vault drawing
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       write (24,*) "Vault coordinates:"
       write (24,*) kmax3+1

       do k=1,kmax3

       nva=kmax3+1

       call line(xvault(k)+sepx,-yvault(k)+sepy,
     + xvault(k+1)+sepx,-yvault(k+1)+sepy,3)
       call line(-xvault(k)+sepx,-yvault(k)+sepy,
     + -xvault(k+1)+sepx,-yvault(k+1)+sepy,1)

c      Write vault coordinates
       write (24,'(I3,3x,F10.4,3x,F10.4)') 
     + k,xvault(k)+sepx,-yvault(k)+sepy

c      Set variable va_   
       va_(k,1)=xvault(k)+sepx
       va_(k,2)=-yvault(k)+sepy
       
       end do

c      Write last vault coordinates
       k=kmax3+1
       write (24,'(I3,3x,F10.4,3x,F10.4)') 
     + k,xvault(k)+sepx,-yvault(k)+sepy

c      Set variable va_
       k=nva  
       va_(k,1)=xvault(k)+sepx
       va_(k,2)=-yvault(k)+sepy


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     4. Cells distribution
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) icontrol

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc      
c      4.1 Uniform rib distribution
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (icontrol.eq.1) then

       read (22,*) ncells

       call eo(ncells,evenodd,nribss)

c      Number of cells is odd number (imparell)

       if (evenodd.eq.1.) then

       do i=0,nribss-1
       rib(i,22)=span/ncells
       end do

       end if ! odd

c      Number of cells is even number (parell)

       if (evenodd.eq.0) then

       rib (0,22)=0.
       do i=1,nribss-1
       rib(i,22)=span/ncells
       end do

       end if ! even

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.2 Elliptical variation
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (icontrol.eq.2) then

       write (*,*) "Sorry, case rib_distribution=2 not implemented yet!"

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.3 Proportional to chord
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Case 3
       if (icontrol.eq.3) then

c      Amplification control coefficient xk
       read (22,*) xk 

       read (22,*) ncells

       call eo(ncells,evenodd,nribss)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case even
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (evenodd.eq.1) then

c      Fisrt computes uniform rib distribution
c      rib(i,22) = width of cell i
       do i=0,nribss-1
       rib(i,22)=span/ncells
       end do

c      Width correction using chord coeficients
c      Enough convergence in 5 steps !
       
       do ic=1,5

c      Computes x-rib rib(i,2)      
c      rib(1,2) = x coordinate of rib i   
       rib(1,2)=rib(0,22)/2.
       do i=2,nribss
       rib(i,2)=rib(i-1,2)+rib(i-1,22)
       end do

c      rib(i,3) Y Leading edge

       do i=1,nribss
       do k=1,kmax1+1

       if (xq1(k).lt.rib(i,2).and.xp1(k).ge.rib(i,2)) then

       xm1=(yp1(k)-yq1(k))/(xp1(k)-xq1(k))
       bm1=yq1(k)-xm1*xq1(k)

       rib(i,3)=-(xm1*rib(i,2)+bm1-b11)

       end if

       end do
       end do
     
c      rib(i,4) Y Trailing edge

       do i=1,nribss
       do k=1,kmax2

       if (xq2(k).lt.rib(i,2).and.xp2(k).ge.rib(i,2)) then

       xm2=(yp2(k)-yq2(k))/(xp2(k)-xq2(k))
       bm2=yq2(k)-xm2*xq2(k)

       rib(i,4)=-((xm2*rib(i,2)+bm2)-b11)

       end if

       end do
       end do

c      Local width correction coefficient ci

       do i=1,nribss
       coefl=((chordmax-abs((rib(i,3)-rib(i,4))))*xk+
     + abs(rib(i,3)-rib(i,4)))/chordmax
       rib(i-1,22)=(span/ncells)*coefl

       end do       

c      Recomputes span and global coefficient

       s=rib(0,22)/2.
       do i=1,nribss-1
       s=s+rib(i,22)
       end do
       coefg=span/(2.*s)

       do i=1,nribss
       rib(i-1,22)=rib(i-1,22)*coefg
       end do   

       end do  ! ic

       end if  ! even

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case odd
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (evenodd.eq.0) then

c      Define first cell and first rib
       rib(0,22)=0.
       rib(1,3)=0.
       rib(1,4)=chordmax
     
c      Fisrt computes uniform rib distribution
c      rib(i,22) = width of cell i
       do i=1,nribss-1
       rib(i,22)=span/ncells
       end do

c      Width correction using chord coeficients
c      Enough convergence in 5 steps !
       
       do ic=1,5

c      Computes x-rib rib(i,2)      
c      rib(1,2) = x coordinate of rib i   
       rib(1,2)=rib(0,22)/2.
       do i=2,nribss
       rib(i,2)=rib(i-1,2)+rib(i-1,22)
       end do

c      rib(i,3) Y Leading edge

       do i=2,nribss
       do k=1,kmax1+1

       if (xq1(k).le.rib(i,2).and.xp1(k).ge.rib(i,2)) then

       xm1=(yp1(k)-yq1(k))/(xp1(k)-xq1(k))
       bm1=yq1(k)-xm1*xq1(k)

       rib(i,3)=-(xm1*rib(i,2)+bm1-b11)

       end if

       end do
       end do
     
c      rib(i,4) Y Trailing edge

       do i=2,nribss
       do k=1,kmax2

       if (xq2(k).le.rib(i,2).and.xp2(k).ge.rib(i,2)) then

       xm2=(yp2(k)-yq2(k))/(xp2(k)-xq2(k))
       bm2=yq2(k)-xm2*xq2(k)

       rib(i,4)=-((xm2*rib(i,2)+bm2)-b11)

       end if

       end do
       end do

c      Local width correction coefficient ci

       do i=2,nribss
       coefl=((chordmax-abs((rib(i,3)-rib(i,4))))*xk+
     + abs(rib(i,3)-rib(i,4)))/chordmax
       rib(i-1,22)=(span/ncells)*coefl

       end do       

c      Recomputes span and global coefficient

       s=rib(0,22)/2.
       do i=1,nribss-1
       s=s+rib(i,22)
       end do
       coefg=span/(2.*s)

       do i=1,nribss
       rib(i-1,22)=rib(i-1,22)*coefg
       end do   

       end do  ! ic

       end if  ! odd

       end if  ! 3 distribution

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.4 Especified width
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      if (icontrol.eq.4) then

      read (22,*) nribss

      do i=0,nribss-1
      read (22,*) ii, rib(i,22)
      end do

c     computes semi-span    
      s=rib(0,22)/2.
      do i=1,nribss-1
      s=s+rib(i,22)
      end do
      skale=2.*s/span

c     normalize cell width
      do i=0,nribss-1
      rib(i,22)=rib(i,22)*skale
      end do

      end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     5. Auxiliar planform writing
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Compute rib(i,2) "x rib"
       
       rib(1,2)=rib(0,22)/2.

       do i=2,nribss
       rib(i,2)=rib(i-1,2)+rib(i-1,22)
       end do

       do i=1,nribss

       do k=1,kmax1

c      rib(i,3) Y Leading edge

       if (xq1(k).le.rib(i,2).and.xp1(k).ge.rib(i,2)) then

       xm1=(yp1(k)-yq1(k))/(xp1(k)-xq1(k))
       bm1=yq1(k)-xm1*xq1(k)

       rib(i,3)=-(xm1*rib(i,2)+bm1-b11)

       end if

       end do

       do k=1,kmax2

c      rib(i,4) Y Trailing edge

       if (xq2(k).le.rib(i,2).and.xp2(k).ge.rib(i,2)) then

       xm2=(yp2(k)-yq2(k))/(xp2(k)-xq2(k))
       bm2=yq2(k)-xm2*xq2(k)

       rib(i,4)=-((xm2*rib(i,2)+bm2)-b11)

       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       sepx=0.
       sepy=0.

       call line(rib(i,2)+sepx,rib(i,3)+sepy,
     + rib(i,2)+sepx,rib(i,4)+sepy,3)
       call line(-rib(i,2)+sepx,rib(i,3)+sepy,
     + -rib(i,2)+sepx,rib(i,4)+sepy,1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vault rib(i,6) rib(i,7) rib(i,9) calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xlong=0.
       xlong1=0.
       xlong2=0.
       xlong3=0.

       do k=1,kmax3

c      xlong1 = vault lenght at segment k

       xlong1=xlong1+sqrt((xvault(k)-xvault(k+1))**2.+
     + (yvault(k)-yvault(k+1))**2.)

c      xlong2 = vault lenght at segment k+1

       xlong2=xlong1+sqrt((xvault(k+1)-xvault(k+2))**2.+
     + (yvault(k+1)-yvault(k+2))**2.)

c      Interpolates rib(i,6) rib(i,7) (x' and z rib)

       if (xlong1.lt.rib(i,2).and.xlong2.ge.rib(i,2)) then

       xlong3=rib(i,2)-xlong1

       rib(i,6)=xq3(k+1)+(xp3(k+1)-xq3(k+1))*xlong3/(xlong2-xlong1)

       xm3=(yp3(k+1)-yq3(k+1))/(xp3(k+1)-xq3(k+1))
       bm3=yq3(k+1)-xm3*xq3(k+1)

       rib(i,7)=b1-(xm3*rib(i,6)+bm3)

       xquasiz=abs((xq3(k+1)-xp3(k+1)))

c      Avoid division by zero
       if (xquasiz.le.0.000001) then 
       xp3(k+1)=xp3(k+1)+0.00001
       end if

       rib(i,9)=(180./pi)*atan((yp3(k+1)-yq3(k+1))/(xq3(k+1)-xp3(k+1)))

       end if

c      Adjusta final tip !!!!!!!!!!!!!!!!!!!!!!!!!
       if (i.eq.nribss) then
       rib (i,6)=xvault(kmax3+1)
       rib (i,7)=b1+yvault(kmax3+1)
       end if
c      Tip adjustement (revise code above and remove!)

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     6. Writes auxliar geometry matrix for use with LEparagliding 2.X
c     File geometry-out.txt
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       write (*,'(I2,4x,8(F7.2,4x))') i,rib(i,2),rib(i,3),rib(i,4),
     + rib(i,6),rib(i,7),rib(i,9),33.33,0.0

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     7. Completes vault drawing
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c     Draws beta angle auxiliar lines

      sepx=0.
      sepy=-400.-b1

      dyv=50.

      do i=1,nribss

      if (rib(i,9).eq.90.) then 
      rib(i,9)=rib(i,9)+0.001
      end if
      
      dxv=50.*sin(rib(i,9)*(pi/180.))
      dyv=50.*cos(rib(i,9)*(pi/180.))

c      write (*,*) i,rib(i,9),dxv,dyv

      call line(rib(i,6)+sepx,rib(i,7)+sepy,
     + rib(i,6)+sepx,rib(i,7)-50.+sepy,1)

      call line(rib(i,6)+sepx,rib(i,7)+sepy,
     + rib(i,6)+dxv+sepx,rib(i,7)-dyv+sepy,2)

      end do
       
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc      
c      8. Write more info in geometry-out.txt
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c 
c      NEW CODE :)
c
c      rib(i,2) = x coordinate rib number "i"
c      rib(i,3) = y coordinate, leading edge rib "i"
c      rib(i,4) = y coordinate, trailing edge rib "i"
    
      write(23,'(A)')"*************************************************"
      write (23,'(A)') "LABORATORI D'ENVOL PARAGLIDING"
      write(23,'(A)')"*************************************************"
      write (23,'(A)') "GEOMETRY PRE-PROCESSOR"
      write (23,'(A)') "Version 1.5 ""Baldiri"" (2018-12-07)"
      write(23,'(A)')"*************************************************"
      write(23,'(A)')"Auxiliar geometry data for use with LEparagliding"
      write(23,'(A)')"*************************************************"
      write (23,'(A)') "1. Matrix of geometry"
      write(23,'(A)')"*************************************************"
      write(23,'(A,A)') "Rib	x-rib       y-LE       y-TE   	    xp",
     + "         z	beta      RP        Washin"

c     Write matrix of geometry
      do i=1,nribss
      write (23,'(I2,4x,8(F7.2,4x))') i,rib(i,2),rib(i,3),rib(i,4),
     +rib(i,6),rib(i,7),rib(i,9),33.33,0.0
      end do

c     Main wing data
      write(23,'(A)')"*************************************************"
      write (23,'(A)') "2. Main geometry paraglider data:" 
      write (23,'(A)') "***********************************************"
      write (23,'(A,I3)') "Cells= ", ncells
c     Case 1 odd (imparell)
      if (evenodd.eq.1) then
      write (23,'(I1,A)') 1, " Number of cells is odd "
      write (23,'(A,I3)') "Number of ribs ", nribss
      end if
c     Case 0 even (parell)
      if (evenodd.eq.0) then
      write (23,'(I1,A)') 0, " Number of cells is even "
      write (23,'(A,I3)') "Practical number of ribs ", nribss
      end if

      fspan=xm*2/100
      pspan=rib(nribss,6)*2/100
      write (23,'(A,F7.2,A)') "Span= ", fspan, " m"
      write (23,'(A,F7.2,A)') "Span_proj= ", pspan, " m"

c     Compute wing surface (area)

      atrapz(0)=rib(1,2)*(rib(1,4)-rib(1,3))
      area=atrapz(0)

      do i=1,nribss-1
      atrapz(i)=(rib(i+1,2)-rib(i,2))*0.5*
     +(rib(i,4)-rib(i,3)+rib(i+1,4)-rib(i+1,3))
      area=area+atrapz(i)
      end do

      area=2*area/10000.

c     Compute wing surface projected (parea)

      atrapz(0)=rib(1,6)*(rib(1,4)-rib(1,3))
      parea=atrapz(0)

      do i=1,nribss-1
      atrapz(i)=(rib(i+1,6)-rib(i,6))*0.5*
     +(rib(i,4)-rib(i,3)+rib(i+1,4)-rib(i+1,3))
      parea=parea+atrapz(i)
      end do

      parea=2*parea/10000.

      write (23,'(A,F7.2,A)') "Surface= ", area, " m2"
      write (23,'(A,F7.2,A)') "Surface_proj= ", parea, " m2"

      faratio=fspan*fspan/area
      paratio=pspan*pspan/parea
      write (23,'(A,F7.2)') "Aspect_Ratio= ", faratio
      write (23,'(A,F7.2)') "Aspect_Ratio_proj= ", paratio
         
      write (23,'(A,1x,F5.2)') "Flattening= ",((area-parea)/area)

c     Millorar, aixo no es exacte fer estadistica
      write (23,'(A,F7.2,A)') "Max_chord= ", rib(1,4)-rib(1,3)," cm"
      write (23,'(A,F7.2,A)') "Mid_chord= ", (area/fspan)*100.," cm"
      write (23,'(A,F7.2,A)') "Min_chord= ", 
     + rib(nribss,4)-rib(nribss,3)," cm"

c     Especial parameters
      write (23,'(A)') "***********************************************"
      write (23,'(A)') "3. Some internal parameters:" 
      write (23,'(A)') "***********************************************"

      if (ivault.eq.2) then
      write (23,'(A)') "Vault case 2: centers of the arcs:" 
      write (23,'(I1,2x,F10.4,2x,F10.4)') 1, o1x, o1y
      write (23,'(I1,2x,F10.4,2x,F10.4)') 1, o2x, o2y
      write (23,'(I1,2x,F10.4,2x,F10.4)') 1, o3x, o3y
      write (23,'(I1,2x,F10.4,2x,F10.4)') 1, o4x, o4y
      end if

c     Especial parameters
      write (23,'(A)') "***********************************************"
      write (23,'(A,A)') "4. Leading edge, trailing edge, and vault ",
     + "coordinates:" 
      write (23,'(A)') "***********************************************"

      write (23,'(A)') "Leading edge coordinates" 
      write (23,'(I4)') nle
      do i=1,nle
      write (23,'(I3,3x,F10.4,3x,F10.4)') i, le_(i,1), le_(i,2)
      end do
      write (23,'(A)') "Trailing edge coordinates" 
      write (23,'(I4)') nte
      do i=1,nte
      write (23,'(I3,3x,F10.4,3x,F10.4)') i, te_(i,1), te_(i,2)
      end do
      write (23,'(A)') "Vault coordinates" 
      write (23,'(I4)') nva
      do i=1,nva
      write (23,'(I3,3x,F10.4,3x,F10.4)') i, va_(i,1), va_(i,2)
      end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc




cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9. END OF MAIN PROGRAM
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc   

       call dxfend(20)

       write (*,*) 
       write (*,*) "OK, pre-processing done!"
       write (*,*) "Open geometry.dxf file and geometry-out.txt files"
       write (*,*) "Complete manually your leparagliding.txt data file"
       write (*,*)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      END MAIN PROGRAM
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c     SUBROUTINES
c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       SUBROUTINE eo(ncells,evenodd,nribss)

       integer evenodd nribss ncells

       control=((float(ncells))/2.)-float(int(float(ncells)/2.))

       write (*,*) control
       
       if (control.eq.0.) then  ! even-parell
       nribss=int((float(ncells)/2.)+1.)
c      nribss=(ncells/2)+1
       evenodd=0
       end if

       if (control.ne.0.) then  ! odd-imparell-senar
       nribss=int(((float(ncells)+1.)/2.))
c       nribss=(ncells+1)/2
       evenodd=1
       end if

       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      20. GRAPHICAL SUBROUTINES
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

     
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE POINT 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE point(x1,y1,pointcolor)
c      line P1-P2

       real x1,y1
       integer pointcolor

       write(20,'(A,/,I1,/,A)') "POINT",8,"default"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,x1,20,-y1
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,pointcolor,0
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINE 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE line(p1x,p1y,p2x,p2y,linecolor)
c      line P1-P2

       real x1,x2,y1,y2,z1,z2

       write(20,'(A,/,I1,/,A)') "LINE",8,"default"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,p1x,20,-p1y
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 11,p2x,21,-p2y
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc        
c     SUBROUTINE LINE 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE line3d(p1x,p1y,p1z,p2x,p2y,p2z,linecolor)
c      line P1-P2
       write(25,'(A,/,I1,/,A)') "LINE",8,"default"
       write(25,'(I1,/,A)') 6,"CONTINUOUS"
       write(25,'(I2,/,F8.3,/,I2,/,F8.3,/,I2,/,F8.3)') 
     + 10,p1x,20,p1y,30,p1z
       write(25,'(I2,/,F8.3,/,I2,/,F8.3,/,I2,/,F8.3)') 
     + 11,p2x,21,p2y,31,p2z
       write(25,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      POLYLINE 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE poly2d(plx,ply,nvertex,linecolor)

       real plx(300),ply(300),plz(300)

       write (20,'(A,/,I1,/,I1,/,I2)') "POLYLINE",8,0,62
       write (20,'(I3,/,I2,/,I1)') linecolor,66,1
       write (20,'(I2,/,F3.1,/,I2,/,F3.1,/,I2,/,F3.1,/,I1)') 
     + 10,0.0,20,0.0,30,0.0,0
       
       do k=1,nvertex

       write (20,'(A,/,I1,/,I1,/,I2)') "VERTEX",8,0,62
       write (20,'(I3,/,I2,/,I1)') linecolor,66,1 
       write (20,'(I2,/,F9.3,/,I2,/,F9.3,/,I2,/,F9.3,/,I1)') 
     + 10,plx(k),20,ply(k),30,0.0,0

       end do
       
       write (20,'(A,/,I1,/,I1,/,I2)') "SEQEND",8,0,62
       write (20,'(I3,/,I1)') linecolor,0 

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ELLIPSE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE ellipse(u0,v0,a,b,tet0,linecolor)

       real xe(300),ye(300)

       real pi

       pi=4.*atan(1.)

       do ll=1,40

       tet=2.*pi*((float(ll)-1.)/39.)

c      write (*,*) ll,float(ll),tet," ",pi,"---"

       xe(ll)=u0+a*cos(tet)*cos(tet0)-b*sin(tet)*sin(tet0)
       ye(ll)=v0+a*cos(tet)*sin(tet0)+b*sin(tet)*cos(tet0)

       end do

       do ll=1,39

       p1x=xe(ll)
       p2x=xe(ll+1)
       p1y=ye(ll)
       p2y=ye(ll+1)

       call line(p1x,p1y,p2x,p2y,linecolor)

c       write (*,*) ll,tet*180./pi,xe(ll),ye(ll)

       end do

       return

       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE ROMANO
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE romano(rn,rx0,ry0,ralp,requi,rcolor)

       integer rn, rn1, rn2, rn3, rcolor

       real rx0, ry0, ralp, requi, dx

       dx=0.

       rn1=int(float(rn)/10.)
       rn2=int((float(rn)-10.*float(rn1))/5.)
       rn3=rn-10*rn1-5*rn2

c      write (*,*) "rn1= ", rn, rn1, rn2, rn3

       do i=1,rn1

       call point(rx0+dx*cos(ralp),ry0-dx*sin(ralp),7)
       call point(rx0+dx*cos(ralp)+requi*sin(ralp),
     + ry0-dx*sin(ralp)+requi*cos(ralp),7)
       dx=dx+requi
       call point(rx0+dx*cos(ralp),ry0-dx*sin(ralp),7)
       call point(rx0+dx*cos(ralp)+requi*sin(ralp),
     + ry0-dx*sin(ralp)+requi*cos(ralp),7)
       dx=dx+requi

       end do

       do i=1,rn2

       call point(rx0+dx*cos(ralp),ry0-dx*sin(ralp),7)
       call point(rx0+(dx+0.5*requi)*cos(ralp)+requi*sin(ralp),
     + ry0-(dx+0.5*requi)*sin(ralp)+requi*cos(ralp),7)
       dx=dx+requi
       call point(rx0+dx*cos(ralp),ry0-dx*sin(ralp),7)
       dx=dx+requi

       end do

       do i=1,rn3

       call point(rx0+dx*cos(ralp),ry0-dx*sin(ralp),7)
       dx=dx+requi

       end do

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE TEXT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE txt(p1x,p1y,htext,atext,xtext,txtcolor)
c      line P1-P2

       real x1,x2,y1,y2,z1,z2,atext,htext
       character*50 xtext
       integer txtcolor

       write(20,'(A,/,I1,/,A)') "TEXT",5,"10A38"
       write(20,'(I1,/,I1)') 8, 0
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,I3)') 62, txtcolor
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,p1x,20,-p1y
       write(20,'(I2,/,F12.2)') 30,0.0
       write(20,'(I2,/,F12.2)') 40, htext
       write(20,'(I2,/,A50)') 1, xtext
       write(20,'(I2,/,F12.2,/I1)') 50, atext,0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE ITEXT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE itxt(p1x,p1y,htext,atext,itext,txtcolor)
c      line P1-P2

       real x1,x2,y1,y2,z1,z2,atext,htext
       integer itext, txtcolor

       write(20,'(A,/,I1,/,A)') "TEXT",5,"10A38"
       write(20,'(I1,/,I1)') 8, 0
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,I3)') 62, txtcolor
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,p1x,20,-p1y
       write(20,'(I2,/,F12.2)') 30,0.0
       write(20,'(I2,/,F12.2)') 40, htext
       write(20,'(I2,/,I12)') 1, itext
       write(20,'(I2,/,F12.2,/I1)') 50, atext,0

       return
       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      DXF init
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       SUBROUTINE dxfinit(nunit)
       
       write(nunit,'(I1,/,A,/,I1)') 0,"SECTION",2
       write(nunit,'(A)') "HEADER"
       write(nunit,'(I1,/,A)') 9,"$EXTMAX"
       write(nunit,'(I2,/,F12.3,/,I2,/,F12.3)') 10,-900.,20,90.
       write(nunit,'(I1,/,A)') 9,"$EXTMIN"
       write(nunit,'(I2,/,F12.3,/,I2,/,F12.3)') 10,5000.,20,-3000.
       write(nunit,'(I1,/,A,/,I1)') 0,"ENDSEC",0
       write(nunit,'(A,/,I1)') "SECTION",2
       write(nunit,'(A,/,I1)') "ENTITIES",0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      DXF end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dxfend(nunit)

       write(nunit,'(A,/,I1,/,A)') "ENDSEC",0,"EOF"
       return
       end

      

