c***************************************************************
c      LE PARAGLIDING v 3.17 "Z"
c      Pere Casellas 2010-2021
c      Laboratori d'envol
c      http://www.laboratoridenvol.com
c      pere AT laboratoridenvol DOT com
c      Version experimental 0.1: 2005-02-13
c      Version 0.8: 2010-01-02 "gnuLAB2"
c      Version 0.9: 2010-02-14
c      Version 1.0: 2010-03-07
c      Version 1.02: 2010-04-17 "Annency"
c      Version 1.1: 2010-04-25 "South Africa"
c      Version 1.11: 2010-12-26 "Montseny"
c      Version 1.2: 2011-01-14 "Adrenaline"
c      Version 1.25: 2011-03-20 "Romano"
c      Version 1.4: 2011-04-25 "V-Ribs"
c      Verssion 1.5: 2011-12-08 "HyperLite"
c      Version 2.0: 2012-01-08 "BHL"
c      Version 2.1: 2012-05-27 "BatLite"
c      Version 2.2: 2013-05-05 "Altair"
c      Version 2.21: 2013-07-17 "Fluid Wings"
c      Version 2.23: 2013-08-13 "BHL-2"
c      Version 2.31: 2013-12-31 "BASE"
c      Version 2.35: 2014-04-21 "BASE"
c      Version 2.37: 2015-04-25 "Omsk"
c      Versiom 2.41: 2015-09-20 "Omsk"
c      Version 2.45: 2016-03-12 "Utah"
c      Version 2.50: 2016-05-09 "Utah"
c      Version 2.51: 2016-06-05
c      Version 2.52: 2016-08-18
c      Version 2.52++: 2016-08-27
c      Version 2.60: 2016-12-12 "Les Escaules"
c      Version 2.70: 2018-02-04 "Baldiri"
c      Version 2.73: 2018-05-12 "Baldiri"
c      Version 2.77; 2018-08-28 "Baldiri" 
c      Version 2.80; 2018-10-12 "Baldiri"
c      Version 2.81: 2018-12-24
c      Version 2.85: 2019-01-01
c      Version 2.88: 2019-01-07
c      Version 2.90: 2019-01-13 
c      Version 2.95: 2019-01-20   
c      Version 2.96: 2019-05-07
c      Version 2.99: 2019-06-24
c      Version 3.00: 2020-01-12 "Pirineus"
c      Version 3.02: 2020-01-26 "Pirineus"
c      Version 3.03: 2020-04-13 "Pirineus"
c      Version 3.10: 2020-05-02 "Pirineus"
c      Version 3.11: 2020-09-06 "Pirineus"
c      Version 3.12: 2020-12-15 "Pirineus"
c      Version 3.14: 2020-12-25 "Pirineus"
c      Version 3.15: 2021-01-17 "Canigó"
c      Version 3.16: 2021-08-29 "Z"
c      Version 3.16+: 2021-11-27 "Z"
c      Version 3.17: 2021-12-12 "Z"   
c      FORTRAN fort77/gfortran (GNU/Linux)
c      GNU General Public License 3.0 (http://www.gnu.org)
c
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c       program leparagliding
c
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      1. VARIABLE NAMES
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccciiiiiiiiiiiiiiiiiiiiiiiic

c      ncells: number of cells
c      nribst: total ribs
c      nribss: in semi-wing
c      rib(i,j): rib i parameter j
c            j=1 rib number
c            j=2 x_rib
c            j=3 y_LE
c            j=4 y_TE
c            j=5 chord
c            j=6 x'
c            j=7 z_rib
c            j=8 alpha washin
c            j=9 beta
c            j=10 rotation point
c            j=11 vent in
c            j=12 vent out
c            j=14 open=1 closed=0
c            j=15 anchors number
c            j=16 A %
c            j=17 B %
c            j=18 C %
c            J=19 D %
c            j=20 E %
c            j=21 F % brake
c            j=22 cell wide (i to i+1)
c            j=23 extrados length
c            j=24 intrados wide
c            j=25 intrados length
c            j=26 inlet length
c            j=30 panel length to the left of rib i - extrados
c            j=31 rib i length - extrados
c            j=32 panel length to the right of rib i - extrados
c            j=33 panel length to the left of rib i - intrados
c            j=33 rib i length - intrados
c            j=35 panel length to the right of rib i - intrados
c            j=36,37,38,39 mark amplification coeficients
c      alpha: airfoil washin angle
c      alpham: max washin
c      beta: airfoil vertical angle
c      calag: calage
c      cple: center of pressure
c      hcp: height pilote - center of pressure
c      assiette:angle between horizontal line and chord
c      finesse: glide ratio
c      aoa: angle of attack AoA
c      nomair(i): airfoil archive
c      np(i,1): airfoil points number
c      u(i,j,20) v(i,j,20): airfoils coordinates
c        K = 1 = original coordinates
c            2 = 100*coordinates
c            3 = scaled coordinates
c            4 = washin coordinates
c            5 = espace coordinates
c            6 = singular points
c                j=1 A anchor point 3D
c                j=2 B anchor point 3D
c                j=3 C anchor point 3D
c                j=4 D anchor point 3D
c                j=5 E anchor point 3D
c                j=6 F anchor point - brake 3D
c                j=7 B intake in point 3D
c                j=8 B intake out point 3D
c            7 = overwide local left
c            8 = overwide local right
c            9 = coordinates overwide left
c            10 = coordinates overwide right
c            11 = coordinates left sewing border
c            12 = coordinates right sewing border
c            14 = panel extreme points left
c            15 = panel extreme points right
c            16 = airfoil borders
c            18 = anchor space coordinates
c            19 = anchor absolute coordinates
c      x(i,j) y(i,j) z(i,j): absolute airfoil coordinates
c      xx(1,j) yy(1,j) zz(1,j): central airfoil (or i=0)
c      hol(100,20,20) airfoil holes properties
c      xl(i,j) xr(i,j) panels length
c      skin(k,j) skin tension
c      xupp, xupple, xuppte, xlow, xlowle, xlowte, xrib sewing allowances
c      mc(ii,j,k) suspension matrix
c           ii = line plan
c           j = path number
c           k = matrix column
c               1 ramifications number of the path
c               2 1 (ramification level 1)
c               3 order in the level 1
c               4 2 (ramification level 2)
c               5 order in the level 2
c               6 3 (ramification level 3)
c               7 order in the level 3
c               8 4 (ramification level 4)
c               9 order in the level 4
c               10 anchor line (1=A,2=B,3=C,4=c,5=D,6=freno)
c               11 anchor rib number
c      cam(ii) paths in plan ii
c      slp suspension line plans
c      corda(i,k) ramification properties of line i
c           k = 1 line plan
c           k = 2 line level (1=riser)
c           k = 3 liner order (in the same level, and left to right)
c           k = 4 action points associated
c           k = 5 path ramifications
c           k = 6 final anchor row 1=A 2=B ...
c           k = 7 anchor rib number
c      x1line(corda(i,1),corda(i,2),corda(i,3)) line i initial x-coordinate
c      y1line(corda(i,1),corda(i,2),corda(i,3)) line i initial y-coordinate
c      z1line(corda(i,1),corda(i,2),corda(i,3)) line i initial z-coordinate
c      x2line(corda(i,1),corda(i,2),corda(i,3)) line i final x-coordinate
c      y2line(corda(i,1),corda(i,2),corda(i,3)) line i final y-coordinate
c      z2line(corda(i,1),corda(i,2),corda(i,3)) line i final z-coordinate
c      x3line(corda(i,1),corda(i,2),corda(i,3)) line i action point x-coordinate
c      y3line(corda(i,1),corda(i,2),corda(i,3)) line i action point y-coordinate
c      z3line(corda(i,1),corda(i,2),corda(i,3)) line i action point z-coordinate
c      xline(i) line i length
c      raml(i,j) ramfication lengths
c
c      hvr(i,j) H and V ribs definiton
c      j=1 H-strap
c      j=2 V-rib partial
c      j=3 V-rib full
c      j=4 VH rib (3 cells)
c
c      V-ribs absolute coordinates
c      rx1(),ry1(),rz1()
c      rx2(),ry2(),rz2()
c      rx3(),ry3(),rz3()
c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      2. VARIABLES TYPE DECLARATION
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       double precision


       integer ncells,nribst

       real*8 xkf,xwf
       real*8 ribdif, htens, xndif
       real*8 x1,y1,z1,x2,y2,z2,x3,y3,z3
       real*8 Apla,Bpla,Cpla,l_line,m_line,n_line
       real*8 l2_line,m2_line,n2_line
       real*8 p1x,p1y,p1z,p2x,p2y,p2z,p3x,p3y,p3z,p4x,p4y,p4z
       real*8 distance,param1,param2,param3 ! general parameters

       real*8 alpha,tetha,alpham,alphac,alphat,alpha1,alpha2,alpr,alpl
       real*8 alple,alp
       real*8 phii(0:100),alpha_ii,chii(0:100)
       real*8 x_apap(0:100),y_apap(0:100),z_apap(0:100)

c       real*8 amte,amter,amtel,amle,amler,amlel
       real*8 amle,amler

       real*8 tetha1,tetha2,tetha3,tetha4,angle
c       real*8 angle1
       real*8 angle2

       real*8 xmk,xmark,xcir,xdes,xdesx,xdesy,xprev,xpost
       real*8 xdes1,xdes2,xcir1,xcir2

       real*8 x0,y0,xx0,yy0,x00,xxa,yyb

       real*8 o1x,o1y,o2x,o2y,o3x,o3y

       real*8 xn,xm,xa,xb,xn1,xm1,xn2,xm2,xn3,xm3

       real*8 xu,xv
c       real*8 xlu1,xlv1,xlu2,xlv2

       real*8 a,b,aa,bb,a1,b1,c1

       real*8 xrsep,yrsep,psep,psey
       real*8 asep,bsep,sepx,sepy,sepxx,sepyy

       real*8 xcos

       real*8 alptri,atri,btri,rtri,satri,h1tri,h2tri,h3tri

       real*8 agor,bgor,cgor,cggor,step1

       real*8 rib(0:100,500)

       character*50 wname,bname,nomair(100),nomairext(100),lyname(50)
       character*50 xtext,lepv,lepd,lepc
       character*2 atp

       character*50 xstring, string1, string2, string3

       character*1 ln1,ln2
       character*2 ln3
       character*4 ln4(500)

       character*50 gname

c       character*200 entireline

c      Coordenades airfoil en gir Z
       real*8 unew(500),vnew(500),wnew(500)
       real*8 pos, rot_z

       real*8 u(0:100,500,99),v(0:100,500,99),w(0:100,500,99) ! airfoil 3D
       real*8 uf(0:100,500,50),vf(0:100,500,50)   ! flat panels development
       real*8 ufe(0:100,500,50),vfe(0:100,500,50) ! panels extrados
       real*8 ufv(0:100,500,99),vfv(0:100,500,99) ! panels vents
       real*8 ufi(0:100,500,50),vfi(0:100,500,50) ! panels intrados
       real*8 ufa(0:100,500,50),vfa(0:100,500,50) ! auxiliar a
       real*8 ufb(0:100,500,50),vfb(0:100,500,50) ! auxiliar b
       real*8 ufc(0:100,500,50),vfc(0:100,500,50) ! auxiliar b
       real*8 uft(0:100,500,50),vft(0:100,500,50) ! auxiliar t
       real*8 ufr(0:100,500,50),vfr(0:100,500,50) ! auxiliar r
       real*8 u_aux(0:100,500,10),v_aux(0:100,500,10),
     + w_aux(0:100,500,10) ! auxiliar general


       real*8 cs1x,cs1y,cs2x,cs2y

       real*8 usalvat(0:100,500,50),vsalvat(0:100,500,50)

       real*8 ru(0:100,500,99),rv(0:100,500,99),rw(0:100,500,99)

       real*8 x(0:100,500),y(0:100,500),z(0:100,500)

       real*8 rx(0:100,500),ry(0:100,500),rz(0:100,500)

       real*8 hx2(0:100,50,10), hy2(0:100,50,10), hz2(0:100,50,10)
       real*8 hx3(0:100,50,10), hy3(0:100,50,10), hz3(0:100,50,10)

       real*8 rx1(0:100,50,10), ry1(0:100,50,10), rz1(0:100,50,10)
       real*8 rx2(0:100,50,10), ry2(0:100,50,10), rz2(0:100,50,10)
       real*8 rx3(0:100,50,10), ry3(0:100,50,10), rz3(0:100,50,10)

       real*8 sx1(0:100,50,10), sy1(0:100,50,10), sz1(0:100,50,10)
       real*8 sx2(0:100,50,10), sy2(0:100,50,10), sz2(0:100,50,10)
       real*8 sx3(0:100,50,10), sy3(0:100,50,10), sz3(0:100,50,10)
       real*8 sx4(0:100,50,10), sy4(0:100,50,10), sz4(0:100,50,10)

       integer np(0:100,9)
       real*8 xx(1,500),yy(1,500),zz(1,500)

       real*8 px0,py0,ptheta
       real*8 pa,pb,pc,pd,pe,pf
       real*8 pa1l,pa2l,phl,pa1r,pa2r,phr
       real*8 pb1t,pb2t,pht,phu,pw1

       real*8 pl1x(0:100,500),pl1y(0:100,500),pl2x(0:100,500),
     + pl2y(0:100,500)
       real*8 pr1x(0:100,500),pr1y(0:100,500),pr2x(0:100,500),
     + pr2y(0:100,500)

       real*8 hol(0:100,20,20),skin(10,10)

       real*8 xsob(10),ysob(10)

       real*8 xupp, xupple, xuppte, xlow, xlowle, xlowte, xrib, xvrib
       real*8 xlowsaved

       real*8 brake(0:100,10)

       integer mc(10,100,20), cam(10), corda(500,10)

       integer cordam, cordat, t

       real*8 xcorda(500,5), ycorda(500,5), zcorda(500,5), raml(10,5)

       real*8 x1line(10,5,100),y1line(10,5,100),z1line(10,5,100)
       
       real*8 x2line(10,5,100),y2line(10,5,100),z2line(10,5,100)

       real*8 phi1(10,5,100),phi2(10,5,100),phi0(10,5,100)

       real*8 calag,cple,hcp,assiette,afinesse,aoa,finesse,planeig
       real*8 calage,cpress,clengr,clengl,clengk,clengb

       real*8 zcontrol, csusl, control

       real*8 acit,xci,yci,aci,cdgx,cdgy,cdg,xpoi,xdis

       real*8 dist,dist1,cdl,cdm,cdn

       real*8 xkar,ykar,zkar

       real*8 farea,parea,fspan,pspan,faratio,paratio

       real*8 comp1(10),comp2(10), xline(500),  xline2(500)

       real*8 hvr(0:200,15)

       real*8 ucnt(0:500,10,20), vcnt(0:500,10,20)

       real*8 ucnt1(0:100,10,500), vcnt1(0:100,10,500)
       real*8 ucnt2(0:100,10,500), vcnt2(0:100,10,500)
       real*8 ucnt3(0:100,10,500), vcnt3(0:100,10,500)
       real*8 ucnt4(0:100,10,500), vcnt4(0:100,10,500)

       integer jcon(0:200,10,500)
       integer jcon2(0:200,10,500),jcon4(0:200,10,500)
       integer jcon9(0:200,10,500),jcon11(0:200,10,500)

       integer npce, npc1e(100), npc2e(100), npc3e(100,100)
       integer npci, npc1i(100), npc2i(100), npc3i(100,100)
       real*8 xpc1e(100,100), xpc2e(100,100) 
       real*8 xpc1i(100,100), xpc2i(100,100)

       real*8 xle(100,100), xleinc(100,100)
       real*8 xpc3e(100,100), ypc3e(100,100)
       real*8 xli(100,100), xliinc(100,100)
       real*8 xpc3i(100,100), ypc3i(100,100)

       real*8 xarp(10), yarp(10)

       real*8 hdist(100), hangle(100)

       real*8 xtri(50),ytri(50)

       real*8 csus(10,10), cdis(10,10)

       real*8 aload(100,10), xload(500), xlide(500), xlifi(500)
       real*8 lvcx(500,500), lvcy(500,500),rvcx(500,500),rvcy(500,500)

       real*8 anccont(0:100,10),ancconti(0:100,10)

       real*8 bd(10,10)

       real*8 xpt1,ypt1,zpt1,xpt2,ypt2,zpt2,xpt3,ypt3,zpt3
       real*8 xpt4,ypt4,zpt4,xpt6,ypt6,zpt6

       integer slpi(10), slp

       real*8 xlin1(5000),ylin1(5000)
       real*8 xlin3(5000),ylin3(5000)

       real*8 xru(3),xrv(3),xsu(3),xsv(3)

       real*8 xtu2(100),xtv2(100),xtu4(100),xtv4(100)
       real*8 xtu9(100),xtv9(100),xtu11(100),xtv11(100)

       real*8 xlte11(100),xl911(100),xlle9(100)
       real*8 xrte11(100),xr911(100),xrle9(100)
       real*8 xc24(100)

c       real*8 px9i(300),py9i(300)
       real*8 px9o(500),py9o(500)

       real*8 xanchor(100,6),yanchor(100,6)
       real*8 xanchoril(100,6),yanchoril(100,6)
       real*8 xanchorir(100,6),yanchorir(100,6)

       real*8 xprb(0:100,6,0:10),yprb(0:100,6,0:10)
       real*8 jconi(6),jconf(6),xkprb(6)
       real*8 jcve(100),jcvi(100)
       real*8 xirl(0:500),xirr(0:500),jirl(0:500),jirr(0:500)
       real*8 distee(0:500),anglee(0:500),siu(0:500),siv(0:500)
       real*8 alprom,xdu,xdv,xpo1,xpo2,ypo1,ypo2

c       real*8 xlll,xrrr,yrrr,ylll
       real*8 xgir
       real*8 xpos,ypos,xpx2,xpy2,xr,xs,xrm,xsm
       real*8 xequis,yequis, xth1, xth2
       real*8 xlabel, zlabel, clli, varrow

       integer typepoint,typetab,typevent,typejonc
       integer typm1(50),typm4(50)
       integer iccolor(50),ele3d(50),ele3dc(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50)
       real*8 xrad

c      Section 21

       integer ngo(100,3)
       real*8 xextra(0:100,10),xintra(0:100,10)
       real*8 xjonc(0:100,500,10),sjo(0:100,10)
       real*8 xjonc2(0:100,500,10),sjo2(0:100,10)

       integer k21blocs,k21blocf(20,10)
       integer ngoo(20,100,3)
       real*8 sjoo(20,100,10)
       real*8 xextraa(20,0:100,10),xintraa(20,0:100,10)
       real*8 x21(20,100,20)
       real*8 joncf(0:100,20,100,10)

c      Section 22
       real*8 xmy(0:100,10)

c      Section 27
       real*8 alc1, alc2

c      Section 28

       real*8 p28(10), a128, a228, lini28(100,10), lfin28(100,10)
       real*8 alpha28(100),calagnew(100)
       real*8 cnewtps(100),cnewcms(100),cnewtpt(100),cnewcmt(100)
       integer n128, n228

c      Section 29

       integer k29d,k29dd,ncuts(200),ini29(200),fin29(200)

       real*8  cutamp(10),cut29(0:10,200)
       real*8 s,sm,haut

       integer iupp(10,10,200),ilow(10,10,200)
       integer xiupp(10,10,200),xilow(10,10,200)
       real*8 kiupp(10,200),kilow(10,200)
       integer uppcuts(200),upptype(200),lowcuts(200),lowtype(200)
       real*8 hautok(0:100,500), zinf(0:100,10,10)
       integer pp29(10,10) ! Print parameters

c      Subroutines used in section 29: planeby123,pointp

       real*8 punt0(3),punt1(3),punt2(3),punt3(3),punt4(3)
       real*8 aplane,bplane,cplane,dplane,xt,dp0

       real*8 csi(0:100,60) ! Brute force in 8.5.5/drwvent
     
c      Section 31
       integer ksk,ng,ngi,ngskt,nribini,nribfin,npoints,ntype31
       integer skinpoints(0:100),ngroup31(0:100),ntypei31(0:100)

c       real*8 xxx,yyy,hhh,a128,a1281,a228,a2282
       real*8 xxx,yyy,hhh,a1281,a2282
       real*8 skinew(101,10), skinnew(0:100,101,10)
       real*8 xsobnew(0:100,101),ysobnew(0:100,101)
       real*8 xmida1,xmida2,xmida3,xmida4
       real*8 xpoint(101),ypoint(101),xvalue,yvalue
       real*8 xx1,xx2,yy1,yy2,zz1,zz2
       real*8 atext,htext

c      Section 32

       real*8 panel_x_coe,panel_x_min,panel_y_coe,rib_x_coe,rib_y_coe


c      Section 4.20 control parameters
       real*8 amplemig,amplerix,ampleriy,amplepix

c      Especial vents
       real*8 lvalp,lv1u,lv1v,lv2u,lv2v,lv3u,lv3v,lv4u,lv4v

c      Geometryc subroutines

c      l,m,n director cosinus       
       real*8 lcosd(3),mcosd(3),ncosd(3)

c      Parameter panels impression

       real*8 ysautt,ysaut

c      Side linghts in panels, use for equidistant marks

       real*8 llarl(0:100,3,100),llarr(0:100,3,100)
       real*8 xinil,xinir
       real*8 xfinl(0:100,3,100),xfinr(0:100,3,100)
       integer iq

       integer ich ! i control header
       character*72 lepuser 

c      Subroutine remapcont
       integer npini,npfin,npobj
       real*8 ucont(0:100,500),vcont(0:100,500)

c      Subroutine elliquad
       real*8 pgx(100),pgy(100) ! generic points
    

c      Auuxiliar values
       real*8 xlen,ylen
       real*8 xyextra,xyintra,xyshift

       real*8 seppix(0:100)

c      Subroutine drwvent
       real*8 xpoly(500),ypoly(500),zpoly(500)
       real*8 x_poly,y_poly,z_poly,x_poly1,y_poly1,z_poly1,
     + x_poly2,y_poly2,z_poly2,xpolylen
       real*8 xlenl,xlenr,xlenlr,xlenrr

c      Subroutine drwvent
       real*8 distrel,distrel1,distrel2


       integer n_words
       integer, parameter   :: nlen=1000
       character (len=nlen) :: entireline
       character (len=100)  :: words(nlen)        

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      COMMON BLOKS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       real*8 pi
       pi=4.0d0*datan(1.0d0)

c      Substitution of BOX(1,3) BOX(1,5) by BOX(-1,3) BOX(-1,5)
c      Set n1draw=1 xyextra=2.0 yxintra=1.0 to return previous version

       n1draw=0 ! parameter to control classic plans. If set to 0 no print.
       xyextra=0.0d0   ! Control BOX Y-position extrados
       xyintra=-1.0d0
       xyshift=500.0d0 ! Control Y-position extrados

c      integer color
c      common typepoint

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Basic LEparagliding data version
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       lepv="3.17"            ! Version
       lepd="2021-12-12"      ! Date
       lepc='"Z"'             ! Code name
       lepuser="GENERAL"  
       ich=0

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      3. INIT
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       ich=0

c      Customized header
       if (ich.eq.1) then
       write (*,*) 
       write (*,*) "**************************************************"
       write (*,'(1x,A72)') lepuser
       write (*,*) "**************************************************"
       else
       write (*,*)
       end if
       write (*,*) "LABORATORI D'ENVOL PARAGLIDING"
       write (*,*) "Paragliders and parachutes design program"
       write (*,*)
       write (*,'(A14,1x,A6,1x,A7,1x,A50)') " LEparagliding",lepv,
     + "version",lepc
       write (*,'(1x,A10)') lepd
       write (*,*)
       write (*,*) "Pere Casellas"
       write (*,*) "pere@laboratoridenvol.com"
       write (*,*) "GNU General Public License 3.0 http://www.gnu.org"
       write (*,*)

       open(unit=20,file='leparagliding.dxf')
       open(unit=22,file='leparagliding.txt')
       open(unit=23,file='lep-out.txt')
       open(unit=30,file='lines.txt')
       open(unit=25,file='lep-3d.dxf') 
       
       call dxfinit(20)

       call dxfinit(25)

c       call mtriangle(0.0d0,200.0d0,10.0d0,0.0d0,1)
c       call mtriangle(20.0d0,200.0d0,10.0d0,pi/2.0d0,2)
c       call mtriangle(40.0d0,200.0d0,10.0d0,pi/3.0d0,3)
c       call mtriangle(60.0d0,200.0d0,10.0d0,pi,4)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4. DATA READING
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Lectura de dades del fitxer

       rewind (22)
       rewind (23)
       rewind (30)

c      4.1 Basic data
       do i=1,9
       read (22,*)
       end do

       read (22,*) bname
       read (22,*)
       read (22,*) wname
       read (22,*)
       read (22,*) xkf
       read (22,*)
       read (22,*) xwf
       read (22,*)
       read (22,*) ncells
       read (22,*)
       read (22,*) nribst
       read (22,*)
       read (22,*) alpham, kbbb         ! case 0,1

c      Read case "2"
       if (kbbb.eq.2) then
       backspace(22)
       read (22,*) alpham, kbbb, alphac ! case 2
       alphat=alpham-alphac
       end if

       read (22,*)
       read (22,*) atp, kaaa
       read (22,*)
       read (22,*)

c      4.2  Ribs geometry
       nribss=int(ncells/2.)+1

c      Ribs geometry rib,x,LE,TE,chord,x',z,beta,RP 

c      Count words in first row of geometry matrix
       read (22,'(A)',end=9) entireline
c       write (*,*) entireline
9      continue
       backspace(22)

c      Count words
       words = ""
       read (entireline,*,iostat=ierr) words
       n_words = count(words /= "")
c       print*,"n_words in first line of geometry matrix=",n_words
c       print*

c       if (n_words.ne.11) then
c       n_words=11
c       end if

c      Read matrix of geometry
       do i=1,nribss

       if (n_words.eq.11) then ! case lep >= 3.16
       read (22,*) rib(i,1), rib(i,2), rib(i,3), rib(i,4), rib(i,6), 
     + rib(i,7), rib(i,9), rib(i,10), rib(i,51), rib(i,250), rib(i,251)
       end if

       if (n_words.eq.9) then ! case lep < 3.16
       read (22,*) rib(i,1), rib(i,2), rib(i,3), rib(i,4), rib(i,6), 
     + rib(i,7), rib(i,9), rib(i,10), rib(i,51)
       rib(i,250)=0.0d0
       rib(i,251)=0.0d0
       end if

c      Anticipates tan(0.0) if beta=0.
       if (rib(i,10).eq.0.) then
       rib(i,10)=0.01
       end if

c      Anticipates xp=0 in central airfoil
       if (rib(1,6).eq.0.) then
       rib(i,6)=0.01
       end if

c      central cell width control
       cencell=rib(1,2)

c      Scale geometry to absolute
       rib(i,2)=rib(i,2)*xwf
       rib(i,3)=rib(i,3)*xwf
       rib(i,4)=rib(i,4)*xwf
       rib(i,6)=rib(i,6)*xwf
       rib(i,7)=rib(i,7)*xwf

c      Chord
       rib(i,5)=rib(i,4)-rib(i,3)

c      Washin calculus

c      Case 0
       
       if (kbbb.eq.0) then
       rib(i,8)=rib(i,51)
       end if

c      Case 1
       if (kbbb.eq.1) then
       ribdif=rib(1,5)-rib(i,5)
       ribdim=rib(1,5)-rib(nribss,5)
       rib(i,8)=alpham*ribdif/ribdim
       end if

c      Case 2
       if (kbbb.eq.2) then
       ribdif=rib(1,5)-rib(i,5)
       ribdim=rib(1,5)-rib(nribss,5)
       rib(i,8)=(alphat*ribdif/ribdim)+alphac
       end if

       end do

c      Add virtual rib nribss+1 (used in V-ribs Type-5)

       if (nribss.ge.2) then
       do j=1,10
       rib(nribss+1,j)=rib(nribss-1,j)
       end do
       rib(nribss+1,6)=rib(nribss,6)+(rib(nribss,6)-rib(nribss-1,6))
       rib(nribss+1,7)=rib(nribss,7)+(rib(nribss,7)-rib(nribss-1,7))
       rib(nribss+1,51)=rib(nribss-1,51)
       rib(nribss+1,250)=rib(nribss-1,250)
       rib(nribss+1,251)=rib(nribss-1,251)
       end if

       write (*,*) "01-Planform read"

c      4.3 Airfoil data: name, intakes location, open cells, disp
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*)
       do i=1,nribss
       read (22,*) rib(i,1),nomair(i),rib(i,11),rib(i,12),rib(i,14)
     + ,rib(i,50),rib(i,55),rib(i,56)
       end do

       nomair(nribss+1)=nomair(nribss-1) ! Additional virtual rib
       rib(nribss+1,11)=rib(nribss-1,11)
       rib(nribss+1,12)=rib(nribss-1,12)
       rib(nribss+1,14)=rib(nribss-1,14)
       rib(nribss+1,50)=rib(nribss-1,50)
       rib(nribss+1,55)=rib(nribss-1,55)
       rib(nribss+1,56)=rib(nribss-1,56)

       write (*,*) "02-Airfoils read"

c      4.4 Airfoil data: anchor points A,B,C,D,E,F location

       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*)
       do i=1,nribss
       read (22,*) rib(i,1),rib(i,15),rib(i,16),rib(i,17),rib(i,18),
     + rib(i,19),rib(i,20),rib(i,21)
       end do

       do j=15,21 ! Additional virtual rib
       rib(nribss+1,j)=rib(nribss-1,j)
       end do

c      4.5 Load rib 0 data

       do k=1,300  ! Be sure all rib parameters are assigned (!)
       rib(0,k)=rib(1,k)
       end do
       rib(0,2)=-rib(1,2)
       rib(0,6)=-rib(1,6)
       
       write (*,*) "03-Anchors position read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.6 Read holes
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) ndis

       do m=1,ndis
       
       read (22,*) nrib1
       read (22,*) nrib2
       read (22,*) nhols

       ir=nrib1

       do l=1,nhols

       hol(ir,l,1)=float(nhols)

       read(22,*) hol(ir,l,9),hol(ir,l,2),hol(ir,l,3),hol(ir,l,4),
     + hol(ir,l,5),hol(ir,l,6),hol(ir,l,7),hol(ir,l,8)

       end do
       
       do ii=nrib1,nrib2

       do l=1,nhols

       hol(ii,l,1)=hol(ir,l,1)
       hol(ii,l,2)=hol(ir,l,2)
       hol(ii,l,3)=hol(ir,l,3)
       hol(ii,l,4)=hol(ir,l,4)
       hol(ii,l,5)=hol(ir,l,5)
       hol(ii,l,6)=hol(ir,l,6)
       hol(ii,l,7)=hol(ir,l,7)
       hol(ii,l,8)=hol(ir,l,8)
       hol(ii,l,9)=hol(ir,l,9)

       if (hol(ii,l,9).eq.11) then ! parameters for unloaded
       ii11=ii
       nhols11=nhols
       end if

       end do

       end do

       end do

       write (*,*) "04-Airfoil holes read"

       ir=1
       
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.7 Read skin tension data
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc  

       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*)

       do k=1,6
       read (22,*) skin(k,1),skin(k,2),skin(k,3),skin(k,4)
       end do
       read (22,*) htens
       htensi=htens
       read (22,*) ndif, xndif

       write (*,*) "05-Skin tension read"
 
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.8 Read sewing allowances
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) xupp, xupple, xuppte
       read (22,*) xlow, xlowle, xlowte
       read (22,*) xrib
       read (22,*) xvrib

       write (*,*) "06-Sewing allowances read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.9 Read marks
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) xmark, xcir, xdes

       write (*,*) "07-Marks read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.10 Read calage estimation parameters
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) finesse
       read (22,*)
       read (22,*) cpress
       read (22,*)
       read (22,*) calage
       read (22,*)
       read (22,*) clengr
       read (22,*)
       read (22,*) clengl
       clengl=clengl*xwf
       read (22,*)
       read (22,*) clengk

       write (*,*) "08-Calage read"

       planeig=finesse
c       write (*,*) "finesse ",finesse,planeig

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.11 Read suspension lines description
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

c      Read pondered media type zcontrol
       read (22,*) zcontrol

c      Read plans number
       read (22,*) slp

       do ii=1,int(slp) ! Brakes included

c      Read paths in plane ii
       read (22,*) cam(ii)

c      Read path i in plane ii
       do i=1,cam(ii)

       read (22,*) mc(ii,i,1), mc(ii,i,2), mc(ii,i,3), mc(ii,i,4), 
     + mc(ii,i,5),mc(ii,i,6), mc(ii,i,7), mc(ii,i,8), mc(ii,i,9),
     + mc(ii,i,14), mc(ii,i,15)

       end do

c      Reread data file
       do i=1,cam(ii)       
       backspace (22)
       end do

       do i=1,cam(ii)

c      Read normally levels 1 to 4
       if (mc(ii,i,1).le.4) then
       read (22,*) mc(ii,i,1), mc(ii,i,2), mc(ii,i,3), mc(ii,i,4), 
     + mc(ii,i,5),mc(ii,i,6), mc(ii,i,7), mc(ii,i,8), mc(ii,i,9),
     + mc(ii,i,14), mc(ii,i,15)
       mc(ii,i,10)=0.
       mc(ii,i,11)=0.
       end if
c      Read additional level number 5
       if (mc(ii,i,1).eq.5) then
       read (22,*) mc(ii,i,1), mc(ii,i,2), mc(ii,i,3), mc(ii,i,4), 
     + mc(ii,i,5),mc(ii,i,6), mc(ii,i,7), mc(ii,i,8), mc(ii,i,9),
     + mc(ii,i,10), mc(ii,i,11), mc(ii,i,14), mc(ii,i,15)
       end if

       end do

       end do

       write (*,*) "09-Lines read"

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.12 Read brakes
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       ii=slp+1

       read (22,*)
       read (22,*)
       read (22,*)

c      Rean main brake length

       read (22,*) clengb

       clengb=clengb*xwf

c      Read paths
       read (22,*) cam(ii)

c       write(*,*) "<<<<<<<<<<<< ", cam(ii)

c      Read path i
       do i=1,cam(ii)

       read (22,*) mc(ii,i,1), mc(ii,i,2), mc(ii,i,3), mc(ii,i,4), 
     + mc(ii,i,5),mc(ii,i,6), mc(ii,i,7), mc(ii,i,8), mc(ii,i,9),
     + mc(ii,i,14), brake(i,3)

c      Fractional anchors option
       brake(i,1)=dfloat(int(brake(i,3)))
       brake(i,2)=brake(i,3)-brake(i,1)
       mc(ii,i,15)=int(brake(i,3))

c       write(*,*) i, brake(i,1), brake(i,2), mc(ii,i,15)

       end do

c      Read Brake distribution

       read (22,*)
       read (22,*) bd(1,1), bd(2,1), bd(3,1), bd(4,1), bd(5,1)
       read (22,*) bd(1,2), bd(2,2), bd(3,2), bd(4,2), bd(5,2)
       bd(1,2)=bd(1,2)*xwf
       bd(2,2)=bd(2,2)*xwf 
       bd(3,2)=bd(3,2)*xwf 
       bd(4,2)=bd(4,2)*xwf 
       bd(5,2)=bd(5,2)*xwf

       write (*,*) "10-Brakes read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.13 Read ramification lengths
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) raml(3,1), raml(3,3)
       read (22,*) raml(4,1), raml(4,3), raml(4,4)
       read (22,*) raml(5,1), raml(5,3)
       read (22,*) raml(6,1), raml(6,3), raml(6,4)

       raml(3,1)=raml(3,1)*xwf 
       raml(3,3)=raml(3,3)*xwf
       raml(4,1)=raml(4,1)*xwf
       raml(4,3)=raml(4,3)*xwf  
       raml(4,4)=raml(4,4)*xwf
       raml(5,1)=raml(5,1)*xwf
       raml(5,3)=raml(5,3)*xwf
       raml(6,1)=raml(6,1)*xwf
       raml(6,3)=raml(6,3)*xwf
       raml(6,4)=raml(6,4)*xwf

       write (*,*) "11-Ramifications read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.14 Read H V and HV ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) nhvr
       read (22,*) xrsep, yrsep

       xrsep=xrsep*xkf
       yrsep=yrsep*xkf

       if (nhvr.ne.0) then
       
       do i=1,nhvr
       read (22,*) hvr(i,1),hvr(i,2),hvr(i,3),hvr(i,4),hvr(i,5),hvr(i,6)
     + ,hvr(i,7),hvr(i,8),hvr(i,9),hvr(i,10)

c      Case 3 special, use f- and r+ in % of chord, instead of absolute cm
c      Yuri request 2016-08-25
c      Set column 7 and 8 in %, and column number 9 to "1"
       if (hvr(i,2).eq.3.and.hvr(i,9).eq.1) then
       hvr(i,7)=(hvr(i,7)/100)*(rib(int(hvr(i,3)),5))

       if (hvr(i,5).eq.1.and.hvr(i,6).eq.0) then
       hvr(i,8)=(hvr(i,8)/100)*(rib(int(hvr(i,3))-1,5))
       end if
       if (hvr(i,5).eq.0.and.hvr(i,6).eq.1) then
       hvr(i,8)=(hvr(i,8)/100)*(rib(int(hvr(i,3))+1,5))
       end if
       if (hvr(i,5).eq.1.and.hvr(i,6).eq.1) then
       hvr(i,8)=(hvr(i,8)/100)*(rib(int(hvr(i,3)),5))
       end if

       end if !  case Type 3

       hvr(i,15)=0.0 ! Set increment left
       hvr(i,16)=0.0 ! Set increment right

       end do

c      Re-read file
       do i=1,nhvr
       backspace(22)
       end do

c      Allow read type 6 in lep >= 2.49
c      Feature will be deleted when updated data file format
       do i=1,nhvr
       if (hvr(i,2).eq.6.or.hvr(i,2).eq.16) then
       read (22,*) hvr(i,1),hvr(i,2),hvr(i,3),hvr(i,4),hvr(i,5),hvr(i,6)
     + ,hvr(i,7),hvr(i,8),hvr(i,9),hvr(i,10),hvr(i,11),hvr(i,12)
       else
       read (22,*) hvr(i,1),hvr(i,2),hvr(i,3),hvr(i,4),hvr(i,5),hvr(i,6)
     + ,hvr(i,7),hvr(i,8),hvr(i,9),hvr(i,10)
       hvr(i,15)=0.0 ! Set increment left
       hvr(i,16)=0.0 ! Set increment right
       end if
       end do
       
c      Inicialitzar valors a 0
       do i=1,nhvr
       hvr(i,15)=0.0d0
       hvr(i,16)=0.0d0
       hvr(i,17)=0.0d0
       hvr(i,18)=0.0d0
       hvr(i,19)=0.0d0
       hvr(i,20)=0.0d0
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Adjust some absolute values in cm by xwf
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       do i=1,nhvr

       if (hvr(i,2).eq.1) then
       hvr(i,7)=hvr(i,7)*1
       end if

       if (hvr(i,2).eq.2) then
       hvr(i,7)=hvr(i,7)*xwf
       hvr(i,8)=hvr(i,8)*xwf
       end if

       if (hvr(i,2).eq.3.and.hvr(i,9).ne.1.) then
       hvr(i,7)=hvr(i,7)*xwf
       hvr(i,8)=hvr(i,8)*xwf
       end if

       if (hvr(i,2).eq.4) then
       hvr(i,7)=hvr(i,7)*xwf
       hvr(i,8)=hvr(i,8)*xwf
       end if

       if (hvr(i,2).eq.5) then
       hvr(i,10)=hvr(i,10)*xwf
       end if

       if (hvr(i,2).eq.6) then
       hvr(i,6)=hvr(i,6)*xwf
       hvr(i,7)=hvr(i,7)*xwf
       hvr(i,11)=hvr(i,11)*xwf
       hvr(i,12)=hvr(i,12)*xwf
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat new Types in %
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       do i=1,nhvr

c      Reformat Type 11 in % to Type 1 in cm
       if (hvr(i,2).eq.11) then
       hvr(i,17)=hvr(i,7)
       hvr(i,7)=(hvr(i,17)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,20)=(hvr(i,17)/100)*(rib(int(hvr(i,5)),5))-hvr(i,7)
       hvr(i,2)=1
       end if

c      Reformat Type 12 in % to Type 2 in cm
       if (hvr(i,2).eq.12) then
       hvr(i,17)=hvr(i,7)
       hvr(i,18)=hvr(i,8)
       hvr(i,7)=(hvr(i,17)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,8)=(hvr(i,18)/100)*(rib(int(hvr(i,3)),5))
c      Proportional value at left 
       hvr(i,15)=(hvr(i,18)/100)*(rib(int(hvr(i,3))-1,5))-hvr(i,8)
c      Proportional value at right
       hvr(i,17)=(hvr(i,18)/100)*(rib(int(hvr(i,3))+1,5))-hvr(i,8)
       hvr(i,2)=2

c       write (*,*) "1>",hvr(i,1),hvr(i,15),hvr(i,8),hvr(i,17)

       end if

c      Reformat Type 13 in % to Type 3 in cm
       if (hvr(i,2).eq.13) then
       hvr(i,17)=hvr(i,7)
       hvr(i,18)=hvr(i,8)
       hvr(i,7)=(hvr(i,17)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,8)=(hvr(i,18)/100)*(rib(int(hvr(i,3)),5))
c      Proportional value at left 
       hvr(i,15)=(hvr(i,18)/100)*(rib(int(hvr(i,3))-1,5))-hvr(i,8)
c      Proportional value at right
       hvr(i,16)=(hvr(i,18)/100)*(rib(int(hvr(i,3))+1,5))-hvr(i,8)
       hvr(i,2)=3
       end if

c      Reformat Type 14 in % to Type 4 in cm
       if (hvr(i,2).eq.14) then
       hvr(i,17)=hvr(i,7)
       hvr(i,18)=hvr(i,8)
       hvr(i,7)=(hvr(i,7)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,8)=(hvr(i,8)/100)*(rib(int(hvr(i,3)),5))
c      Proportional value at left 
       hvr(i,15)=(hvr(i,17)/100)*(rib(int(hvr(i,3))-1,5))-hvr(i,7)
c      Proportional value at right
       hvr(i,16)=(hvr(i,17)/100)*(rib(int(hvr(i,3))+2,5))-hvr(i,7)
       hvr(i,2)=4
       end if

c      Reformat Type 15 in % to Type 5 in cm
       if (hvr(i,2).eq.15) then
       hvr(i,10)=(hvr(i,10)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,2)=5
       end if

c      Reformat Type 16 in % to Type 6 in cm
       if (hvr(i,2).eq.16) then
       hvr(i,6)=(hvr(i,6)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,7)=(hvr(i,7)/100)*(rib(int(hvr(i,3)),5))
       hvr(i,11)=(hvr(i,11)/100)*(rib(int(hvr(i,8)),5))
       hvr(i,12)=(hvr(i,12)/100)*(rib(int(hvr(i,8)),5))
       hvr(i,2)=6
       end if

c      NOTA: valors hvr(i,11) i hvr(i,12) són per a donar continuitat 
c      creant amples ajustat per dreta-esquerra segons corda rib

       end do

       end if

       write (*,*) "12-H V VH ribs read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.15 Read extrados colors
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) npce

c      k=total ribs with colors marks
       do k=1,npce

       read (22,*) npc1e(k), npc2e(k)

c      l=mark number in k rib
       do l=1,npc2e(k)

       read (22,*) npc3e(k,l), xpc1e(k,l), xpc2e(k,l)

       end do

       end do  

       write (*,*) "15-Extrados colors read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.16 Read intrados colors
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) npci

c      k=total ribs with colors marks
       do k=1,npci

       read (22,*) npc1i(k), npc2i(k)

c      l=mark number in k rib
       do l=1,npc2i(k)

       read (22,*) npc3i(k,l), xpc1i(k,l), xpc2i(k,l)

       end do

       end do

       write (*,*) "16-Intrados colors read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.17 Read aditional rib points
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) narp

       if (narp.eq.0) then
c      Do noting
       end if

       if (narp.ne.0) then
       do i=1,narp
       read (22,*) xarp(i), yarp(i)
       end do
       end if

       write (*,*) "17-Aditional rib points read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.18 Read elastic lines corrections
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) csusl

       read (22,*) cdis(2,1), cdis(2,2)
       read (22,*) cdis(3,1), cdis(3,2), cdis(3,3)
       read (22,*) cdis(4,1), cdis(4,2), cdis(4,3), cdis(4,4)
       read (22,*) cdis(5,1), cdis(5,2), cdis(5,3),cdis(5,4),cdis(5,5)

       do i=1,5

       read (22,*) csus(i,1), csus(i,2), csus(i,3), csus(i,4)

       end do

       write (*,*) "18-Elastic lines corrections read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SECTIONS 4.19,4.20 added since version >= 2.70
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 19 DXF layer names
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) k

       do i=1,k
       read(22,*) gname,lyname(i)
       end do

       write (*,*) "19-DXF layer names read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 20 marks types
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)

       read (22,*) k

       do i=1,k
       read(22,*) gname,typm1(i),typm2(i),typm3(i),
     + typm4(i),typm5(i),typm6(i)
       end do

       write (*,*) "20-DXF mark types read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 21 joncs definition
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k21d

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Do nothing if rods scheme 0
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k21d.eq.0) then
       k21blocs=0
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read data for nose rods scheme 1
c      Only one bloc using rods type 1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k21d.eq.1) then

       m=1 ! Only one bloc
       read (22,*) ng21 ! max groups in section 21

       do ng=1,ng21 ! read in group
       read (22,*) ngoo(m,ng,1),ngoo(m,ng,2),ngoo(m,ng,3)
       read (22,*) xextraa(m,ng,1),xextraa(m,ng,2),xextraa(m,ng,3),
     + xextraa(m,ng,4)
       read (22,*) xintraa(m,ng,1),xintraa(m,ng,2),xintraa(m,ng,3),
     + xintraa(m,ng,4)
       read (22,*) sjoo(m,ng,1),sjoo(m,ng,2),sjoo(m,ng,3),sjoo(m,ng,4)
       end do
       
c      Define jonc group rib(i,166) - NOT USED ??????
       do i=1,nribss
       rib(i,166)=0.
       end do
       do ng=1,ng21
       do i=1,nribss
       if (i.ge.ngo(ng,2).and.i.le.ngo(ng,3)) then
       rib(i,166)=float(ng)
       end if
c       write(*,*) "NG=",i,ng,rib(i,166)
       end do ! ribs
       end do ! groups

       k21blocs=1 ! set number of blocs 1
       k21blocf(1,1)=1 ! set bloc 1
       k21blocf(1,2)=1 ! set jonc type 1
       k21blocf(1,3)=ng21 ! set jonc type 1

       end if ! Type 1

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read data for nose rods scheme 2
c      In scheme 2 we have various blocs
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k21d.eq.2) then

       read (22,*) k21blocs ! number of blocs

c      Read each type
       do m=1,k21blocs

       read (22,*) k21blocf(m,1), k21blocf(m,2)

c      Case classic joncs in the nose
       if (k21blocf(m,2).eq.1) then

       read (22,*) k21blocf(m,3) ! Number of groups in bloc m
       do ng=1,k21blocf(m,3) ! read in group
       read (22,*) ngoo(m,ng,1),ngoo(m,ng,2),ngoo(m,ng,3)
       read (22,*) xextraa(m,ng,1),xextraa(m,ng,2),xextraa(m,ng,3),
     + xextraa(m,ng,4)
       read (22,*) xintraa(m,ng,1),xintraa(m,ng,2),xintraa(m,ng,3),
     + xintraa(m,ng,4)
       read (22,*) sjoo(m,ng,1),sjoo(m,ng,2),sjoo(m,ng,3),sjoo(m,ng,4)
       end do

       end if

c      Case arc joncs
       if (k21blocf(m,2).eq.2) then

       read (22,*) k21blocf(m,3) ! Number of groups in bloc m
       do ng=1,k21blocf(m,3) ! read in group
       read (22,*) ngoo(m,ng,1),ngoo(m,ng,2),ngoo(m,ng,3)
       read (22,*) x21(m,ng,1),x21(m,ng,2),x21(m,ng,3),x21(m,ng,4),
     + x21(m,ng,5)
       read (22,*) sjoo(m,ng,1),sjoo(m,ng,2),sjoo(m,ng,3),sjoo(m,ng,4)
       end do ! ng group

       end if

       end do ! bloc m
   
       end if ! Type 2

       write (*,*) "21-Joncs definition read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 22 nose mylars definition
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k22d

c      Do nothing!
       if (k22d.eq.0) then
       end if

c      Read data for nose mylars type 1
       if (k22d.eq.1) then

       read (22,*) ng22 ! max groups in section 21

       do ng=1,ng22 ! read in group
       read (22,*) ngo(ng,1),ngo(ng,2),ngo(ng,3)
       read (22,*) xmy(ng,1),xmy(ng,2),xmy(ng,3),xmy(ng,4),
     + xmy(ng,5),xmy(ng,6)
       end do
       
       end if ! Type 1

c      Define mylar group rib(i,168)
       do i=1,nribss
       rib(i,168)=0.
       end do
       do ng=1,ng22
       do i=1,nribss
       if (i.ge.ngo(ng,2).and.i.le.ngo(ng,3)) then
       rib(i,168)=float(ng)
       end if
       end do
       end do

       write (*,*) "22-Nose mylars definition read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 23 tab reinforcements definition
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k23d
       if (k23d.eq.0) then

c      Define default parameters

       else

c      Read custom parameters

       end if

       write (*,*) "23-Tab reinforcements definition read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 24 general 2D DXF options
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k
       if (k.eq.0) then

c      Define default parameters
       iccolor(1)=1    ! red
       iccolor(2)=30   ! orange
       iccolor(3)=3    ! green
       iccolor(4)=4    ! cyan
       iccolor(5)=6    ! magenta
       iccolor(6)=5    ! blue

       else

c      Read custom parameters
       read (22,*) gname, iccolor(1)
       read (22,*) gname, iccolor(2)
       read (22,*) gname, iccolor(3)
       read (22,*) gname, iccolor(4)
       read (22,*) gname, iccolor(5)
       read (22,*) gname, iccolor(6)

       end if

       write (*,*) "24-General 2D DXF options read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 25 general 3D DXF options
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k
       if (k.eq.0) then

c      Define default parameters
       iccolor(11)=8    ! red
       iccolor(12)=8  ! orange
       iccolor(13)=8    ! green
       iccolor(14)=8    ! cyan
       iccolor(15)=8    ! magenta
       iccolor(16)=30    ! blue
       ele3d(11)=0
       ele3dc(11)=5	!blue extrados
       ele3d(12)=0
       ele3dc(12)=1	!red vents
       ele3d(13)=0
       ele3dc(13)=3	!green intrados

       else

c      Read custom parameters
       read (22,*) gname, iccolor(11)
       read (22,*) gname, iccolor(12)
       read (22,*) gname, iccolor(13)
       read (22,*) gname, iccolor(14)
       read (22,*) gname, iccolor(15)
       read (22,*) gname, iccolor(16)
       read (22,*) gname, ele3d(11), ele3dc(11)
       read (22,*) gname, ele3d(12), ele3dc(12)
       read (22,*) gname, ele3d(13), ele3dc(13)

       end if

       write (*,*) "25-General 3D DXF options read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 26 Glue vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k26d

       if (k26d.eq.0) then
       else
       end if

       if (k26d.eq.1) then
       do i=1,nribss

       read (22,*) j, rib(i,165)
      
       if (rib(i,165).eq.4.or.rib(i,165).eq.-4) then
       backspace(22)
       read (22,*) j, rib(i,165),csi(i,19),csi(i,20)
       if (i.eq.1) then
       csi(i,20)=csi(i,19) ! Set coherent central cell
       end if
       end if

       if (rib(i,165).eq.5.or.rib(i,165).eq.-5) then
       backspace(22)
       read (22,*) j, rib(i,165),csi(i,19),csi(i,20),csi(i,18)
       if (i.eq.1) then
       csi(i,20)=csi(i,19) ! Set coherent central cell
       end if
       end if

       if (rib(i,165).eq.6.or.rib(i,165).eq.-6) then
       backspace(22)
       read (22,*) j, rib(i,165),csi(i,19),csi(i,20)
       end if

       end do ! i
       end if

       rib(0,165)=rib(1,165)

       write (*,*) "26-Glue vents read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 27 Special wingtip
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k

       if (k.eq.0) then
       else
       end if

       if (k.eq.1) then
       read (22,*) gname, alc1
       alc1=alc1*pi/180.
       read (22,*) gname, alc2
       alc2=alc2*pi/180.
       rib(nribss,3)=rib(nribss-1,3)+
     + (rib(nribss,2)-rib(nribss-1,2))*tan(alc1)
       rib(nribss,4)=rib(nribss-1,4)+
     + (rib(nribss,2)-rib(nribss-1,2))*tan(alc2)
       rib(nribss,5)=rib(nribss,4)-rib(nribss,3)
       end if

       write (*,*) "27-Special wingtip read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 28 Parameters for calage variation
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k28p
       if (k28p.eq.0) then ! set default values

       
       else
 
       if (k28p.eq.1) then
       read (22,*) nriser28
       read (22,*) p28(1), p28(2), p28(3), p28(4), p28(5), p28(6)
       read (22,*) a128, n128, a228, n228
       end if
       
       end if

       write (*,*) "28-Parameters for calage variation read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 29 3D-SHAPING
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k29d ! Data control
  
c      Do nothing
       if (k29d.eq.0) then
c      Set default values for no cuts
       k29dd=1
       ng29=1
       ini29(1)=1
       fin29(1)=nribss
       uppcuts(1)=0
       upptype(1)=1
       lowcuts(1)=0
       lowtype(1)=1
       do i=1,nribss
       rib(i,169)=0.
       end do
c      Set default print parameters
       do i=1,5
       pp29(i,1)=0
       pp29(i,2)=0
       pp29(i,3)=1
       pp29(i,4)=1
       pp29(i,5)=0
       end do
       end if

c       k29dd=0

c      3D-type type 1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k29d.eq.1) then

c      Initialize defaults
c      Define 3d group rib(i,169)
       do i=1,nribss
       rib(i,169)=0.
       end do

       read (22,*) k29dd  ! 3D-type (not used)

       read (22,*) gname,ng29

       do ng=1,ng29  ! Iterate in each group

       read (22,*) gname, k, ini29(ng), fin29(ng)
       read (22,*) gname, uppcuts(ng), upptype(ng)

       do i=ini29(ng),fin29(ng)
       rib(i,169)=k
       end do

       if (uppcuts(ng).eq.0) then
       end if
     
       if (uppcuts(ng).eq.1) then
       read (22,*) iupp(1,1,ng),iupp(1,2,ng),iupp(1,3,ng),kiupp(1,ng)
       end if

       if (uppcuts(ng).eq.2) then
       read (22,*) iupp(1,1,ng),iupp(1,2,ng),iupp(1,3,ng),kiupp(1,ng)
       read (22,*) iupp(2,1,ng),iupp(2,2,ng),iupp(2,3,ng),kiupp(2,ng)
       end if

       read (22,*) gname, lowcuts(ng), lowtype(ng)

       if (lowcuts(ng).eq.0) then
       end if
     
       if (lowcuts(ng).eq.1) then
       read (22,*) ilow(1,1,ng),ilow(1,2,ng),ilow(1,3,ng),kilow(1,ng)
       end if

       end do ! In each group

       end if ! 3D active type 1

c      3D-type type 2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k29d.eq.2) then

c      Read data

c      Initialize defaults
c      Define 3d group rib(i,169)
       do i=1,nribss
       rib(i,169)=0.
       end do

       read (22,*) k29dd  ! 3D-type (not used)

       read (22,*) gname,ng29

       do ng=1,ng29  ! Iterate in each group

       read (22,*) gname, k, ini29(ng), fin29(ng)
       read (22,*) gname, uppcuts(ng), upptype(ng)

       do i=ini29(ng),fin29(ng)
       rib(i,169)=k
       end do

       if (uppcuts(ng).eq.0) then
       end if
     
       if (uppcuts(ng).eq.1) then
       read (22,*) iupp(1,1,ng),xiupp(1,2,ng),xiupp(1,3,ng),kiupp(1,ng)
       end if

       if (uppcuts(ng).eq.2) then
       read (22,*) iupp(1,1,ng),xiupp(1,2,ng),xiupp(1,3,ng),kiupp(1,ng)
       read (22,*) iupp(2,1,ng),xiupp(2,2,ng),xiupp(2,3,ng),kiupp(2,ng)
       end if

       read (22,*) gname, lowcuts(ng), lowtype(ng)

       if (lowcuts(ng).eq.0) then
       end if
     
       if (lowcuts(ng).eq.1) then
       read (22,*) ilow(1,1,ng),xilow(1,2,ng),xilow(1,3,ng),kilow(1,ng)
       end if

       end do ! In each group

c      Compute discrete points ir airfoils section

     
c      Return to type 1
       k29d=1

       end if ! 3D active type 2

c      Read print parameters
       if (k29d.ne.0) then
       read (22,*)
       read (22,*) gname,pp29(1,1),pp29(1,2),pp29(1,3),pp29(1,4)
       read (22,*) gname,pp29(2,1),pp29(2,2),pp29(2,3),pp29(2,4)
       read (22,*) gname,pp29(3,1),pp29(3,2),pp29(3,3),pp29(3,4)
       read (22,*) gname,pp29(4,1),pp29(4,2),pp29(4,3),pp29(4,4)
       read (22,*) gname,pp29(5,1),pp29(5,2),pp29(5,3),pp29(5,4)
       end if

c      Print panels using 3D subroutines
       if (k29d.eq.0) then
       k29d=1
       end if

c      Compute discrete points
       rib(0,169)=rib(1,169)

       write (*,*) "29-3D-Shaping read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read 30 AIRFOIL THICKNESS MODIFICATION
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k
       if (k.eq.0) then

       do i=1,nribss
       rib(i,160)=1.0 ! Standard thickness
       end do

       else

       if (k.eq.1) then

       do i=1,nribss

       read (22,*) i9, rib(i,160)

       end do

       end if

       end if

       write (*,*) "30-Airfoil modification read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      31. Read new skin tension
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k31d

       if (k31d.eq.0) then

       else

       if (k31d.eq.1) then

       read (22,*) ngskt ! max groups

       do ng=1,ngskt ! read in group
    
       read (22,*)
       read (22,*) ngi, nribini, nribfin, npoints, ntype31

       do i=nribini,nribfin
       skinpoints(i)=npoints
       ngroup31(i)=ngi
       ntypei31(i)=ntype31
       end do

       do k=1,npoints ! read points
       read (22,*) ksk, skinew(k,1),skinew(k,2),
     + skinew(k,3),skinew(k,4)

       do i=nribini,nribfin ! assign in each rib group
       skinnew(i,k,1)=skinew(k,1)
       skinnew(i,k,2)=skinew(k,2)
       skinnew(i,k,3)=skinew(k,3)
       skinnew(i,k,4)=skinew(k,4)
       end do

       end do ! read all points in group

       end do

       end if

c      Set 0 rib
       skinpoints(0)=skinpoints(1)
       ngroup31(0)=ngroup31(1)
       ntypei31(0)=ntypei31(1)
       do k=1,npoints
       skinnew(0,k,1)=skinnew(1,k,1)
       skinnew(0,k,2)=skinnew(1,k,2)
       skinnew(0,k,3)=skinnew(1,k,3)
       skinnew(0,k,4)=skinnew(1,k,4)
       end do

       end if

       write (*,*) "31-New skin tension read"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      32. Read parameters for part separation
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       read (22,*)
       read (22,*)
       read (22,*)
       read (22,*) k32d

       if (k32d.eq.0) then

       panel_x_coe=1.0
       panel_x_min=1.0
       panel_y_coe=1.0
       rib_x_coe=1.0
       rib_y_coe=1.0

       else

       if (k32d.eq.1) then
       read (22,*) gname, panel_x_coe
       read (22,*) gname, panel_x_min
       read (22,*) gname, panel_y_coe
       read (22,*) gname, rib_x_coe
       read (22,*) gname, rib_y_coe
       end if

       end if

       write (*,*) "32-Parameters for part separation read"


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Some warnings and errors found in data
c      Do not cover all errors, but some of habitual
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Number of ribs and cells case even odd 
c      Ribs even > cells -1
c      Ribs odd > cells

       if (ncells.ne.nribst-1) then
       write (*,*) "ERROR: number of cells will be number of ribs -1"
       end if

       
c     COMPLETE



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       write (*,*) "All data read! Calculus start..."
       write (*,*)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Alguns paràmetres de mides
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xmida1=12.0d0*xkf/1.5d0  ! Mida de lletra 1
       xmida2=10.0d0*xkf/1.5d0  ! Mida de lletra 2  
       xmida3=6.0d0*xkf/1.5d0   ! Mida de lletra 3 petita
       xmida4=3.0d0*xkf/1.5d0   ! Mida de lletra 4 molt petita 

       xmida3=xmida3 ! primer us
       xmida4=xmida4   

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      PARAMETERS TO BE DEFINED IN DATA FILE
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Revise all overrides
c      Try to normalize to cm as soon as possible      
       typepoint=typm4(1)
       typevent=typm4(4)
       typetab=typm4(5)
       typejonc=typm4(6)

       if (typm4(1).eq.1) then
       xdes=typm6(1)/10.0d0 !override classic xdes
       end if

       if (typm4(1).eq.2) then
       xrad=typm5(1)
       xdes=typm6(1)/10.0d0 !override classic xdes
       end if

c      Compte amb aquesta definició!
       if (typm4(5).le.3) then
       typm5(5)=typm5(5)/10.0d0 !override classic 1 cm
       typm6(5)=typm6(5)/10.0d0 !override classic xdes 1.2 mm
       end if

       xdes1=typm3(1)/10.0d0
       xdes2=typm6(1)/10.0d0
       xcir1=typm2(1)/10.0d0
       xcir2=typm5(1)/10.0d0

c       write (*,*) "xdes=",xdes

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.19 Center of gravity calculus (2D)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Planform

       acit=rib(1,2)*rib(1,5)
       cdgx=0.5*rib(1,2)*acit
       cdgy=0.5*(rib(1,3)+rib(1,4))*acit

       do i=1,nribss-1

       aci=0.5*(rib(i,5)+rib(i+1,5))*(rib(i+1,2)-rib(i,2))
       xci=0.5*(rib(i,2)+rib(i+1,2))
       yci=0.25*(rib(i,3)+rib(i,4)+rib(i+1,3)+rib(i+1,4))

       cdgx=cdgx+xci*aci
       cdgy=cdgy+yci*aci

       acit=acit+aci

       end do

       cdgx=cdgx/acit
       cdgy=cdgy/acit

       cdg=100.*((cdgy-rib(1,3))/rib(1,5))

       if (atp.eq."ds".or.atp.eq."ss") then
       write (*,'(A,F5.2,A)') " Area = ", acit*2./10000., " m2"
       else
       write (*,'(A,F5.2,A,F7.1,A)') " Area = ", acit*2./10000., " m2 ",
     + 10.7639*acit*2./10000.," ft2"
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      4.20 Adjust some parameters
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Ample panells extrados a efectes de separació
       amplemig=0.0d0
       npaes=int(nribss/2)
       do i=2,npaes
       amplemig=amplemig+rib(i,2)-rib(i-1,2)
       end do
       amplemig=amplemig/float(npaes-1)

c      Escala descensos de ribs no suspentats
c      WARNING revisar concepte (!)
       do i=1,nribss

       rib(i,50)=rib(i,50)*xwf

       end do

c      Parts separation parameters (SECTION 32)
c      Default parameters
       amplerix=1.0*rib_x_coe
       ampleriy=1.0*rib_y_coe
       amplepix=1.1*panel_x_coe

c      Rib separation parameters
       seprix=350.*xwf*amplerix
       sepriy=90.*xwf*ampleriy

c      Panels separation
c      seppix(i)=60.*xwf
c      seppix(i)=(amplemig*1.7+(0.20d0*xupp))*amplepix

c      Define separation between panels proportional to its width
       seppix(0)=-30.0d0
       do i=1,nribss
       seppix(i)=(seppix(i-1)+xwf*(rib(i,2)-rib(i-1,2))*amplepix+
     + 0.2d0*xupp+10.0d0*panel_x_min)
       end do
      
c      Compute some ribs additional parameters
c      Lengths from LE to anchor points A,B,...E

      do i=0,nribss

      rib(i,66)=(rib(i,16)*rib(i,5)/100.)
      rib(i,67)=(rib(i,17)*rib(i,5)/100.)
      rib(i,68)=(rib(i,18)*rib(i,5)/100.)
      rib(i,69)=(rib(i,19)*rib(i,5)/100.)
      rib(i,70)=(rib(i,20)*rib(i,5)/100.)

      end do

c     y separation for panels parts

      ysautt=(rib(1,5)+rib(nribss-2,5))*0.5d0*xwf*0.2d0*panel_y_coe

c     Some parameters for internal marks (subroutine xmarsi)
      xini=0.0d0
      xfin=0.0d0

c     Adjust beta rotation in rib 0
      rib(0,9)=-rib(1,9)
c     Adjust rot_z rotation in rib 0
      rib(0,250)=-rib(1,250)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     4.21 DXF layers  (project)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5. GRAPHIC DESIGN
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5.1 Planform
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,1)

c      Ribs
       do i=1,nribss
       call line(rib(i,2),rib(i,3),rib(i,2),rib(i,4),5)
       call line(-rib(i,2),rib(i,3),-rib(i,2),rib(i,4),5)

       call itxt(rib(i,2)-110.*(typm3(9)/10.),rib(i,3)-15,
     + typm3(9),0.0d0,i,7)
       call itxt(-rib(i,2)-110.*(typm3(9)/10.),rib(i,3)-15,
     + typm3(9),0.0d0,i,7)

       end do

c      Draw rotated ribs ("Z" versions")

       do i=1,nribss
c      Using auxiliar points 1,2,3
       x3=rib(i,2)
       y3=rib(i,3)+(rib(i,4)-rib(i,3))*rib(i,251)/100.0
       x1=x3+(y3-rib(i,3))*dsin(rib(i,250)*pi/180.0)
       y1=y3-(y3-rib(i,3))*dcos(rib(i,250)*pi/180.0)
       x2=x3-(rib(i,4)-y3)*dsin(rib(i,250)*pi/180.0)
       y2=y3+(rib(i,4)-y3)*dcos(rib(i,250)*pi/180.0)

       if (dabs(rib(i,250)).gt.0.01d0) then ! 0.000 in IF
       call line(x1,y1,x2,y2,2)
       call line(-x1,y1,-x2,y2,2)
       end if

       end do

c      Leading edge        
       call line(-rib(1,2),rib(1,3),rib(1,2),rib(1,3),1)
       do i=1,nribss-1
       call line(rib(i,2),rib(i,3),rib(i+1,2),rib(i+1,3),1)
       call line(-rib(i,2),rib(i,3),-rib(i+1,2),rib(i+1,3),1)
       end do
 
c      Trailing edge  
       call line(-rib(1,2),rib(1,4),rib(1,2),rib(1,4),3)
       do i=1,nribss-1
       call line(rib(i,2),rib(i,4),rib(i+1,2),rib(i+1,4),3)
       call line(-rib(i,2),rib(i,4),-rib(i+1,2),rib(i+1,4),3)
       end do

c      Vents

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      DRAW vents in CASES in 1-1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k26d.eq.1) then

      
       do i=1,nribss

c      Vents: Line 1-2 in, Line 3-4 out
       pgx(1)=rib(i-1,2)
       pgy(1)=rib(i-1,3)+rib(i-1,5)*rib(i,11)/100.
       pgx(2)=rib(i,2)
       pgy(2)=rib(i,3)+rib(i,5)*rib(i,11)/100.
       pgx(3)=rib(i,2)
       pgy(3)=rib(i,3)+rib(i,5)*rib(i,12)/100.
       pgx(4)=rib(i-1,2)
       pgy(4)=rib(i-1,3)+rib(i-1,5)*rib(i,12)/100.

c      Draw especial vents CASE 0
       if (rib(i,165).eq.0.) then
       call line(pgx(3),pgy(3),pgx(4),pgy(4),6)
       call line(-pgx(3),pgy(3),-pgx(4),pgy(4),6)
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       end if

c      Draw especial vents CASE 1
       if (rib(i,165).eq.1) then
       call line(pgx(3),pgy(3),pgx(4),pgy(4),6)
       call line(-pgx(3),pgy(3),-pgx(4),pgy(4),6)
       end if

c      Draw especial vents CASE 4
       if (rib(i,165).eq.4.) then
c      Line 5-6
       param1=csi(i,19)
       param2=csi(i,20)
       pgy(5)=pgy(1)+((pgy(4)-pgy(1)))*(1.-(param1/100.))
       pgy(6)=pgy(2)+((pgy(3)-pgy(2)))*(1.-(param2/100.))
       call line(pgx(1),pgy(5),pgx(2),pgy(6),6)
       call line(-pgx(1),pgy(5),-pgx(2),pgy(6),6)
c      Line 3-4
       call line(pgx(3),pgy(3),pgx(4),pgy(4),6)
       call line(-pgx(3),pgy(3),-pgx(4),pgy(4),6)
       end if

c      Draw especial vents CASE 5
       if (rib(i,165).eq.5.) then
c      Arc 5-6
       param1=csi(i,19)
       param2=csi(i,20)
c      Fletxa as % of vent
       param3=csi(i,18)*(pgy(4)-pgy(1)+pgy(3)-pgy(2))/200.
       pgy(5)=pgy(1)+((pgy(4)-pgy(1)))*(1.-(param1/100.))
       pgy(6)=pgy(2)+((pgy(3)-pgy(2)))*(1.-(param2/100.))
c      Arc 5-6
       call arcfle(pgx(1),pgy(5),pgx(2),pgy(6),param3,1,6)
       call arcfle(-pgx(1),pgy(5),-pgx(2),pgy(6),param3,1,6)
c      Line 3-4
       call line(pgx(3),pgy(3),pgx(4),pgy(4),6)
       call line(-pgx(3),pgy(3),-pgx(4),pgy(4),6)
       end if

c      Draw especial vents CASE 6
       if (rib(i,165).eq.6) then
       call line(pgx(3),pgy(3),pgx(4),pgy(4),6)
       call line(-pgx(3),pgy(3),-pgx(4),pgy(4),6)
       param1=csi(i,19)
       param2=csi(i,20)
       call elliquad(pgx,pgy,param1,param2)
       call elliquad(-pgx,pgy,param1,param2)
       end if

c      Draw especial vents CASE -1
       if (rib(i,165).eq.-1.) then
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       end if

c      Draw especial vents CASE -2
       if (rib(i,165).eq.-2.) then
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       call line(pgx(4),pgy(4),pgx(2),pgy(2),6)
       call line(-pgx(4),pgy(4),-pgx(2),pgy(2),6)
       end if

c      Draw especial vents CASE -3
       if (rib(i,165).eq.-3.) then
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       call line(pgx(1),pgy(1),pgx(3),pgy(3),6)
       call line(-pgx(1),pgy(1),-pgx(3),pgy(3),6)
       end if

c      Draw especial vents CASE -4
       if (rib(i,165).eq.-4.) then
c      Line 5-6
       param1=csi(i,19)
       param2=csi(i,20)
       pgy(5)=pgy(1)+((pgy(4)-pgy(1)))*(1.-(param1/100.))
       pgy(6)=pgy(2)+((pgy(3)-pgy(2)))*(1.-(param2/100.))
       call line(pgx(1),pgy(5),pgx(2),pgy(6),6)
       call line(-pgx(1),pgy(5),-pgx(2),pgy(6),6)
c      Line 1-2
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       end if

c      Draw especial vents CASE -5
       if (rib(i,165).eq.-5.) then
c      Arc 5-6
       param1=csi(i,19)
       param2=csi(i,20)
c      Fletxa as % of vent
       param3=csi(i,18)*(pgy(4)-pgy(1)+pgy(3)-pgy(2))/200.
       pgy(5)=pgy(1)+((pgy(4)-pgy(1)))*(1.-(param1/100.))
       pgy(6)=pgy(2)+((pgy(3)-pgy(2)))*(1.-(param2/100.))
c      Arc 5-6
       call arcfle(pgx(1),pgy(5),pgx(2),pgy(6),param3,-1,6)
       call arcfle(-pgx(1),pgy(5),-pgx(2),pgy(6),param3,-1,6)
c      Line 1-2
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       end if

c      Draw especial vents CASE -6
       if (rib(i,165).eq.-6) then
       call line(pgx(1),pgy(1),pgx(2),pgy(2),6)
       call line(-pgx(1),pgy(1),-pgx(2),pgy(2),6)
       param1=csi(i,19)
       param2=csi(i,20)
       call elliquad(pgx,pgy,param1,param2)
       call elliquad(-pgx,pgy,param1,param2)
       end if

        end do

        end if ! k26d=1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw vents classic in 1-1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k26d.eq.0) then

c      Intake in

       if (cencell.ge.0.01.and.rib(1,14).eq.1)  then  
       call line(-rib(1,2),rib(1,3)+rib(1,5)*rib(1,11)/100.,rib(1,2),
     + rib(1,3)+rib(1,5)*rib(1,11)/100.,6)
       end if

       do i=2,nribss
       if(rib(i,14).eq.1) then
       call line(rib(i-1,2),rib(i-1,3)+rib(i-1,5)*rib(1,11)/100.,
     + rib(i,2),rib(i,3)+rib(i,5)*rib(1,11)/100.,6)
       call line(-rib(i-1,2),rib(i-1,3)+rib(i-1,5)*rib(1,11)/100.,
     + -rib(i,2),rib(i,3)+rib(i,5)*rib(1,11)/100.,6)
       end if

       if(rib(i,14).eq.0) then
       call line(rib(i-1,2),rib(i-1,3)+rib(i-1,5)*rib(1,11)/100.,
     + rib(i,2),rib(i,3)+rib(i,5)*rib(1,11)/100.,9)
       call line(-rib(i-1,2),rib(i-1,3)+rib(i-1,5)*rib(1,11)/100.,
     + -rib(i,2),rib(i,3)+rib(i,5)*rib(1,11)/100.,9)
       end if          

       end do

c      Central cell
       i=1
       if(rib(i,14).eq.0) then
       call line(-rib(i,2),rib(i,3)+rib(i,5)*rib(1,11)/100.,
     + rib(i,2),rib(i,3)+rib(i,5)*rib(1,11)/100.,9)
       end if      
        
c      Intake out

       if (cencell.ge.0.01.and.rib(1,14).eq.1)  then  
       call line(-rib(1,2),rib(1,3)+rib(1,5)*rib(1,12)/100.,rib(1,2),
     + rib(1,3)+rib(1,5)*rib(1,12)/100.,6)
       end if

       do i=2,nribss
       if(rib(i,14).eq.1) then
       call line(rib(i-1,2),rib(i-1,3)+rib(i-1,5)*rib(1,12)/100.,
     + rib(i,2),rib(i,3)+rib(i,5)*rib(1,12)/100.,6)
       call line(-rib(i-1,2),rib(i-1,3)+rib(i-1,5)*rib(1,12)/100.,
     + -rib(i,2),rib(i,3)+rib(i,5)*rib(1,12)/100.,6)
       end if
       end do

       end if ! k26d=0


c      Anchor points

       xpoi=3. ! segment

       do i=1,nribss

       do k=1,int(rib(i,15))

       call line(rib(i,2)-xpoi,rib(i,3)+rib(i,5)*rib(i,15+k)/100.,
     + rib(i,2)+xpoi,rib(i,3)+rib(i,5)*rib(i,15+k)/100.,1)

       call line(xpoi-rib(i,2),rib(i,3)+rib(i,5)*rib(i,15+k)/100.,
     + -rib(i,2)-xpoi,rib(i,3)+rib(i,5)*rib(i,15+k)/100.,1)
       
       end do
       end do

c      Brakes in 2D included fractionary points

       do k=1,cam(ii)     ! cam in brake lines

       i=int(brake(k,3))  ! rib

       if (rib(i,21).ne.0.) then

       xr=rib(i,2)
       xs=rib(i,3)+rib(i,5)*rib(i,21)/100.

       brake(k,1)=float(int(brake(k,3)))
       brake(k,2)=brake(k,3)-brake(k,1)

       if (i.lt.nribss.and.brake(k,2).ne.0.) then
       xrm=rib(i+1,2)
       xsm=rib(i+1,3)+rib(i+1,5)*rib(i+0,21)/100.0d0 ! i+0 ok
       xr=xr+brake(k,2)*(xrm-xr)
       xs=xs+brake(k,2)*(xsm-xs)
       end if

       call ellipse(xr,xs,1.5d0*xcir,1.5d0*xcir,0.0d0,1)
       call ellipse(-xr,xs,1.5d0*xcir,1.5d0*xcir,0.0d0,1)

       end if

       end do

c      Restitute virtual anchor for 3D if rib i+1 not defined
c      Not strictly necessary
       do k=1,cam(ii)
       i=int(brake(k,3)) 
       if (i.lt.nribss.and.rib(i+1,21).eq.0.and.brake(k,2).ne.0) then
       rib(i+1,21)=100.  ! only 100% case, or specify value
       end if   
       end do

c      Extrados colors

       xpoi=2. ! segment

       do k=1,npce
      
       i=npc1e(k)

       do l=1,npc2e(k)

       ydist=100.-xpc1e(k,l)

       call line(rib(i,2)-xpoi,rib(i,3)+rib(i,5)*ydist/100.,
     + rib(i,2)+xpoi,rib(i,3)+rib(i,5)*ydist/100.,4)
       
       end do
       end do

c      Intrados colors

       if (atp.ne."ss") then

       xpoi=2. ! segment

       do k=1,npci
      
       i=npc1i(k)

       do l=1,npc2i(k)

       ydist=100.-xpc1i(k,l)

       call line(-rib(i,2)-xpoi,rib(i,3)+rib(i,5)*ydist/100.,
     + -rib(i,2)+xpoi,rib(i,3)+rib(i,5)*ydist/100.,7)
       
       end do
       end do

       end if

c      Miniribs and unloaded middle ribs

       rib(0,2)=-rib(1,2)
       rib(0,3)=rib(1,3)
       rib(0,4)=rib(1,4)

       do i=1,nribss

c      Draw only if minirib present
       if (rib(i,56).gt.1) then

       xru(1)=0.5*(rib(i,2)+rib(i-1,2))
       xrv(1)=0.5*(rib(i,3)+rib(i-1,3))
       xru(2)=0.5*(rib(i,2)+rib(i-1,2))
       xrv(2)=0.5*(rib(i,4)+rib(i-1,4))
       xrv(1)=xrv(2)-0.5*(rib(i,5)+rib(i-1,5))*rib(i,56)/100.

       call line(xru(1),xrv(1),xru(2),xrv(2),8)
       call line(-xru(1),xrv(1),-xru(2),xrv(2),8)
       
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5.2 Canopy design - vault
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,1)

       x0=0.
       y0=380.*xkf

       call line(-rib(1,6),y0+rib(1,7),rib(1,6),y0+rib(1,7),5)
       do i=1,nribss-1
       call line(rib(i,6),y0+rib(i,7),rib(i+1,6),y0+rib(i+1,7),5)
       call line(-rib(i,6),y0+rib(i,7),-rib(i+1,6),y0+rib(i+1,7),5)
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5.3 Boxes
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Matrix 6x4

       do asep=0.,7.,1.
       do bsep=0.,3.,1.

       x1=-630.*xkf+asep*1260.*xkf
       x2=630.*xkf+asep*1260.*xkf
       y1=-50.*xkf+bsep*890.95*xkf
       y2=840.95*xkf+bsep*890.95*xkf

       call line(x1,y1,x2,y1,9)
       call line(x1,y1,x1,y2,9)
       call line(x2,y1,x2,y2,9)
       call line(x1,y2,x2,y2,9)
       
       end do
       end do

c      Additional boxes for 3D-shaping

       if (n1draw.eq.1) then

       if (k29d.ne.0) then

       do asep=2.,4.,1.
       do bsep=-1.,-2.,-1.

       x1=-630.*xkf+asep*1260.*xkf
       x2=630.*xkf+asep*1260.*xkf
       y1=-50.*xkf+bsep*890.95*xkf
       y2=840.95*xkf+bsep*890.95*xkf

       if (asep.ne.3.) then
       call line(x1,y1,x2,y1,9)
       call line(x1,y1,x1,y2,9)
       call line(x2,y1,x2,y2,9)
       call line(x1,y2,x2,y2,9)
       end if
       
       end do
       end do

       end if
       end if ! n1draw

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6. AIRFOILS coordinates calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Read airfoils
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss

c      rewind 23
       open (24, file=nomair(i))
       rewind (24)

       k=len_trim(nomair(i))
       nomairext(i)=nomair(i)(k-2:k)

c       write (*,*) i,nomair(i),k,nomairext(i),"OK"

c      Case .txt airfoil

       if (nomairext(i).eq."txt") then

c      6.1 Read global points
       read (24,*) 
       read (24,*) np(i,1) ! total points
       read (24,*) np(i,2) ! extrados points
       read (24,*) np(i,3) ! intake points
       read (24,*) np(i,4) ! intrados points

       np(i,5)=np(i,2)+np(i,3)-1
       
c      Rib 0 points
       np(0,1)=np(1,1)
       np(0,2)=np(1,2)
       np(0,3)=np(1,3)
       np(0,4)=np(1,4)
       np(0,5)=np(1,5)

c      Rib nribss+1 points
       np(nribss+1,1)=np(nribss-1,1)
       np(nribss+1,2)=np(nribss-1,2)
       np(nribss+1,3)=np(nribss-1,3)
       np(nribss+1,4)=np(nribss-1,4)
       np(nribss+1,5)=np(nribss-1,5)

c      6.2 Read airfoil coordinates
       do j=1,np(i,1)
       read (24,*) u(i,j,1),v(i,j,1)
       v(i,j,1)=v(i,j,1)*rib(i,160)
       end do

       end if ! case .txt

c      Case .dat airfoil

       if (nomairext(i).eq."dat") then
c      Go to reformat airfoil (u,v) and np
       call datair(i,rib,np,u,v)

       end if

       end do ! i

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Detect cut points if defined by points (case 1)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Do nothing

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Detect cut points if defined by % along contour from TE (case 2)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k29dd.eq.2) then

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Detect cut points if defined by % (case 3)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       if (k29dd.eq.3) then

       do i=1,nribss
       ng=rib(i,169)
       do j=1,np(i,1)-1

c       write (*,*) xiupp(1,2,ng),u(i,j,1)
c       if (u(i,j,1).lt.xiupp(1,2,ng).and.u(i,j+1,1).ge.xiupp(1,2,ng)) then
       iupp(1,2,ng)=j
c       end if
c       if (u(i,j,1).gt.xiupp(1,3,ng).and.u(i,j+1,1).ge.xiupp(1,3,ng)) then
c       iupp(1,3,ng)=j
c       end if
c       if (u(i,j,1).gt.xiupp(2,2,ng).and.u(i,j+1,1).ge.xiupp(2,2,ng)) then
c       iupp(2,2,ng)=j
c       end if
c       if (u(i,j,1).gt.xiupp(2,3,ng).and.u(i,j+1,1).ge.xiupp(2,3,ng)) then
c       iupp(2,3,ng)=j
c       end if
c      Think intrados/extrdos cases

c       if (u(i,j,1).lt.xilow(1,2,ng).and.u(i,j+1,1).ge.xilow(1,2,ng)) then
c       ilow(1,2,ng)=j
c       end if
c       if (u(i,j,1).lt.xilow(1,3,ng).and.u(i,j+1,1).ge.xilow(1,3,ng)) then
c       ilow(1,3,ng)=j
c       end if

       end do
       end do

c       end if ! k29dd=3


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Airfoil coordinates modifications
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss+1

       tetha=rib(i,8)*pi/180.0d0
       rot_z=rib(i,250)*pi/180.0d0
       pos=rib(i,5)*rib(i,251)/100.0d0

       do j=1,np(i,1)

c      6.3 Airfoil coordinates *100
       u(i,j,2)=100.*u(i,j,1)
       v(i,j,2)=100.*v(i,j,1)

c      6.4 Airfoil escaled and displaced coordinates
       u(i,j,3)=rib(i,5)*u(i,j,1)
       v(i,j,3)=rib(i,5)*v(i,j,1)-rib(i,50)

c      6.5 Airfoil washin coordinates, rotation in X-axis
       u(i,j,4)=(u(i,j,3)-(rib(i,10)/100.)*rib(i,5))*dcos(tetha)+
     + (v(i,j,3))*dsin(tetha)+(rib(i,10)/100.)*rib(i,5)
       v(i,j,4)=(-u(i,j,3)+(rib(i,10)/100.)*rib(i,5))*dsin(tetha)+
     + (v(i,j,3))*dcos(tetha)

c      6.5+ Airfoil rotation in Z by pos

       wnew(j)=-u(i,j,4)*dsin(rot_z)+pos*dsin(rot_z)
       unew(j)=u(i,j,4)*dcos(rot_z)+pos*(1-dcos(rot_z))
       vnew(j)=v(i,j,4)

       u(i,j,4)=unew(j)
       v(i,j,4)=vnew(j)
       w(i,j,4)=wnew(j)

c      6.6 Airfoil (u,v,w) espace coordinates
c       u(i,j,5)=u(i,j,4)
c       v(i,j,5)=v(i,j,4)*dcos(rib(i,9)*pi/180.)
c       w(i,j,5)=-v(i,j,4)*dsin(rib(i,9)*pi/180.)

c      6.6 Airfoils rotation in Y-axis
       w(i,j,5)=-w(i,j,4)*dcos(rib(i,9)*pi/180.)-
     + v(i,j,4)*dsin(rib(i,9)*pi/180.)
       u(i,j,5)=u(i,j,4)
       v(i,j,5)=-w(i,j,4)*dsin(rib(i,9)*pi/180.)+
     + v(i,j,4)*dcos(rib(i,9)*pi/180.)

c      6.7 Airfoil (x,y,z) absolute coordinates
       x(i,j)=rib(i,6)-w(i,j,5)
       y(i,j)=rib(i,3)+u(i,j,5)
       z(i,j)=rib(i,7)-v(i,j,5)

       u_aux(i,j,9)=y(i,j)
       v_aux(i,j,9)=z(i,j)
       w_aux(i,j,9)=x(i,j)

c      6.8 Tornar a posar la costella al seu lloc
       v(i,j,3)=v(i,j,3)+rib(i,50)

c      6.5,6.6,6.7 Call to subroutine xyzt
c       u_aux(i,j,1)=u(i,j,3)
c       v_aux(i,j,1)=v(i,j,3)-rib(i,50)
c       w_aux(i,j,1)=0.0d0
c       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
c       x(i,j)=w_aux(i,j,5)
c       y(i,j)=u_aux(i,j,5)
c       z(i,j)=v_aux(i,j,5)

c      6.8 Tornar a posar la costella al seu lloc
c      WARNING! Això no ho veig clar
c      Fer experiment per a verificar. És necessari?
c       v(i,j,3)=v(i,j,3)+rib(i,50)

c      Calcule nose point np(i,6) with coordinates (0,0)
       if(dabs(u(i,j,2)).lt.0.000001d0.and.dabs(v(i,j,2)).lt.
     + 0.000001d0) then
       np(i,6)=j
       np(0,6)=np(1,6)
       end if

       end do ! j

c      Additional point in airfoil plane (use in 10.1+)
       j=1
       u_aux(i,j,1)=(u(i,1,3)+u(i,np(i,6),3))*0.5d0
       v_aux(i,j,1)=50.0d0
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       x_apap(i)=w_aux(i,j,5)
       y_apap(i)=u_aux(i,j,5)
       z_apap(i)=v_aux(i,j,5)

       end do ! i

c      6.9 Airfoil 0 = 1' (symetrical to airfoil 1) BUT NON DISPLACED COORD

       do j=1,np(1,1)

       u(0,j,1)=u(1,j,1)
c      v(0,j,1)=u(1,j,1) ERROR
       v(0,j,1)=v(1,j,1)

c      Airfoil coordinates *100
       u(0,j,2)=u(1,j,2)
       v(0,j,2)=v(1,j,2)

c      Airfoil escaled coordinates
       u(0,j,3)=u(1,j,3)
       v(0,j,3)=v(1,j,3)

c      Airfoil washin coordinates
       u(0,j,4)=u(1,j,4)
       v(0,j,4)=v(1,j,4)

c      Airfoil (u,v,w) espace coordinates
       u(0,j,5)=-u(1,j,5)
       v(0,j,5)=v(1,j,5)
       w(0,j,5)=w(1,j,5)

c      Airfoil (x,y,z) absolute coordinates
       x(0,j)=-x(1,j)
       y(0,j)=y(1,j)
       z(0,j)=z(1,j)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Tornar a posar la costella al seu lloc
c      WARNING WARNIG
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       v(0,j,3)=u(1,j,3)+rib(1,50)  ERROR
       v(0,j,3)=v(1,j,3)

       end do

c      6.10 Assignation 3D coordinates airfoil 0:

       i=1 ! WARNIING
       do j=1,np(1,1)
       xx(i,j)=-rib(i,6)+w(1,j,5)
       yy(i,j)=rib(i,3)+u(1,j,5)
       zz(i,j)=rib(i,7)-v(1,j,5)
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.10+ Compute TE-anchor lengths along airfoil contour
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

       do klz=1,rib(i,15) ! Iterate in A,B,C,D,E

       do j=np(i,1),2,-1

c      Detect segment j-1,j where anchor A,B,C,D,E is and interpolate
c      point u,v = rib(i,110+klz) rib(i,120+klz)

       if (u(i,j-1,3).le.rib(i,65+klz).and.u(i,j,3).gt.rib(i,65+klz).
     + and.u(i,j,3).ge.0) then

c      Interpolation v=xm * u + xb
       rib(i,110+klz)=rib(i,65+klz)
       xm=(v(i,j,3)-v(i,j-1,3))/(u(i,j,3)-u(i,j-1,3))
       xb=v(i,j-1,3)-xm*u(i,j-1,3)
       rib(i,120+klz)=xm*rib(i,110+klz)+xb

c      Compute distances along bottom surface

       rib(i,130+klz)=0.
       do jj=np(i,1),j+1,-1
       rib(i,130+klz)=rib(i,130+klz)+sqrt((u(i,jj,3)-u(i,jj-1,3))**2+
     + (v(i,jj,3)-v(i,jj-1,3))**2)
       end do
       rib(i,130+klz)=rib(i,130+klz)+sqrt((u(i,j,3)-rib(i,110+klz))**2+
     + (v(i,j,3)-rib(i,120+klz))**2)

c      Verificar amb CAD!!!

       end if

       end do ! j

c       write (*,*) i,klz,rib(i,131)

       end do ! klz

       end do ! rib i

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.11 Compute external cutt edges in airfoils (i,j,16)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      REVISAR LA PREOGRAMACIO. SIMPLIFICAR

       xcos=xrib/10. ! rib sewing allowance mm to cm

       do i=0,nribss
      
       do j=2,np(i,1)-1

c      Amplification factor
       xcosk=1.0

c      Fer mitja entre j-1 i j+1
       alpha1=(datan((v(i,j+1,3)-v(i,j,3))/((u(i,j+1,3)-u(i,j,3)))))
       alpha2=(datan((v(i,j,3)-v(i,j-1,3))/((u(i,j,3)-u(i,j-1,3)))))

       alpha=0.5*(alpha1+alpha2)

c      Alpha correction in sawtooht mono-surface airfoils
c      Dóna la volta a la vora superior

       if (alpha1.lt.0.and.alpha2.gt.0.and.j.ge.np(i,2)) then
c       alpha=alpha+pi
c       write (*,*) "correccio"
       end if     

       if (i.eq.1) then
c       write (*,*) "AQUI ",i,j,alpha1,alpha2,alpha
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Correcció xcosk a vores dent de serra
       if (atp.eq."ss".and.j.ge.np(i,2)+np(i,3)-1) then
       xcosk=1./(dsin(0.5*(pi+alpha1-alpha2))) 
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       u(i,j,16)=u(i,j,3)-xcos*xcosk*dsin(alpha)

       if(v(i,j,3).ge.0.) then
       v(i,j,16)=v(i,j,3)+xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,3).ge.0.and.j.ge.np(i,2)) then
       u(i,j,16)=u(i,j,3)+xcos*xcosk*dsin(alpha)
       v(i,j,16)=v(i,j,3)-xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,3).lt.0.) then
       u(i,j,16)=u(i,j,3)+xcos*xcosk*dsin(alpha)
       v(i,j,16)=v(i,j,3)-xcos*xcosk*dcos(alpha)
       end if

       if(u(i,j,3).eq.0) then
       u(i,j,16)=u(i,j,3)-xcos*xcosk
       v(i,j,16)=v(i,j,3)
       end if

       end do

       j=1

       alpha=(datan((v(i,j+1,3)-v(i,j,3))/((u(i,j+1,3)-u(i,j,3)))))

       u(i,j,16)=u(i,j,3)-xcos*xcosk*dsin(alpha)

       if(v(i,j,3).ge.0.) then
       v(i,j,16)=v(i,j,3)+xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,3).lt.0.) then
       u(i,j,16)=u(i,j,3)+xcos*xcosk*dsin(alpha)
       v(i,j,16)=v(i,j,3)-xcos*xcosk*dcos(alpha)

       end if

       j=np(i,1)

       alpha=(datan((v(i,j,3)-v(i,j-1,3))/((u(i,j,3)-u(i,j-1,3)))))

       u(i,j,16)=u(i,j,3)-xcos*xcosk*dsin(alpha)

       if(v(i,j,3).ge.0.) then
       v(i,j,16)=v(i,j,3)+xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,3).le.0.) then
       u(i,j,16)=u(i,j,3)+xcos*xcosk*dsin(alpha)
       v(i,j,16)=v(i,j,3)-xcos*xcosk*dcos(alpha)
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.11+ Airfoils thickness
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Aproximate calculus (not inperpolated)
c      Special airfoils not considered
c      Please improve

       do i=0,nribss

c      Extrados thickness
       do j=1,np(i,1)-1
       if (v(i,j+1,3).ge.v(i,j,3).and.u(i,j+1,3).lt.u(i,j,3)) then
       xth1=v(i,j+1,3)
       end if
c      Intrados thickness
       if (v(i,j+1,3).le.v(i,j,3).and.u(i,j+1,3).gt.u(i,j,3)) then
       xth2=v(i,j+1,3)
       end if
       end do
c      Airfoil thickness
       rib(i,148)=xth1-xth2
       rib(i,149)=100.*rib(i,148)/rib(i,5)

c      write (*,*) "Thicknees= ", i, rib(i,148), rib(i,149)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12 Airfoils drawing (complete)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Note: In section 8.5.0.0 we draw ovalized 2D airfoils
              
c      Box (1,2)
       
       sepxx=700.*xkf
       sepyy=100.*xkf
c      sepyy=100

       kx=0
       ky=0
       kyy=0

       do i=1,nribss

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*1.0*float(ky)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Numering ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call itxt(sepx+19.-84.*(typm3(9)/7.),sepy,typm3(9),0.0d0,i,7)
       call itxt(sepx+19.-84.*(typm3(9)/7.),sepy+890.95*xkf,typm3(9),
     + 0.0d0,i,7)
       call itxt(sepx-16.-84.*(typm3(9)/7.)+2530.*xkf,sepy,typm3(9),
     + 0.0d0,i,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.0 Miniribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Upper surface minirib
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (rib(i,56).gt.1.and.rib(i,56).ne.100.and.atp.ne."ss") 
     + then

       rib(i,60)=0. ! Extrados minirib length

c      Detect point extrados
       do j=1,np(i,2)-1
       xminirib=rib(i-1,5)*rib(i,56)/100.       
       if (u(i-1,1,3)-u(i-1,j,3).lt.xminirib.and.u(i-1,1,3)-u(i-1,j+1,3)
     + .ge.xminirib) then
       jcontrole=j
       jcve(i)=j ! control vector extrados

       rib(i,107)=xminirib-(u(i-1,1,3)-u(i-1,j,3))
       xequise=u(i-1,j,3)-rib(i,107)
       yequise=v(i-1,j,3)-rib(i,107)*(v(i-1,j,3)-v(i-1,j+1,3))/
     + (u(i-1,j,3)-u(i-1,j+1,3))
       end if
       end do

c      Draw extrados minirib, Print and MC
       do j=1,jcontrole-1
       call line(sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,
     + sepx+u(i-1,j+1,3),-v(i-1,j+1,3)+sepy-sepriy*0.5,1)

       call line(sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5,
     + sepx+u(i-1,j+1,16),-v(i-1,j+1,16)+sepy-sepriy*0.5,3)
       call line(2530.*xkf+sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5
     + ,2530.*xkf+sepx+u(i-1,j+1,16),-v(i-1,j+1,16)+sepy-sepriy*0.5,1)

       call line(sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5,
     + sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,5)

       rib(i,60)=rib(i,60)+sqrt((u(i-1,j,3)-u(i-1,j+1,3))**2.+
     + (v(i-1,j,3)-v(i-1,j+1,3))**2.)
       end do

       j=1
       call line(2530.*xkf+sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5
     + ,2530.*xkf+sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,1)

c      Draw romano and itxt mark in minirib

       x1=2530.*xkf+sepx+u(i-1,j,3)
       y1=-v(i-1,j,3)+sepy-sepriy*0.5
c       call romano(i,x1-rib(i,60)*0.35,y1,0.0d0,1.0d0,7)
       x1=sepx+u(i-1,j,3)
       y1=-v(i-1,j,3)+sepy-sepriy*0.5
       call itxt(x1-rib(i,60)*0.35-30.,y1+1.,3.0d0,0.0d0,i,7)

c      Last segment
       j=jcontrole
       call line(sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,
     + sepx+xequise,-yequise+sepy-sepriy*0.5,1)
       alpha=datan(-(v(i-1,j,3)-v(i-1,j+1,3))/(u(i-1,j,3)-u(i-1,j+1,3)))
       xequisee=xequise+xrib*0.1*dsin(alpha)
       yequisee=yequise+xrib*0.1*dcos(alpha)

       call line(sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5,
     + sepx+xequisee,-yequisee+sepy-sepriy*0.5,3)
       call line(2530.*xkf+sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*
     + 0.5,2530.*xkf+sepx+xequisee,-yequisee+sepy-sepriy*0.5,1)

       call line(sepx+xequisee,-yequisee+sepy-sepriy*0.5,
     + sepx+xequise,-yequise+sepy-sepriy*0.5,5)
       call line(2530.*xkf+sepx+xequisee,-yequisee+sepy-sepriy*0.5,
     + 2530.*xkf+sepx+xequise,-yequise+sepy-sepriy*0.5,1)

       rib(i,60)=rib(i,60)+sqrt((u(i-1,j,3)-xequisee)**2.+
     + (v(i-1,j,3)-yequisee)**2.)

       end if ! upper surface

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Bottom surface minirib
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (rib(i,56).gt.1.and.rib(i,56).ne.100.and.atp.ne."ss") 
     + then

       rib(i,61)=0. ! Intrados minirib length

c      Detect point intrados
       do j=np(i,1),np(i,2),-1
       xminirib=rib(i-1,5)*rib(i,56)/100.       
       if (u(i-1,1,3)-u(i-1,j,3).lt.xminirib.and.u(i-1,1,3)-u(i-1,j-1,3)
     + .ge.xminirib) then
       jcontroli=j
       jcvi(i)=j ! control vector intrados

       rib(i,107)=xminirib-(u(i-1,1,3)-u(i-1,j,3))
       xequisi=u(i-1,j,3)-rib(i,107)
       yequisi=v(i-1,j,3)-rib(i,107)*(v(i-1,j,3)-v(i-1,j-1,3))/
     + (u(i-1,j,3)-u(i-1,j-1,3))
       end if
       end do

c      Draw intrados minirib, Print and MC
       do J=np(i,1),jcontroli+1,-1
       call line(sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,
     + sepx+u(i-1,j-1,3),-v(i-1,j-1,3)+sepy-sepriy*0.5,1)

       call line(sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5,
     + sepx+u(i-1,j-1,16),-v(i-1,j-1,16)+sepy-sepriy*0.5,3) 
       call line(2530.*xkf+sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5
     + ,2530.*xkf+sepx+u(i-1,j-1,16),-v(i-1,j-1,16)+sepy-sepriy*0.5,1) 

       call line(sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5,
     + sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,5)

       rib(i,61)=rib(i,61)+sqrt((u(i-1,j,3)-u(i-1,j-1,3))**2.+
     + (v(i-1,j,3)-v(i-1,j-1,3))**2.)

       end do

       j=np(i,1)
       call line(2530.*xkf+sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5
     + ,2530.*xkf+sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,1)

c      Last segment
       j=jcontroli
       call line(sepx+u(i-1,j,3),-v(i-1,j,3)+sepy-sepriy*0.5,
     + sepx+xequisi,-yequisi+sepy-sepriy*0.5,1)
       alpha=datan((v(i-1,j,3)-v(i-1,j-1,3))/(u(i-1,j,3)-u(i-1,j-1,3)))
       xequisie=xequisi+xrib*0.1*dsin(alpha)
       yequisie=yequisi-xrib*0.1*dcos(alpha)

       call line(sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5,
     + sepx+xequisie,-yequisie+sepy-sepriy*0.5,3)
       call line(2530.*xkf+sepx+u(i-1,j,16),-v(i-1,j,16)+sepy-sepriy*0.5
     + ,2530.*xkf+sepx+xequisie,-yequisie+sepy-sepriy*0.5,1)

       call line(sepx+xequisie,-yequisie+sepy-sepriy*0.5,
     + sepx+xequisi,-yequisi+sepy-sepriy*0.5,5)
       call line(2530.*xkf+sepx+xequisie,-yequisie+sepy-sepriy*0.5,
     + 2530.*xkf+sepx+xequisi,-yequisi+sepy-sepriy*0.5,1)

       rib(i,61)=rib(i,61)+sqrt((u(i-1,j,3)-xequisie)**2.+
     + (v(i-1,j,3)-yequisie)**2.)

c      Draw segment minirib
       call line(sepx+xequise,-yequise+sepy-sepriy*0.5,
     + sepx+xequisi,-yequisi+sepy-sepriy*0.5,1)
       call line(2530.*xkf+sepx+xequise,-yequise+sepy-sepriy*0.5,
     + 2530.*xkf+sepx+xequisi,-yequisi+sepy-sepriy*0.5,1)

c      Draw control romano point

       x1=2530.*xkf+sepx+0.5*(xequisi+xequise)
       y1=sepy-sepriy*0.5-0.5*(yequisi+yequise)
       call romano(i,x1+1.,y1+2.,0.0d0,typm6(9)*0.1,7)

       end if ! bottom surface

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.1 Airfoil extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

        do j=1,np(i,2)-1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa airfoils basic contour
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,3),-v(i,j,3)+sepy,sepx+u(i,j+1,3),
     + -v(i,j+1,3)+sepy,1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa airfoils washin basic contour al seu lloc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,4),-v(i,j,4)+sepy+xkf*890.95-rib(i,50),
     + sepx+u(i,j+1,4),-v(i,j+1,4)+sepy+xkf*890.95-rib(i,50),3)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Airfoils borders
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j+1,16),
     + -v(i,j+1,16)+sepy,3)

       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j,3),
     + -v(i,j,3)+sepy,5)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.2 Air inlets
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case "pc"
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (atp.eq."pc") then

       j=np(i,2)
       k=np(i,2)+np(i,3)-1

c      Basic contour using straight line
       call line(sepx+u(i,j,3),-v(i,j,3)+sepy,sepx+u(i,k,3),
     + -v(i,k,3)+sepy,1)

c      Washin basic contour using straight line
       call line(sepx+u(i,j,4),-v(i,j,4)+sepy+xkf*890.85-rib(i,50),
     + sepx+u(i,k,4),-v(i,k,4)+sepy+xkf*890.85-rib(i,50),3)
 
c      Airfoil borders
       
       xdv=v(i,j,3)-v(i,k,3)
       xdu=u(i,k,3)-u(i,j,3)
       alpha=datan(xdv/xdu)
       if (xdv.eq.0) then
       alpha=0.
       end if

       u(i,j+2,16)=u(i,j,3)-xrib*0.1*dsin(alpha)
       v(i,j+2,16)=v(i,j,3)-xrib*0.1*dcos(alpha)
       u(i,k-2,16)=u(i,k,3)-xrib*0.1*dsin(alpha)
       v(i,k-2,16)=v(i,k,3)-xrib*0.1*dcos(alpha)

       if (rib(i,149).ne.0.) then
       call line(sepx+u(i,j+2,16),-v(i,j+2,16)+sepy,sepx+u(i,k-2,16),
     + -v(i,k-2,16)+sepy,3)
       end if

c      Two lines intersection

c      up nose
       
       xru(1)=u(i,j,16)
       xru(2)=u(i,j-1,16)
       xrv(1)=v(i,j,16)
       xrv(2)=v(i,j-1,16)
       xsu(1)=u(i,j+2,16)
       xsu(2)=u(i,k-2,16)
       xsv(1)=v(i,j+2,16)
       xsv(2)=v(i,k-2,16)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       u(i,j+1,16)=xtu
       v(i,j+1,16)=xtv

       if (rib(i,149).ne.0.) then
       call line(sepx+u(i,j+1,16),-v(i,j+1,16)+sepy,sepx+u(i,j,16),
     + -v(i,j,16)+sepy,3)
       call line(sepx+u(i,j+1,16),-v(i,j+1,16)+sepy,sepx+u(i,j+2,16),
     + -v(i,j+2,16)+sepy,3)
       end if

c      bottom nose
       
       xru(1)=u(i,k,16)
       xru(2)=u(i,k+1,16)
       xrv(1)=v(i,k,16)
       xrv(2)=v(i,k+1,16)
       xsu(1)=u(i,j+2,16)
       xsu(2)=u(i,k-2,16)
       xsv(1)=v(i,j+2,16)
       xsv(2)=v(i,k-2,16)
      
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       u(i,k-1,16)=xtu
       v(i,k-1,16)=xtv

c      Print segments if not zero thickness
       if (rib(i,149).ne.0.) then
       call line(sepx+u(i,k-1,16),-v(i,k-1,16)+sepy,sepx+u(i,k-2,16),
     + -v(i,k-2,16)+sepy,3)
       call line(sepx+u(i,k-1,16),-v(i,k-1,16)+sepy,sepx+u(i,k,16),
     + -v(i,k,16)+sepy,3)
       end if

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
C      Case "ds" or "ss"
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (atp.eq."ds".or.atp.eq."ss") then

       do j=np(i,2),np(i,2)+np(i,3)-2

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa airfoils basic contour
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,3),-v(i,j,3)+sepy,sepx+u(i,j+1,3),
     + -v(i,j+1,3)+sepy,1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa airfoils washin basic contour al seu lloc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,4),-v(i,j,4)+sepy+xkf*890.95-rib(i,50),
     + sepx+u(i,j+1,4),-v(i,j+1,4)+sepy+xkf*890.95-rib(i,50),3)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Airfoils borders
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j+1,16),
     + -v(i,j+1,16)+sepy,3)

       
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j,3),
     + -v(i,j,3)+sepy,5)

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.3 Airfoil intrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       do j=1,np(i,1)-1
        do j=np(i,2)+np(i,3)-1,np(i,1)-1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa airfoils basic contour
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,3),-v(i,j,3)+sepy,sepx+u(i,j+1,3),
     + -v(i,j+1,3)+sepy,1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa airfoils washin basic contour al seu lloc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,4),-v(i,j,4)+sepy+xkf*890.85-rib(i,50),
     + sepx+u(i,j+1,4),-v(i,j+1,4)+sepy+xkf*890.85-rib(i,50),3)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Airfoils borders
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j+1,16),
     + -v(i,j+1,16)+sepy,3)

       
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j,3),
     + -v(i,j,3)+sepy,5)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.4 Dibuixa punts-segments singulars vores airfoils
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       j=np(i,1)

       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j,3),
     + -v(i,j,3)+sepy,5)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.5 Draw holes
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do l=1,hol(i,1,1)

c      Dibuixa forat tipus 1 (alleugerament elliptics)
       if (hol(i,l,9).eq.1) then

       xx0=(hol(i,l,2))*rib(i,5)/100.0d0+sepx
       yy0=(-(hol(i,l,3))*rib(i,5)/100.0d0+sepy)
       xxa=(hol(i,l,4))*rib(i,5)/100.0d0
       yyb=((hol(i,l,5))*rib(i,5)/100.0d0)

       call ellipse(xx0,yy0,xxa,yyb,(hol(i,l,6)),3)
       end if

c      Dibuixa forat tipus 3 (triangles)

       if (hol(i,l,9).eq.3) then

       alptri=hol(i,l,6)*pi/180.
       atri=hol(i,l,4)*rib(i,5)/100.
       btri=hol(i,l,5)*rib(i,5)/100.
       rtri=hol(i,l,7)*rib(i,5)/100.
       
c      Marcador de costat negatiu
       satri=atri/sqrt(atri*atri)

       atri=abs(atri)

       cgor=0.5*pi-alptri
       ctri=dsqrt(atri*atri+btri*btri-2.*atri*btri*dcos(cgor))
       agor=dacos((ctri*ctri+btri*btri-atri*atri)/(2.*btri*ctri))
       bgor=dacos((ctri*ctri+atri*atri-btri*btri)/(2.*atri*ctri))
       aggor=pi-agor
       bggor=pi-bgor
       cggor=pi-cgor
       h1tri=rtri/dsin(0.5*cgor)
       h2tri=rtri/dsin(0.5*bgor)
       h3tri=rtri/dsin(0.5*agor)

       x1=hol(i,l,2)*rib(i,5)/100.
       y1=hol(i,l,3)*rib(i,5)/100.

       x2=x1+satri*atri*dcos(alptri)
       y2=y1+atri*dsin(alptri)

       x3=x1
       y3=y1+btri

       o1x=x1+satri*(h1tri*dcos(alptri+0.5*cgor))
       o1y=y1+h1tri*dsin(alptri+0.5*cgor)

       o2x=x2-satri*(h2tri*dcos(-alptri+0.5*bgor))
       o2y=y2+h2tri*dsin(-alptri+0.5*bgor)

       o3x=x3+satri*(h3tri*dsin(0.5*agor))
       o3y=y3-h3tri*dcos(0.5*agor)

c      Inicialitza comptatge punts triangle
       k=1

       step1=cggor/6.
       do tetha=0.,cggor+0.01,step1
       xtri(k)=o1x-satri*rtri*dcos(tetha)
       ytri(k)=o1y-rtri*dsin(tetha)
       k=k+1
       end do

       step2=bggor/6.
       do tetha=alptri,alptri+bggor+0.01,step2
       xtri(k)=o2x+satri*rtri*dsin(tetha)
       ytri(k)=o2y-rtri*dcos(tetha)
       k=k+1
       end do

       step3=aggor/6.
       do tetha=agor,pi+0.01,step3
       xtri(k)=o3x+satri*rtri*dcos(tetha)
       ytri(k)=o3y+rtri*dsin(tetha)
       k=k+1
       end do

       xtri(k)=xtri(1)
       ytri(k)=ytri(1)

c      Dibuixa triangles

       if (satri.eq.1.) then
       do k=1,21
       call line(sepx+xtri(k),-ytri(k)+sepy,
     + sepx+xtri(k+1),-ytri(k+1)+sepy,3)
       end do
       end if

       if (satri.eq.-1.) then
       do k=1,21
       call line(sepx+xtri(k),-ytri(k)+sepy,
     + sepx+xtri(k+1),-ytri(k+1)+sepy,3)
       end do
       end if

       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.6 Print joncs
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      SOLVE INTERFERENCE BETWEEN BLOCS!!!!

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.6.1 First) Iterate in blocs type 1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      For each bloc do
       do m=1,k21blocs
c      For each group do
       do ng=1,k21blocf(m,3)

c      Detect rib belonging to group
       if (i.ge.ngoo(m,ng,2).and.i.le.ngoo(m,ng,3)) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case bloc type 1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k21blocf(m,2).eq.1) then

c       write (*,*) "t1 ",k21blocf(m,1),k21blocf(m,2),i


c       if (rib(i,166).ne.0) then

       do jjk=1,4
       xextra(ng,jjk)=xextraa(m,ng,jjk)
       xintra(ng,jjk)=xintraa(m,ng,jjk)
       sjo(ng,jjk)=sjoo(m,ng,jjk)
       end do

       rib(i,166)=float(ng)

       call joncs(i,u,v,rib,xintra,xextra,xjonc,npo,atp,np)
       call pjoncs(i,xjonc,npo,sjo,sepx,sepy,rib,xkf)

       joncf(i,m,ng,2)=rib(i,167) ! Jonc lenght


c       end if

       end if ! bloc type 1

       end if ! detect rib

       end do ! group n

       end do ! bloc m

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.6.2 Second) Iterate in blocs type 2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      For each bloc do
       do m=1,k21blocs
c      For each group do
       do ng=1,k21blocf(m,3)

c      Detect rib belonging to group
       if (i.ge.ngoo(m,ng,2).and.i.le.ngoo(m,ng,3)) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case bloc rods type 2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k21blocf(m,2).eq.2) then

c       write (*,*) "t2 ",k21blocf(m,1),k21blocf(m,2),i

       do jjk=1,4
       sjo2(ng,jjk)=sjoo(m,ng,jjk)
       end do

       rib(i,166)=float(ng)
       nparc=41
       
       call joncs2(i,u,v,rib,x21,xjonc2,nparc,atp,np,m,ng)
       call pjoncs2(i,xjonc2,nparc,sjo2,sepx,sepy,rib,xkf)   

       joncf(i,m,ng,2)=rib(i,167) ! Jonc lenght

c      Print romano points BOX(1,7) -exp-
c       call romanop(i,1,sepx+xjonc2(i,1,1),sepy-xjonc2(i,1,2), ! BOX(1,7)
c     + sepx+xjonc2(i,nparc,1),sepy-xjonc2(i,nparc,2),0,0,0,xkf)


       end if ! bloc type 2

       end if ! detect rib
   
       end do ! group n

       end do ! bloc m

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.12.7 Print mylars
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (rib(i,168).ne.0) then
       call mylars(i,u,v,sepx,sepy,rib,xmy,np,xkf,atp)
       end if

c      Change airfoil loction

       kx=int((float(i)/6.))
       ky=i-kx*6
       kyy=kyy+1

       end do  ! i airfoil

      
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.13 Airfoils drawing (para mesa de corte)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
              
c      Box (1,4)

       sepxx=700.*xkf
       sepyy=100.*xkf

       kx=0
       ky=0
       kyy=0

       do i=1,nribss

       sepx=2530.*xkf+sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky)

       call romano(i,sepx+0.89d0*rib(i,5),sepy-1.0d0,0.0d0,
     + typm6(9)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.13.1 Airfoils borders
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Case "ds" or "ss"

       if (atp.eq."ds".or.atp.eq."ss") then

       do j=1,np(i,1)-1
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j+1,16),
     + -v(i,j+1,16)+sepy,1)
       end do

       end if

c      Case "pc"

       jvi=np(i,2)           ! vent in
       jvo=np(i,2)+np(i,3)-1 ! vent out

       if (atp.eq."pc") then

c      Extrados

       do j=1,np(i,2)-1
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j+1,16),
     + -v(i,j+1,16)+sepy,1)

       end do

c      Nose

c      Print segments if not zero thickness
       if (rib(i,149).ne.0.) then

       call line(sepx+u(i,jvi,16),-v(i,jvi,16)+sepy,sepx+u(i,jvo,16),
     + -v(i,jvo,16)+sepy,2)

c      Erase old code below:
c       call line(sepx+u(i,j+2,16),-v(i,j+2,16)+sepy,sepx+u(i,k-2,16),
c     + -v(i,k-2,16)+sepy,3)

c       call line(sepx+u(i,j+1,16),-v(i,j+1,16)+sepy,sepx+u(i,j,16),
c     + -v(i,j,16)+sepy,3)
c       call line(sepx+u(i,j+1,16),-v(i,j+1,16)+sepy,sepx+u(i,j+2,16),
c     + -v(i,j+2,16)+sepy,3)

c       call line(sepx+u(i,k-1,16),-v(i,k-1,16)+sepy,sepx+u(i,k-2,16),
c     + -v(i,k-2,16)+sepy,3)
c       call line(sepx+u(i,k-1,16),-v(i,k-1,16)+sepy,sepx+u(i,k,16),
c     + -v(i,k,16)+sepy,3)
       end if

c      Intrados

       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j+1,16),
     + -v(i,j+1,16)+sepy,1)

       end do

       end if

     

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.13.2 Draw singular points-segments in airfoils border
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       j=np(i,1)
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j,3),
     + -v(i,j,3)+sepy,1)

       j=1
       call line(sepx+u(i,j,16),-v(i,j,16)+sepy,sepx+u(i,j,3),
     + -v(i,j,3)+sepy,1)

c See also: 9.3 Draw anchor points in airfoils

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      6.13.3 Draw elliptical holes (MC)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do l=1,hol(i,1,1)

c      Holes type 1 (ellipses)
       if (hol(i,l,9).eq.1) then

       xx0=hol(i,l,2)*rib(i,5)/100.+sepx
       yy0=(-hol(i,l,3)*rib(i,5)/100.+sepy)
       xxa=hol(i,l,4)*rib(i,5)/100.
       yyb=(hol(i,l,5)*rib(i,5)/100.)

       call ellipse(xx0,yy0,xxa,yyb,hol(i,l,6),1)

       end if

c      Dibuixa forat tipus 3 (triangles)

       if (hol(i,l,9).eq.3) then

       alptri=hol(i,l,6)*pi/180.
       atri=hol(i,l,4)*rib(i,5)/100.
       btri=hol(i,l,5)*rib(i,5)/100.
       rtri=hol(i,l,7)*rib(i,5)/100.
       
c      Marcador de costat negatiu
       satri=atri/sqrt(atri*atri)

       atri=abs(atri)

       cgor=0.5*pi-alptri
       ctri=dsqrt(atri*atri+btri*btri-2.*atri*btri*dcos(cgor))
       agor=dacos((ctri*ctri+btri*btri-atri*atri)/(2.*btri*ctri))
       bgor=dacos((ctri*ctri+atri*atri-btri*btri)/(2.*atri*ctri))
       aggor=pi-agor
       bggor=pi-bgor
       cggor=pi-cgor
       h1tri=rtri/dsin(0.5*cgor)
       h2tri=rtri/dsin(0.5*bgor)
       h3tri=rtri/dsin(0.5*agor)

       x1=hol(i,l,2)*rib(i,5)/100.
       y1=hol(i,l,3)*rib(i,5)/100.

       x2=x1+satri*atri*dcos(alptri)
       y2=y1+atri*dsin(alptri)

       x3=x1
       y3=y1+btri

       o1x=x1+satri*(h1tri*dcos(alptri+0.5*cgor))
       o1y=y1+h1tri*dsin(alptri+0.5*cgor)

       o2x=x2-satri*(h2tri*dcos(-alptri+0.5*bgor))
       o2y=y2+h2tri*dsin(-alptri+0.5*bgor)

       o3x=x3+satri*(h3tri*dsin(0.5*agor))
       o3y=y3-h3tri*dcos(0.5*agor)

c       write (*,*) atri,btri,ctri,agor,bgor,cgor

c      Inicialitza comptatge punts triangle
       k=1

       step1=cggor/6.
       do tetha=0.,cggor+0.01,step1
       xtri(k)=o1x-satri*rtri*dcos(tetha)
       ytri(k)=o1y-rtri*dsin(tetha)
       k=k+1
       end do

       step2=bggor/6.
       do tetha=alptri,alptri+bggor+0.01,step2
       xtri(k)=o2x+satri*rtri*dsin(tetha)
       ytri(k)=o2y-rtri*dcos(tetha)
       k=k+1
       end do

       step3=aggor/6.
       do tetha=agor,pi+0.01,step3
       xtri(k)=o3x+satri*rtri*dcos(tetha)
       ytri(k)=o3y+rtri*dsin(tetha)
       k=k+1
       end do

       xtri(k)=xtri(1)
       ytri(k)=ytri(1)

c      Dibuixa triangles

       if (satri.eq.1.) then
       do k=1,21
       call line(sepx+xtri(k),-ytri(k)+sepy,
     + sepx+xtri(k+1),-ytri(k+1)+sepy,1)
       end do
       end if

       if (satri.eq.-1.) then
       do k=1,21
       call line(sepx+xtri(k),-ytri(k)+sepy,
     + sepx+xtri(k+1),-ytri(k+1)+sepy,1)
       end do
       end if

       end if

       end do

       kx=int((float(i)/6.))
       ky=i-kx*6
       kyy=kyy+1

       end do

      

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5+ Drawing planform in 2D view x-y
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      5+.1 Planform

c      Box (3,1)

       x0=0.
       y0=2000.*xkf
       
c      Ribs

       do i=1,nribss

       do j=1,np(i,1)-1

       x1=x(i,j)+x0
       y1=y(i,j)+y0
       x2=x(i,j+1)+x0
       y2=y(i,j+1)+y0

       call line(x1,y1,x2,y2,1)
       call line(-x1,y1,-x2,y2,1)

       end do

       end do

c      Trailing edge

       do i=1,nribss-1

       call line(x(i,1)+x0,y(i,1)+y0,x(i+1,1)+x0,y(i+1,1)+y0,1)
       call line(-x(i,1)+x0,y(i,1)+y0,-x(i+1,1)+x0,y(i+1,1)+y0,1)

       end do

       call line(-x(1,1)+x0,y(1,1)+y0,x(1,1)+x0,y(1,1)+y0,1)

c      Leading edge

c      Calcula punt de LE
       do j=10,np(1,2)
       if (u(1,j,3).eq.0) then
       jzero=j
       end if
       end do

       j=jzero

       do i=1,nribss-1

       call line(x(i,j)+x0,y(i,j)+y0,x(i+1,j)+x0,y(i+1,j)+y0,1)
       call line(-x(i,j)+x0,y(i,j)+y0,-x(i+1,j)+x0,y(i+1,j)+y0,1)

       end do

       call line(-x(1,j)+x0,y(1,j)+y0,x(1,j)+x0,y(1,j)+y0,1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vents - Air intakes
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
c      Classic vents
       if (k31d.eq.0) then

c      Vent in
       do i=1,nribss

       j=np(i,2)

c      Control if cell is closed

       if(int(rib(i,14)).eq.1) then
       call line(x(i-1,j)+x0,y(i-1,j)+y0,x(i,j)+x0,y(i,j)+y0,3)
       call line(-x(i-1,j)+x0,y(i-1,j)+y0,-x(i,j)+x0,y(i,j)+y0,3)
       end if
       if(int(rib(i,14)).eq.0) then
       call line(x(i-1,j)+x0,y(i-1,j)+y0,x(i,j)+x0,y(i,j)+y0,9)
       call line(-x(i-1,j)+x0,y(i-1,j)+y0,-x(i,j)+x0,y(i,j)+y0,9)
       end if

       end do

c      Vent out
       do i=1,nribss

       j=np(i,2)+np(i,3)-1

c      Control if cell is closed

       if(int(rib(i,14)).eq.1) then
       call line(x(i-1,j)+x0,y(i-1,j)+y0,x(i,j)+x0,y(i,j)+y0,3)
       call line(-x(i-1,j)+x0,y(i-1,j)+y0,-x(i,j)+x0,y(i,j)+y0,3)
       end if

       end do
       end if ! k31d=0

c      Case new vents
c      Estructura similar al cas 3D secció 21.2
       if (k31d.eq.1) then

       do i=1,nribss

       p1x=x(i-1,np(i,2))+x0
       p1y=y(i-1,np(i,2))+y0
       p2x=x(i,np(i,2))+x0
       p2y=y(i,np(i,2))+y0

       j=np(i,2)+np(i,3)-1

       p3x=x(i-1,j)+x0
       p3y=y(i-1,j)+y0
       p4x=x(i,j)+x0
       p4y=y(i,j)+y0

       if (rib(i,165).eq.0) then
       call line(p1x,p1y,p2x,p2y,3)
       call line(-p1x,p1y,-p2x,p2y,3)
       call line(p3x,p3y,p4x,p4y,3)
       call line(-p3x,p3y,-p4x,p4y,3)
       end if

       if (rib(i,165).eq.1) then
       call line(p3x,p3y,p4x,p4y,3)
       call line(-p3x,p3y,-p4x,p4y,3)
       end if

       if (rib(i,165).eq.-1) then
       call line(p1x,p1y,p2x,p2y,3)
       call line(-p1x,p1y,-p2x,p2y,3)
       end if

       if (rib(i,165).eq.-2) then
       call line(p1x,p1y,p2x,p2y,3)
       call line(-p1x,p1y,-p2x,p2y,3)
       call line(p3x,p3y,p2x,p2y,3)
       call line(-p3x,p3y,-p2x,p2y,3)
       end if

       if (rib(i,165).eq.-3) then
       call line(p1x,p1y,p2x,p2y,3)
       call line(-p1x,p1y,-p2x,p2y,3)
       call line(p1x,p1y,p4x,p4y,3)
       call line(-p1x,p1y,-p4x,p4y,3)
       end if

       end do

       end if ! k31d=1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5+.2 Drawing real*8 canopy in 2D view x-z
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (4,1)

       x0=0.
       y0=3000.*xkf

       do i=1,nribss

       do j=1,np(i,1)-1

       x1=x(i,j)+0.
       y1=z(i,j)+3000.*xkf
       x2=x(i,j+1)+0.
       y2=z(i,j+1)+3000.*xkf

       call line(x1,y1,x2,y2,7)
       call line(-x1,y1,-x2,y2,7)

       end do

       end do

c      Vent in

       do i=1,nribss

       j=np(i,2)

c      Control if cell is closed

       if(int(rib(i,14)).eq.1) then
       call line(x(i-1,j)+x0,z(i-1,j)+y0,x(i,j)+x0,z(i,j)+y0,3)
       call line(-x(i-1,j)+x0,z(i-1,j)+y0,-x(i,j)+x0,z(i,j)+y0,3)
       end if
       if(int(rib(i,14)).eq.0) then
       call line(x(i-1,j)+x0,z(i-1,j)+y0,x(i,j)+x0,z(i,j)+y0,9)
       call line(-x(i-1,j)+x0,z(i-1,j)+y0,-x(i,j)+x0,z(i,j)+y0,9)
       end if

       end do

c      Vent out
       do i=1,nribss

       j=np(i,2)+np(i,3)-1

c      Control if cell is closed

       if(int(rib(i,14)).eq.1) then
       call line(x(i-1,j)+x0,z(i-1,j)+y0,x(i,j)+x0,z(i,j)+y0,3)
       call line(-x(i-1,j)+x0,z(i-1,j)+y0,-x(i,j)+x0,z(i,j)+y0,3)
       end if

       end do

c      Drawing leading edge
c      Calculus point in LE
       do j=10,np(1,2)
       if (u(1,j,3).eq.0) then
       jzero=j
       end if
       end do

       j=jzero

       do i=1,nribss-1

       call line(x(i,j)+x0,z(i,j)+y0,x(i+1,j)+x0,z(i+1,j)+y0,5)
       call line(-x(i,j)+x0,z(i,j)+y0,-x(i+1,j)+x0,z(i+1,j)+y0,5)

       end do

       call line(-x(1,j)+x0,z(1,j)+y0,x(1,j)+x0,z(1,j)+y0,5)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      5+.3 Drawing real*8 canopy in 2D view y-z
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (4,2)

       x0=1260.*xkf
       y0=3000.*xkf

c      Airfoils y-z
       do i=1,nribss

       do j=1,np(i,1)-1
       call line(-y(i,j)+x0,z(i,j)+y0,-y(i,j+1)+x0,z(i,j+1)+y0,3)
       end do

c      Trailing edge
       j=np(i,1)
       call line(-y(i-1,j)+x0,z(i-1,j)+y0,-y(i,j)+x0,z(i,j)+y0,2)
c      Inlet in       
       j=np(i,2)
       if(rib(i,14).eq.1) then
       call line(-y(i-1,j)+x0,z(i-1,j)+y0,-y(i,j)+x0,z(i,j)+y0,1)
       end if
       if(rib(i,14).eq.0) then
       call line(-y(i-1,j)+x0,z(i-1,j)+y0,-y(i,j)+x0,z(i,j)+y0,9)
       end if

c      Inlet out     
c       if(rib(i-1,14).eq.1.and.rib(i,14).eq.1) then
       if(rib(i,14).eq.1) then
       j=np(i,2)+np(i,3)-1
       call line(-y(i-1,j)+x0,z(i-1,j)+y0,-y(i,j)+x0,z(i,j)+y0,1)
       end if

c      Long lines
       do j=2, np(i,2)-1,5
       call line(-y(i-1,j)+x0,z(i-1,j)+y0,-y(i,j)+x0,z(i,j)+y0,4)
       end do
       do j=np(i,2)+np(i,3)+1,np(i,1)-1,5
       call line(-y(i-1,j)+x0,z(i-1,j)+y0,-y(i,j)+x0,z(i,j)+y0,8)
       end do

       end do

c      Ultim perfil
c       i=nribss
c       do j=1,np(i,1)-1
c       call line(-y(i,j)+x0,z(i,j)+y0,-y(i,j+1)+x0,z(i,j+1)+y0,4)
c       end do



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7. PANEL DEVELOPMENT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7.1 Panel 1'-1 extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=1

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,np(1,2)-1 ! extrados panels point j

c      Distances between points rib 0 and 1
       pa=dsqrt((x(i,j)-xx(i,j))**2.+(y(i,j)-yy(i,j))**2.+
     + (z(i,j)-zz(i,j))**2.)
       pb=dsqrt((x(i,j+1)-xx(i,j))**2.+(y(i,j+1)-yy(i,j))**2.+
     + (z(i,j+1)-zz(i,j))**2.)
       pc=dsqrt((x(i,j)-x(i,j+1))**2.+(y(i,j)-y(i,j+1))**2.+
     + (z(i,j)-z(i,j+1))**2.)
       pd=dsqrt((x(i,j)-xx(i,j+1))**2.+(y(i,j)-yy(i,j+1))**2.+
     + (z(i,j)-zz(i,j+1))**2.)
       pe=dsqrt((xx(i,j+1)-xx(i,j))**2.+(yy(i,j+1)-yy(i,j))**2.+
     + (zz(i,j+1)-zz(i,j))**2.)
       pf=dsqrt((x(i,j+1)-xx(i,j+1))**2.+(y(i,j+1)-yy(i,j+1))**2.+
     + (z(i,j+1)-zz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
      
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      REVISAR!!!!!
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       pl1x(0,j)=pl1x(i,j)
       pl1y(0,j)=pl1y(i,j)

       pr1x(0,j)=pr1x(i,j)
       pr1y(0,j)=pr1y(i,j)

       pl2x(0,j)=pl2x(i,j)
       pl2y(0,j)=pl2y(i,j)

       pr2x(0,j)=pr2x(i,j)
       pr2y(0,j)=pr2y(i,j)

c       write (*,*) "1: ", pl1y(0,j), pr1y(0,j)
c       write (*,*) "2: ", pl2y(0,j), pr2y(0,j)
c      Result OK y iguals!!!

       end do
       
c      Extrados

c      Box (1,3)

       i=1
       
       psep=1970.*xkf+seppix(i)*float(i-1)  ! WARNING
       psey=400.*xkf

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7.2 Panel 1'-1 intrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      7.2.1 Intrados

c      Box (2,3)

       i=1

       px0=0.
       py0=0.
       ptheta=0.

       do j=np(1,2)+np(1,3)-1,np(1,1)-1 ! extrados panels, point j

c      Distances between points
       pa=dsqrt((x(i,j)-xx(i,j))**2.+(y(i,j)-yy(i,j))**2.+
     + (z(i,j)-zz(i,j))**2.)
       pb=dsqrt((x(i,j+1)-xx(i,j))**2.+(y(i,j+1)-yy(i,j))**2.+
     + (z(i,j+1)-zz(i,j))**2.)
       pc=dsqrt((x(i,j)-x(i,j+1))**2.+(y(i,j)-y(i,j+1))**2.+
     + (z(i,j)-z(i,j+1))**2.)
       pd=dsqrt((x(i,j)-xx(i,j+1))**2.+(y(i,j)-yy(i,j+1))**2.+
     + (z(i,j)-zz(i,j+1))**2.)
       pe=dsqrt((xx(i,j+1)-xx(i,j))**2.+(yy(i,j+1)-yy(i,j))**2.+
     + (zz(i,j+1)-zz(i,j))**2.)
       pf=dsqrt((x(i,j+1)-xx(i,j+1))**2.+(y(i,j+1)-yy(i,j+1))**2.+
     + (z(i,j+1)-zz(i,j+1))**2.)
       
c       write (*,*) i,pa,pb,pc,pd,pe,pf

       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0

       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0


       pl1x(0,j)=pl1x(i,j)
       pl1y(0,j)=pl1y(i,j)

       pr1x(0,j)=pr1x(i,j)
       pr1y(0,j)=pr1y(i,j)

       pl2x(0,j)=pl2x(i,j)
       pl2y(0,j)=pl2y(i,j)

       pr2x(0,j)=pr2x(i,j)
       pr2y(0,j)=pr2y(i,j)

       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do
       
c      Intrados

       i=1
       
       psep=1970.*xkf+seppix(i)*float(i-1) ! WARNING
       psey=1291.*xkf
       ncontrol=1

c      Control if cell is closed
       if(int(rib(i,14)).eq.0.and.int(rib(i+1,14)).eq.0) then
       psey=400.*xkf
       ncontrol=0
       end if
       
c      7.2.2 Air intakes (vents) panels

       i=1

       px0=0.
       py0=0.
       ptheta=0.

       do j=np(1,2), np(1,2)+np(1,3)-2 ! vent panels, point j

c      Distances between points
       
       pa=dsqrt((x(i,j)-xx(i,j))**2.+(y(i,j)-yy(i,j))**2.+
     + (z(i,j)-zz(i,j))**2.)
       pb=dsqrt((x(i,j+1)-xx(i,j))**2.+(y(i,j+1)-yy(i,j))**2.+
     + (z(i,j+1)-zz(i,j))**2.)
       pc=dsqrt((x(i,j)-x(i,j+1))**2.+(y(i,j)-y(i,j+1))**2.+
     + (z(i,j)-z(i,j+1))**2.)
       pd=dsqrt((x(i,j)-xx(i,j+1))**2.+(y(i,j)-yy(i,j+1))**2.+
     + (z(i,j)-zz(i,j+1))**2.)
       pe=dsqrt((xx(i,j+1)-xx(i,j))**2.+(yy(i,j+1)-yy(i,j))**2.+
     + (zz(i,j+1)-zz(i,j))**2.)
       pf=dsqrt((x(i,j+1)-xx(i,j+1))**2.+(y(i,j+1)-yy(i,j+1))**2.+
     + (z(i,j+1)-zz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0

       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Assigna panell 0 zona vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       pl1x(0,j)=pl1x(i,j)
       pl1y(0,j)=pl1y(i,j)

       pr1x(0,j)=pr1x(i,j)
       pr1y(0,j)=pr1y(i,j)

       pl2x(0,j)=pl2x(i,j)
       pl2y(0,j)=pl2y(i,j)

       pr2x(0,j)=pr2x(i,j)
       pr2y(0,j)=pr2y(i,j)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end do

c      Vents drawing

       if (n1draw.eq.1) then ! Draw central vent
       if (k26d.eq.0) then

c      Verify central cell width  
       if (cencell.ge.0.01)  then  

       i=1
       
       psep=1970.*xkf+seppix(i)*float(i-1) ! WARNING
       psey=1371.*xkf
       ncontrol=0

c      Control if cell is closed
       if(int(rib(1,14)).eq.0.and.int(rib(1+1,14)).eq.0) then
       ncontrol=1
       end if
c      Dibuixa boques
       ncontrol=1

       do j=np(1,2),np(1,2)+ncontrol*(np(1,3)-2)+(ncontrol-1)

       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pr1x(i,j),
     + psey-pr1y(i,j),6)
       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),5)
       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pl2x(i,j),
     + psey-pl2y(i,j),4)
       call line(psep+pr1x(i,j),psey-pr1y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),3)
       call line(psep+pr1x(i,j),psey-pr1y(i,j),psep+pl2x(i,j),
     + psey-pl2y(i,j),2)
       call line(psep+pl2x(i,j),psey-pl2y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),3)

       end do

       end if

       end if ! k26d=0
       end if ! n1draw

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7.3 Panels 1 to nribss-1 extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss-1 ! panel i

       px0=0.
       py0=0.
       ptheta=0.

c      Extrados

       do j=1,np(i,2)-1,1 ! extrados panels point j

c      Distances between points
       pa=dsqrt((x(i+1,j)-x(i,j))**2.+(y(i+1,j)-y(i,j))**2.+
     + (z(i+1,j)-z(i,j))**2.)
       pb=dsqrt((x(i+1,j+1)-x(i,j))**2.+(y(i+1,j+1)-y(i,j))**2.+
     + (z(i+1,j+1)-z(i,j))**2.)
       pc=dsqrt((x(i+1,j+1)-x(i+1,j))**2.+(y(i+1,j+1)-y(i+1,j))**2.+
     + (z(i+1,j+1)-z(i+1,j))**2.)
       pd=dsqrt((x(i+1,j)-x(i,j+1))**2.+(y(i+1,j)-y(i,j+1))**2.+
     + (z(i+1,j)-z(i,j+1))**2.)
       pe=dsqrt((x(i,j+1)-x(i,j))**2.+(y(i,j+1)-y(i,j))**2.+
     + (z(i,j+1)-z(i,j))**2.)
       pf=dsqrt((x(i+1,j+1)-x(i,j+1))**2.+(y(i+1,j+1)-y(i,j+1))**2.+
     + (z(i+1,j+1)-z(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do
       
       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7.4 Panels 1 to nribss-1 Intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      7.4.1 Intrados

       do i=1,nribss-1 ! panel i

       px0=0.
       py0=0.
       ptheta=0.

       do j=np(i,2)+np(i,3)-1,np(i,1)-1 ! extrados panels, point j

c      Distances between points
       pa=dsqrt((x(i+1,j)-x(i,j))**2.+(y(i+1,j)-y(i,j))**2.+
     + (z(i+1,j)-z(i,j))**2.)
       pb=dsqrt((x(i+1,j+1)-x(i,j))**2.+(y(i+1,j+1)-y(i,j))**2.+
     + (z(i+1,j+1)-z(i,j))**2.)
       pc=dsqrt((x(i+1,j+1)-x(i+1,j))**2.+(y(i+1,j+1)-y(i+1,j))**2.+
     + (z(i+1,j+1)-z(i+1,j))**2.)
       pd=dsqrt((x(i+1,j)-x(i,j+1))**2.+(y(i+1,j)-y(i,j+1))**2.+
     + (z(i+1,j)-z(i,j+1))**2.)
       pe=dsqrt((x(i,j+1)-x(i,j))**2.+(y(i,j+1)-y(i,j))**2.+
     + (z(i,j+1)-z(i,j))**2.)
       pf=dsqrt((x(i+1,j+1)-x(i,j+1))**2.+(y(i+1,j+1)-y(i,j+1))**2.+
     + (z(i+1,j+1)-z(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0

       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do
       
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc       
c     7.4.2 Air intakes (vents) panels calculus and drawing
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
c      Salva un vector per evitar interferencia vents-intrados
       do i=0,nribss
       npx=np(i,2)+np(i,3)-1
       pl1x(i,499)=pl1x(i,npx)
       pl1y(i,499)=pl1y(i,npx)
       pl2x(i,499)=pl2x(i,npx)
       pl2y(i,499)=pl2y(i,npx)
       pr1x(i,499)=pr1x(i,npx)
       pr1y(i,499)=pr1y(i,npx)
       pr2x(i,499)=pr2x(i,npx)
       pr2y(i,499)=pr2y(i,npx)
       end do


       do i=0,nribss-1 ! panel i

       px0=0.
       py0=0.
       ptheta=0.

       do j=np(i,2), np(i,2)+np(i,3)-1 ! vent panels, point j

c      Distances between points
       pa=dsqrt((x(i+1,j)-x(i,j))**2.+(y(i+1,j)-y(i,j))**2.+
     + (z(i+1,j)-z(i,j))**2.)
       pb=dsqrt((x(i+1,j+1)-x(i,j))**2.+(y(i+1,j+1)-y(i,j))**2.+
     + (z(i+1,j+1)-z(i,j))**2.)
       pc=dsqrt((x(i+1,j+1)-x(i+1,j))**2.+(y(i+1,j+1)-y(i+1,j))**2.+
     + (z(i+1,j+1)-z(i+1,j))**2.)
       pd=dsqrt((x(i+1,j)-x(i,j+1))**2.+(y(i+1,j)-y(i,j+1))**2.+
     + (z(i+1,j)-z(i,j+1))**2.)
       pe=dsqrt((x(i,j+1)-x(i,j))**2.+(y(i,j+1)-y(i,j))**2.+
     + (z(i,j+1)-z(i,j))**2.)
       pf=dsqrt((x(i+1,j+1)-x(i,j+1))**2.+(y(i+1,j+1)-y(i,j+1))**2.+
     + (z(i+1,j+1)-z(i,j+1))**2.)
       
c       write (*,*) i,pa,pb,pc,pd,pe,pf

       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0

       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))

       end do
       
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7.4.3 Vents drawing
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (n1draw.eq.1) then ! Override classic vents

       if (k26d.eq.0) then ! Draw classic vents

c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1371.*xkf
       ncontrol=0

c      Control if cell is closed
       if(int(rib(i,14)).eq.0.and.int(rib(i+1,14)).eq.0) then
       ncontrol=1
       end if

       ncontrol=1       

       do j=np(i,2),np(i,2)+ncontrol*(np(i,3)-2)+(ncontrol-1)

       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pr1x(i,j),
     + psey-pr1y(i,j),6)
       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),5)
       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pl2x(i,j),
     + psey-pl2y(i,j),4)
       call line(psep+pr1x(i,j),psey-pr1y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),3)
       call line(psep+pr1x(i,j),psey-pr1y(i,j),psep+pl2x(i,j),
     + psey-pl2y(i,j),2)
       call line(psep+pl2x(i,j),psey-pl2y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),3)

       end do

       end do

       end if ! Vents classical

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      7.4.4 Vents drawing Adre
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k26d.eq.0) then ! Draw classic vents

c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

c      Count in ribs
       do i=iini,nribss-1
       
       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=1371.*xkf
       ncontrol=0

c      Control if cell is closed
       if(int(rib(i,14)).eq.0.and.int(rib(i+1,14)).eq.0) then
       ncontrol=1
       end if

       ncontrol=1       

c      Verify central cell width  
   
       do j=np(i,2),np(i,2)+ncontrol*(np(i,3)-2)+(ncontrol-1)

       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pr1x(i,j),
     + psey-pr1y(i,j),6)
c       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pr2x(i,j),
c     + psey-pr2y(i,j),5)
       call line(psep+pl1x(i,j),psey-pl1y(i,j),psep+pl2x(i,j),
     + psey-pl2y(i,j),4)
       call line(psep+pr1x(i,j),psey-pr1y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),3)
c       call line(psep+pr1x(i,j),psey-pr1y(i,j),psep+pl2x(i,j),
c     + psey-pl2y(i,j),2)
       call line(psep+pl2x(i,j),psey-pl2y(i,j),psep+pr2x(i,j),
     + psey-pr2y(i,j),3)

       end do

       end do

       end if ! Vents classical

       end if ! n1draw


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     8. SKIN TENSION
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.1 Calculs previs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Vores de costura

       xcos=xupp/10. ! extrados

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Longituds i amples de celles
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      8.1.1 Extrados longitud cella extrema       
       i=nribss
       rib(nribss,23)=0.
       do j=1,np(nribss,2)-1
       rib(nribss,23)=rib(i,23)+sqrt((pr2x(i-1,j)-pr1x(i-1,j))**2+
     + (pr2y(i-1,j)-pr1y(i-1,j))**2)
       end do

c      8.1.2 Intrados longitud cella extrema       
       i=nribss
       rib(nribss,25)=0.
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       rib(i,25)=rib(i,25)+sqrt((pr2x(i-1,j)-pr1x(i-1,j))**2+
     + (pr2y(i-1,j)-pr1y(i-1,j))**2)
       end do

c      8.1.2+ Inlet longitud cella extrema       
       i=nribss
       rib(nribss,26)=0.
       do j=np(i,2),np(i,2)+np(i,3)-2
       rib(i,26)=rib(i,26)+sqrt((pr2x(i-1,j)-pr1x(i-1,j))**2+
     + (pr2y(i-1,j)-pr1y(i-1,j))**2)
       end do

c      Resta de celles
       do i=0,nribss-1

       rib(i,23)=0.
       rib(i,25)=0.
       rib(i,26)=0.

c      8.1.3 Longitud extrados
       do j=1,np(i,2)-1
       rib(i,23)=rib(i,23)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)
       end do

c      8.1.4 Longitud intrados
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       rib(i,25)=rib(i,25)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)
       end do

c      8.1.5 Longitud inlet
       do j=np(i,2),np(i,2)+np(i,3)-2
       rib(i,26)=rib(i,26)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)
       end do

c      8.1.6 Punts de calcul amples de celles

c      Calcula punts je ji per definir ample celles, calcula ample

       je=int(np(i,2)/2)
       rib(i,22)=dsqrt((pr1x(i,je)-pl1x(i,je))**2.+(pr1y(i,je)
     + -pl1y(i,je))**2.)

       ji=int((np(i,2)+np(i,3)-1+np(i,1))/2)
       rib(i,24)=dsqrt((pr1x(i,ji)-pl1x(i,ji))**2.+(pr1y(i,ji)
     + -pl1y(i,ji))**2.)

c      Print linia esquerra
c       do j=1,np(i,2)-1
c       call line(pl1x(i,j),-pl1y(i,j),pl2x(i,j),-pl2y(i,j),1)
c       end do

       end do

c      Ample celles extremes       
       i=nribss
       je=int(np(i,2)/2)
       rib(i,22)=dsqrt((pr1x(i-1,je)-pl1x(i-1,je))**2.+(pr1y(i-1,je)
     + -pl1y(i-1,je))**2.)

       ji=int((np(i,2)+np(i,3)-1+np(i,1))/2)
       rib(i,24)=dsqrt((pr1x(i-1,ji)-pl1x(i-1,ji))**2.+(pr1y(i-1,ji)
     + -pl1y(i-1,ji))**2.)

c      WARNING 20190624: Ample inlet not defined here!

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2 SOBREAMPLES EXTRADOS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c        write (*,*) "pi 8.2. =",pi

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case classic skin tension k31d=0
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k31d.eq.0) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2.1 Sobreamples esquerra extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

c      Initialize sob points from TE to LE

       do k=1,6
       xsob(k)=((100.-(skin(7-k,1)))/100.)*rib(i,23)
       ysob(k)=rib(i,22)*skin(7-k,2)/100.
       end do

c      Longituds u

       u(i,1,7)=0.
       
       do j=1,np(i,2)-1
       u(i,j+1,7)=u(i,j,7)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)
       end do

c      Sobreamples v      

       v(i,1,7)=rib(i,22)*skin(6,2)/100.

       do j=1,np(i,2)-1

c      LE zone

       if(u(i,j+1,7).le.xsob(2)) then
       xm=(ysob(2)-ysob(1))/(xsob(2)-xsob(1))
       xn=ysob(2)-xm*xsob(2)
       v(i,j+1,7)=xm*(u(i,j+1,7))+xn
       xm1=xm
       xn1=xn
       end if
       
       if(u(i,j+1,7).gt.xsob(2).and.u(i,j+1,7).le.xsob(3)) then
       xm=(ysob(3)-ysob(2))/(xsob(3)-xsob(2))
       xn=ysob(2)-xm*xsob(2)
       v(i,j+1,7)=xm*(u(i,j+1,7))+xn
       xm2=xm
       xn2=xn
       end if

c      Central panel

       if(u(i,j+1,7).gt.xsob(3).and.u(i,j+1,7).le.xsob(4)) then
       xm=(ysob(4)-ysob(3))/(xsob(4)-xsob(3))
       xn=ysob(3)-xm*xsob(3)
       v(i,j+1,7)=xm*(u(i,j+1,7))+xn
       xm2=xm
       xn2=xn
       end if

c      TE zone

       if(u(i,j+1,7).gt.xsob(4).and.u(i,j+1,7).le.xsob(5)) then
       xm=(ysob(5)-ysob(4))/(xsob(5)-xsob(4))
       xn=ysob(4)-xm*xsob(4)
       v(i,j+1,7)=xm*(u(i,j+1,7))+xn
       xm3=xm
       xn3=xn

       end if

       if(u(i,j+1,7).gt.xsob(5)) then
       xm=(ysob(6)-ysob(5))/(xsob(6)-xsob(5))
       xn=ysob(5)-xm*xsob(5)
       v(i,j+1,7)=xm*(u(i,j+1,7))+xn
       xm3=xm
       xn3=xn
       end if

c      Calcula punts esquerra

       xdv=(pl2y(i,j)-pl1y(i,j))
       xdu=(pl2x(i,j)-pl1x(i,j))

       if (xdv.ne.0.) then
       alpl=abs(datan((pl2y(i,j)-pl1y(i,j))/(pl2x(i,j)-pl1x(i,j))))
       else
       alpl=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 2-I
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 2-II
       siu(j)=-1.
       siv(j)=-1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 2-III
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 2-IV
       siu(j)=1.
       siv(j)=-1.
       end if

c      WARNING!!!!!!!!!!! pl2x,pl2y or pl1x,pl1y?????????
c      Amb "2" fa un salt la vora esquerra...

       u(i,j+1,9)=pl2x(i,j)+siu(j)*v(i,j+1,7)*dsin(alpl)
       v(i,j+1,9)=pl2y(i,j)+siv(j)*v(i,j+1,7)*dcos(alpl)

       u(i,j+1,11)=u(i,j+1,9)+siu(j)*xupp*0.1*dsin(alpl)
       v(i,j+1,11)=v(i,j+1,9)+siv(j)*xupp*0.1*dcos(alpl)

c      Impresió de control
c       if (j.eq.10) then
c       write (*,*) "OOO ",i,u(i,j+1,9),v(i,j+1,9)  
c       end if
       
       end do ! j=1,np(i,2)-1

c      Punt inicial j=1
       
       alpl=abs(datan((pl2y(i,1)-pl1y(i,1))/(pl2x(i,1)-pl1x(i,1))))

c      Potser hauria de ser pl1x i pl1y???? Yes
       u(i,1,9)=pl1x(i,j)+siu(1)*v(i,1,7)*dsin(alpl)
       v(i,1,9)=pl1y(i,j)+siv(1)*v(i,1,7)*dcos(alpl)

       u(i,1,11)=u(i,1,9)+siu(1)*xupp*0.1*dsin(alpl)
       v(i,1,11)=v(i,1,9)+siv(1)*xupp*0.1*dcos(alpl)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Opció usar subrutina (sobreescriu punts anteriors)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call puntslat(i,pl1x,pl1y,pl2x,pl2y,1,np(i,2)-1,u,v,xupp,-1)


       end do  ! i

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2.2 Sobreamples dreta extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Sobreamples dreta

       do i=0,nribss

c      Initialize sob points

       do k=1,6

       xsob(k)=((100.-(skin(7-k,1)))/100.)*rib(i+1,23)
       ysob(k)=rib(i,22)*skin(7-k,2)/100.

       end do

c      Longitud u

       u(i,1,8)=0.
       
       do j=1,np(i,2)-1

       u(i,j+1,8)=u(i,j,8)+sqrt((pr2x(i,j)-pr1x(i,j))**2+
     + (pr2y(i,j)-pr1y(i,j))**2)

       end do

c      Sobreamples v      

       v(i,1,8)=rib(i,22)*skin(6,2)/100.

       do j=1,np(i,2)-1

c      LE zone

       if(u(i,j+1,8).le.xsob(2)) then
       xm=(ysob(2)-ysob(1))/(xsob(2)-xsob(1))
       xn=ysob(2)-xm*xsob(2)
       v(i,j+1,8)=xm*(u(i,j+1,8))+xn
       xm1=xm
       xn1=xn
       end if

       if(u(i,j+1,8).gt.xsob(2).and.u(i,j+1,8).le.xsob(3)) then
       xm=(ysob(3)-ysob(2))/(xsob(3)-xsob(2))
       xn=ysob(2)-xm*xsob(2)
       v(i,j+1,8)=xm*(u(i,j+1,8))+xn
       xm2=xm
       xn2=xn
       end if

c      Central panel

       if(u(i,j+1,8).gt.xsob(3).and.u(i,j+1,8).le.xsob(4)) then
       xm=(ysob(4)-ysob(3))/(xsob(4)-xsob(3))
       xn=ysob(3)-xm*xsob(3)
       v(i,j+1,8)=xm*(u(i,j+1,8))+xn
       xm2=xm
       xn2=xn
       end if

c      TE zone

       if(u(i,j+1,8).gt.xsob(4).and.u(i,j+1,8).le.xsob(5)) then
       xm=(ysob(5)-ysob(4))/(xsob(5)-xsob(4))
       xn=ysob(4)-xm*xsob(4)
       v(i,j+1,8)=xm*(u(i,j+1,8))+xn
       xm3=xm
       xn3=xn
       end if

       if(u(i,j+1,8).gt.xsob(5)) then
       xm=(ysob(6)-ysob(5))/(xsob(6)-xsob(5))
       xn=ysob(5)-xm*xsob(5)
       v(i,j+1,8)=xm*(u(i,j+1,8))+xn
       xm3=xm
       xn3=xn
       end if

c      Calcula punts dreta

       xdv=(pr2y(i,j)-pr1y(i,j))
       xdu=(pr2x(i,j)-pr1x(i,j))

       if (xdv.ne.0.) then
       alpr=abs(datan((pr2y(i,j)-pr1y(i,j))/(pr2x(i,j)-pr1x(i,j))))
       else
       alpr=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 3-I
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 3-II
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 3-III
       siu(j)=-1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 3-IV
       siu(j)=-1.
       siv(j)=1.
       end if

       u(i,j+1,10)=pr2x(i,j)+siu(j)*v(i,j+1,8)*dsin(alpr)
       v(i,j+1,10)=pr2y(i,j)+siv(j)*v(i,j+1,8)*dcos(alpr)

       u(i,j+1,12)=u(i,j+1,10)+siu(j)*xupp*0.1*dsin(alpr)
       v(i,j+1,12)=v(i,j+1,10)+siv(j)*xupp*0.1*dcos(alpr)

       end do  ! j=1,np(i,2)-1

c      Initial point not defined in previous bucle

       alpr=abs(datan((pr2y(i,1)-pr1y(i,1))/(pr2x(i,1)-pr1x(i,1))))

       u(i,1,10)=pr1x(i,1)+siu(1)*v(i,1,8)*dsin(alpr)
       v(i,1,10)=pr1y(i,1)+siv(1)*v(i,1,8)*dcos(alpr)
       
       u(i,1,12)=u(i,1,10)+siu(1)*xupp*0.1*dsin(alpr)
       v(i,1,12)=v(i,1,10)+siv(1)*xupp*0.1*dcos(alpr)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Opció usar subrutina (sobreescriu punts anteriors)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call puntslat(i,pr1x,pr1y,pr2x,pr2y,1,np(i,2)-1,u,v,xupp,1)


c      Leading edge segment unformated rib(i,96) extra

       if (i.lt.nribss) then
       j=np(i,2)
       rib(i,96)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do  ! i

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       end if  ! Case classic skin tension k31d=0
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case new skin tension k31d=1 Linear interpolation EXTRADOS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k31d.eq.1) then

c       write (*,*) "NOTE: NEW skin tension"

c      Case 1: Linear interpolation and cell width is rib(i,22) in extrados
c      and rib(i,24) in intrados
c      If (ntypei31(i).eq.1) then

c      Initialize sob points
       do i=0,nribss
       do k=1,skinpoints(i)
       xsobnew(i,k)=((100.-(skinnew(i,skinpoints(i)+1-k,1)))/100.)
     + *rib(i,23)
       ysobnew(i,k)=rib(i,22)*skinnew(i,skinpoints(i)+1-k,2)/100.
       end do ! k
       end do ! i (initialize all sob points)

       do i=0,nribss
 
c      Initialize vector extrados left side
       do j=1,np(i,2)
       u(i,j,50)=u(i,j,7)
       u(i,j,51)=u(i,j,8) ! ? verificar significat vectors 50 i 51
       end do  ! j

c      Assign lengths and sob distances
       u(i,1,7)=0.
       u(i,1,8)=0.

       do j=1,np(i,2)
       do k=1,skinpoints(i)-1

c      Left side
       if (u(i,j,7).ge.xsobnew(i,k).and.u(i,j,7).le.xsobnew(i,k+1)
     + *1.001) ! NOTE: Comparar reals és perillós, afegim multiplicador
     + then
       xm=(ysobnew(i,k+1)-ysobnew(i,k))/(xsobnew(i,k+1)-xsobnew(i,k))
       xn=ysobnew(i,k+1)-xm*xsobnew(i,k+1)
       v(i,j,7)=xm*(u(i,j,7))+xn
       end if

       u(i,j+1,7)=u(i,j,7)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)

       end do ! k

       end do ! j

c      Compute points left side
       call puntslat(i,pl1x,pl1y,pl2x,pl2y,1,np(i,2),u,v,xupp,-1)

       end do  ! i

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Right side: Use length of rib(i+1,23)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Initialize again sob points
       do i=0,nribss
       do k=1,skinpoints(i)
       xsobnew(i,k)=((100.-(skinnew(i+1,skinpoints(i+1)+1-k,1)))/100.)
     + *rib(i+1,23)
       ysobnew(i,k)=rib(i,22)*skinnew(i+1,skinpoints(i+1)+1-k,2)/100.
       end do ! k
       end do ! i (initialize all sob points)

       do i=0,nribss
 
c      Initialize vector extrados left side
       do j=1,np(i,2)
       u(i,j,50)=u(i,j,7)
       u(i,j,51)=u(i,j,8) ! ? verificar significat vectors 50 i 51
       end do  ! j

c      Assign lengths and sob distances
       u(i,1,7)=0.
       u(i,1,8)=0.

       do j=1,np(i,2)
       do k=1,skinpoints(i)

c      Right side
       if (i.lt.nribss) then

       if (u(i,j,8).ge.xsobnew(i+0,k).and.u(i,j,8).le.xsobnew(i+0,k+1)
     + *1.001) ! NOTE: Comparar reals és perillós, afegim multiplicador
     + then
       xm=(ysobnew(i+0,k+1)-ysobnew(i+0,k))/
     +    (xsobnew(i+0,k+1)-xsobnew(i+0,k))
       xn=ysobnew(i+0,k+1)-xm*xsobnew(i+0,k+1)
       v(i,j,8)=xm*(u(i,j,8))+xn
       end if

       u(i,j+1,8)=u(i,j,8)+sqrt((pr2x(i,j)-pr1x(i,j))**2+
     + (pr2y(i,j)-pr1y(i,j))**2)

c      VERIFICAR QUE:
c      u(i,np(i,2),8)=xsobnew(i+1,kmax) !!!!!!!!!!!!!!!!!!
c      I coherencia amb pr* !!!!

       end if

       end do ! k

       end do ! j

c       write (*,*) i,u(i,np(i,2),7),xsobnew(i-1,skinpoints(i)),
c     + u(i,np(i,2),8),xsobnew(i,skinpoints(i))

c      Compute points right side
       call puntslat(i,pr1x,pr1y,pr2x,pr2y,1,np(i,2),u,v,xupp,1)

c      Leading edge segment unformated rib(i,96) extra
       if (i.lt.nribss) then
       j=np(i,2)
       rib(i,96)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do  ! i

c       end if ! end case 1.1

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       end if  ! k31d=1 Linear interpolation EXTRADOS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2.3 Reformat right side of extrados panels (optional)
c            "antiprecission"
c      Method not recommended
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Define provisional vector 29, used later in 11.4 (Panels marks)

       do i=0,nribss-1
       do j=1,np(i,2)
       u(i,j,29)=u(i,j,10)
       v(i,j,29)=v(i,j,10)
       end do
       end do

c      Jump to the end if ndif=1000 (no effect)
       if (ndif.ne.1000) then 
      
c      Avoid xndif=0
       if (xndif.eq.0.) then
       xndif=0.01
       end if

c      Salva punts corva interior a vector 29 per a usos posterior
c      rib(i,36)

       do i=0,nribss-1
       do j=1,np(i,2)

       u(i,j,29)=u(i,j,10)
       v(i,j,29)=v(i,j,10)

       end do
       end do

c      Calcula diferencies de longitud costat exterior - interior

c       ndif=15
c       xndif=0.9

       do i=1,nribss-1
       rib(i,80)=0.
       rib(i,79)=0.
       end do

       do i=1,nribss-1

       do j=np(i,2)-ndif,np(i,2)-1

       rib(i,80)=rib(i,80)+sqrt((u(i,j,11)-u(i,j+1,11))**2.+
     + (v(i,j,11)-v(i,j+1,11))**2.)

       rib(i,79)=rib(i,79)+sqrt((u(i-1,j,12)-u(i-1,j+1,12))**2.+
     + (v(i-1,j,12)-v(i-1,j+1,12))**2.)

       end do

       rib(i,81)=(rib(i,80)-rib(i,79))*xndif

c       write (*,*) "rib(i,81) ", i, rib(i,81)

       end do

c      Redefinir punts 10 i 12 del morro dels panells

       do i=1,nribss-1

       xxa=dsqrt((u(i-1,np(i-1,2),9)-u(i-1,np(i-1,2),10))**2.+
     + (v(i-1,np(i-1,2),9)-v(i-1,np(i-1,2),10))**2.)

       tetha3=dacos(rib(i,81)/(2.*xxa))

       tetha1=datan((v(i-1,np(i-1,2),9)-v(i-1,np(i-1,2),10))/
     + (u(i-1,np(i-1,2),10)-u(i-1,np(i-1,2),9)))

       tetha2=pi-tetha3-tetha1

       u(i-1,np(i,2),28)=u(i-1,np(i,2),10)+rib(i,81)*dcos(tetha2)
       v(i-1,np(i,2),28)=v(i-1,np(i,2),10)+rib(i,81)*dsin(tetha2)
      
       end do

c      Alineació del tram modificat      

       do i=1,nribss-1

       tetha4=datan((v(i-1,np(i,2),28)-v(i-1,np(i,2),10))/
     + (u(i-1,np(i,2),28)-u(i-1,np(i,2),10)))

       rib(i,82)=dsqrt((u(i-1,np(i-1,2)-ndif,10)-u(i-1,np(i-1,2),10))
     + **2.+(v(i-1,np(i-1,2)-ndif,10)-v(i-1,np(i-1,2),10))**2.)

       do j=np(i-1,2)-ndif, np(i-1,2)

       xdis=dsqrt((u(i-1,j,10)-u(i-1,np(i-1,2)-ndif,10))**2.+
     + (v(i-1,j,10)-v(i-1,np(i-1,2)-ndif,10))**2.)

       u(i-1,j,10)=u(i-1,j,10)+(xdis**3./(rib(i,82)**3.))*
     + rib(i,81)*dcos(tetha4)
       v(i-1,j,10)=v(i-1,j,10)+(xdis**3./(rib(i,82)**3.))*
     + rib(i,81)*dsin(tetha4)

       end do

       end do

c      Actualitza les vores i punts especials

       do i=0,nribss-2

       do j=np(i,2)-ndif, np(i,2)

       alpr=abs(datan((v(i,j,10)-v(i,j-1,10))/
     + (u(i,j,10)-u(i,j-1,10))))
       u(i,j,12)=u(i,j,10)+xcos*dsin(alpr)
       v(i,j,12)=v(i,j,10)-xcos*dcos(alpr)

       end do

       alple=abs(datan((v(i,np(i,2),10)-v(i,np(i,2),9))/
     + (u(i,np(i,2),10)-u(i,np(i,2),9))))

       u(i,np(i,2),15)=u(i,np(i,2),10)+xupple*0.1*dsin(alple)
       v(i,np(i,2),15)=v(i,np(i,2),10)+xupple*0.1*dcos(alple)

       u(i,np(i,2),25)=u(i,np(i,2),15)+xupp*0.1*dcos(alple)
       v(i,np(i,2),25)=v(i,np(i,2),15)-xupp*0.1*dsin(alple)


       amle=(v(i,np(i,2),10)-v(i,np(i,2),9))/
     + (u(i,np(i,2),10)-u(i,np(i,2),9))

ccccccc Warning pr2y...       
       amler=((pr2y(i,np(i,2)-1)-pr1y(i,np(i,2)-1))/
     + (pr2x(i,np(i,2)-1)-pr1x(i,np(i,2)-1)))

       b1=v(i,np(i,2),15)-amle*u(i,np(i,2),15)
       b2=v(i,np(i,2),12)-amler*u(i,np(i,2),12)

       u(i,np(i,2),27)=(b2-b1)/(amle-amler)
       v(i,np(i,2),27)=amle*u(i,np(i,2),27)+b1

       end do


       end if ! Jump section if ne=1000
       
c14     continue

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2.4 REFORMAT PANELS FOR PERFECT MATCHING
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Detect if ndif parameter is set for reformat
       if (ndif.eq.1000) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     Compute rib and panels lengths (also done in chapter 11. (!!!!))
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

       rib(i,30)=0. ! extra panel left
       rib(i,31)=0. ! extra rib
       rib(i,32)=0. ! extra panel right
       rib(i,33)=0. ! intra panel left
       rib(i,34)=0. ! intra rib
       rib(i,35)=0. ! intra panel right

c      At left
       do j=1,np(i,2)-1

       rib(i,30)=rib(i,30)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + ((v(i-1,j,10)-v(i-1,j+1,10))**2.))

       rib(i,31)=rib(i,31)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       rib(i,32)=rib(i,32)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       end do

       do j=np(i,2)+np(i,3),np(i,1)-1

       rib(i,33)=rib(i,33)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + ((v(i-1,j,10)-v(i-1,j+1,10))**2.))

       rib(i,34)=rib(i,34)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       rib(i,35)=rib(i,35)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       end do

c      Amplification cofficients
       rib(i,36)=rib(i,30)/rib(i,31)
       rib(i,37)=rib(i,32)/rib(i,31)
       rib(i,38)=rib(i,33)/rib(i,34)
       rib(i,39)=rib(i,35)/rib(i,34)

       rib(0,36)=rib(1,36)
       rib(0,37)=rib(1,36)
       rib(0,38)=rib(1,38)
       rib(0,39)=rib(1,38)

c      Differences with control coefficient xndif

       rib(i,90)=xndif*(rib(i,31)-rib(i,30))
       rib(i,92)=xndif*(rib(i,31)-rib(i,32))

       end do

c      Define rib 0
       rib(0,30)=rib(1,32)
       rib(0,31)=rib(1,31)
       rib(0,32)=rib(1,30)

       rib(0,33)=rib(1,35)
       rib(0,34)=rib(1,34)
       rib(0,35)=rib(1,33)

       rib(0,90)=xndif*(rib(0,31)-rib(0,30))
       rib(0,92)=xndif*(rib(0,31)-rib(0,32))


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Identify point jirl-r where initialize reformating skin(3,1) in %
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

c      Left side

       xirl(i)=rib(i,30)*skin(3,1)/100.

       rib(i,40)=0.
       do j=1,np(i,2)-1
       rib(i,40)=rib(i,40)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + (v(i-1,j,10)-v(i-1,j+1,10))**2.)
       if (rib(i,40).lt.rib(i,30)-xirl(i)) then
       x40=rib(i,40)
       jirl(i)=j
       end if
       end do

c      Right side

       xirr(i)=rib(i,32)*skin(3,1)/100.

       rib(i,42)=0.
       do j=1,np(i,2)-1
       rib(i,42)=rib(i,42)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+
     + (v(i,j,9)-v(i,j+1,9))**2.)
       if (rib(i,42).lt.rib(i,32)-xirr(i)) then
       x42=rib(i,42)
       jirr(i)=j
       end if
       end do

       end do

c      Assign in rib 0
       jirl(0)=jirl(1)
       jirr(0)=jirr(1)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat the last segments
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat left side - extrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss

c      Calcule length of the reformating polyline

       dist1=0.
       do j=1,jirl(i)-1
       dist1=dist1+sqrt((v(i-1,j,10)-v(i-1,j+1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j+1,10))**2.)
       end do
       
       dist2=0.
       do j=jirl(i),np(i,2)-1
       dist2=dist2+sqrt((v(i-1,j,10)-v(i-1,j+1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j+1,10))**2.)
       end do

       dist3=dist2+rib(i,90)

       distk=dist3/dist2  ! amplification coefficient

c      Reformat
      
       j=jirl(i-1)-1
       u(i-1,j,30)=u(i-1,j,10)
       v(i-1,j,30)=v(i-1,j,10)

       dis22=0.

       do j=jirl(i),np(i,2)-1

c      Atention whit angle definition using abs tangents
c      Make subroutines
c      Angles and distances, left side

       xdv=(v(i-1,j+1,10)-v(i-1,j,10))
       xdu=(u(i-1,j+1,10)-u(i-1,j,10))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))
       else
       anglee(j)=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i-1,j,10)-v(i-1,j+1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j+1,10))**2.)

       end do

c      Define

       do j=jirl(i),np(i,2)-1
       u(i-1,j+1,30)=u(i-1,j,10)+siu(j)*distk*distee(j)*dcos(anglee(j))
       v(i-1,j+1,30)=v(i-1,j,10)+siv(j)*distk*distee(j)*dsin(anglee(j))
       u(i-1,j+1,10)=u(i-1,j+1,30)
       v(i-1,j+1,10)=v(i-1,j+1,30)
       end do

       j=np(i,2)+1
       u(i-1,j,10)=u(i-1,j-1,10)+u(i-1,j-1,10)-u(i-1,j-2,10)
       v(i-1,j,10)=v(i-1,j-1,10)+v(i-1,j-1,10)-v(i-1,j-2,10)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat right side - extrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

c      Calcule length of the reformating polyline

       dist1=0.
       do j=1,jirr(i)-1
       dist1=dist1+sqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)
       end do
       
       dist2=0.
       do j=jirr(i),np(i,2)-1
       dist2=dist2+sqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)
       end do

       dist3=dist2+rib(i,92)

       distk=dist3/dist2  ! amplification coefficient

c      Reformat
      
       j=jirr(i-1)-1
       u(i,j,32)=u(i,j,9)
       v(i,j,32)=v(i,j,9)

       do j=jirr(i),np(i,2)-1

c      Atention whit angle definition using abs tangents
c      Make subroutines
c      Angles and distances, left side

       xdv=(v(i,j+1,9)-v(i,j,9))
       xdu=(u(i,j+1,9)-u(i,j,9))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))
       else
       anglee(j)=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)

       end do

c      Define

       do j=jirr(i),np(i,2)-1
       u(i,j+1,32)=u(i,j,9)+siu(j)*distk*distee(j)*dcos(anglee(j))
       v(i,j+1,32)=v(i,j,9)+siv(j)*distk*distee(j)*dsin(anglee(j))
       u(i,j+1,9)=u(i,j+1,32)
       v(i,j+1,9)=v(i,j+1,32)
       end do

       j=np(i,2)+1
       u(i,j,9)=u(i,j-1,9)+u(i,j-1,9)-u(i,j-2,9)
       v(i,j,9)=v(i,j-1,9)+v(i,j-1,9)-v(i,j-2,9)

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Final verification left and right side
c      Can be erased
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
       do i=1,nribss

       rib(i,40)=0.
       do j=1,np(i,2)-1
       rib(i,40)=rib(i,40)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + (v(i-1,j,10)-v(i-1,j+1,10))**2.)
       end do
      
       rib(i,42)=0.
       do j=1,np(i,2)-1
       rib(i,42)=rib(i,42)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+
     + (v(i,j,9)-v(i,j+1,9))**2.)
       end do

c       write (*,*) "IGUALS ",i,rib(i,40),rib(i,31),rib(i,42)

       end do

       end if ! end reformat 

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Distorsion calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Leading edge segment formated rib(i,97) extra

       do i=0,nribss-1

       if (i.lt.nribss) then
       j=np(i,2)
       rib(i,97)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
c       write (*,*) "rib(i,97) ",i,rib(i,97)
       end if

       end do

       do i=0,nribss-1

c       write (*,*) "DISTORSION 1 LE (mm)",i,(rib(i,97)-rib(i,96))*10
      
       end do

c      Iterations
       do itera=1,5

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     Distorsion correction
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Correction only for case ndif=1000

       if (ndif.eq.1000) then

       do i=1,nribss-1

       k=jirl(i)

       dist=dsqrt(((u(i,k,9)-u(i,np(i,2),9))**2.)+
     + ((v(i,k,9)-v(i,np(i,2),9))**2.))
      
       epsilon=(rib(i,97)-rib(i,96))

c      Angle of rotation
       if (abs(epsilon).lt.0.01) then
       omega=0.
       else
c      Experimental correction
       omega=1.0*dasin(epsilon/dist)*epsilon/(abs(epsilon))
       end if

c      Rotate left side (all correction)

       do j=jirl(i),np(i,2)-1

c      Atention whit angle definition using abs tangents
c      Make subroutines
c      Angles and distances, left side

       xdv=(v(i,j+1,9)-v(i,j,9))
       xdu=(u(i,j+1,9)-u(i,j,9))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))+omega
       else
       anglee(j)=2.*datan(1.0d0)+omega
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)

       end do  ! end j

c      Define

       do j=jirr(i),np(i,2)-1
       u(i,j+1,32)=u(i,j,9)+siu(j)*distee(j)*dcos(anglee(j))
       v(i,j+1,32)=v(i,j,9)+siv(j)*distee(j)*dsin(anglee(j))
       u(i,j+1,9)=u(i,j+1,32)
       v(i,j+1,9)=v(i,j+1,32)
       end do

       end do  ! end i

       end if  ! if ndif=1000


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Distorsion 2 calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Leading edge segment formated rib(i,97) extra

       do i=0,nribss-1

       if (i.lt.nribss) then
       j=np(i,2)
       rib(i,97)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do ! i

       end do ! itera


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     8.2.5 Calcule external points
c     Seam borders left (11) and right (12)
c     Points LE 11,12,14,15,24,25
c     Points TE 11,12,14,15,24,25
c     IMPROVED by subroutine extpoints in 2018-12-26
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      icasec=1 tangent
c      icasec=2 orthogonal

       icasecle=1
       icasecte=1

c      Load vectors

c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss

       npi=1
       npf=np(i,2)
       npo=npf-npi+1

c      Copy data in a free vector
       do j=1,npo

       uf(i,j,9)=u(i,npi+j-1,9)
       uf(i,j,10)=u(i,npi+j-1,10)
       uf(i,j,11)=u(i,npi+j-1,11)
       uf(i,j,12)=u(i,npi+j-1,12)
       vf(i,j,9)=v(i,npi+j-1,9)
       vf(i,j,10)=v(i,npi+j-1,10)
       vf(i,j,11)=v(i,npi+j-1,11)
       vf(i,j,12)=v(i,npi+j-1,12)

       ufe(i,j,9)=u(i,npi+j-1,9)
       ufe(i,j,10)=u(i,npi+j-1,10)
       ufe(i,j,11)=u(i,npi+j-1,11)
       ufe(i,j,12)=u(i,npi+j-1,12)
       vfe(i,j,9)=v(i,npi+j-1,9)
       vfe(i,j,10)=v(i,npi+j-1,10)
       vfe(i,j,11)=v(i,npi+j-1,11)
       vfe(i,j,12)=v(i,npi+j-1,12)

       end do

c      Call external points subroutine
c       call extpoints(i,uf,vf,npo,xupp,xupple,xuppte,1)

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2.6 Draw sobreamples extrados panels
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       if (n1draw.eq.1) then ! draw

c      Box (1,3)

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

cccccccccccccccccccccccccccccccccccccccccccccccccccccc    
c      Draw minirib extrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (i.ge.0.and.rib(i+1,56).gt.1.and.rib(i+1,56).ne.100
     + .and.atp.ne."ss") then

       xpo1=(u(i,1,9)+u(i,1,10))/2.
       ypo1=(v(i,1,9)+v(i,1,10))/2.
       j=jcve(i+1)
       xpo2=(u(i,j,9)+u(i,j,10))/2.
       ypo2=(v(i,j,9)+v(i,j,10))/2.

c      Avoid division by zero!!!
       if (xpo2-xpo1.ne.0.) then
       alpha=datan((ypo2-ypo1)/(xpo2-xpo1))
       end if
       if (abs(xpo2-xpo1).lt.0.00001) then
       alpha=pi/2.
       end if

       xpo3=xpo1+rib(i+1,60)*dcos(alpha)
       ypo3=ypo1+rib(i+1,60)*dsin(alpha)
       xdesx=xdes*dsin(alpha)
       xdesy=xdes*dcos(alpha)

c      Draw reference points for miniribs in extrados
       call line(psep+xpo1,psey-ypo1,psep+xpo3,psey-ypo3,5)
       call pointg(psep+xpo1-xdesx,psey-ypo1-xdesy,xcir,1)
       call pointg(psep+xpo3-xdesx,psey-ypo3-xdesy,xcir,1)

c      Laser cuting
       xadd=2520.*xkf
       call point(psep+xpo1+xadd,psey-ypo1,1)
       call point(psep+xpo3+xadd,psey-ypo3,1)

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccc

       npo=np(i,2)

c      Call draw panel extrados (complete)
c       call dpanelc(i,uf,vf,npo,psep,psey)

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.2.7 Dibuixa sobreamples panells extrados Adre
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,5)

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa marques romanes AD
       call romano(i,psep+5.,psey+0.5,0.0d0,typm6(8)*0.1,7)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

c      Draw romano in last panel
       if (i.eq.nribss-1) then
       call romano(i+1,psep+5.,psey+0.5,0.0d0,typm6(8)*0.1,7)
       end if

c      Call draw panel extrados (complete)
c       call dpanelb(i,uf,vf,npo,psep,psey)

       end do

       end if ! n1draw

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.3 SOBREAMPLES VENTS
c      REVISAR, NO FINALITZAT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      FUNCIONA (amb artificis!) es pot millorar

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.3.1 Sobreamples vents
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xcos=xlow/10. ! vent sewing allowance

c      Save xlow
       xlowsaved=xlow

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Artifici 1:
c      Salva punts 9,10,11,12 a un vector de seguretat
c      per evitar interferencies en calcul de punts extrados a secció 11.4
c      i recupera després de calcul sobreamples de vents
c      que dónen problemes per algun motiu
c      Eliminar aquesta secció i la seva restitució més a baix
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=iini,nribss

       
       do j=1,np(i,1) ! salva tots els punts

       usalvat(i,j,9)=u(i,j,9)
       vsalvat(i,j,9)=v(i,j,9)
       usalvat(i,j,10)=u(i,j,10)
       vsalvat(i,j,10)=v(i,j,10)

       usalvat(i,j,11)=u(i,j,11)
       vsalvat(i,j,11)=v(i,j,11)
       usalvat(i,j,12)=u(i,j,12)
       vsalvat(i,j,12)=v(i,j,12)

       end do
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.3.1 Sobreamples esquerra vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=iini,nribss

c      Set sewing border in vents according vent type
       if (k31d.eq.1.and.rib(i+1,165).ge.1) then
       xlow=xupp 
       else
       xlow=xlowsaved
       end if

c      Initialize sob points

c      CASE 0
       if (k31d.eq.0) then
       xsob(1)=0.
       ysob(1)=rib(i,22)*skin(1,2)/100.
       xsob(2)=rib(i,26)
       ysob(2)=rib(i,24)*skin(6,4)/100.
       end if

c      CASE 1.1
       if (k31d.eq.1) then
       xsob(1)=0.
       ysob(1)=rib(i,22)*skinnew(i,1,2)/100.
       xsob(2)=rib(i,26)
       ysob(2)=rib(i,24)*skinnew(i,skinpoints(i),4)/100.
       end if

c      Longituds u

       u(i,np(i,2),7)=0.
       
       do j=np(i,2),np(i,2)+np(i,3)-1
       u(i,j+1,7)=u(i,j,7)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)
       end do

c      Sobreample v      

       if (k31d.eq.0) then
       v(i,np(i,2),7)=rib(i,22)*skin(1,2)/100.
       end if
       if (k31d.eq.1) then
       v(i,np(i,2),7)=rib(i,22)*skinnew(i,1,2)/100.
       end if

       do j=np(i,2),np(i,2)+np(i,3)-1

       xm=(ysob(2)-ysob(1))/(xsob(2)-xsob(1))
       xn=ysob(2)-xm*xsob(2)

       v(i,j+1,7)=xm*(u(i,j+1,7))+xn

c      Solve some numeric problems!!!?
       if (v(i,j+1,7).le.0.001) then
       v(i,j+1,7)=0.0d0
       end if

       xm1=xm
       xn1=xn  
      
c      Calcula punts esquerra

       xdv=(pl2y(i,j)-pl1y(i,j))
       xdu=(pl2x(i,j)-pl1x(i,j))

       if (xdv.ne.0.) then
       alpl=abs(datan((pl2y(i,j)-pl1y(i,j))/(pl2x(i,j)-pl1x(i,j))))
       else
       alpl=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 2-I
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 2-II
       siu(j)=-1.
       siv(j)=-1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 2-III
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 2-IV
       siu(j)=1.
       siv(j)=-1.
       end if

       u(i,j,9)=pl1x(i,j)+siu(j)*v(i,j,7)*dsin(alpl)
       v(i,j,9)=pl1y(i,j)+siv(j)*v(i,j,7)*dcos(alpl)

       u(i,j,11)=u(i,j,9)+siu(j)*xlow*0.1*dsin(alpl)
       v(i,j,11)=v(i,j,9)+siv(j)*xlow*0.1*dcos(alpl)

c      PROBLEM with pl2y(i,j) value when j=np(i,2)
c      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       
       end do

       npx=np(i,2)

       alpl=abs(datan((pl2y(i,npx)-pl1y(i,npx))/
     + (pl2x(i,npx)-pl1x(i,npx))))
       alpl2=alpl

c      pl2x(i,npx-1) no correcte
       u(i,npx,9)=pl1x(i,npx)-v(i,npx,7)*dsin(alpl)
       v(i,npx,9)=pl1y(i,npx)+v(i,npx,7)*dcos(alpl)

       u(i,npx,11)=u(i,npx,9)-xlow*0.1*dsin(alpl)
       v(i,npx,11)=v(i,npx,9)+xlow*0.1*dcos(alpl)

       npx=np(i,2)+np(i,3)-1

       alpl=abs(datan((pl2y(i,npx)-pl1y(i,npx))/
     + (pl2x(i,npx)-pl1x(i,npx))))
       alpl2=alpl

c      pl2x(i,npx-1) no correcte
       u(i,npx,9)=pl1x(i,npx)-v(i,npx,7)*dsin(alpl)
       v(i,npx,9)=pl1y(i,npx)+v(i,npx,7)*dcos(alpl)

       u(i,npx,11)=u(i,npx,9)-xlow*0.1*dsin(alpl)
       v(i,npx,11)=v(i,npx,9)+xlow*0.1*dcos(alpl)
     
       end do ! i

       i=2
       if (i.eq.2) then
       do j=np(i,2),np(i,2)+np(i,3)-1
c       write (*,*) "vent 11 ",i,j,u(i,j,11),v(i,j,11)
       end do
       end if



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.3.2 Sobreamples dreta vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=iini,nribss-1

c      Set sewing border in vents according vent type
       if (k31d.eq.1.and.rib(i+1,165).ge.1) then
       xlow=xupp 
       else
       xlow=xlowsaved
       end if

c      Initialize sob points

c      Case k31d=0
       if (k31d.eq.0) then
       xsob(1)=0.
       ysob(1)=rib(i,22)*skin(1,2)/100.
       xsob(2)=rib(i,26)
       ysob(2)=rib(i,24)*skin(6,4)/100.
       end if

c      Case k31d=1
       if (k31d.eq.1) then
       xsob(1)=0.
       ysob(1)=rib(i,22)*skinnew(i+1,1,2)/100.
       xsob(2)=rib(i+1,26)
       ysob(2)=rib(i,24)*skinnew(i+1,skinpoints(i+1),4)/100.
       end if

c      Longituds u

       u(i,np(i,2),8)=0.
       
       do j=np(i,2),np(i,2)+np(i,3)-2
       u(i,j+1,8)=u(i,j,8)+sqrt((pr2x(i,j)-pr1x(i,j))**2+
     + (pr2y(i,j)-pr1y(i,j))**2)
       end do

c      Sobreample v      

       if (k31d.eq.0) then
       v(i,np(i,2),8)=rib(i,22)*skin(1,2)/100.
       end if
       if (k31d.eq.1) then
       v(i,np(i,2),8)=rib(i,22)*skinnew(i+1,1,2)/100.
       end if


       do j=np(i,2),np(i,2)+np(i,3)-2

       xm=(ysob(2)-ysob(1))/(xsob(2)-xsob(1))
       xn=ysob(2)-xm*xsob(2)

       v(i,j+1,8)=xm*(u(i,j+1,8))+xn

       xm1=xm
       xn1=xn  
      
c      Calcula punts dreta

       alpr=abs(datan((pr2y(i,j)-pr1y(i,j))/(pr2x(i,j)-pr1x(i,j))))

       u(i,j+1,10)=pr2x(i,j)+v(i,j+1,8)*dsin(alpr)
       v(i,j+1,10)=pr2y(i,j)-v(i,j+1,8)*dcos(alpr)

       u(i,j+1,12)=u(i,j+1,10)+xlow*0.1*dsin(alpr)
       v(i,j+1,12)=v(i,j+1,10)-xlow*0.1*dcos(alpr)

       end do

       npx=np(i,2)

       alpr=abs(datan((pr2y(i,npx)-pr1y(i,npx))/
     + (pr2x(i,npx)-pr1x(i,npx))))
       alpr2=alpr

       u(i,npx,10)=pr1x(i,npx)+v(i,npx,8)*dsin(alpr)
       v(i,npx,10)=pr1y(i,npx)-v(i,npx,8)*dcos(alpr)
       
       u(i,npx,12)=u(i,npx,10)+xlow*0.1*dsin(alpr)
       v(i,npx,12)=v(i,npx,10)-xlow*0.1*dcos(alpr)

       end do ! i

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.3.3 Calcula cantonades vents
c      Versio millorada segons 8.2.5
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss

       npi=np(i,2)
       npf=np(i,2)+np(i,3)-1
       npo=npf-npi+1

c      Copy data in a free vector
       do j=1,npo

       uf(i,j,9)=u(i,npi+j-1,9)
       uf(i,j,10)=u(i,npi+j-1,10)
       uf(i,j,11)=u(i,npi+j-1,11)
       uf(i,j,12)=u(i,npi+j-1,12)
       vf(i,j,9)=v(i,npi+j-1,9)
       vf(i,j,10)=v(i,npi+j-1,10)
       vf(i,j,11)=v(i,npi+j-1,11)
       vf(i,j,12)=v(i,npi+j-1,12)

       ufv(i,j,9)=u(i,npi+j-1,9)
       ufv(i,j,10)=u(i,npi+j-1,10)
       ufv(i,j,11)=u(i,npi+j-1,11)
       ufv(i,j,12)=u(i,npi+j-1,12)
       vfv(i,j,9)=v(i,npi+j-1,9)
       vfv(i,j,10)=v(i,npi+j-1,10)
       vfv(i,j,11)=v(i,npi+j-1,11)
       vfv(i,j,12)=v(i,npi+j-1,12)

       end do

c      Call external points subroutine
c       call extpoints(i,uf,vf,npo,xupp,xupp,xupp,1)

       end do

c      Retore xlow
       xlow=xlowsaved


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.3.4 Vents drawing > send to 8.5.2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       if (k31d.eq.1.and.k26d.ne.0) then ! Draw classic vents

c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1371.*xkf
       ncontrol=0

c      Control if cell is closed
       if(int(rib(i,14)).eq.0.and.int(rib(i+1,14)).eq.0) then
       ncontrol=1
       end if

       ncontrol=1       

c      Call draw panel extrados (complete)
c      call dpanelc(i,uf,vf,npo,psep,psey)

       end do

c       end if ! Vents case 1


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Artifici 1:
c      Recupera punts 9,10,11,12 del vector de seguretat
c      per evitar interferencies en calcul de punts extrados a secció 11.4
c      i recupera després de calcul sobreamples de vents
c      que dónen problemes per algun motiu
c      Eliminar aquesta secció i la seva restitució més amunt
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=iini,nribss
       do j=1,np(i,1) ! salva tots els punts

       u(i,j,9)=usalvat(i,j,9)
       v(i,j,9)=vsalvat(i,j,9)
       u(i,j,10)=usalvat(i,j,10)
       v(i,j,10)=vsalvat(i,j,10)

       u(i,j,11)=usalvat(i,j,11)
       v(i,j,11)=vsalvat(i,j,11)
       u(i,j,12)=usalvat(i,j,12)
       v(i,j,12)=vsalvat(i,j,12)

       end do
       end do

       i=2
       if (i.eq.2) then
       do j=1,np(i,2)
c      write (*,*) "salvat-11 ",i,u(i,j,11),v(i,j,11)
       end do
       end if



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4 SOBREAMPLES INTRADOS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Artifici 2:
c      Recupera un vector per evitar interferencia vents-intrados
c      Veure apartat 7.4.2
c      Vaja truc!!!
       do i=0,nribss
       npx=np(i,2)+np(i,3)-1
       pl1x(i,npx)=pl1x(i,499)
       pl1y(i,npx)=pl1y(i,499)
       pl2x(i,npx)=pl2x(i,499)       
       pl2y(i,npx)=pl2y(i,499)       
       pr1x(i,npx)=pr1x(i,499)
       pr1y(i,npx)=pr1y(i,499)
       pr2x(i,npx)=pr2x(i,499)
       pr2y(i,npx)=pr2y(i,499)
       end do
       
       xcos=xlow/10. ! intrados sewing allowance

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case classic skin tension k31d=0
c      Includes 8.4.1 and 8.4.2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k31d.eq.0) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.1 Sobreamples esquerra intrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

c      Initialize sob points

       do k=1,6

       xsob(k)=((100.-(skin(7-k,3)))/100.)*rib(i,25)
       ysob(k)=rib(i,24)*skin(7-k,4)/100.

       end do

c      Longituds u

       u(i,np(i,2)+np(i,3)-1,7)=0.
       
       do j=np(i,2)+np(i,3)-1,np(i,1)-1

       u(i,j+1,7)=u(i,j,7)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)

       end do

c      Sobreample v      

       v(i,np(i,2)+np(i,3)-1,7)=rib(i,24)*skin(6,4)/100.

       do j=np(i,2)+np(i,3)-1,np(i,1)-1

c      LE zone

       if(u(i,j+1,7).le.xsob(2)) then

       xm=(ysob(2)-ysob(1))/(xsob(2)-xsob(1))
       xn=ysob(2)-xm*xsob(2)

       v(i,j+1,7)=xm*(u(i,j+1,7))+xn

       xm1=xm
       xn1=xn

       end if
       
       if(u(i,j+1,7).gt.xsob(2).and.u(i,j+1,7).le.xsob(3)) then

       xm=(ysob(3)-ysob(2))/(xsob(3)-xsob(2))
       xn=ysob(2)-xm*xsob(2)

       v(i,j+1,7)=xm*(u(i,j+1,7))+xn

       xm2=xm
       xn2=xn

       end if

c      Central panel

       if(u(i,j+1,7).gt.xsob(3).and.u(i,j+1,7).le.xsob(4)) then

       xm=(ysob(4)-ysob(3))/(xsob(4)-xsob(3))
       xn=ysob(3)-xm*xsob(3)

       v(i,j+1,7)=xm*(u(i,j+1,7))+xn

       xm2=xm
       xn2=xn

       end if

c      TE zone

       if(u(i,j+1,7).gt.xsob(4).and.u(i,j+1,7).le.xsob(5)) then

       xm=(ysob(5)-ysob(4))/(xsob(5)-xsob(4))
       xn=ysob(4)-xm*xsob(4)

       v(i,j+1,7)=xm*(u(i,j+1,7))+xn

       xm3=xm
       xn3=xn

       end if

       if(u(i,j+1,7).gt.xsob(5)) then

       xm=(ysob(6)-ysob(5))/(xsob(6)-xsob(5))
       xn=ysob(5)-xm*xsob(5)

       v(i,j+1,7)=xm*(u(i,j+1,7))+xn

       xm3=xm
       xn3=xn

       end if

c      Calcula punts esquerra

       alpl=abs(datan((pl2y(i,j)-pl1y(i,j))/(pl2x(i,j)-pl1x(i,j))))

       u(i,j+1,9)=pl2x(i,j)-v(i,j+1,7)*dsin(alpl)
       v(i,j+1,9)=pl2y(i,j)+v(i,j+1,7)*dcos(alpl)

       u(i,j+1,11)=u(i,j+1,9)-xlow*0.1*dsin(alpl)
       v(i,j+1,11)=v(i,j+1,9)+xlow*0.1*dcos(alpl)
       
       end do

c       u(i,np(i,1),14)=u(i,np(i,1),9)+xlowte*0.1*dcos(alpl)
c       v(i,np(i,1),14)=v(i,np(i,1),9)+xlowte*0.1*dsin(alpl)
       
       npx=np(i,2)+np(i,3)-1

       alpl=abs(datan((pl2y(i,npx-1)-pl1y(i,npx-1))/
     + (pl2x(i,npx-1)-pl1x(i,npx-1))))
       alpl2=alpl

c      pl2x(i,npx-1) no correcte
       u(i,npx,9)=pl1x(i,npx)-v(i,npx,7)*dsin(alpl)
       v(i,npx,9)=pl1y(i,npx)+v(i,npx,7)*dcos(alpl)

       u(i,npx,11)=u(i,npx,9)-xlow*0.1*dsin(alpl)
       v(i,npx,11)=v(i,npx,9)+xlow*0.1*dcos(alpl)

c       u(i,npx,14)=u(i,npx,9)-xlowle*0.1*dcos(alpl)
c       v(i,npx,14)=v(i,npx,9)-xlowle*0.1*dsin(alpl)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.2 Sobreamples dreta intrados   
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Sobreamples dreta

       do i=0,nribss

c      Initialize sob points

       do k=1,6

       xsob(k)=((100.-(skin(7-k,3)))/100.)*rib(i+1,25)
       ysob(k)=rib(i,24)*skin(7-k,4)/100.

       end do

c      Longitud u

       u(i,np(i,2)+np(i,3)-1,8)=0.

       do j=np(i,2)+np(i,3)-1,np(i,1)-1

       u(i,j+1,8)=u(i,j,8)+sqrt((pr2x(i,j)-pr1x(i,j))**2+
     + (pr2y(i,j)-pr1y(i,j))**2)

       end do

c      Sobreample v      

       v(i,np(i,2)+np(i,3)-1,8)=rib(i,24)*skin(6,4)/100.

       do j=np(i,2)+np(i,3)-2,np(i,1)-1

c      LE zone

       if(u(i,j+1,8).le.xsob(2)) then

       xm=(ysob(2)-ysob(1))/(xsob(2)-xsob(1))
       xn=ysob(2)-xm*xsob(2)

       v(i,j+1,8)=xm*(u(i,j+1,8))+xn

       xm1=xm
       xn1=xn

       end if

       if(u(i,j+1,8).gt.xsob(2).and.u(i,j+1,8).le.xsob(3)) then

       xm=(ysob(3)-ysob(2))/(xsob(3)-xsob(2))
       xn=ysob(2)-xm*xsob(2)

       v(i,j+1,8)=xm*(u(i,j+1,8))+xn

       xm2=xm
       xn2=xn

       end if

c      Central panel

       if(u(i,j+1,8).gt.xsob(3).and.u(i,j+1,8).le.xsob(4)) then

       xm=(ysob(4)-ysob(3))/(xsob(4)-xsob(3))
       xn=ysob(3)-xm*xsob(3)

       v(i,j+1,8)=xm*(u(i,j+1,8))+xn

       xm2=xm
       xn2=xn

       end if

c      TE zone

       if(u(i,j+1,8).gt.xsob(4).and.u(i,j+1,8).le.xsob(5)) then

       xm=(ysob(5)-ysob(4))/(xsob(5)-xsob(4))
       xn=ysob(4)-xm*xsob(4)

       v(i,j+1,8)=xm*(u(i,j+1,8))+xn

       xm3=xm
       xn3=xn

       end if

       if(u(i,j+1,8).gt.xsob(5)) then

       xm=(ysob(6)-ysob(5))/(xsob(6)-xsob(5))
       xn=ysob(5)-xm*xsob(5)

       v(i,j+1,8)=xm*(u(i,j+1,8))+xn

       xm3=xm
       xn3=xn

       end if

c      Calcula punts dreta

       alpr=abs(datan((pr2y(i,j)-pr1y(i,j))/(pr2x(i,j)-pr1x(i,j))))

c      OPTION add corrections in sign (see 8.2.2)
c      But probably in normal intrados panels is not necessary

       u(i,j+1,10)=pr2x(i,j)+v(i,j+1,8)*dsin(alpr)
       v(i,j+1,10)=pr2y(i,j)-v(i,j+1,8)*dcos(alpr)

       u(i,j+1,12)=u(i,j+1,10)+xlow*0.1*dsin(alpr)
       v(i,j+1,12)=v(i,j+1,10)-xlow*0.1*dcos(alpr)

       end do  ! j=np(i,2)+np(i,3)-1,np(i,1)-1

c      Initial point not definined in previous bucle
       
       npx=np(i,2)+np(i,3)-1

       alpr=abs(datan((pr2y(i,npx)-pr1y(i,npx))/
     + (pr2x(i,npx)-pr1x(i,npx))))
       alpr2=alpr

       u(i,npx,10)=pr1x(i,npx)+v(i,npx,8)*dsin(alpr)
       v(i,npx,10)=pr1y(i,npx)-v(i,npx,8)*dcos(alpr)
       
       u(i,npx,12)=u(i,npx,10)+xlow*0.1*dsin(alpr)
       v(i,npx,12)=v(i,npx,10)-xlow*0.1*dcos(alpr)

c      Leading edge segment unformated rib(i,98) intra

       if (i.lt.nribss) then
       j=np(i,2)+np(i,3)-1
       rib(i,98)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do  ! i

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       end if  ! Case classic skin tension k31d=0
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case new skin tension k31d=1 Linear interpolation INTRADOS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k31d.eq.1) then

c       write (*,*) "NOTE: NEW skin tension in intrados"

c      Case 1: Linear interpolation and cell width is rib(i,24)
c       if (ntypei31(i).eq.1) then

c      Initialize sob points
       do i=0,nribss
       do k=1,skinpoints(i)
       xsobnew(i,k)=((100.-(skinnew(i,skinpoints(i)+1-k,3)))/100.)
     + *rib(i,25)
       ysobnew(i,k)=rib(i,24)*skinnew(i,skinpoints(i)+1-k,4)/100.
c       write (*,*) i,k,xsobnew(i,k),ysobnew(i,k)
       end do ! k
       end do ! i (initialize all sob points)

       do i=0,nribss
 
c      Initialize vector extrados left side
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       u(i,j,50)=u(i,j,7)
c      u(i,j,51)=u(i,j,8) ? verificar significat vectors 50 i 51
       end do  ! j

c      Assign lengths and sob distances
       u(i,np(i,2)+np(i,3)-1,7)=0.
       u(i,np(i,2)+np(i,3)-1,8)=0.

       do j=np(i,2)+np(i,3)-1,np(i,1)
       do k=1,skinpoints(i)

c      Left side
       if (u(i,j,7).ge.xsobnew(i,k).and.u(i,j,7).le.xsobnew(i,k+1)
     + *1.001) ! NOTE: Comparar reals és perillós, afegim multiplicador
     + then
       xm=(ysobnew(i,k+1)-ysobnew(i,k))/(xsobnew(i,k+1)-xsobnew(i,k))
       xn=ysobnew(i,k+1)-xm*xsobnew(i,k+1)
       v(i,j,7)=xm*(u(i,j,7))+xn

       end if

       u(i,j+1,7)=u(i,j,7)+sqrt((pl2x(i,j)-pl1x(i,j))**2+
     + (pl2y(i,j)-pl1y(i,j))**2)

c      Right side
       if (i.lt.nribss) then

       if (u(i,j,8).ge.xsobnew(i+1,k).and.u(i,j,8).le.
     + xsobnew(i+1,k+1)
     + *1.001) ! NOTE: Comparar reals és perillós, afegim multiplicador
     + then
       xm=(ysobnew(i+1,k+1)-ysobnew(i+1,k))/
     +    (xsobnew(i+1,k+1)-xsobnew(i+1,k))
       xn=ysobnew(i+1,k+1)-xm*xsobnew(i+1,k+1)
       v(i,j,8)=xm*(u(i,j,8))+xn

       end if

       u(i,j+1,8)=u(i,j,8)+sqrt((pr2x(i,j)-pr1x(i,j))**2+
     + (pr2y(i,j)-pr1y(i,j))**2)

       end if

       end do ! k

       end do ! j

c      Compute points left side
       call puntslat(i,pl1x,pl1y,pl2x,pl2y,np(i,1)-np(i,4)+1,
     + np(i,1)-1,u,v,xlow,-1)

c      Compute points right side
       call puntslat(i,pr1x,pr1y,pr2x,pr2y,np(i,1)-np(i,4)+1,
     + np(i,1)-1,u,v,xlow,1)

c      Leading edge segment unformated rib(i,98) intra
       if (i.lt.nribss) then
       j=np(i,2)+np(i,3)-1
       rib(i,98)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do  ! i

c       end if ! end case 1.1

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       end if  ! k31d=1 Linear interpolation INTRADOS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.3 Not necessary?
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.4 REFORMAT PANELS FOR PERFECT MATCHING
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Detect if ndif parameter is set for reformat
       if (ndif.eq.1000) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     Compute rib and panels lengths (also done in chapter 11. (!))
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

       rib(i,33)=0. ! intra panel left
       rib(i,34)=0. ! intra rib
       rib(i,35)=0. ! intra panel right

       do j=np(i,2)+np(i,3)-1,np(i,1)-1

       rib(i,33)=rib(i,33)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + ((v(i-1,j,10)-v(i-1,j+1,10))**2.))

       rib(i,34)=rib(i,34)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       rib(i,35)=rib(i,35)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       end do

c      Amplification cofficients
       rib(i,38)=rib(i,33)/rib(i,34)
       rib(i,39)=rib(i,35)/rib(i,34)

       rib(0,38)=rib(1,38)
       rib(0,39)=rib(1,38)

c      Differences with control coefficient xndif

       rib(i,93)=xndif*(rib(i,34)-rib(i,33))
       rib(i,95)=xndif*(rib(i,34)-rib(i,35))

       end do

c      Define rib 0
     
       rib(0,33)=rib(1,35)
       rib(0,34)=rib(1,34)
       rib(0,35)=rib(1,33)

       rib(0,93)=xndif*(rib(0,34)-rib(0,33))
       rib(0,95)=xndif*(rib(0,34)-rib(0,35))

c      Define special rib (probably is not necessary)

       rib(nribss,35)=rib(nribss,34)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Identify point jirl-r where initialize reformating skin(3,3) in %
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

c      Left side

       xirl(i)=rib(i,33)*skin(3,3)/100.

       rib(i,43)=0.
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       rib(i,43)=rib(i,43)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + (v(i-1,j,10)-v(i-1,j+1,10))**2.)
       if (rib(i,43).lt.xirl(i)) then
       x43=rib(i,43)
       jirl(i)=j
       end if
       end do

c      Right side

       xirr(i)=rib(i,35)*skin(3,3)/100.

       rib(i,45)=0.
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       rib(i,45)=rib(i,45)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+
     + (v(i,j,9)-v(i,j+1,9))**2.)
       if (rib(i,45).lt.xirr(i)) then
       x45=rib(i,45)
       jirr(i)=j
       end if
       end do

       end do

c      Assign in rib 0
       jirl(0)=jirl(1)
       jirr(0)=jirr(1)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat the last segments
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat left side - intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss

c      Calcule length of the reformating polyline

       dist1=0.0d0
       do j=jirl(i),np(i,1)-1
       dist1=dist1+dsqrt((v(i-1,j,10)-v(i-1,j+1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j+1,10))**2.)
       end do
       
       dist2=0.0d0
       do j=np(i,2)+np(i,3)-1,jirl(i)-1
       dist2=dist2+dsqrt((v(i-1,j,10)-v(i-1,j+1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j+1,10))**2.)
       end do

c       write (*,*) "rib(i,33)=",i,dist1+dist2,rib(i,33),
c     + dist1+dist2-rib(i,33)


       dist3=dist2+rib(i,93)

       distk=dist3/dist2  ! amplification coefficient

c      Reformat
      
       j=jirl(i-1)+1
       u(i-1,j,33)=u(i-1,j,10)
       v(i-1,j,33)=v(i-1,j,10)

c      Eliminar dis22!!!!!!!!!!!!!!!!!!!!!
       dis22=0.

       do j=jirl(i),np(i,2)+np(i,3),-1

c      Atention whit angle definition using abs tangents
c      Make subroutines
c      Angles and distances, left side

       xdv=(v(i-1,j-1,10)-v(i-1,j,10))
       xdu=(u(i-1,j-1,10)-u(i-1,j,10))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))
       else
       anglee(j)=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i-1,j,10)-v(i-1,j-1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j-1,10))**2.)

       end do

c      Define

       do j=jirl(i),np(i,2)+np(i,3),-1
       u(i-1,j-1,30)=u(i-1,j,10)+siu(j)*distk*distee(j)*dcos(anglee(j))
       v(i-1,j-1,30)=v(i-1,j,10)+siv(j)*distk*distee(j)*dsin(anglee(j))
       u(i-1,j-1,10)=u(i-1,j-1,30)
       v(i-1,j-1,10)=v(i-1,j-1,30)
       end do

c      AFEGIR calcul punts extrems!!!!!!!!!!!

c       j=np(i,2)+np(i,3)-1
c       u(i-1,j,10)=u(i-1,j-1,10)+u(i-1,j-1,10)-u(i-1,j-2,10)
c       v(i-1,j,10)=v(i-1,j-1,10)+v(i-1,j-1,10)-v(i-1,j-2,10)

c      VERIFICATION

       dist=0.0d0
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       dist=dist+sqrt((v(i-1,j,10)-v(i-1,j+1,10))**2.+
     + (u(i-1,j,10)-u(i-1,j+1,10))**2.)
       end do
c       write (*,*) "VERFICACIO L ",i,dist,rib(i,33),rib(i,34),rib(i,35)

       end do ! i

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat right side - intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

c      Calcule length of the reformating polyline

       dist1=0.0d0
       do j=jirr(i),np(i,1)-1
       dist1=dist1+sqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)
       end do
       
       dist2=0.0d0
       do j=np(i,2)+np(i,3)-1,jirr(i)-1
       dist2=dist2+sqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)
       end do

c       write (*,*) "rib(i,35)=",i,dist1+dist2,rib(i,35),
c     + dist1+dist2-rib(i,35)


       dist3=dist2+rib(i,95)

       distk=dist3/dist2  ! amplification coefficient

c      Reformat
      
       j=jirr(i-1)+1
       u(i,j,35)=u(i,j,9)
       v(i,j,35)=v(i,j,9)

       do j=jirl(i),np(i,2)+np(i,3),-1

c      Atention whit angle definition using abs tangents
c      Make subroutines
c      Angles and distances, left side

       xdv=(v(i,j-1,9)-v(i,j,9))
       xdu=(u(i,j-1,9)-u(i,j,9))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))
       else
       anglee(j)=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i,j,9)-v(i,j-1,9))**2.+
     + (u(i,j,9)-u(i,j-1,9))**2.)

       end do

c      Define

       do j=jirl(i),np(i,2)+np(i,3),-1
       u(i,j-1,32)=u(i,j,9)+siu(j)*distk*distee(j)*dcos(anglee(j))
       v(i,j-1,32)=v(i,j,9)+siv(j)*distk*distee(j)*dsin(anglee(j))
       u(i,j-1,9)=u(i,j-1,32)
       v(i,j-1,9)=v(i,j-1,32)
       end do

c      AFEGIR calcul punts extrems!!!!!!!!!!!

       j=np(i,2)+np(i,3)-2
       u(i,j,9)=u(i,j-1,9)+u(i,j-1,9)-u(i,j,9)
       v(i,j,9)=v(i,j-1,9)+v(i,j-1,9)-v(i,j,9)

c      VERIFICATION

       dist=0.0d0
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       dist=dist+sqrt((v(i,j,9)-v(i,j+1,9))**2.+
     + (u(i,j,9)-u(i,j+1,9))**2.)
       end do
c       write (*,*) "VERFICACIO R ",i,dist,rib(i,33),rib(i,34),rib(i,35)


       end do ! i

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Final verification left and right side
c      Can be erased
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
       do i=1,nribss

       rib(i,40)=0.
       do j=1,np(i,2)-1
       rib(i,40)=rib(i,40)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + (v(i-1,j,10)-v(i-1,j+1,10))**2.)
       end do
      
       rib(i,42)=0.
       do j=1,np(i,2)-1
       rib(i,42)=rib(i,42)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+
     + (v(i,j,9)-v(i,j+1,9))**2.)
       end do

c       write (*,*) "IGUALS ",i,rib(i,40),rib(i,31),rib(i,42)

       end do

       end if ! end reformat 

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Distorsion calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Leading edge segment formated rib(i,99) intra

       do i=0,nribss-1

       if (i.lt.nribss) then
       j=np(i,2)+np(i,3)-1
       rib(i,99)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     Distorsion correction
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Correction only for case ndif=1000

c      NOT DISTORSION CORRECTION 1001 !!!!!!!!!!!!!!!!!!!!!!

c      Iterations

       do itera=1,5

       if (ndif.eq.1000) then

c      Not reformating rib 1 to preserve simmetry

       do i=2,nribss-1

       k1=jirl(i)
       k2=np(i,2)+np(i,3)-1

c      Straight distance in reformat area
       dist=dsqrt(((u(i,k1,9)-u(i,k2,9))**2.)+
     + ((v(i,k1,9)-v(i,k2,9))**2.))
      
       epsilon=(rib(i,99)-rib(i,98))

c      Angle of rotation
       if (abs(epsilon).lt.0.01) then
       omega=0.
       else
c      Experimental correction
       omega=1.0*dasin(epsilon/dist)*epsilon/(abs(epsilon))
       end if

c      Rotate left side (all correction)

       do j=jirl(i),np(i,2)+np(i,3),-1

c      Atention whit angle definition using abs tangents
c      Make subroutines
c      Angles and distances, left side

       xdv=(v(i,j-1,9)-v(i,j,9))
       xdu=(u(i,j-1,9)-u(i,j,9))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))-omega
       else
       anglee(j)=2.*datan(1.0d0)-omega
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i,j,9)-v(i,j-1,9))**2.+
     + (u(i,j,9)-u(i,j-1,9))**2.)

       end do  ! end j

c      Define

       do j=jirl(i),np(i,2)+np(i,3),-1
       u(i,j-1,32)=u(i,j,9)+siu(j)*distee(j)*dcos(anglee(j))
       v(i,j-1,32)=v(i,j,9)+siv(j)*distee(j)*dsin(anglee(j))
       u(i,j-1,9)=u(i,j-1,32)
       v(i,j-1,9)=v(i,j-1,32)
       end do

c      AFEGIR calcul punts extrems!!!!!!!!!!! ?
c      com reformat normal

       end do  ! end i

       end if  ! if ndif=1000

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Distorsion 2 calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Leading edge segment formated rib(i,99) extra

       do i=0,nribss-1

       if (i.lt.nribss) then
       j=np(i,2)+np(i,3)-1
       rib(i,99)=dsqrt((u(i,j,9)-u(i,j,10))**2.+
     + ((v(i,j,9)-v(i,j,10))**2.))
       end if

       end do ! i

       end do ! itera


c      DISTORSIONS
       do i=0,nribss-1
c       write (*,*) "99-98 ",rib(i,99),rib(i,98),rib(i,99)-rib(i,98)
       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.5 Calcula cantonades panells intrados
c      Versio millorada segons 8.2.5
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
     
c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss

       npi=np(i,2)+np(i,3)-1
       npf=np(i,1)
       npo=npf-npi+1

c      Copy data in a free vector
       do j=1,npo

       uf(i,j,9)=u(i,npi+j-1,9)
       uf(i,j,10)=u(i,npi+j-1,10)
       uf(i,j,11)=u(i,npi+j-1,11)
       uf(i,j,12)=u(i,npi+j-1,12)
       vf(i,j,9)=v(i,npi+j-1,9)
       vf(i,j,10)=v(i,npi+j-1,10)
       vf(i,j,11)=v(i,npi+j-1,11)
       vf(i,j,12)=v(i,npi+j-1,12)

       ufi(i,j,9)=u(i,npi+j-1,9)
       ufi(i,j,10)=u(i,npi+j-1,10)
       ufi(i,j,11)=u(i,npi+j-1,11)
       ufi(i,j,12)=u(i,npi+j-1,12)
       vfi(i,j,9)=v(i,npi+j-1,9)
       vfi(i,j,10)=v(i,npi+j-1,10)
       vfi(i,j,11)=v(i,npi+j-1,11)
       vfi(i,j,12)=v(i,npi+j-1,12)

       end do

c      Call external points subroutine
c       call extpoints(i,uf,vf,npo,xupp,xuppte,xupple,1)

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.6 Dibuixa sobreamples panells intrados i vores de costura
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (n1draw.eq.1) then ! draw

c      Control if type is not "ss"
       if (atp.ne."ss") then

c      Box

c      Saltar cella 0 si gruix nul
       iini=0
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1
   
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf

cccccccccccccccccccccccccccccccccccccccccccccccccccccc    
c      Draw minirib intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (i.ge.0.and.rib(i+1,56).gt.1.and.rib(i+1,56).ne.100.and
     + .atp.ne."ss") then

       xpo1=(u(i,np(i,1),9)+u(i,np(i,1),10))/2.
       ypo1=(v(i,np(i,1),9)+v(i,np(i,1),10))/2.
       j=jcvi(i+1)
       xpo2=(u(i,j,9)+u(i,j,10))/2.
       ypo2=(v(i,j,9)+v(i,j,10))/2.

c      Evita divisions per zero!!!
       if (xpo2-xpo1.ne.0.) then
       alpha=datan((ypo2-ypo1)/(xpo2-xpo1))
       end if
       if (abs(xpo2-xpo1).lt.0.00001) then
       alpha=pi/2.
       end if

       xpo3=xpo1-rib(i+1,61)*dcos(alpha)
       ypo3=ypo1-rib(i+1,61)*dsin(alpha)
       xdesx=xdes*dsin(alpha)
       xdesy=xdes*dcos(alpha)

c      Draw reference points for miniribs in intrados
       call line(psep+xpo1,psey-ypo1,psep+xpo3,psey-ypo3,5)
       call pointg(psep+xpo1-xdesx,psey-ypo1-xdesy,xcir,1)
       call pointg(psep+xpo3-xdesx,psey-ypo3-xdesy,xcir,1)

c      Laser cuting
       xadd=2520.*xkf
       call point(psep+xpo1+xadd,psey-ypo1,1)
       call point(psep+xpo3+xadd,psey-ypo3,1)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Call draw panel intrados (complete)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      To 8.5 section

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.4.7 Dibuixa sobreamples panells intrados i vores de costura
c      Adre
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      To 8.5 section


c      End if control if not "ss"
       end if

       end if ! n1draw



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5 Draw all panels
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.0.1 LAUNCH 3D-shaping calculus
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (k29d.eq.1) then

c      Set vector 47 for 3D airfoil coordinates       
       do i=0,nribss
       do j=1,np(i,1)
       u(i,j,47)=x(i,j)
       v(i,j,47)=y(i,j)
       w(i,j,47)=z(i,j)
       end do
       end do

c      Load "free" vectors in a new vector...
c      "69" points at left  side panel between rib i and i+1
c      "70" points at right side panel between rib i and i+1

       do i=0,nribss-1

c      Extrados
       do j=1,np(i,2)
       u(i,j,69)=ufe(i,j,9)
       v(i,j,69)=vfe(i,j,9)
       u(i,j,70)=ufe(i,j,10)
       v(i,j,70)=vfe(i,j,10)
       end do

c      Vents
       do j=np(i,2),np(i,2)+np(i,3)-1
       u(i,j,69)=ufv(i,j-np(i,2)+1,9)
       v(i,j,69)=vfv(i,j-np(i,2)+1,9)
       u(i,j,70)=ufv(i,j-np(i,2)+1,10)
       v(i,j,70)=vfv(i,j-np(i,2)+1,10)
       end do

c      Intrados
       do j=np(i,2)+np(i,3)-1,np(i,1)
       u(i,j,69)=ufi(i,j-(np(i,2)+np(i,3)-2),9)
       v(i,j,69)=vfi(i,j-(np(i,2)+np(i,3)-2),9)
       u(i,j,70)=ufi(i,j-(np(i,2)+np(i,3)-2),10)
       v(i,j,70)=vfi(i,j-(np(i,2)+np(i,3)-2),10)
       end do

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc      
c      Call main 3d subroutine 
c      Computes median airfoil (48)
c      Computes hautok(i,j)
c      Computes ovalized median airfoil (49)
c      Computes median local 2D airfoil (53)
c      Computes ovalized median local 2D airfoil (54)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss
       call panels3d(i,rib,np,u,v,w,
     + uppcuts,iupp,kiupp,lowcuts,ilow,kilow,hautok)
       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Call compute zones of influence
c      zinf(i,6,1) first cut extrados
c      zinf(i,6,2) second cut extrados
c      zinf(i,6,4) first cut intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
       do i=0,nribss
       call czinf(i,rib,np,u,v,w,
     + uppcuts,iupp,kiupp,lowcuts,ilow,kilow,hautok,zinf)
       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.0.2 Draw ovalized airfoils in 2D
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,8)
       
       sepxx=700.*xkf
       sepyy=100.*xkf
       kx=0
       ky=0
       kyy=0

       do i=1,nribss

       sepx=6.0*1260.0*xkf+sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*1.0*float(ky)

c      Draw vents (copied from 9.4)

c      ini
       j=np(i,2)
       alpha1=pi+datan((w(i,j,53)-w(i,j-1,53))/(v(i,j,53)-v(i,j-1,53)))
       call line(sepx+v(i,j,53),-w(i,j,53)+sepy,sepx+v(i,j,53)-
     + 4.*dsin(alpha1),-w(i,j,53)-4.*dcos(alpha1)+sepy,1)

       x1=2530.*xkf+sepx+v(i,j,53)+0.1*typm6(4)*dsin(alpha1)
       y1=-w(i,j,53)+sepy+0.1*typm6(4)*dcos(alpha1)
       x2=2530.*xkf+sepx+v(i,j,53)-0.1*(typm5(4)-typm6(4))*dsin(alpha1)
       y2=-0.1*(typm5(4)-typm6(4))*dcos(alpha1)-w(i,j,53)+sepy

       if (typevent.eq.1) then
c      Double point
c       call point(x1,y1,3)
c       call point(x2,y2,3)
       end if

       if (typevent.eq.2) then
c      Segment
c       call linevent(x1,y1,x2,y2,3)
       end if

       if (typevent.eq.3) then
c      Segment 101
c       call segment101(x1,y1,x2,y2,3)
       end if

c      fi
       j=np(i,2)+np(i,3)-1
       alpha1=pi+datan((w(i,j+1,53)-w(i,j-1,53))/(v(i,j+1,53)-
     + v(i,j-1,53)))
       call line(sepx+v(i,j,53),-w(i,j,53)+sepy,sepx+v(i,j,53)-
     + 4.*dsin(alpha1),-w(i,j,53)-4.*dcos(alpha1)+sepy,1)

       x1=2530.*xkf+sepx+v(i,j,53)+0.1*typm6(4)*dsin(alpha1)
       y1=-w(i,j,53)+sepy+0.1*typm6(4)*dcos(alpha1)
       x2=2530.*xkf+sepx+v(i,j,53)-0.1*(typm5(4)-typm6(4))*dsin(alpha1)
       y2=-0.1*(typm5(4)-typm6(4))*dcos(alpha1)-w(i,j,53)+sepy

       if (typevent.eq.1) then
c      Double point
c       call point(x1,y1,3)
c       call point(x2,y2,3)
       end if

       if (typevent.eq.2) then
c      Segment
c       call linevent(x1,y1,x2,y2,3)
       end if

       if (typevent.eq.3) then
c      Segment 101
c       call segment101(x1,y1,x2,y2,3)
       end if

c      Numbering
       call romano(i,sepx+0.89d0*rib(i,5),sepy-1.0d0,0.0d0,
     + typm6(9)*0.1,4)
       call itxt(sepx-16.-84.*(typm3(9)/7.),sepy,typm3(9),0.0d0,i,7)

c      Draw middle 2D airfoil (index 53) and ovalized (index 54)
c      Nota: millorar dibuix SK

       if (atp.ne."ss") then
       do j=1,np(i,1)-1
       call line(sepx+v(i,j,53),sepy-w(i,j,53),sepx+v(i,j+1,53),
     + sepy-w(i,j+1,53),7)
       call line(sepx+v(i,j,54),sepy-w(i,j,54),sepx+v(i,j+1,54),
     + sepy-w(i,j+1,54),4)
       end do ! j
       end if

       if (atp.eq."ss") then
       do j=1,np(i,2)-1
       call line(sepx+v(i,j,53),sepy-w(i,j,53),sepx+v(i,j+1,53),
     + sepy-w(i,j+1,53),7)
       call line(sepx+v(i,j,54),sepy-w(i,j,54),sepx+v(i,j+1,54),
     + sepy-w(i,j+1,54),4)
       end do ! j
       end if

       if (atp.eq."ss".and.rib(i,165).eq.1) then
       do j=np(i,2)-1,np(i,2)+np(i,3)-2
       call line(sepx+v(i,j,53),sepy-w(i,j,53),sepx+v(i,j+1,53),
     + sepy-w(i,j+1,53),7)
       call line(sepx+v(i,j,54),sepy-w(i,j,54),sepx+v(i,j+1,54),
     + sepy-w(i,j+1,54),4)
       end do ! j
       end if

       kx=int((float(i)/6.))
       ky=i-kx*6
       kyy=kyy+1

c      Draw points cuts 3D-shaping
       if (k29d.eq.1) then

       ng=rib(i,169)

c      Extrados points
       if (uppcuts(ng).eq.0) then
       end if

       if (uppcuts(ng).eq.1) then
       j=iupp(1,2,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),3)
       j=iupp(1,3,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),6)
       end if

       if (uppcuts(ng).eq.2) then
       j=iupp(1,2,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),3)
       j=iupp(1,3,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),6)
       j=iupp(2,3,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),2)
       end if

c      Intrados points
       if (atp.ne."ss") then
       if (lowcuts(ng).eq.0) then
       end if
       if (lowcuts(ng).eq.1) then
       j=ilow(1,2,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),32)
       j=ilow(1,3,ng)
       call line(sepx+v(i,j,53),sepy-w(i,j,53),
     + sepx+v(i,j,54),sepy-w(i,j,54),5)
       end if
       end if

       end if ! k29d=1

       end do ! i


       end if ! k29d=1


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (n1draw.eq.1) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Plotter panels
c      Box (1,3)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.1 Extrados without vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Plotter BOX(1,3)

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

c      Print panel numbers
       xlen=rib(2,2)-rib(1,2)
c      Boxes (0,3),(-1,3)
       if (k29d.eq.1) then
       call itxt2(psep+1.1*xlen,-psey-890.95*xkf*1.0+30.,
     + typm3(9),0.0d0,i+1,7)
       if (atp.ne."ss") then
       call itxt2(psep+1.1*xlen,-psey-890.95*xkf*0.0+30.,
     + typm3(9),0.0d0,i+1,7)
       end if
       end if
c      Boxes (1,3) (2,3)
       call itxt2(psep+1.1*xlen,-psey+890.95*xkf*1.0-64.,
     + typm3(9),0.0d0,i+1,7)
       if (atp.ne."ss") then
       call itxt2(psep+1.1*xlen,-psey+890.95*xkf*2.0-64.,
     + typm3(9),0.0d0,i+1,7)
       end if

c      load data extrados from a free vector

       npi=1
       npf=np(i,2)
       npo=npf-npi+1

       do j=1,npo

       uf(i,j,9)=ufe(i,j,9)
       uf(i,j,10)=ufe(i,j,10)
       uf(i,j,11)=ufe(i,j,11)
       uf(i,j,12)=ufe(i,j,12)
       vf(i,j,9)=vfe(i,j,9)
       vf(i,j,10)=vfe(i,j,10)
       vf(i,j,11)=vfe(i,j,11)
       vf(i,j,12)=vfe(i,j,12)

       end do

c      Print panels extrados without vents
       if (k26d.eq.0.or.rib(i+1,165).ne.1) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xuppte,1)
       call dpanelc(i,uf,vf,npo,psep,psey)
       end if

       end do

c      Laser BOX(1,5)

       do i=iini,nribss-1
       
       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

c      Print panels extrados without vents
       if (k26d.eq.0.or.rib(i+1,165).ne.1) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xuppte,1)
       call dpanelb(i,uf,vf,npo,psep,psey)
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.2 Extrados with vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Plotter BOX(1,3)

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

c      load data extrados from a free vector

c      Piece 1
       npi=1
       npf=np(i,2)
       npo1=npf-npi+1

       do j=1,npo1
       uf(i,j,9)=ufe(i,j,9)
       uf(i,j,10)=ufe(i,j,10)
       uf(i,j,11)=ufe(i,j,11)
       uf(i,j,12)=ufe(i,j,12)
       vf(i,j,9)=vfe(i,j,9)
       vf(i,j,10)=vfe(i,j,10)
       vf(i,j,11)=vfe(i,j,11)
       vf(i,j,12)=vfe(i,j,12)
       end do

       npi=np(i,2)
       npf=np(i,2)+np(i,3)-1
       npo2=npf-npi+1

c      Move piece 2 to 1 by translation and rotation
       cs1x=(uf(i,npo1,9)+uf(i,npo1,10))*0.5
       cs1y=(vf(i,npo1,9)+vf(i,npo1,10))*0.5
       cs2x=(ufv(i,1,9)+ufv(i,1,10))*0.5
       cs2y=(vfv(i,1,9)+vfv(i,1,10))*0.5

       alpha=(datan((v(i,npo1,10)-v(i,npo1,9))/
     + (u(i,npo1,10)-u(i,npo1,9))))

c      1) Traslació -cs2x
       do j=1,npo2
       ufb(i,j,9)=ufv(i,j,9)-cs2x
       ufb(i,j,10)=ufv(i,j,10)-cs2x
       ufb(i,j,11)=ufv(i,j,11)-cs2x
       ufb(i,j,12)=ufv(i,j,12)-cs2x
       end do

c      2) Rotació alpha
       do j=1,npo2
       ufa(i,j,9)=ufb(i,j,9)*dcos(alpha)-vfv(i,j,9)*dsin(alpha)
       vfa(i,j,9)=ufb(i,j,9)*dsin(alpha)+vfv(i,j,9)*dcos(alpha)
       ufa(i,j,10)=ufb(i,j,10)*dcos(alpha)-vfv(i,j,10)*dsin(alpha)
       vfa(i,j,10)=ufb(i,j,10)*dsin(alpha)+vfv(i,j,10)*dcos(alpha)
       ufa(i,j,11)=ufb(i,j,11)*dcos(alpha)-vfv(i,j,11)*dsin(alpha)
       vfa(i,j,11)=ufb(i,j,11)*dsin(alpha)+vfv(i,j,11)*dcos(alpha)
       ufa(i,j,12)=ufb(i,j,12)*dcos(alpha)-vfv(i,j,12)*dsin(alpha)
       vfa(i,j,12)=ufb(i,j,12)*dsin(alpha)+vfv(i,j,12)*dcos(alpha)
       end do

c      3) Traslació (cs1x,cs1y)
       do j=1,npo2
       ufb(i,j,9)=ufa(i,j,9)+cs1x
       ufb(i,j,10)=ufa(i,j,10)+cs1x
       ufb(i,j,11)=ufa(i,j,11)+cs1x
       ufb(i,j,12)=ufa(i,j,12)+cs1x
       vfb(i,j,9)=vfa(i,j,9)+cs1y
       vfb(i,j,10)=vfa(i,j,10)+cs1y
       vfb(i,j,11)=vfa(i,j,11)+cs1y
       vfb(i,j,12)=vfa(i,j,12)+cs1y
       end do

c      Load Piece 2
       do j=2,npo2  ! 2 to avoid double definition

       uf(i,j+npo1-1,9)=ufb(i,j,9)
       uf(i,j+npo1-1,10)=ufb(i,j,10)
       uf(i,j+npo1-1,11)=ufb(i,j,11)
       uf(i,j+npo1-1,12)=ufb(i,j,12)
       vf(i,j+npo1-1,9)=vfb(i,j,9)
       vf(i,j+npo1-1,10)=vfb(i,j,10)
       vf(i,j+npo1-1,11)=vfb(i,j,11)
       vf(i,j+npo1-1,12)=vfb(i,j,12)

       end do

       npo=npf

c      Print panels extrados with vents
       
       if (k26d.eq.1.and.rib(i+1,165).eq.1) then
c      WARNING!!! Amples laterals xupp no fan efecte a la subrutina
c      Cal definir abans als vectors u(i,j,11) v u(i,j,12) v
       call extpoints(i,uf,vf,npo,xupp,xupple,xuppte,1)
       call dpanelc(i,uf,vf,npo,psep,psey)
       call line(psep+uf(i,npo1,9),psey-vf(i,npo1,9),
     + psep+uf(i,npo1,10),psey-vf(i,npo1,10),1)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print points vents (left)

       xu=uf(i,npo,9)
       xv=vf(i,npo,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,npo,9)-vf(i,npo-1,9))/
     + (uf(i,npo,9)-uf(i,npo-1,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)

c      Print points vents (right)

       xu=uf(i,npo,10)
       xv=vf(i,npo,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,npo,10)-vf(i,npo-1,10))/
     + (uf(i,npo,10)-uf(i,npo-1,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end if

       end do

c      Laser BOX(1,5)

       do i=iini,nribss-1

       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

c      Print panels extrados with vents
       if (k26d.eq.1.and.rib(i+1,165).eq.1) then
       call extpoints(i,uf,vf,npo,xupp,xuppte,xupple,1)
       call dpanelb(i,uf,vf,npo,psep,psey)

       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.3 Vents amb vores
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1371.*xkf

c      load data vents from a free vector

       npi=np(i,2)
       npf=np(i,2)+np(i,3)-1
       npo=npf-npi+1

       do j=1,npo

       uf(i,j,9)=ufv(i,j,9)
       uf(i,j,10)=ufv(i,j,10)
       uf(i,j,11)=ufv(i,j,11)
       uf(i,j,12)=ufv(i,j,12)
       vf(i,j,9)=vfv(i,j,9)
       vf(i,j,10)=vfv(i,j,10)
       vf(i,j,11)=vfv(i,j,11)
       vf(i,j,12)=vfv(i,j,12)

       end do

c      Print panels vents
       if (k26d.eq.1.and.rib(i+1,165).eq.0) then

c       write (*,*) i,xlow,xlowle,xlowte

c      WARNING!!! xlow NOT USED in subroutine (defided previosly in 8.3.1 and 8.3.2)
       call extpoints(i,uf,vf,npo,xlow,xlowle,xupple,1)
       call dpanelc(i,uf,vf,npo,psep,psey)
       end if

c      Vents case -2 (joint to intrados)
c      NO CAL
       if (k26d.eq.1.and.rib(i+1,165).eq.-2) then
c       call extpoints(i,uf,vf,npo,xlow,xlowle,xupple,1)
c       call dpanelc(i,uf,vf,npo,psep,psey)
c       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),psep+uf(i,1,10),
c     + psey-vf(i,1,10),1)
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.4 Intrados without vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Control if type is not "ss"
       if (atp.ne."ss") then

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf

c      load data vents from a free vector

       npi=np(i,2)+np(i,3)-1
       npf=np(i,1)
       npo=npf-npi+1

       do j=1,npo

       uf(i,j,9)=ufi(i,j,9)
       uf(i,j,10)=ufi(i,j,10)
       uf(i,j,11)=ufi(i,j,11)
       uf(i,j,12)=ufi(i,j,12)
       vf(i,j,9)=vfi(i,j,9)
       vf(i,j,10)=vfi(i,j,10)
       vf(i,j,11)=vfi(i,j,11)
       vf(i,j,12)=vfi(i,j,12)

       end do

c      Print panels intrados
       if (k26d.eq.0.or.rib(i+1,165).ge.0) then
       call extpoints(i,uf,vf,npo,xupp,xlowte,xlowle,1)
       call dpanelc(i,uf,vf,npo,psep,psey)
       end if

       end do

c      Laser BOX(1,5)

       do i=iini,nribss-1
       
       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf

c      Print panels intrados
       if (k26d.eq.0.or.rib(i+1,165).ge.0) then
       call extpoints(i,uf,vf,npo,xupp,xlowte,xlowle,1)
       call dpanelb(i,uf,vf,npo,psep,psey)
       end if

       end do

       end if  ! control intrados "ss"


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.5.5 Intrados with vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Control if type is not "ss"
       if (atp.ne."ss") then

       do i=iini,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf

c      load data intrados from a free vector

       npi=np(i,2)+np(i,3)-1
       npf=np(i,1)
       npo1=npf-npi+1

       do j=1,npo1
       ufa(i,j,9)=ufi(i,j,9)
       ufa(i,j,10)=ufi(i,j,10)
       ufa(i,j,11)=ufi(i,j,11)
       ufa(i,j,12)=ufi(i,j,12)
       vfa(i,j,9)=vfi(i,j,9)
       vfa(i,j,10)=vfi(i,j,10)
       vfa(i,j,11)=vfi(i,j,11)
       vfa(i,j,12)=vfi(i,j,12)
       end do

       cs1x=(ufa(i,1,9)+ufa(i,1,10))*0.5 ! Point 1
       cs1y=(vfa(i,1,9)+vfa(i,1,10))*0.5 ! Point 1
       
       alpha1=(datan((vfa(i,1,10)-vfa(i,1,9))/
     + (ufa(i,1,10)-ufa(i,1,9))))

c      1) Print panels intrados without vents and without LE
       if (k26d.eq.1.and.rib(i+1,165).le.-1) then
       call extpoints(i,ufa,vfa,npo1,xupp,xlowte,xlowle,1)
       call dpanelc1(i,ufa,vfa,npo,psep,psey)
       end if

c      2) Load vents 

       npi=np(i,2)
       npf=np(i,2)+np(i,3)-1
       npo2=npf-npi+1      
             
       do j=1,npo2
       ufb(i,j,9)=ufv(i,j,9)
       ufb(i,j,10)=ufv(i,j,10)
       ufb(i,j,11)=ufv(i,j,11)
       ufb(i,j,12)=ufv(i,j,12)
       vfb(i,j,9)=vfv(i,j,9)
       vfb(i,j,10)=vfv(i,j,10)
       vfb(i,j,11)=vfv(i,j,11)
       vfb(i,j,12)=vfv(i,j,12)
       end do

c      3) Translate vents from point 2 to (0,0)
      
       cs2x=(ufb(i,npo2,9)+ufb(i,npo2,10))*0.5
       cs2y=(vfb(i,npo2,9)+vfb(i,npo2,10))*0.5
       
       do j=1,npo2
       ufb(i,j,9)=ufv(i,j,9)-cs2x
       ufb(i,j,10)=ufv(i,j,10)-cs2x
       ufb(i,j,11)=ufv(i,j,11)-cs2x
       ufb(i,j,12)=ufv(i,j,12)-cs2x
       vfb(i,j,9)=vfv(i,j,9)-cs2y
       vfb(i,j,10)=vfv(i,j,10)-cs2y
       vfb(i,j,11)=vfv(i,j,11)-cs2y
       vfb(i,j,12)=vfv(i,j,12)-cs2y
       end do

c      4) Rotation angle alpha

       alpha2=(datan((vfb(i,npo2,10)-vfb(i,npo2,9))/
     + (ufb(i,npo2,10)-ufb(i,npo2,9))))
       alpha=-(alpha2-alpha1)
      
       do j=1,npo2
       ufc(i,j,9)=ufb(i,j,9)*dcos(alpha)-vfb(i,j,9)*dsin(alpha)
       vfc(i,j,9)=ufb(i,j,9)*dsin(alpha)+vfb(i,j,9)*dcos(alpha)
       ufc(i,j,10)=ufb(i,j,10)*dcos(alpha)-vfb(i,j,10)*dsin(alpha)
       vfc(i,j,10)=ufb(i,j,10)*dsin(alpha)+vfb(i,j,10)*dcos(alpha)
       ufc(i,j,11)=ufb(i,j,11)*dcos(alpha)-vfb(i,j,11)*dsin(alpha)
       vfc(i,j,11)=ufb(i,j,11)*dsin(alpha)+vfb(i,j,11)*dcos(alpha)
       ufc(i,j,12)=ufb(i,j,12)*dcos(alpha)-vfb(i,j,12)*dsin(alpha)
       vfc(i,j,12)=ufb(i,j,12)*dsin(alpha)+vfb(i,j,12)*dcos(alpha)
       end do

c      5) Translate vents from point (0,0) to 1
       
       do j=1,npo2
       uf(i,j,9)=ufc(i,j,9)+cs1x
       uf(i,j,10)=ufc(i,j,10)+cs1x
       uf(i,j,11)=ufc(i,j,11)+cs1x
       uf(i,j,12)=ufc(i,j,12)+cs1x
       vf(i,j,9)=vfc(i,j,9)+cs1y
       vf(i,j,10)=vfc(i,j,10)+cs1y
       vf(i,j,11)=vfc(i,j,11)+cs1y
       vf(i,j,12)=vfc(i,j,12)+cs1y
       end do

c      6) Force last point of vent as first point of intrados (?)

       uf(i,npo2,9)=ufa(i,1,9)
       uf(i,npo2,10)=ufa(i,1,10)
       uf(i,npo2,11)=ufa(i,1,11)
       uf(i,npo2,12)=ufa(i,1,12)
       vf(i,npo2,9)=vfa(i,1,9)
       vf(i,npo2,10)=vfa(i,1,10)
       vf(i,npo2,11)=vfa(i,1,11)
       vf(i,npo2,12)=vfa(i,1,12)
       
c      7) Print vents without TE case -1
       if (k26d.eq.1.and.rib(i+1,165).eq.-1.) then
       call extpoints(i,uf,vf,npo2,xupp,xlowte,xlowle,1)
       call dpanelc2(i,uf,vf,npo2,psep,psey)
      
c      Print points vents (left)

       xu=uf(i,1,9)
       xv=vf(i,1,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,1,9)-vf(i,2,9))/
     + (uf(i,1,9)-uf(i,2,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)

c      Print points vents (right)

       xu=uf(i,1,10)
       xv=vf(i,1,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,1,10)-vf(i,2,10))/
     + (uf(i,1,10)-uf(i,2,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if


c      8) Print vents without TE case -2
       if (k26d.eq.1.and.rib(i+1,165).eq.-2.) then
       call extpoints(i,uf,vf,npo2,xupp,xlowte,xlowle,1)
       call dpanelcm2(i,uf,vf,npo2,psep,psey)
       do j=1,npo2-1 ! LASER
       call line(psep+2520.*xkf+uf(i,j,12),psey-vf(i,j,12),
     + psep+2520.*xkf+uf(i,j+1,12),psey-vf(i,j+1,12),3)
       end do
       call line(psep+uf(i,npo2,9),psey-vf(i,npo2,9),psep+uf(i,1,10),
     + psey-vf(i,1,10),1)

c      Linia de vora diagonal
       lvalp=datan((vf(i,npo2,9)-vf(i,1,10))/
     + ((uf(i,1,10)-uf(i,npo2,9))))
       lv1u=uf(i,npo2,9)-xlowle*0.1*dsin(lvalp)
       lv1v=vf(i,npo2,9)-xlowle*0.1*dcos(lvalp)
       lv2u=uf(i,1,10)-xlowle*0.1*dsin(lvalp)
       lv2v=vf(i,1,10)-xlowle*0.1*dcos(lvalp)
      
c      Intersection of segments with diagonal
c      Point left
       xru(1)=uf(i,npo2,11)
       xru(2)=uf(i,npo2-1,11)
       xrv(1)=vf(i,npo2,11)
       xrv(2)=vf(i,npo2-1,11)
       xsu(1)=lv1u
       xsu(2)=lv2u
       xsv(1)=lv1v
       xsv(2)=lv2v
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       lv3u=xtu
       lv3v=xtv
c      Point right
       xru(1)=uf(i,2,12)
       xru(2)=uf(i,1,12)
       xrv(1)=vf(i,2,12)
       xrv(2)=vf(i,1,12)
       xsu(1)=lv1u
       xsu(2)=lv2u
       xsv(1)=lv1v
       xsv(2)=lv2v
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       lv4u=xtu
       lv4v=xtv

c      Print versions
       call line(psep+lv3u,psey-lv3v,psep+lv4u,psey-lv4v,3)
       call line(psep+lv3u,psey-lv3v,psep+uf(i,npo2,11),
     + psey-vf(i,npo2,11),3)
       call line(psep+lv4u,psey-lv4v,psep+uf(i,1,12),psey-vf(i,1,12),3)
       call line(psep+uf(i,npo2,9),psey-vf(i,npo2,9),
     + psep+uf(i,npo2,9)-xlowle*0.1*dsin(lvalp),
     + psey-vf(i,npo2,9)+xlowle*0.1*dcos(lvalp),3)
       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,10)-xlowle*0.1*dsin(lvalp),
     + psey-vf(i,1,10)+xlowle*0.1*dcos(lvalp),3)
       call line(psep+uf(i,npo2,9),psey-vf(i,npo2,9),
     + psep+uf(i,npo2,11),psey-vf(i,npo2,11),3)
 
c      Laser version
       call line(psep+2520.*xkf+lv3u,psey-lv3v,psep+
     + 2520.*xkf+lv4u,psey-lv4v,3)
       call line(psep+2520.*xkf+lv3u,psey-lv3v,psep+
     + 2520.*xkf+uf(i,npo2,11),
     + psey-vf(i,npo2,11),3)
       call line(psep+2520.*xkf+lv4u,psey-lv4v,psep+
     + 2520.*xkf+uf(i,1,12),psey-vf(i,1,12),3)

c      Print points vents (left)

       xu=uf(i,1,9)
       xv=vf(i,1,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,1,9)-vf(i,2,9))/
     + (uf(i,1,9)-uf(i,2,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
c       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
c       call point(psep+xu+2520.*xkf,-xv+psey,7)

c      Print points vents (right)

       xu=uf(i,1,10)
       xv=vf(i,1,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,1,10)-vf(i,2,10))/
     + (uf(i,1,10)-uf(i,2,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if ! case vent -2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


c      9) Print vents without TE case -3
       if (k26d.eq.1.and.rib(i+1,165).eq.-3.) then
       call extpoints(i,uf,vf,npo2,xupp,xlowte,xlowle,1)
       call dpanelcm3(i,uf,vf,npo2,psep,psey)
       do j=1,npo2-1 ! LASER
       call line(psep+2520.*xkf+uf(i,j,11),psey-vf(i,j,11),
     + psep+2520.*xkf+uf(i,j+1,11),psey-vf(i,j+1,11),3)
       end do
       call line(psep+uf(i,1,9),psey-vf(i,1,9),psep+uf(i,npo2,10),
     + psey-vf(i,npo2,10),1)

c      Linia de vora diagonal
       lvalp=datan((vf(i,npo2,10)-vf(i,1,9))/
     + ((uf(i,npo2,10)-uf(i,1,9))))
       lv1u=uf(i,1,9)+xlowle*0.1*dsin(lvalp)
       lv1v=vf(i,1,9)-xlowle*0.1*dcos(lvalp)
       lv2u=uf(i,npo2,10)+xlowle*0.1*dsin(lvalp)
       lv2v=vf(i,npo2,10)-xlowle*0.1*dcos(lvalp)
     
c      Intersection of segments with diagonal
c      Point left
       xru(1)=uf(i,2,11)
       xru(2)=uf(i,1,11)
       xrv(1)=vf(i,2,11)
       xrv(2)=vf(i,1,11)
       xsu(1)=lv1u
       xsu(2)=lv2u
       xsv(1)=lv1v
       xsv(2)=lv2v
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       lv3u=xtu
       lv3v=xtv
c      Point right
       xru(1)=uf(i,npo2,12)
       xru(2)=uf(i,npo2-1,12)
       xrv(1)=vf(i,npo2,12)
       xrv(2)=vf(i,npo2-1,12)
       xsu(1)=lv1u
       xsu(2)=lv2u
       xsv(1)=lv1v
       xsv(2)=lv2v
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       lv4u=xtu
       lv4v=xtv

c      Print versions
       call line(psep+lv3u,psey-lv3v,psep+lv4u,psey-lv4v,3)
       call line(psep+lv3u,psey-lv3v,psep+uf(i,1,11),
     + psey-vf(i,1,11),3)
       call line(psep+lv4u,psey-lv4v,psep+uf(i,npo2,12),
     + psey-vf(i,npo2,12),3)
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,9)+xlowle*0.1*dsin(lvalp),
     + psey-vf(i,1,9)+xlowle*0.1*dcos(lvalp),3)
       call line(psep+uf(i,npo2,10),psey-vf(i,npo2,10),
     + psep+uf(i,npo2,10)+xlowle*0.1*dsin(lvalp),
     + psey-vf(i,npo2,10)+xlowle*0.1*dcos(lvalp),3)
       call line(psep+uf(i,npo2,10),psey-vf(i,npo2,10),
     + psep+uf(i,npo2,12),psey-vf(i,npo2,12),3)

c      Laser version
       call line(psep+2520.*xkf+lv3u,psey-lv3v,psep+
     + 2520.*xkf+lv4u,psey-lv4v,3)
       call line(psep+2520.*xkf+lv3u,psey-lv3v,psep+
     + 2520.*xkf+uf(i,1,11),psey-vf(i,1,11),3)
       call line(psep+2520.*xkf+lv4u,psey-lv4v,psep+
     + 2520.*xkf+uf(i,npo2,12),psey-vf(i,npo2,12),3)

c      Print points vents (left)

       xu=uf(i,1,9)
       xv=vf(i,1,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,1,9)-vf(i,2,9))/
     + (uf(i,1,9)-uf(i,2,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)

c      Print points vents (right)

       xu=uf(i,1,10)
       xv=vf(i,1,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((vf(i,1,10)-vf(i,2,10))/
     + (uf(i,1,10)-uf(i,2,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
c       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
c       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if ! case vent -3
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc




       end do

c      Laser BOX(1,5)

       do i=iini,nribss-1
       
       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf
    
c      Print panels intrados without vents
       if (k26d.eq.1.and.rib(i+1,165).le.-1) then
       call extpoints(i,ufa,vfa,npo1,xupp,xlowte,xlowle,1)
       call dpanelb1(i,ufa,vfa,npo1,psep,psey)
       end if

c      Print vents
       if (k26d.eq.1.and.rib(i+1,165).eq.-1) then
       call extpoints(i,uf,vf,npo2,xupp,xupple,xlowle,1)
       call dpanelb2(i,uf,vf,npo2,psep,psey)
       end if

       end do

       end if  ! control intrados "ss"


       end if ! n1draw section 8.5

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.6 Draw all panels (with 3D cuts)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k29d.eq.1) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Plotter panels
c      BOX (0,3)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Sign adjustement
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       do i=iini,nribss-1
       is1=1
       is2=1
       is4=1
       if (zinf(i,6,1).lt.0.) then
c       is1=-1
       end if
       if (zinf(i,6,2).lt.0.) then
c       is2=-1
       end if
       if (zinf(i,6,4).lt.0.) then
c       is4=-1
       end if
c       write (*,*) "Signe  ", i,is1,is2,is4
c       write (*,*) "Signe- ", i,is1*-1,-1*is2,-1*is4

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.6.1 Extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Plotter BOX(-1,3)

c      FORCED RECURSE
c      Please REVIEW all xcirc,xdes denitions!!!!
c      Used in subroutine drwvent to call prinfpv
       do i=0,nribss
       csi(i,50)=xcir
       csi(i,51)=xdes
       end do
cccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      REVISAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       zinf(0,6,2)=zinf(1,6,2)
       zinf(0,6,1)=zinf(1,6,1)
       zinf(0,6,4)=zinf(1,6,4)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=iini,nribss-1

       ic2=dint(rib(i+1,165)) ! vent type
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=xyshift*xkf-890.95*xyextra*xkf ! remove 890.95 to set BOX (1,3)

c      REDEFINITION (!) for proper printing
       ng=rib(i+1,169)

       if (i.eq.0) then
       ng=rib(1,169)
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Previ BRUTE FORCE, use for subroutine drwvent
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       npi=1
       npf=np(i,2)
       npo=npf-npi+1

       do j=1,npo
       ufa(i,j,9)=ufe(i,j,9)
       ufa(i,j,10)=ufe(i,j,10)
       ufa(i,j,11)=ufe(i,j,11)
       ufa(i,j,12)=ufe(i,j,12)
       vfa(i,j,9)=vfe(i,j,9)
       vfa(i,j,10)=vfe(i,j,10)
       vfa(i,j,11)=vfe(i,j,11)
       vfa(i,j,12)=vfe(i,j,12)
       end do

c       cs1x=(ufa(i,1,9)+ufa(i,1,10))*0.5 ! Point 1
c       cs1y=(vfa(i,1,9)+vfa(i,1,10))*0.5 ! Point 1

c      IN DOUBT... USE BRUTE FORCE!!!!!!!!!!!!!!!!!!!!!
       csi(i,21)=ufa(i,npo,9)
       csi(i,22)=vfa(i,npo,9)
       csi(i,23)=ufa(i,npo,10)
       csi(i,24)=vfa(i,npo,10)
       csi(i,25)=ufa(i,npo,11)
       csi(i,26)=vfa(i,npo,11)
       csi(i,27)=ufa(i,npo,12)
       csi(i,28)=vfa(i,npo,12)
       
c       alpha1=(datan((vfa(i,1,10)-vfa(i,1,9))/
c     + (ufa(i,1,10)-ufa(i,1,9))))

c       csi(i,29)=alpha1
c       csi(i,30)=xlow
c       csi(i,31)=xlowte
c       csi(i,32)=xlowle
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      End BRUTE FORCE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


cccccccccccccccccccccccccccccccccccccccccccccccccccccc    
c      Draw minirib extrados (copy code from 8.2.6)
cccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (i.ge.0.and.rib(i+1,56).gt.1.and.rib(i+1,56).ne.100
     + .and.atp.ne."ss") then

       xpo1=(u(i,1,9)+u(i,1,10))/2.
       ypo1=(v(i,1,9)+v(i,1,10))/2.
       j=jcve(i+1)
       xpo2=(u(i,j,9)+u(i,j,10))/2.
       ypo2=(v(i,j,9)+v(i,j,10))/2.

c      Avoid division by zero!!!
       if (xpo2-xpo1.ne.0.) then
       alpha=datan((ypo2-ypo1)/(xpo2-xpo1))
       end if
       if (abs(xpo2-xpo1).lt.0.00001) then
       alpha=pi/2.
       end if

       xpo3=xpo1+rib(i+1,60)*dcos(alpha)
       ypo3=ypo1+rib(i+1,60)*dsin(alpha)
       xdesx=xdes*dsin(alpha)
       xdesy=xdes*dcos(alpha)

c      Draw reference points for miniribs in extrados
       call line(psep+xpo1,psey-ypo1,psep+xpo3,psey-ypo3,5)
       call pointg(psep+xpo1-xdesx,psey-ypo1-xdesy,xcir,1)
       call pointg(psep+xpo3-xdesx,psey-ypo3-xdesy,xcir,1)

c      Laser cuting
       xadd=2520.*xkf
       call point(psep+xpo1+xadd,psey-ypo1,1)
       call point(psep+xpo3+xadd,psey-ypo3,1)

       end if
      
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case extrados 0 cuts
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (uppcuts(ng).eq.0) then

c      Extrados panel from TE to LE

       npi=1
       npf=np(i,2)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufe(i,j,9)
       uf(i,j,10)=ufe(i,j,10)
       uf(i,j,11)=ufe(i,j,11)
       uf(i,j,12)=ufe(i,j,12)
       vf(i,j,9)=vfe(i,j,9)
       vf(i,j,10)=vfe(i,j,10)
       vf(i,j,11)=vfe(i,j,11)
       vf(i,j,12)=vfe(i,j,12)
       end do

c      Set panel side lengths part 1
       call llarlr(i,1,1,npo,uf,vf,llarl,llarr)

c      Update vents for perfect matching (BRUTE FORCE)
c      Use vectors auxiliar t
c      !!!!!!!!!!!!!!!!!!!!!!! NO VA NI FA RES ARA!!!!!!!!!!!
       j=1
       uft(i,j,9)=ufe(i,npf,9)
       uft(i,j,10)=ufe(i,npf,10)
       uft(i,j,11)=ufe(i,npf,11)
       uft(i,j,12)=ufe(i,npf,12)
       vft(i,j,9)=vfe(i,npf,9)
       vft(i,j,10)=vfe(i,npf,10)
       vft(i,j,11)=vfe(i,npf,11)
       vft(i,j,12)=vfe(i,npf,12)
       do j=2,np(i,3)
       uft(i,j,9)=ufv(i,j,9)
       uft(i,j,10)=ufv(i,j,10)
       uft(i,j,11)=ufv(i,j,11)
       uft(i,j,12)=ufv(i,j,12)
       vft(i,j,9)=vfv(i,j,9)
       vft(i,j,10)=vfv(i,j,10)
       vft(i,j,11)=vfv(i,j,11)
       vft(i,j,12)=vfv(i,j,12)
       end do

c      Roman marks
       x1=uf(i,1,9)
       y1=vf(i,1,9)
       x2=uf(i,1,10)
       y2=vf(i,1,10)
       y3=1.0d0
       call romanop(i,1,x1,y1,x2,y2,y3,psep,psey,xkf)

c      Print panels extrados without vents
       if (k26d.eq.0.or.rib(i+1,165).le.0) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xuppte,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,3)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,7)
       end if

c      Print equidistant points
       xinil=0.0d0
       xinir=0.0d0
       call xmarksi(i,1,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf)

c      Print panels extrados with vents
       if (k26d.eq.1.and.rib(i+1,165).ge.1) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xuppte,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,2)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,6)

c      Set panel side lengths part 4
       call llarlr(i,1,4,np(i,3),ufv,vfv,llarl,llarr)

c      Print vents
       call drwvent(i,np,uf,vf,ufv,vfv,psep,psey,xupp,xupple,
     + xuppte,xkf,1,ic2,csi)   ! case print
       call drwvent(i,np,uf,vf,ufv,vfv,psep+2520.*xkf,psey,xupp,xupple,
     + xuppte,xkf,2,ic2,csi)   ! case laser
       end if
   
       end if ! Extrados 0 cuts

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case extrados 1 cut
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (uppcuts(ng).eq.1) then
c      Extrados panel from TE to first cut
       npo=iupp(1,3,ng)
       do j=1,npo
       uf(i,j,9)=ufe(i,j,9)
       uf(i,j,10)=ufe(i,j,10)
       uf(i,j,11)=ufe(i,j,11)
       uf(i,j,12)=ufe(i,j,12)
       vf(i,j,9)=vfe(i,j,9)
       vf(i,j,10)=vfe(i,j,10)
       vf(i,j,11)=vfe(i,j,11)
       vf(i,j,12)=vfe(i,j,12)
       end do

c      Roman marks
       x1=uf(i,1,9)
       y1=vf(i,1,9)
       x2=uf(i,1,10)
       y2=vf(i,1,10)
       y3=1.0d0
       call romanop(i,1,x1,y1,x2,y2,y3,psep,psey,xkf)

c      Set panel side lengths part 1
       call llarlr(i,1,1,npo,uf,vf,llarl,llarr)

c      Print equidistant points
       xinil=0.0d0
       xinir=0.0d0
       call xmarksi(i,1,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf)

       call extpoints(i,uf,vf,npo,xupp,xupp,xuppte,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,2)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,6)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,1),1*is1,psep,psey,1,xupp)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,1),1*is1,psep+2520.*xkf,psey,
     + 2,xupp)

c      Extrados panel from cut to LE
       ysaut=-ysautt

       npi=iupp(1,3,ng)
       npf=np(i,2)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufe(i,j+npi-1,9)
       uf(i,j,10)=ufe(i,j+npi-1,10)
       uf(i,j,11)=ufe(i,j+npi-1,11)
       uf(i,j,12)=ufe(i,j+npi-1,12)
       vf(i,j,9)=vfe(i,j+npi-1,9)
       vf(i,j,10)=vfe(i,j+npi-1,10)
       vf(i,j,11)=vfe(i,j+npi-1,11)
       vf(i,j,12)=vfe(i,j+npi-1,12)
       end do

c      Roman marks
       x1=uf(i,1,9)
       y1=vf(i,1,9)
       x2=uf(i,1,10)
       y2=vf(i,1,10)
       y3=1.0d0
c       call romanop(i,x1,-y1,x2,-y2,y3,psep,psey+ysaut,xkf)

c      Set panel side lengths part 2
       call llarlr(i,1,2,npo,uf,vf,llarl,llarr)

c      Print equidistant points
       xinil=xfinl(i,1,1)
       xinir=xfinr(i,1,1)
       call xmarksi(i,1,2,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey+ysaut,xcir,xdes,xkf)

c      Print panels without vents       
       if (k26d.eq.0.or.rib(i+1,165).le.0) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xupp,1)
       call dpanelcc(i,uf,vf,npo,psep,psey+ysaut,4)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey+ysaut,8)
       call arc3p(i,1,uf,vf,zinf(i+1,6,1),-1*is1,psep,psey+ysaut,1,xupp)
       call arc3p(i,1,uf,vf,zinf(i+1,6,1),-1*is1,psep+2520.*xkf,
     + psey+ysaut,2,xupp)



c      CALL ROMANO ARC EXPERIMENTAL
       call romanoparc(i,1,1,uf,vf,zinf(i+1,6,1),-1,psep,psey+ysaut,
     + 1,xkf)



       end if

c      Print panels with vents       
       if (k26d.eq.0.or.rib(i+1,165).ge.1) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xupp,1)
       call dpanelcc(i,uf,vf,npo,psep,psey+ysaut,1)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey+ysaut,5)
       call arc3p(i,1,uf,vf,zinf(i+1,6,1),-1*is1,psep,psey+ysaut,1,xupp)
       call arc3p(i,1,uf,vf,zinf(i+1,6,1),-1*is1,psep+2520.*xkf,
     + psey+ysaut,2,xupp)

c      Set panel side lengths part 4
       call llarlr(i,1,4,np(i,3),ufv,vfv,llarl,llarr)



c      CALL ROMANO ARC EXPERIMENTAL
       call romanoparc(i,1,1,uf,vf,zinf(i+1,6,1),-1,psep,psey+ysaut,
     + 1,xkf)



c      Print vents
       call drwvent(i,np,uf,vf,ufv,vfv,psep,psey+ysaut,xupp,xupple,
     + xuppte,xkf,1,ic2,csi)   ! case print
       call drwvent(i,np,uf,vf,ufv,vfv,psep+2520.*xkf,psey+ysaut,xupp,
     + xupple,xuppte,xkf,2,ic2,csi)   ! case laser
       end if

       end if ! Extrados 1 cut

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case extrados 2 cuts
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (uppcuts(ng).eq.2) then

c      Extrados panel from TE to first cut
       npo=iupp(1,3,ng)
       do j=1,npo
       uf(i,j,9)=ufe(i,j,9)
       uf(i,j,10)=ufe(i,j,10)
       uf(i,j,11)=ufe(i,j,11)
       uf(i,j,12)=ufe(i,j,12)
       vf(i,j,9)=vfe(i,j,9)
       vf(i,j,10)=vfe(i,j,10)
       vf(i,j,11)=vfe(i,j,11)
       vf(i,j,12)=vfe(i,j,12)
       end do

c      Roman marks
       x1=uf(i,1,9)
       y1=vf(i,1,9)
       x2=uf(i,1,10)
       y2=vf(i,1,10)
       y3=1.0d0
       call romanop(i,1,x1,y1,x2,y2,y3,psep,psey,xkf)

c      Set panel side lengths part 1
       call llarlr(i,1,1,npo,uf,vf,llarl,llarr)

c      Print equidistant points
       xinil=0.0d0
       xinir=0.0d0
       call xmarksi(i,1,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf)

       call extpoints(i,uf,vf,npo,xupp,xupp,xuppte,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,2)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,6)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,1),1*is1,psep,psey,1,xupp)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,1),1*is1,psep+2520.*xkf,psey,2,
     + xupp)

c      Extrados panel from first to second cut
       ysaut=-ysautt
      
       npi=iupp(1,3,ng)
       npf=iupp(2,3,ng)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufe(i,j+npi-1,9)
       uf(i,j,10)=ufe(i,j+npi-1,10)
       uf(i,j,11)=ufe(i,j+npi-1,11)
       uf(i,j,12)=ufe(i,j+npi-1,12)
       vf(i,j,9)=vfe(i,j+npi-1,9)
       vf(i,j,10)=vfe(i,j+npi-1,10)
       vf(i,j,11)=vfe(i,j+npi-1,11)
       vf(i,j,12)=vfe(i,j+npi-1,12)
       end do

c      Set panel side lengths part 2
       call llarlr(i,1,2,npo,uf,vf,llarl,llarr)

c      Print equidistant points
       xinil=xfinl(i,1,1)
       xinir=xfinr(i,1,1)
c       write (*,*) "X ",i,xinil,xinir
       call xmarksi(i,1,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey+ysaut,xcir,xdes,xkf)
       call extpoints(i,uf,vf,npo,xupp,xupp,xupp,1)
       call dpanelcc(i,uf,vf,npo,psep,psey+ysaut,1)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey+ysaut,5)

       call arc3p(i,1,uf,vf,zinf(i+1,6,1),-1*is1,psep,psey+ysaut,1,xupp)
       call arc3p(i,1,uf,vf,zinf(i+1,6,1),-1*is1,psep+2520.*xkf,psey+
     + ysaut,2,xupp)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,2),1*is2,psep,psey+ysaut,
     + 1,xupp)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,2),1*is2,psep+2520.*xkf,psey+
     + ysaut,2,xupp)


c      CALL ROMANO ARC EXPERIMENTAL
       call romanoparc(i,1,1,uf,vf,zinf(i+1,6,1),-1,psep,psey+ysaut,
     + 1,xkf)

c      Extrados panel from second cut to LE
       ysaut=-ysautt*2.0d0
      
       npi=iupp(2,3,ng)
       npf=np(i,2)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufe(i,j+npi-1,9)
       uf(i,j,10)=ufe(i,j+npi-1,10)
       uf(i,j,11)=ufe(i,j+npi-1,11)
       uf(i,j,12)=ufe(i,j+npi-1,12)
       vf(i,j,9)=vfe(i,j+npi-1,9)
       vf(i,j,10)=vfe(i,j+npi-1,10)
       vf(i,j,11)=vfe(i,j+npi-1,11)
       vf(i,j,12)=vfe(i,j+npi-1,12)
       end do

c      Set panel side lengths part 3
       call llarlr(i,1,3,npo,uf,vf,llarl,llarr)

c      Print equidistant points
       xinil=xfinl(i,1,2)
       xinir=xfinr(i,1,2)
       call xmarksi(i,1,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey+ysaut,xcir,xdes,xkf)

c      Print panels without vents       
       if (k26d.eq.0.or.rib(i+1,165).le.0) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xupp,1)
       call dpanelcc(i,uf,vf,npo,psep,psey+ysaut,4)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey+ysaut,8)



       call arc3p(i,1,uf,vf,zinf(i+1,6,2),-1*is2,psep,psey+ysaut,1,xupp)
       call arc3p(i,1,uf,vf,zinf(i+1,6,2),-1*is2,psep+2520.*xkf,psey+
     + ysaut,2,xupp)




       end if

c      CALL ROMANO ARC EXPERIMENTAL
       call romanoparc(i,1,1,uf,vf,zinf(i+1,6,2),-1,psep,psey+ysaut,
     + 2,xkf)


c      Print panels with vents       
       if (k26d.eq.0.or.rib(i+1,165).ge.1) then
       call extpoints(i,uf,vf,npo,xupp,xupple,xupp,1)
       call dpanelcc(i,uf,vf,npo,psep,psey+ysaut,1)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey+ysaut,5)
       call arc3p(i,1,uf,vf,zinf(i+1,6,2),-1*is2,psep,psey+ysaut,1,xupp)
       call arc3p(i,1,uf,vf,zinf(i+1,6,2),-1*is2,psep+2520.*xkf,psey+
     + ysaut,2,xupp)



c      CALL ROMANO ARC EXPERIMENTAL
       call romanoparc(i,1,1,uf,vf,zinf(i+1,6,2),-1,psep,psey+ysaut,
     + 2,xkf)



c      Set panel side lengths part 4
       call llarlr(i,1,4,np(i,3),ufv,vfv,llarl,llarr)

c      Print vents
       call drwvent(i,np,uf,vf,ufv,vfv,psep,psey+ysaut,xupp,xupple,
     + xuppte,xkf,1,ic2,csi)   ! case print
       call drwvent(i,np,uf,vf,ufv,vfv,psep+2520.*xkf,psey+ysaut,xupp,
     + xupple,xuppte,xkf,2,ic2,csi)   ! case laser
       end if

       ysaut=-ysautt

       end if ! 2 extrados cuts
 
       end do ! rib i

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      8.6.2 Intrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Plotter BOX(0,3) and BOX (0,5)

       if (atp.ne."ss") then

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1

       ic2=dint(rib(i+1,165)) ! vent type

       psep=1970.*xkf+seppix(i)*1.0d0
       psey=xyshift*xkf-890.95*xyintra*xkf ! remove 890.95 to set BOX (1,3)

c      REDEFINITION (!) for proper printing
       ng=rib(i+1,169)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Previ BRUTE FORCE, use for subroutine drwvent
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       npi=np(i,2)+np(i,3)-1
       npf=np(i,1)
       npo1=npf-npi+1

       do j=1,npo1
       ufa(i,j,9)=ufi(i,j,9)
       ufa(i,j,10)=ufi(i,j,10)
       ufa(i,j,11)=ufi(i,j,11)
       ufa(i,j,12)=ufi(i,j,12)
       vfa(i,j,9)=vfi(i,j,9)
       vfa(i,j,10)=vfi(i,j,10)
       vfa(i,j,11)=vfi(i,j,11)
       vfa(i,j,12)=vfi(i,j,12)
       end do

       cs1x=(ufa(i,1,9)+ufa(i,1,10))*0.5 ! Point 1
       cs1y=(vfa(i,1,9)+vfa(i,1,10))*0.5 ! Point 1

c      IN DOUBT... USE BRUTE FORCE!!!!!!!!!!!!!!!!!!!!!
       csi(i,1)=ufa(i,1,9)
       csi(i,2)=vfa(i,1,9)
       csi(i,3)=ufa(i,1,10)
       csi(i,4)=vfa(i,1,10)
       csi(i,5)=ufa(i,1,11)
       csi(i,6)=vfa(i,1,11)
       csi(i,7)=ufa(i,1,12)
       csi(i,8)=vfa(i,1,12)
       
       alpha1=(datan((vfa(i,1,10)-vfa(i,1,9))/
     + (ufa(i,1,10)-ufa(i,1,9))))

       csi(i,9)=alpha1
       csi(i,10)=xlow
       csi(i,11)=xlowte
       csi(i,12)=xlowle
       csi(i,13)=xupple

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      End BRUTE FORCE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


cccccccccccccccccccccccccccccccccccccccccccccccccccccc    
c      Draw minirib intrados (copied from 8.4.6)
c      and adding "ysaut"
cccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (lowcuts(ng).eq.1) then
       ysaut=-ysautt
       else
       ysaut=0.0d0
       end if

       if (i.ge.0.and.rib(i+1,56).gt.1.and.rib(i+1,56).ne.100.and
     + .atp.ne."ss") then

       xpo1=(u(i,np(i,1),9)+u(i,np(i,1),10))/2.
       ypo1=(v(i,np(i,1),9)+v(i,np(i,1),10))/2.
       j=jcvi(i+1)
       xpo2=(u(i,j,9)+u(i,j,10))/2.
       ypo2=(v(i,j,9)+v(i,j,10))/2.

c      Evita divisions per zero!!!
       if (xpo2-xpo1.ne.0.) then
       alpha=datan((ypo2-ypo1)/(xpo2-xpo1))
       end if
       if (abs(xpo2-xpo1).lt.0.00001) then
       alpha=pi/2.
       end if

       xpo3=xpo1-rib(i+1,61)*dcos(alpha)
       ypo3=ypo1-rib(i+1,61)*dsin(alpha)
       xdesx=xdes*dsin(alpha)
       xdesy=xdes*dcos(alpha)

c      Draw reference points for miniribs in intrados
       call line(psep+xpo1,psey-ypo1+ysaut,psep+xpo3,psey-ypo3+ysaut,5)
       call pointg(psep+xpo1-xdesx,psey-ypo1-xdesy+ysaut,xcir,1)
       call pointg(psep+xpo3-xdesx,psey-ypo3-xdesy+ysaut,xcir,1)

c      Laser cuting
       xadd=2520.*xkf
       call point(psep+xpo1+xadd,psey-ypo1+ysaut,1)
       call point(psep+xpo3+xadd,psey-ypo3+ysaut,1)

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case intrados 0 cuts
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (lowcuts(ng).eq.0) then

c      Intrados panel from LE to TE

       npi=np(i,2)+np(i,3)-1
       npf=np(i,1)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufi(i,j,9)
       uf(i,j,10)=ufi(i,j,10)
       uf(i,j,11)=ufi(i,j,11)
       uf(i,j,12)=ufi(i,j,12)
       vf(i,j,9)=vfi(i,j,9)
       vf(i,j,10)=vfi(i,j,10)
       vf(i,j,11)=vfi(i,j,11)
       vf(i,j,12)=vfi(i,j,12)
       end do

c      Set panel side lengths part 1
       call llarlr(i,2,1,npo,uf,vf,llarl,llarr)

c      Roman marks
       x1=uf(i,npo,10)
       y1=vf(i,npo,10)
       x2=uf(i,npo,9)
       y2=vf(i,npo,9)
       y3=1.0d0
       call romanop(i,-1,x1,-y1,x2,-y2,y3,psep,psey,xkf)

c      Print equidistant points
       xinil=0.0d0
       xinir=0.0d0
       call xmarksi(i,2,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf)

c      Print intrados marks (experimental)
       xinil=0.0d0
       xinir=0.0d0
       call iam(i,2,1,np,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf,
     + typm1,typm2,typm3,typm4,typm5,typm6,xrib)


c      Print intrados without vents
       if (k26d.eq.0.or.rib(i+1,165).ge.0) then
       call extpoints(i,uf,vf,npo,xlow,xlowte,xlowle,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,3)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,7)
       end if

c      Print intrados with vents
       if (k26d.eq.1.and.rib(i+1,165).lt.0) then
       call extpoints(i,uf,vf,npo,xlow,xlowte,xlowle,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,4)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,8)

c      Print vents

c      Print intrados marks (experimental)
       xinil=llarl(i,2,1)
       xinir=llarr(i,2,1)
       call iam(i,2,4,np,np(i,3),ufv,vfv,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf,
     + typm1,typm2,typm3,typm4,typm5,typm6,xrib)

c      Set panel side lengths part 4
       call llarlr(i,2,4,np(i,3),ufv,vfv,llarl,llarr)

       call drwvent(i,np,uf,vf,ufv,vfv,psep,psey,xlow,xlowle,
     + xlowte,xkf,1,ic2,csi)   ! case print
       call drwvent(i,np,uf,vf,ufv,vfv,psep+2520.*xkf,psey,xlow,xlowle,
     + xlowte,xkf,2,ic2,csi)   ! case laser

       end if

c      Think why???????????????????
c      Si no els punts queden desplaçats a l'extrados!!!
       ysaut=-ysautt

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case intrados 1 cut
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (lowcuts(ng).eq.1) then


c      Intrados panel from first cut to TE
       ysaut=-ysautt

       npi=ilow(1,3,ng)-(np(i,2)+np(i,3)-2)
       npf=np(i,1)-(np(i,2)+np(i,3)-2)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufi(i,j+npi-1,9)
       uf(i,j,10)=ufi(i,j+npi-1,10)
       uf(i,j,11)=ufi(i,j+npi-1,11)
       uf(i,j,12)=ufi(i,j+npi-1,12)
       vf(i,j,9)=vfi(i,j+npi-1,9)
       vf(i,j,10)=vfi(i,j+npi-1,10)
       vf(i,j,11)=vfi(i,j+npi-1,11)
       vf(i,j,12)=vfi(i,j+npi-1,12)
       end do

c      Set panel side lengths part 1
       call llarlr(i,2,1,npo,uf,vf,llarl,llarr)

c      Roman marks
       x1=uf(i,npo,10)
       y1=vf(i,npo,10)
       x2=uf(i,npo,9)
       y2=vf(i,npo,9)
       y3=1.0d0
       call romanop(i,-1,x1,-y1,x2,-y2,y3,psep,psey+ysaut,xkf)

c      Print equidistant points
       xinil=0.0d0
       xinir=0.0d0
       call xmarksi(i,2,1,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey+ysaut,xcir,xdes,xkf)



c      Print intrados marks (experimental)
       xinil=0.0d0
       xinir=0.0d0
       call iam(i,2,1,np,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey+ysaut,xcir,xdes,xkf,
     + typm1,typm2,typm3,typm4,typm5,typm6,xrib)



c       if (k26d.eq.0.or.rib(i+1,165).ge.0) then
       call extpoints(i,uf,vf,npo,xlow,xlowte,xlow,1)
       call dpanelcc(i,uf,vf,npo,psep,psey+ysaut,4)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey+ysaut,8)
       call arc3p(i,1,uf,vf,zinf(i+1,6,4),-1*is4,psep,psey+ysaut,1,xlow)
       call arc3p(i,1,uf,vf,zinf(i+1,6,4),-1*is4,psep+2520.*xkf,psey+
     + ysaut,2,xlow)
c       end if

c      Extrados panel from LE to first cut
       npi=np(i,2)+np(i,3)-1
       npf=ilow(1,3,ng)
       npo=npf-npi+1

       do j=1,npo
       uf(i,j,9)=ufi(i,j,9)
       uf(i,j,10)=ufi(i,j,10)
       uf(i,j,11)=ufi(i,j,11)
       uf(i,j,12)=ufi(i,j,12)
       vf(i,j,9)=vfi(i,j,9)
       vf(i,j,10)=vfi(i,j,10)
       vf(i,j,11)=vfi(i,j,11)
       vf(i,j,12)=vfi(i,j,12)
       end do

c      Set panel side lengths part 2
       call llarlr(i,2,2,npo,uf,vf,llarl,llarr)

c      Print equidistant points
       xinil=xfinl(i,2,1)
       xinir=xfinr(i,2,1)
       call xmarksi(i,2,2,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf)

c      Print intrados marks (experimental)
       xinil=llarl(i,2,1)
       xinir=llarr(i,2,1)
       call iam(i,2,2,np,npo,uf,vf,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf,
     + typm1,typm2,typm3,typm4,typm5,typm6,xrib)


c      Print without vents
       if (k26d.eq.0.or.rib(i+1,165).ge.0) then
       call extpoints(i,uf,vf,npo,xlow,xlow,xlowle,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,2)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,6)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,4),1*is4,psep,psey,1,xlow)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,4),1*is4,psep+2520.*xkf,psey,2,
     + xlow)
       end if

c      CALL ROMANO ARC EXPERIMENTAL
       call romanoparc(i,-1,npo,uf,vf,zinf(i+1,6,4),1,psep,psey,
     + 1,xkf)

c      Print with vents
       if (k26d.eq.1.and.rib(i+1,165).lt.0) then
       call extpoints(i,uf,vf,npo,xlow,xlow,xlowle,1)
       call dpanelcc(i,uf,vf,npo,psep,psey,1)
       call dpanelcc(i,uf,vf,npo,psep+2520.*xkf,psey,5)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,4),1*is4,psep,psey,1,xlow)
       call arc3p(i,npo,uf,vf,zinf(i+1,6,4),1*is4,psep+2520.*xkf,psey,2,
     + xlow)

c      Set panel side lengths part 4
       call llarlr(i,2,4,np(i,3),ufv,vfv,llarl,llarr)

c      Print vents
       call drwvent(i,np,uf,vf,ufv,vfv,psep,psey,xlow,xlowle,
     + xlowte,xkf,1,ic2,csi)   ! case print
       call drwvent(i,np,uf,vf,ufv,vfv,psep+2520.*xkf,psey,xlow,xlowle,
     + xlowte,xkf,2,ic2,csi)   ! case laser

c      Print intrados marks (experimental)
       xinil=llarl(i,2,1)+llarl(i,2,2)
       xinir=llarr(i,2,1)+llarr(i,2,2)
       call iam(i,2,4,np,np(i,3),ufv,vfv,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf,
     + typm1,typm2,typm3,typm4,typm5,typm6,xrib)

       end if








       end if ! lowcuts=1

       end do ! i

       end if ! "ss"

       end if ! k29d=1

c      Print llarl and llarl. Use in section 11.4 for print equidistant marks
c       write (*,*) "EXTRADOS"
c       do i=1,nribss
c       write (*,*) "part 1 ",i,llarl(i,1,1),llarr(i,1,1)
c       write (*,*) "part 2 ",i,llarl(i,1,2),llarr(i,1,2)
c       write (*,*) "part 3 ",i,llarl(i,1,3),llarr(i,1,3)
c       end do
c       write (*,*) "INTRADOS"
c       do i=1,nribss
c       write (*,*) "part 1 ",i,llarl(i,2,1),llarr(i,2,1)
c       write (*,*) "part 2 ",i,llarl(i,2,2),llarr(i,2,2)
c       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc       
c      9. SINGULAR RIB POINTS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       
c        write (*,*) "pi 9. =",pi

c      9.1 Compute anchor points

       do i=0,nribss         ! Itera in ribs

       do k=1,6 ! Itera in A,B,C,D,E,F

       do j=1,np(i,1)-1

c       if(u(i,j,3).le.rib(i,5)*rib(i,15+k)/100.and.u(i,j+1,3)
c     + .ge.rib(i,5)*rib(i,15+k)/100.and.j.ge.np(i,2)) then

c      Please, don't compare directly two double precision numbers !!!

       if(real(u(i,j,3)).le.real(rib(i,5)*rib(i,15+k)/100).and.
     + real(u(i,j+1,3)).ge.real(rib(i,5)*rib(i,15+k)/100).and.
     + j.ge.np(i,2)) then

       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xn=v(i,j,3)-xm*u(i,j,3)
       u(i,k,6)=rib(i,5)*rib(i,15+k)/100.0d0
       v(i,k,6)=xm*u(i,k,6)+xn

c       anccount(i,k)=j  ! anchor "j" detection in i rib

c       write (*,*) "Anchor control i,k,j = ",i,k,anccont(i,k)


       end if

       end do

       end do

       end do

c      9.1+ Detecta punts j a extrados propers a ancoratges

       
c        write (*,*) "pi 9.1+ =",pi

       do i=0,nribss         ! Itera in ribs

       do k=1,6 ! Itera in A,B,C,D,E,F

       do j=np(i,2),2,-1

       if(u(i,j,3).le.rib(i,5)*rib(i,15+k)/100..and.u(i,j-1,3)
     + .ge.rib(i,5)*rib(i,15+k)/100..and.j.le.np(i,2)) then

       anccont(i,k)=j

       end if

       end do

       end do

       end do


c      9.1++ Detecta punts j a intrados propers a ancoratges
c      Atenció casos ds i ss (ESTUDIAR)


       do i=0,nribss         ! Itera in ribs

       do k=1,6 ! Itera in A,B,C,D,E,F

       do j=1,np(i,1)-1

       if(u(i,j,3).le.rib(i,5)*rib(i,15+k)/100..and.u(i,j+1,3)
     + .ge.rib(i,5)*rib(i,15+k)/100..and.u(i,j,3).le.u(i,j+1,3)) then

       ancconti(i,k)=j

       end if

       end do

       end do

       end do
       

c      9.2 Compute inlets points

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ENTRE 9.1+ i 9.2 es perd el valor de pi INEXPLICABLE
       pi=4.0d0*datan(1.0d0)   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c        write (*,*) "pi 9.2. =",pi

       do i=1,nribss         ! Itera in ribs

       do k=11,12 ! air in out

       do j=1,np(i,1)

       if(u(i,j,3).le.rib(i,5)*rib(i,k)/100.0d0.and.u(i,j+1,3)
     + .ge.rib(i,5)*rib(i,k)/100.0d0.and.j.ge.np(i,2)-1) then

       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xn=v(i,j,3)-xm*u(i,j,3)
       u(i,k-4,6)=rib(i,5)*rib(i,k)/100.0d0
       v(i,k-4,6)=xm*u(i,k,6)+xn

       end if

       end do

       end do

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.3 Draw anchor points in airfoils
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       
c        write (*,*) "pi 9.3 =",pi

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

       kx=0
       ky=0
       kyy=0

       do i=1,nribss

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky)

       do j=1,rib(i,15)

c      9.3.1 Anchor points
       call line(sepx+u(i,j,6),-v(i,j,6)+sepy,sepx+u(i,j,6),
     + -0.+sepy,7)

c      9.3.2 Anchor points in mesa de corte

c      Case 1: classic 3 orange points
       if (typetab.eq.1) then
       call point(2530.*xkf+sepx+u(i,j,6),-v(i,j,6)+
     + sepy+typm6(5),30)
       call point(2530.*xkf+sepx+u(i,j,6),-v(i,j,6)+
     + sepy-1.*typm5(5)+typm6(5),30)
       call point(2530.*xkf+sepx+u(i,j,6),-v(i,j,6)+
     + sepy-2.*typm5(5)+typm6(5),30)
       end if

c      Case 2: rotated 3 orange points
       if (typetab.eq.2) then
c      Define "ji" of the anchor in the other "j" count 1,2,3,4,5
       ji=ancconti(i,j)  ! Compte, aqui "j" és "k"
       alpha1=datan((v(i,ji-1,3)-v(i,ji+1,3))/(u(i,ji-1,3)-u(i,ji+1,3)))
c      Amb desplaçament typm6(5) xdes com a intra
       xpeq=typm6(5)*dsin(alpha1)
       ypeq=typm6(5)*dcos(alpha1)
       call point(2530.*xkf+sepx+u(i,j,6)+xpeq,-v(i,j,6)+
     + sepy+ypeq,30)
       call point(2530.*xkf+sepx+u(i,j,6)+
     + (typm6(5)-1.*typm5(5))*dsin(alpha1),-v(i,j,6)+
     + sepy+(typm6(5)-1.*typm5(5))*dcos(alpha1),30)
       call point(2530.*xkf+sepx+u(i,j,6)+
     + (typm6(5)-2.*typm5(5))*dsin(alpha1),-v(i,j,6)+
     + sepy+(typm6(5)-2.*typm5(5))*dcos(alpha1),30)
       end if

c      Case 3: triangle 2 mm
c      REVISAR CAS ss !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       if (typetab.eq.3) then
c      Define "ji" of the anchor in the other "j" count 1,2,3,4,5
       ji=ancconti(i,j)  ! Compte, aqui "j" és "k"
       alpha1=datan((v(i,ji-1,3)-v(i,ji+1,3))/(u(i,ji-1,3)-u(i,ji+1,3)))
c      Amb desplaçament typm6(5) xdes com a intra
       xpeq=typm6(5)*dsin(alpha1)
       ypeq=typm6(5)*dcos(alpha1)
       call mtriangle(2530.*xkf+sepx+u(i,j,6)+xpeq,-v(i,j,6)+sepy+ypeq,
     + typm5(5),alpha1,30)
       end if

       end do

c      9.4 Marca entrada aire a les costelles

c      ini
       j=np(i,2)
       alpha1=pi+datan((v(i,j,3)-v(i,j-1,3))/(u(i,j,3)-u(i,j-1,3)))
       call line(sepx+u(i,j,3),-v(i,j,3)+sepy,sepx+u(i,j,3)-
     + 4.*dsin(alpha1),-v(i,j,3)-4.*dcos(alpha1)+sepy,1)

       x1=2530.*xkf+sepx+u(i,j,3)+0.1*typm6(4)*dsin(alpha1)
       y1=-v(i,j,3)+sepy+0.1*typm6(4)*dcos(alpha1)
       x2=2530.*xkf+sepx+u(i,j,3)-0.1*(typm5(4)-typm6(4))*dsin(alpha1)
       y2=-0.1*(typm5(4)-typm6(4))*dcos(alpha1)-v(i,j,3)+sepy

       if (typevent.eq.1) then
c      Double point
       call point(x1,y1,3)
       call point(x2,y2,3)
       end if

       if (typevent.eq.2) then
c      Segment
       call linevent(x1,y1,x2,y2,3)
       end if

       if (typevent.eq.3) then
c      Segment 101
       call segment101(x1,y1,x2,y2,3)
       end if

c      fi
       j=np(i,2)+np(i,3)-1
       alpha1=pi+datan((v(i,j+1,3)-v(i,j-1,3))/(u(i,j+1,3)-u(i,j-1,3)))
       call line(sepx+u(i,j,3),-v(i,j,3)+sepy,sepx+u(i,j,3)-
     + 4.*dsin(alpha1),-v(i,j,3)-4.*dcos(alpha1)+sepy,1)

       x1=2530.*xkf+sepx+u(i,j,3)+0.1*typm6(4)*dsin(alpha1)
       y1=-v(i,j,3)+sepy+0.1*typm6(4)*dcos(alpha1)
       x2=2530.*xkf+sepx+u(i,j,3)-0.1*(typm5(4)-typm6(4))*dsin(alpha1)
       y2=-0.1*(typm5(4)-typm6(4))*dcos(alpha1)-v(i,j,3)+sepy

       if (typevent.eq.1) then
c      Double point
       call point(x1,y1,3)
       call point(x2,y2,3)
       end if

       if (typevent.eq.2) then
c      Segment
       call linevent(x1,y1,x2,y2,3)
       end if

       if (typevent.eq.3) then
c      Segment 101
       call segment101(x1,y1,x2,y2,3)
       end if

c     9.5 Aditional points (junquillos)

       if (narp.ne.0) then ! Only if narp.eq.0 k17d
       do l=1,narp
       call point(2530.*xkf+sepx+xarp(l)*rib(i,5)/100.,
     + -yarp(l)*rib(i,5)/100.+sepy,5)
c       call point(2530.*xkf+sepx+10.8*rib(i,5)/100.,
c     + +5.53*rib(i,5)/100.+sepy,5)
       end do
       end if

       kx=int((float(i)/6.))
       ky=i-kx*6
       kyy=kyy+1

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9 MIDDLE PANEL UNLOADED RIBS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,6)
c      1260.*4.*xkf
       
       sepxx=1260.*4.*xkf+700.*xkf
       sepyy=100.*xkf
c      sepyy=100

       kx=0
       ky=0
       kyy=0

       do i=1,nribss

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*1.0*float(ky)

c      Detect complete unloaded rib
       if (rib(i,56).eq.100.and.atp.ne."ss") then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.1 Define intermediate airfoil beetwen i-1 and i
c      Interpole chord and thickness
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do j=1,np(i,1)
       u(i,j,43)=u(i-1,j,2)*0.5*(rib(i,5)+rib(i-1,5))/100.
       v(i,j,43)=v(i-1,j,2)*(0.5*(rib(i,149)+rib(i-1,149))/
     + rib(i-1,149))*0.5*(rib(i,5)+rib(i-1,5))/100.
       end do

c      Calculate midline in panel

       do j=1,np(i,1)
       u(i,j,44)=(u(i-1,j,9)+u(i-1,j,10))/2.
       v(i,j,44)=(v(i-1,j,9)+v(i-1,j,10))/2.

c       u(i,j,44)=u(i-1,j,9)
c       v(i,j,44)=v(i-1,j,9)

       end do

c      Compare lengths extra in rib (150) and panels (153)
       
       rib(i,150)=0.
       rib(i,153)=0.
       do j=1,np(i,2)-1    
       rib(i,150)=rib(i,150)+dsqrt((u(i,j,43)-u(i,j+1,43))**2.+
     + (v(i,j,43)-v(i,j+1,43))**2.)
       rib(i,153)=rib(i,153)+dsqrt((u(i,j,44)-u(i,j+1,44))**2.+
     + (v(i,j,44)-v(i,j+1,44))**2.)
       end do
       rib(i,156)=rib(i,150)-rib(i,153)

c      Compare lengths vent in rib (151) and panels (154)
c      9-10 Vent panel still not defined (!)
       
       rib(i,151)=0.
       rib(i,154)=0.
       do j=np(i,2),np(i,2)+np(i,3)-2
       rib(i,151)=rib(i,151)+dsqrt((u(i,j,43)-u(i,j+1,43))**2.+
     + (v(i,j,43)-v(i,j+1,43))**2.)
       rib(i,154)=rib(i,154)+dsqrt((u(i,j,44)-u(i,j+1,44))**2.+
     + (v(i,j,44)-v(i,j+1,44))**2.)
       end do
       rib(i,157)=rib(i,151)-rib(i,154)
       j1=np(i,2)
       j2=np(i,2)+np(i,3)-1
c       rib(i,151)=dsqrt((u(i,j1,44)-u(i,j2,44))**2.+
c     + (v(i,j1,44)-v(i,j2,44))**2.)

c      Compare lengths intra in rib (152) and panels (155)
       
       rib(i,152)=0.
       rib(i,155)=0.
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       rib(i,152)=rib(i,152)+dsqrt((u(i,j,43)-u(i,j+1,43))**2.+
     + (v(i,j,43)-v(i,j+1,43))**2.)
       rib(i,155)=rib(i,155)+dsqrt((u(i,j,44)-u(i,j+1,44))**2.+
     + (v(i,j,44)-v(i,j+1,44))**2.)
       end do
       rib(i,158)=rib(i,152)-rib(i,155)

c       write (*,*) i,rib(i,150),rib(i,153),rib(i,156)
c       write (*,*) i,rib(i,151),rib(i,154),rib(i,157)
c       write (*,*) i,rib(i,152),rib(i,155),rib(i,158)

c      Reformat rib extrados

       do j=1,np(i,2)-1  ! all extrados

       xdv=(v(i,j+1,43)-v(i,j,43))
       xdu=(u(i,j+1,43)-u(i,j,43))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))
       else
       anglee(j)=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i,j,43)-v(i,j+1,43))**2.+
     + (u(i,j,43)-u(i,j+1,43))**2.)

       end do

c      Define reformated airfoil extrados

       distk=rib(i,153)/rib(i,150)
       do j=1,np(i,2)-1
       u(i,j+1,45)=u(i,j,43)+siu(j)*distk*distee(j)*dcos(anglee(j))
       v(i,j+1,45)=v(i,j,43)+siv(j)*distk*distee(j)*dsin(anglee(j))
       u(i,j+1,43)=u(i,j+1,45)
       v(i,j+1,43)=v(i,j+1,45)
       end do

c      Verify reformated airfoil extrados

       rib(i,150)=0.
       do j=1,np(i,2)-1
       rib(i,150)=rib(i,150)+dsqrt((u(i,j,43)-u(i,j+1,43))**2.+
     + (v(i,j,43)-v(i,j+1,43))**2.)
       end do
c       write (*,*) "RE ",i,rib(i,150),rib(i,153),rib(i,150)-rib(i,153)


c      Reformat rib intrados

       do j=np(i,1),np(i,2)+np(i,3),-1  ! all intrados

       xdv=(v(i,j,43)-v(i,j-1,43))
       xdu=(u(i,j,43)-u(i,j-1,43))
       if (xdu.ne.0.) then
       anglee(j)=abs(datan(xdv/xdu))
       else
       anglee(j)=2.*datan(1.0d0)
       end if

c       write (*,*) "ANGLE ",i,j,anglee(j)

       if (xdu.ge.0.and.xdv.ge.0) then ! case 1-I
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 1-II
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 1-III
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 1-IV
       siu(j)=-1.
       siv(j)=-1.
       end if

       distee(j)=dsqrt((v(i,j,43)-v(i,j-1,43))**2.+
     + (u(i,j,43)-u(i,j-1,43))**2.)

       end do

c      Define reformated airfoil intrados

       distk=rib(i,155)/rib(i,152)
       do j=np(i,1),np(i,2)+np(i,3),-1        
       u(i,j-1,45)=u(i,j,43)-siu(j)*distk*distee(j)*dcos(anglee(j))
       v(i,j-1,45)=v(i,j,43)-siv(j)*distk*distee(j)*dsin(anglee(j))
       u(i,j-1,43)=u(i,j-1,45)
       v(i,j-1,43)=v(i,j-1,45)
       end do

c      Verify reformated airfoil intrados

       rib(i,152)=0.
       do j=np(i,1),np(i,2)+np(i,3),-1         
       rib(i,152)=rib(i,152)+dsqrt((u(i,j,43)-u(i,j-1,43))**2.+
     + (v(i,j,43)-v(i,j-1,43))**2.)
       end do
c       write (*,*) "RI ",i,rib(i,152),rib(i,155),rib(i,152)-rib(i,155)

c      Reformat vent ds (simplified method)

       if (atp.eq."ds") then

       if (np(i,3).eq.3) then ! interpolate only 1 point
       j=np(i,2)+1
       u(i,j,43)=(u(i,j-1,43)+u(i,j+1,43))*0.5
       v(i,j,43)=(v(i,j-1,43)+v(i,j+1,43))*0.5
       end if

       if (np(i,3).ge.4) then ! interpolate only 2 point
       j=np(i,2)+1
       u(i,j,43)=(2.*u(i,j-1,43)+1.*u(i,j+2,43))/3.
       v(i,j,43)=(2.*v(i,j-1,43)+1.*v(i,j+2,43))/3.
       j=np(i,2)+2
       u(i,j,43)=(1.*u(i,j-2,43)+2.*u(i,j+1,43))/3.
       v(i,j,43)=(1.*v(i,j-2,43)+2.*v(i,j+1,43))/3.
       end if

       end if

c      Reformat vent pc (lineal vent)

       if (atp.eq."pc") then

       xdu=(u(i,np(i,2)+np(i,3)-1,43)-u(i,np(i,2),43))/(np(i,3)-1)
       xdv=(v(i,np(i,2)+np(i,3)-1,43)-v(i,np(i,2),43))/(np(i,3)-1)
       do j=np(i,2),np(i,2)+np(i,3)-2
       u(i,j+1,43)=u(i,j,43)+xdu
       v(i,j+1,43)=v(i,j,43)+xdv
       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.2 Compute external cut edges in airfoils (i,j,46)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xcos=xrib/10. ! rib sewing allowance mm to cm
      
       do j=2,np(i,1)-1

c      Amplification factor
       xcosk=1.0

c      Fer mitja entre j-1 i j+1
       alpha1=(datan((v(i,j+1,43)-v(i,j,43))/((u(i,j+1,43)-u(i,j,43)))))
       alpha2=(datan((v(i,j,43)-v(i,j-1,43))/((u(i,j,43)-u(i,j-1,43)))))

       alpha=0.5*(alpha1+alpha2)

c      Alpha correction in sawtooht mono-surface airfoils
c      Dóna la volta a la vora superior

       if (alpha1.lt.0.and.alpha2.gt.0.and.j.ge.np(i,2)) then
       alpha=alpha+pi
       end if

       u(i,j,46)=u(i,j,43)-xcos*xcosk*dsin(alpha)

       if(v(i,j,43).ge.0.) then
       v(i,j,46)=v(i,j,43)+xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,43).lt.0.) then
       u(i,j,46)=u(i,j,43)+xcos*xcosk*dsin(alpha)
       v(i,j,46)=v(i,j,43)-xcos*xcosk*dcos(alpha)
       end if

       if(u(i,j,3).eq.0) then
       u(i,j,46)=u(i,j,43)-xcos*xcosk
       v(i,j,46)=v(i,j,43)
       end if

       end do

       j=1

       alpha=(datan((v(i,j+1,43)-v(i,j,43))/((u(i,j+1,43)-u(i,j,43)))))

       u(i,j,46)=u(i,j,43)-xcos*xcosk*dsin(alpha)

       if(v(i,j,43).ge.0.) then
       v(i,j,46)=v(i,j,43)+xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,43).lt.0.) then
       u(i,j,46)=u(i,j,43)+xcos*xcosk*dsin(alpha)
       v(i,j,46)=v(i,j,43)-xcos*xcosk*dcos(alpha)

       end if

       j=np(i,1)

       alpha=(datan((v(i,j,43)-v(i,j-1,43))/((u(i,j,43)-u(i,j-1,43)))))

       u(i,j,46)=u(i,j,43)-xcos*xcosk*dsin(alpha)

       if(v(i,j,43).ge.0.) then
       v(i,j,46)=v(i,j,43)+xcos*xcosk*dcos(alpha)
       end if

       if(v(i,j,43).le.0.) then
       u(i,j,46)=u(i,j,43)+xcos*xcosk*dsin(alpha)
       v(i,j,46)=v(i,j,43)-xcos*xcosk*dcos(alpha)
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.3 Print unloaded ribs, internal line (i,j,43)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       Now not used

c       do j=1,np(i,2)-1
c       call line(sepx+u(i,j,43),-v(i,j,43)+sepy-sepriy*0.5,
c     + sepx+u(i,j+1,43),-v(i,j+1,43)+sepy-sepriy*0.5,1)
c       end do
c       do j=np(i,2),np(i,2)+np(i,3)-2
c       call line(sepx+u(i,j,43),-v(i,j,43)+sepy-sepriy*0.5,
c     + sepx+u(i,j+1,43),-v(i,j+1,43)+sepy-sepriy*0.5,2)
c       end do
c       do j=np(i,2)+np(i,3)-1,np(i,1)-1
c       call line(sepx+u(i,j,43),-v(i,j,43)+sepy-sepriy*0.5,
c     + sepx+u(i,j+1,43),-v(i,j+1,43)+sepy-sepriy*0.5,3)
c       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.4 Print unloaded ribs, external line (i,j,46)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do j=1,np(i,2)-1
       call line(sepx+u(i,j,46),-v(i,j,46)+sepy-sepriy*0.5,
     + sepx+u(i,j+1,46),-v(i,j+1,46)+sepy-sepriy*0.5,1)
       end do
       do j=np(i,2),np(i,2)+np(i,3)-2
       call line(sepx+u(i,j,46),-v(i,j,46)+sepy-sepriy*0.5,
     + sepx+u(i,j+1,46),-v(i,j+1,46)+sepy-sepriy*0.5,2)
       end do
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       call line(sepx+u(i,j,46),-v(i,j,46)+sepy-sepriy*0.5,
     + sepx+u(i,j+1,46),-v(i,j+1,46)+sepy-sepriy*0.5,1)
       end do

       j=1
       call line(sepx+u(i,j,46),-v(i,j,46)+sepy-sepriy*0.5,
     + sepx+u(i,j,43),-v(i,j,43)+sepy-sepriy*0.5,1)
       j=np(i,1)
       call line(sepx+u(i,j,46),-v(i,j,46)+sepy-sepriy*0.5,
     + sepx+u(i,j,43),-v(i,j,43)+sepy-sepriy*0.5,1)
      
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.5 Draw romano and itxt mark in rib
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc     
       j=1
       x1=sepx+u(i,j,43)
       y1=-v(i,j,43)+sepy-sepriy*0.5
       call romano(i,x1-20.,y1,0.0d0,typm6(9)*0.1,7)
       call itxt(x1,y1,5.0d0,0.0d0,i,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.6 Draw vents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      ini
       j=np(i,2)

       alpha1=datan((v(i,j,43)-v(i,j-1,43))/(u(i,j,43)-u(i,j-1,43)))
      
       call point(sepx+u(i,j,43)+xdes*dsin(alpha1),
     + -v(i,j,43)+sepy-sepriy*0.5+xdes*dcos(alpha1),3)
       call point(sepx+u(i,j,43)-1.8*dsin(alpha1),
     + -1.8*dcos(alpha1)-v(i,j,43)+sepy-sepriy*0.5,3)

c      fi
       j=np(i,2)+np(i,3)-1

       alpha1=datan((v(i,j+1,43)-v(i,j-1,43))/(u(i,j+1,43)-u(i,j-1,43)))
       
       call point(sepx+u(i,j,43)+xdes*dsin(alpha1),
     + -v(i,j,43)+sepy-sepriy*0.5+xdes*dcos(alpha1),3)
       call point(sepx+u(i,j,43)-2.*dsin(alpha1),
     + -2*dcos(alpha1)-v(i,j,43)+sepy-sepriy*0.5,3)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.7 Marks extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,60  ! Up to 60 marks

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       do j=1,np(i,2)-1

       xprev=rib(i,41)

       rib(i,41)=rib(i,41)+sqrt((u(i,j,43)-u(i,j+1,43))**2.+((v(i,j,43)
     + -v(i,j+1,43))**2.))

       xpost=rib(i,41)

       if(xmk.lt.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,43)-u(i,j+1,43))**2.+((v(i,j,43)
     + -v(i,j+1,43))**2.))

       dist1=xmk-xprev

       xu=u(i,j,43)+(u(i,j+1,43)-u(i,j,43))*(dist1/dist)
       xv=v(i,j,43)+(v(i,j+1,43)-v(i,j,43))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=(datan((v(i,j+1,43)-v(i,j,43))/(u(i,j+1,43)-u(i,j,43))))
       if (xv.lt.0.) then
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       end if
       if (xv.ge.0.) then
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       end if

c      Dibuixa punt a les costelles

       call point(sepx+xu,sepy-sepriy*0.5-xv,7)
       
       end if 

       end do ! j extrados

       end do ! mark K

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.8 Marks intrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,60

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       do j=np(i,1),np(i,2)+np(i,3),-1

       xprev=rib(i,44)

       rib(i,44)=rib(i,44)+sqrt((u(i,j,43)-u(i,j-1,43))**2.+((v(i,j,43)
     + -v(i,j-1,43))**2.))

       xpost=rib(i,44)

       if(xmk.lt.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,43)-u(i,j-1,43))**2.+((v(i,j,43)
     + -v(i,j-1,43))**2.))

       dist1=xmk-xprev

       xu=u(i,j,43)+(u(i,j-1,43)-u(i,j,43))*(dist1/dist)
       xv=v(i,j,43)+(v(i,j-1,43)-v(i,j,43))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=(datan((v(i,j,43)-v(i,j-1,43))/(u(i,j,43)-u(i,j-1,43))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Dibuixa punt a les costelles
       call point(sepx+xu,sepy-sepriy*0.5-xv,7)

       end if

       end do ! j intrados

       end do ! k


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.9 Draw holes in unloaded ribs
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       do l=1,nhols11

c       write (*,*) i,nhols11,ii11

c      Dibuixa forat tipus 11 (alleugerament elliptics)
     
       xx0=(hol(ii11,l,2))*0.5*(rib(i-1,5)+rib(i,5))/100.0d0+sepx
       yy0=(-(hol(ii11,l,3))*0.5*(rib(i-1,5)+rib(i,5))
     + /100.0d0+sepy-sepriy*0.5)
       xxa=(hol(ii11,l,4))*0.5*(rib(i-1,5)+rib(i,5))/100.0d0
       yyb=((hol(ii11,l,5))*0.5*(rib(i-1,5)+rib(i,5))/100.0d0)

       call ellipse(xx0,yy0,xxa,yyb,(hol(ii11,l,6)),1)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Change airfoil location
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end if  ! Calcule and draw rib i

       kx=int((float(i)/6.))
       ky=i-kx*6
       kyy=kyy+1

       end do ! rib i


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.10 Draw equidistant points in panels
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.10.1 Extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

c      Detect complete unloaded rib
       if (rib(i,56).eq.100.and.atp.ne."ss") then

c      Initial point

       j=1
       xu=u(i,j,44)
       xv=v(i,j,44)

       alp=abs(datan((v(i,j+1,44)-v(i,j,44))/(u(i,j+1,44)-u(i,j,44))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

       call point(psep+xu-seppix(i),psey-xv,4)
       call point(psep+xu-seppix(i)-2520.*xkf,psey-xv,4)

c      Final point

       j=np(i,2)
       xu=u(i,j,44)
       xv=v(i,j,44)

       alp=abs(datan((v(i,j-1,44)-v(i,j,44))/(u(i,j-1,44)-u(i,j,44))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

       call point(psep+xu-seppix(i),psey-xv,4)
       call point(psep+xu-seppix(i)-2520.*xkf,psey-xv,4)

c      Internal equidistant points

       do k=1,60  ! Up to 60 marks

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       do j=1,np(i,2)-1

       xprev=rib(i,41)

       rib(i,41)=rib(i,41)+sqrt((u(i,j,44)-u(i,j+1,44))**2.+
     + ((v(i,j,44)-v(i,j+1,44))**2.))

       xpost=rib(i,41)

       if(xmk.lt.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,44)-u(i,j+1,44))**2.+((v(i,j,44)
     + -v(i,j+1,44))**2.))

       dist1=xmk-xprev

       xu=u(i,j,44)+(u(i,j+1,44)-u(i,j,44))*(dist1/dist)
       xv=v(i,j,44)+(v(i,j+1,44)-v(i,j,44))*(dist1/dist)

c      Despla a vores punts de control de costures
c       alp=(datan((v(i,j+1,44)-v(i,j,44))/(u(i,j+1,44)-u(i,j,44))))
c       if (xv.lt.0.) then
c       xu=xu+xdes*dsin(alp)
c       xv=xv-xdes*dcos(alp)
c       end if
c       if (xv.ge.0.) then
c       xu=xu-xdes*dsin(alp)
c       xv=xv+xdes*dcos(alp)
c       end if

c      Dibuixa punt a les costelles

c       call point(psep+xu-seppix(i),psey-xv,1)

c      Despla a vores punts de control de costures
       alp=(datan((v(i,j+1,44)-v(i,j,44))/(u(i,j+1,44)-u(i,j,44))))
       if (xv.lt.0.) then
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       end if
       if (xv.ge.0.) then
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       end if

       call point(psep+xu-seppix(i),psey-xv,1)
       call point(psep+xu-seppix(i)-2520.*xkf,psey-xv,1)

       end if ! xmk

       end do ! j extrados

       end do ! mark K

       end if ! unloaded rib

       end do ! rib i


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      9.9.10.2 Intrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss

       psep=1970.*xkf+2520.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf

c      Detect complete unloaded rib
       if (rib(i,56).eq.100.and.atp.ne."ss") then

c      Initial point

       j=np(i,1)
       xu=u(i,j,44)
       xv=v(i,j,44)

       alp=abs(datan((v(i,j-1,44)-v(i,j,44))/(u(i,j-1,44)-u(i,j,44))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

       call point(psep+xu-seppix(i),psey-xv,4)
       call point(psep+xu-seppix(i)-2520.*xkf,psey-xv,4)

c      Final point

       j=np(i,2)+np(i,3)-1
       xu=u(i,j,44)
       xv=v(i,j,44)

       alp=abs(datan((v(i,j-1,44)-v(i,j,44))/(u(i,j-1,44)-u(i,j,44))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

       call point(psep+xu-seppix(i),psey-xv,4)
       call point(psep+xu-seppix(i)-2520.*xkf,psey-xv,4)

c      Internal equidistant points

       do k=1,60  ! Up to 60 marks

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       do j=np(i,1),np(i,2)+np(i,3),-1

       xprev=rib(i,43)

       rib(i,43)=rib(i,43)+sqrt((u(i,j,44)-u(i,j-1,44))**2.+
     + ((v(i,j,44)-v(i,j-1,44))**2.))

       xpost=rib(i,43)

       if(xmk.lt.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,44)-u(i,j-1,44))**2.+((v(i,j,44)
     + -v(i,j-1,44))**2.))

       dist1=xmk-xprev

       xu=u(i,j,44)+(u(i,j-1,44)-u(i,j,44))*(dist1/dist)
       xv=v(i,j,44)+(v(i,j-1,44)-v(i,j,44))*(dist1/dist)

c      Despla a vores punts de control de costures
c       alp=(datan((v(i,j+1,44)-v(i,j,44))/(u(i,j+1,44)-u(i,j,44))))
c       if (xv.lt.0.) then
c       xu=xu+xdes*dsin(alp)
c       xv=xv-xdes*dcos(alp)
c       end if
c       if (xv.ge.0.) then
c       xu=xu-xdes*dsin(alp)
c       xv=xv+xdes*dcos(alp)
c       end if

c      Dibuixa punt a les costelles

c       call point(psep+xu-seppix(i),psey-xv,1)

c      Despla a vores punts de control de costures
       alp=(datan((v(i,j-1,44)-v(i,j,44))/(u(i,j-1,44)-u(i,j,44))))
c       if (xv.lt.0.) then
c       xu=xu+xdes*dsin(alp)
c       xv=xv-xdes*dcos(alp)
c       end if
c       if (xv.ge.0.) then
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
c       end if

       call point(psep+xu-seppix(i),psey-xv,1)
       call point(psep+xu-seppix(i)-2520.*xkf,psey-xv,1)

       end if ! xmk

       end do ! j extrados

       end do ! mark K

       end if ! unloaded rib

       end do ! rib i


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      10. CALAGE
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
c        write (*,*) "pi 10. =",pi

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      10.1 Basic calculus
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       calag=(calage/100.0d0)*rib(1,5) ! calage in cm
       hcp=clengl+clengr            ! height karabiners-canopy
       cple=(cpress/100.0d0)*rib(1,5)  ! center or pressure in cm
       assiette=dasin(((cple-calag)/hcp))*(180.0d0/pi)
       afinesse=(datan(1.0d0/planeig))*(180.0d0/pi)
       aoa=afinesse-assiette

c       write (*,*) ">>>>>>>>>>>>>>>>"
c       write (*,*) planeig,pi
c       write (*,*) afinesse,assiette



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      10.1+ Angle beetween glidepath and airfoil plane
c            Angle beetween glide path and chord line
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       
       alpha_ii=afinesse*pi/180.0d0
c       write (*,*) alpha_ii

       do i=0,nribss

c      Plane defined by the space airfoil using points
c      j=1, j=int(np(i,2), j=np(i,2)
c      Warning! Solve case thickness = 0.0 !!!
       j1=1
       j2=int((np(i,2)/2.0))
       j3=np(i,2)
       x1=x(i,j1)
c       x2=x(i,j2)
       x2=x_apap(i)
       x3=x(i,j3)
       y1=y(i,j1)
c       y2=y(i,j2)
       y2=y_apap(i)
       y3=y(i,j3)
       z1=z(i,j1)
c       z2=z(i,j2)
       z2=z_apap(i)
       z3=z(i,j3)

       Apla=(y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
       Bpla=(z2-z1)*(x3-x1)-(x2-x1)*(z3-z1)
       Cpla=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)

c      Director cosines of glidepath line
       l_line=0.0d0
       m_line=-dcos(alpha_ii)
       n_line=dsin(alpha_ii)

c      Angle phii between plane and line
c      Handbook of Mathematics, Bronshtein and Semendyayev. Mir, Moscow.
       phii(i)=dasin((Apla*l_line+Bpla*m_line+Cpla*n_line)/
     + (dsqrt((Apla*Apla+Bpla*Bpla+Cpla*Cpla)*
     + (l_line*l_line+m_line*m_line+n_line*n_line))))

c      Director cosines of the chord line
c      First point is nose point j=np(i,6), last point is nose point j=1
       l2_line=(x(i,1)-x(i,np(i,6)))/rib(i,5)
       m2_line=(y(i,1)-y(i,np(i,6)))/rib(i,5)
       n2_line=(z(i,1)-z(i,np(i,6)))/rib(i,5)

c       write (*,*) i,rib(i,9),l2_line,m2_line,n2_line

c      Angle between two lines in space
c      Handbook of Mathematics, Bronshtein and Semendyayev. Mir, Moscow.
       chii(i)=pi-dacos((l_line*l2_line+m_line*m2_line+n_line*n2_line)/
     + dsqrt((l_line*l_line+m_line*m_line+n_line*n_line)*
     + (l2_line*l2_line+m2_line*m2_line+n2_line*n2_line)))

c       write (*,*) i,np(i,6), -phii(i)*180.0d0/pi,chii(i)*180.0d0/pi
c       write (*,*) i,phii(i)*180.0d0/pi,chii(i)*180.0d0/pi,
c     + l2_line,m2_line,n2_line

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      10.2 Karabiners location
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xkar=clengk/2.
       ykar=calag+rib(1,3)
       zkar=hcp

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      10.3 Dibuixa calage
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (2,1)

       x0=0.
       y0=900.*xkf

c      Central airfoil
       i=1

       do j=1,np(i,1)-1

       call line(x0+u(i,j,3),-v(i,j,3)+y0,x0+u(i,j+1,3),
     + -v(i,j+1,3)+y0,1)

       end do

c      Chord
       call line(x0,y0,x0+rib(i,5),y0,8)

c      Pilot-CP and Pilot-C
       call line(x0+ykar,y0+0.,x0+ykar,y0+zkar,1)
       call line(x0+cple,y0+0.,x0+ykar,y0+zkar,3)

c      Assiette and AoA angles
       call line(x0+cple,y0+0.,x0-100.,y0-(100.+cple)*
     + dtan(assiette*pi/180.),4)
       call line(x0+cple,y0+0.,x0-100.,y0+(100.+cple)*
     + dtan(aoa*pi/180.),5)

       xtext="pilot"
       call txt(x0+ykar+20.,y0+zkar,10.0d0,0.0d0,xtext,7)
       xtext="C"
       call txt(x0+ykar,y0-10.,10.0d0,0.0d0,xtext,7)
       xtext="Cp"
       call txt(x0+cple,y0-10.,10.0d0,0.0d0,xtext,7)
       
c      Write text about calage parameters
       xtext="calage= "
       call txt(x0-220*xkf,y0+60.,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') calage
       call txt(x0-50*xkf,y0+60.,10.0d0,0.0d0,xtext,7)
       
       xtext="center pressure= "
       call txt(x0-220*xkf,y0+80,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') cpress
       call txt(x0-50*xkf,y0+80,10.0d0,0.0d0,xtext,7)
       
       xtext="glide ratio= "
       call txt(x0-220*xkf,y0+100,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') planeig
       call txt(x0-50*xkf,y0+100,10.0d0,0.0d0,xtext,7)
       
       xtext="glide angle= "
       call txt(x0-220*xkf,y0+120,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') afinesse
       call txt(x0-50*xkf,y0+120,10.0d0,0.0d0,xtext,7)
       
       xtext="angle of attack= "
       call txt(x0-220*xkf,y0+140,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') aoa
       call txt(x0-50*xkf,y0+140,10.0d0,0.0d0,xtext,7)
       
       xtext="assiette= "
       call txt(x0-220*xkf,y0+160,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') assiette
       call txt(x0-50*xkf,y0+160,10.0d0,0.0d0,xtext,7)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     11. CALCULA LONGITUDS EXTRA INTRA EN PANELLS I PERFILS. MARKS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     WARNING: Additional vent marks in section 8.5 (!)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
c        write (*,*) "pi 11. =",pi

c      11.1 Extrados

       do i=1,nribss

       rib(i,30)=0. ! extra panel left
       rib(i,31)=0. ! extra rib
       rib(i,32)=0. ! extra panel right
       rib(i,33)=0. ! intra panel left
       rib(i,34)=0. ! intra rib
       rib(i,35)=0. ! intra panel right

c      Compute lengths extrados
       do j=1,np(i,2)-1

c      WARNING longituds a dreta i esquerra de la costella extrados!
c      Arreglat amb el vector 29 definit mes enrera

c       rib(i,30)=rib(i,30)+sqrt((u(i-1,j,29)-u(i-1,j+1,29))**2.+
c     + ((v(i-1,j,29)-v(i-1,j+1,29))**2.))

c      ATENCIO, veure si compatible amb cas reformat especial

       rib(i,30)=rib(i,30)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + ((v(i-1,j,10)-v(i-1,j+1,10))**2.))

       rib(i,31)=rib(i,31)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       rib(i,32)=rib(i,32)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       end do

c      Compute lengths intrados
       do j=np(i,2)+np(i,3),np(i,1)-1

       rib(i,33)=rib(i,33)+sqrt((u(i-1,j,10)-u(i-1,j+1,10))**2.+
     + ((v(i-1,j,10)-v(i-1,j+1,10))**2.))

       rib(i,34)=rib(i,34)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       rib(i,35)=rib(i,35)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       end do

c      Amplification cofficients
       rib(i,36)=rib(i,30)/rib(i,31)
       rib(i,37)=rib(i,32)/rib(i,31)
       rib(i,38)=rib(i,33)/rib(i,34)
       rib(i,39)=rib(i,35)/rib(i,34)

       rib(0,36)=rib(1,36)
       rib(0,37)=rib(1,36)
       rib(0,38)=rib(1,38)
       rib(0,39)=rib(1,38)

c       write (*,*) "rib(i,36) ",i, rib(i,36), rib(i,30)

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     AND COMPUTE AGAIN!!! "AMPLICATION" COEFFICIENTS
c     in new vectors rib(i,190) to rib(i,201)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Initilize vectors
       do i=0,nribss-1
       rib(i,190)=0. ! rib extra i
       rib(i,191)=0. ! panel extra left i
       rib(i,192)=0. ! rib extra i+1
       rib(i,193)=0. ! panel extra right i
       rib(i,194)=0. ! k 191/190
       rib(i,195)=0. ! k 193/192
       rib(i,196)=0. ! rib intra i
       rib(i,197)=0. ! panel intra left i
       rib(i,198)=0. ! rib intra i+1
       rib(i,199)=0. ! panel intra right i
       rib(i,200)=0. ! k 197/196
       rib(i,201)=0. ! k 199/198
       end do

       do i=0,nribss-1 ! for all ribs at left

c      A. Compute lengths extrados
       do j=1,np(i,2)-1
c      WARNING longituds a dreta i esquerra de la costella extrados!
c      Arreglat amb el vector 29 definit mes enrera
c       rib(i,30)=rib(i,30)+sqrt((u(i-1,j,29)-u(i-1,j+1,29))**2.+
c     + ((v(i-1,j,29)-v(i-1,j+1,29))**2.))
c      ATENCIO, veure si compatible amb cas reformat especial
       rib(i,190)=rib(i,190)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))
       rib(i,191)=rib(i,191)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))
       rib(i,192)=rib(i,192)+sqrt((u(i+1,j,3)-u(i+1,j+1,3))**2.+
     + ((v(i+1,j,3)-v(i+1,j+1,3))**2.))
       rib(i,193)=rib(i,193)+sqrt((u(i,j,10)-u(i,j+1,10))**2.+
     + ((v(i,j,10)-v(i,j+1,10))**2.))
       end do
       rib(i,194)=rib(i,191)/rib(i,190) ! Extrados left
       rib(i,195)=rib(i,193)/rib(i,192) ! Extrados right

c       write (*,*) i,"extra ",rib(i,194),rib(i,195)

c      B. Compute lengths intrados
       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       rib(i,196)=rib(i,196)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))
       rib(i,197)=rib(i,197)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))
       rib(i,198)=rib(i,198)+sqrt((u(i+1,j,3)-u(i+1,j+1,3))**2.+
     + ((v(i+1,j,3)-v(i+1,j+1,3))**2.))
       rib(i,199)=rib(i,199)+sqrt((u(i,j,10)-u(i,j+1,10))**2.+
     + ((v(i,j,10)-v(i,j+1,10))**2.))
       end do ! j
       rib(i,200)=rib(i,197)/rib(i,196) ! Intrados left
       rib(i,201)=rib(i,199)/rib(i,198) ! Intrados right

c       write (*,*) i,"intra ",rib(i,200),rib(i,201)

       end do ! i ribs


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.2 Comprovació de longituds
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       do i=1,nribss

c       write (*,*) "Extrados ", i, rib(i,30), rib(i,31), rib(i,32) 

c       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc      
c      11.3 Dibuixa marques a costelles
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       sepxx=700.*xkf
       sepyy=100.*xkf

       kx=0
       ky=0
       kyy=0

c      Verify thickness of last rib
       
       xsum=0.
       ic=0
       i=nribss
       do j=1,np(i,1)
       xsum=xsum+abs(v(i,j,3))
       end do
       if (xsum.ne.0.0) then
       ic=1
       end if

ccccccccccccccccccccccccccccccccccccccccccccccc
c     11.3.1 Extrados
ccccccccccccccccccccccccccccccccccccccccccccccc

c      Iteration in ribs    
       do i=1,nribss-1+ic

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Punt TE
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       j=1

       xu=u(i,j,3)
       xv=v(i,j,3)

c      Despla a vores punts de control de costures
       alp=pi/2.
       if (xv.lt.0.) then
c       xu=xu+xdes*dsin(alp)
c       xv=xv-xdes*dcos(alp)
       end if
       if (xv.ge.0.) then
c       xu=xu+xdes*dsin(alp)
c       xv=xv-xdes*dcos(alp)
       end if

       call pointg(sepx+xu,sepy-xv,xcir,4)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Punts interiors
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Equidistant points in ribs extrados (print)

       do k=1,60

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       do j=1,np(i,2)-1

       xprev=rib(i,41)

       rib(i,41)=rib(i,41)+sqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       xpost=rib(i,41)

       if(xmk.lt.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,3)-u(i,j+1,3))**2.+((v(i,j,3)
     + -v(i,j+1,3))**2.))

       dist1=xmk-xprev

       xu=u(i,j,3)+(u(i,j+1,3)-u(i,j,3))*(dist1/dist)
       xv=v(i,j,3)+(v(i,j+1,3)-v(i,j,3))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=(datan((v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))))
       if (xv.lt.0.) then
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       end if
       if (xv.ge.0.) then
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       end if

       call pointg(sepx+xu,sepy-xv,xcir,3)

c      Dibuixa punt a les costelles de la taula de tall
c      2530 per ajustar a BOX(1,4)
       call point(2530.*xkf+sepx+xu,sepy-xv,7)
       
       end if

       end do ! j extrados

c      new
       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.3.2 Intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Punts interiors

       do k=1,60

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

c      Comprova si el parapent es tipus "ds" or "pc"
c      If type "ss" not needed

       if (atp.eq."ds".or.atp.eq."pc") then

       do j=np(i,1),np(i,2)+np(i,3),-1

       xprev=rib(i,44)

       rib(i,44)=rib(i,44)+sqrt((u(i,j,3)-u(i,j-1,3))**2.+((v(i,j,3)
     + -v(i,j-1,3))**2.))

       xpost=rib(i,44)

       if(xmk.lt.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,3)-u(i,j-1,3))**2.+((v(i,j,3)
     + -v(i,j-1,3))**2.))

       dist1=xmk-xprev

       xu=u(i,j,3)+(u(i,j-1,3)-u(i,j,3))*(dist1/dist)
       xv=v(i,j,3)+(v(i,j-1,3)-v(i,j,3))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=(datan((v(i,j,3)-v(i,j-1,3))/(u(i,j,3)-u(i,j-1,3))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

       call pointg(sepx+xu,sepy-xv,xcir,3)

c      Dibuixa punt a les costelles de la taula de tall
c      2530 per ajustar a BOX(1,4)
       call point(2530.*xkf+sepx+xu,sepy-xv,7)
     
       end if

       end do ! j intrados

c      Final verificació ds
       end if

       end do ! k

       kx=int((float(i)/6.))
       ky=i-kx*6
       kyy=kyy+1
       
       end do  ! i

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4 Panels marks
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.1 Extrados panels mark 
c      Case classic
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (n1draw.eq.1) then ! Draw marks classic

       do i=0,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=400.*xkf

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.1.2 Marks extrados left  
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Initial and final points

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Initial point
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       j=1

       xu=u(i,j,9)
       xv=v(i,j,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j+1,9)-v(i,j,9))/(u(i,j+1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)

c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Final point
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       j=np(i,2)

       xu=u(i,j,9)
       xv=v(i,j,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j-1,9)-v(i,j,9))/(u(i,j-1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)

c      Point laser      
       call point(psep+xu+2520.*xkf,-xv+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Interior points
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,60

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       xmk=xmk*rib(i,36) ! amplificacio de segment
      
c      Dibuixa a extrados left     

       do j=1,np(i,2)-1

       xprev=rib(i,40)

       rib(i,40)=rib(i,40)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       xpost=rib(i,40)

       if(xmk.le.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       dist1=xmk-xprev

       xu=u(i,j,9)+(u(i,j+1,9)-u(i,j,9))*(dist1/dist)
       xv=v(i,j,9)+(v(i,j+1,9)-v(i,j,9))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j+1,9)-v(i,j,9))/(u(i,j+1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)

c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       
       end if

       end do ! j extrados left

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.1.3 Marks Panel extrados right
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Interiors
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xmk=xmark*float(k)

       xmk=xmk*rib(i,37) ! amplificacio de segment

c      Dibuixa a extrados right     

       do j=1,np(i,2)-1

       xprev=rib(i,42)

       rib(i,42)=rib(i,42)+sqrt((u(i,j,10)-u(i,j+1,10))**2.+((v(i,j,10)
     + -v(i,j+1,10))**2.))

       xpost=rib(i,42)

       if(xmk.le.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,10)-u(i,j+1,10))**2.+((v(i,j,10)
     + -v(i,j+1,10))**2.))

       dist1=xmk-xprev

       xu=u(i,j,10)+(u(i,j+1,10)-u(i,j,10))*(dist1/dist)
       xv=v(i,j,10)+(v(i,j+1,10)-v(i,j,10))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j+1,10)-v(i,j,10))/(u(i,j+1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)

c      Point laser     
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       
       end if

       end do ! j extrados right

       end do ! k

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Initial and final mark points outside the k-60-loop
c      Note by Pawel 20190507
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Initial point
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       j=1

       xu=u(i,j,10)
       xv=v(i,j,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j+1,10)-v(i,j,10))/(u(i,j+1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)

c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Final point
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       j=np(i,2)

       xu=u(i,j,10)
       xv=v(i,j,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j-1,10)-v(i,j,10))/(u(i,j-1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

       call pointg(psep+xu,psey-xv,xcir,4)

c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)

       end do ! i extrados points

       end if ! n1draw points extrados right (and left?) 








ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marks in case k29d = 1
       if (k29d.eq.1) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.1-3D Extrados panel marks
c      Case 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
           
       do i=iini,nribss-1

       ic2=dint(rib(i+1,165)) ! vent type
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=xyshift*xkf-890.95*xyextra*xkf ! remove 890.95 to set BOX (1,3)

c      REDEFINITION (!) for proper printing
       ng=rib(i+1,169)

       if (i.eq.0) then
       ng=rib(1,169)
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.1.2-3D Marks
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Extrados points, case 3D, initial and final left and right
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Falta els punts dels vents!

       do j=1,npo
c       write (*,*) i,j,j9,j10,xcir,xdes
       end do
     
c      Case 0 cuts
       if (uppcuts(ng).eq.0) then
       npi=1
       npf=np(i,2)
       call prinifp(i,npi,npf,u,v,psep,psey,xcir,xdes,xkf)
       end if

c      Case 1 cut
       if (uppcuts(ng).eq.1) then
       npi=1
       npf=iupp(1,3,ng)
       call prinifp(i,npi,npf,u,v,psep,psey,xcir,xdes,xkf)
       npi=iupp(1,3,ng)
       npf=np(i,2)
       call prinifp(i,npi,npf,u,v,psep,psey+ysaut,xcir,xdes,xkf)
       end if

c      Case 2 cuts
       if (uppcuts(ng).eq.2) then
       npi=1
       npf=iupp(1,3,ng)
       call prinifp(i,npi,npf,u,v,psep,psey,xcir,xdes,xkf)
       npi=iupp(1,3,ng)
       npf=iupp(2,3,ng)
       call prinifp(i,npi,npf,u,v,psep,psey+ysaut,xcir,xdes,xkf)
       npi=iupp(2,3,ng)
       npf=np(i,2)
       call prinifp(i,npi,npf,u,v,psep,psey+ysaut*2.,xcir,xdes,xkf)
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Intrados points, case 3D, initial and final left and right
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc






       end do ! i ribs


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.2-3D Intrados panel marks
c      Case 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


c      Plotter BOX(0,3) and BOX (0,5)

       if (atp.ne."ss") then

c      Avoid central panel if thickness is 0
       iini=0  ! panel 0 (central)
       if (cencell.lt.0.01) then
       iini=1
       end if

       do i=iini,nribss-1

       ic2=dint(rib(i+1,165)) ! vent type

       psep=1970.*xkf+seppix(i)*1.0d0
       psey=xyshift*xkf-890.95*xyintra*xkf ! remove 890.95 to set BOX (1,3)

c      REDEFINITION (!) for proper printing
       ng=rib(i+1,169)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Intrados points, case 3D, initial and final left and right
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Falta els punts dels vents!
     
c      Case 0 cuts
       if (lowcuts(ng).eq.0) then
       npi=np(i,2)+np(i,3)-1
       npf=np(i,1)
       call prinifp(i,npi,npf,u,v,psep,psey,xcir,xdes,xkf)
       end if

c      Case 1 cut
       if (lowcuts(ng).eq.1) then
       npi=np(i,2)+np(i,3)-1
       npf=ilow(1,3,ng)
       call prinifp(i,npi,npf,u,v,psep,psey,xcir,xdes,xkf)
       npi=ilow(1,3,ng)
       npf=np(i,1)
       call prinifp(i,npi,npf,u,v,psep,psey+ysaut,xcir,xdes,xkf)
       end if

       end do ! i ribs

       end if ! "ss"


       end if ! k29d = 1













ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.2 Intrados panel marks
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (n1draw.eq.1) then ! draw

c      Control if type is not "ss"
       if (atp.ne."ss") then

       do i=0,nribss-1
       
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=1291.*xkf

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.2.1 Intrados panel marks Left
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Initial
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       j=np(i,2)+np(i,3)-1

       xu=u(i,j,9)
       xv=v(i,j,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j,9)-v(i,j+1,9))/(u(i,j,9)-u(i,j+1,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)

c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Final
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       j=np(i,1)

       xu=u(i,j,9)
       xv=v(i,j,9)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j-1,9)-v(i,j,9))/(u(i,j-1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)
c      Per calcular angle vora de fuga:
       xlll=psep+xu
       ylll=-xv+psey
c      See lep-2.73 to undestand use of thesse variables
cccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     Interior
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,60

c      Partial lengths init

       rib(i,40)=0.
       rib(i,41)=0.
       rib(i,42)=0.
       rib(i,43)=0.
       rib(i,44)=0.
       rib(i,45)=0.

       xmk=xmark*float(k)

       xmk=xmk*rib(i,38) ! amplificacio de segment
      
c      Dibuixa a intrados left     

       do j=np(i,1),np(i,2)+np(i,3),-1

       xprev=rib(i,43)

       rib(i,43)=rib(i,43)+sqrt((u(i,j,9)-u(i,j-1,9))**2.+((v(i,j,9)
     + -v(i,j-1,9))**2.))

       xpost=rib(i,43)

       if(xmk.le.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,9)-u(i,j-1,9))**2.+((v(i,j,9)
     + -v(i,j-1,9))**2.))

       dist1=xmk-xprev

       xu=u(i,j,9)+(u(i,j-1,9)-u(i,j,9))*(dist1/dist)
       xv=v(i,j,9)+(v(i,j-1,9)-v(i,j,9))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j-1,9)-v(i,j,9))/(u(i,j-1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)

c      Point laser      
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       
       end if

       end do ! j intrados left

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.2.2 Marks Panel intrados right
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Interior
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xmk=xmark*float(k)

       xmk=xmk*rib(i,39) ! amplificacio de segment

c      Dibuixa a intrados right     

       do j=np(i,1),np(i,2)+np(i,3),-1

       xprev=rib(i,45)

       rib(i,45)=rib(i,45)+sqrt((u(i,j,10)-u(i,j-1,10))**2.+((v(i,j,10)
     + -v(i,j-1,10))**2.))

       xpost=rib(i,45)

       if(xmk.le.xpost.and.xmk.ge.xprev) then

c      dibuixa marca

       dist=dsqrt((u(i,j,10)-u(i,j-1,10))**2.+((v(i,j,10)
     + -v(i,j-1,10))**2.))

       dist1=xmk-xprev

       xu=u(i,j,10)+(u(i,j-1,10)-u(i,j,10))*(dist1/dist)
       xv=v(i,j,10)+(v(i,j-1,10)-v(i,j,10))*(dist1/dist)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j-1,10)-v(i,j,10))/(u(i,j-1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)

c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       
       end if

       end do ! j intrados right

       end do ! k

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Initial and final mark points outside the k-60-loop
c      Note by Pawel 20190507
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Initial
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       j=np(i,2)+np(i,3)-1

       xu=u(i,j,10)
       xv=v(i,j,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j,10)-v(i,j+1,10))/(u(i,j,10)-u(i,j+1,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)

c      Point laser       
       call point(psep+xu+2520.*xkf,-xv+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Final
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       j=np(i,1)

       xu=u(i,j,10)
       xv=v(i,j,10)

c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j-1,10)-v(i,j,10))/(u(i,j-1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)

c      Point imp
       call pointg(psep+xu,psey-xv,xcir,4)
       call point(psep+xu+2520.*xkf,-xv+psey,7)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


cccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.2.4 Roman numbers in intrados
c      Dibuixa marques romanes AD
cccccccccccccccccccccccccccccccccccccccccccccccccccc

c      xlll, ylll computed above       

       xrrr=psep+xu
       yrrr=-xv+psey
       alprom=abs(atan((yrrr-ylll)/(xrrr-xlll)))

       call romano(i+1,psep-5.*dcos(alprom)+xu+2520.*xkf, 
     + -xv+psey-0.7*dcos(alprom)-5.*dsin(alprom),pi-alprom,
     + typm6(8)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      11.4.3 Anchor points mark in intrados (Experimental)
c      2015-09-06 Request by Scott
c      2018-01-20 Request by Nicolas
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Draw intrados marks
       icontrolmi=1

       if (icontrolmi.eq.1) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Left side
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,rib(i,15) ! rib(i,15)=anchors number

       xlen=0.
       j=np(i,1)
       xlenp=dsqrt((v(i,j,9)-v(i,j-1,9))**2.+(u(i,j,9)-u(i,j-1,9))**2.)

       do j=np(i,1),np(i,2)+1,-1

c      Detect and draw anchor point
       if (rib(i,130+klz).ge.xlen.and.rib(i,130+klz).lt.xlenp) then

c       write (*,*) "Anchors ",i,j,klz,xlen,rib(i,130+klz),xlenp

       rib(i,107)=rib(i,130+klz)-xlen
       rib(i,108)=dsqrt((v(i,j,9)-v(i,j-1,9))**2.+(u(i,j,9)-u(i,j-1,9))
     + **2.)

c      Interpolate
       xequis=u(i,j,9)-(rib(i,107)*(u(i,j,9)-u(i,j-1,9)))/
     + rib(i,108)
       yequis=v(i,j,9)-(rib(i,107)*(v(i,j,9)-v(i,j-1,9)))/
     + rib(i,108)

c      Define anchor points in planar panel
       xanchoril(i,klz)=xequis
       yanchoril(i,klz)=yequis

c      Draw
       xdu=u(i,j,9)-u(i,j-1,9)
       xdv=v(i,j,9)-v(i,j-1,9)

       if (xdu.ne.0) then
       alpha=-(datan(xdv/xdu))
       end if
       if (xdu.eq.0.) then
       alpha=pi/2.
       end if
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case imp
c      Line 4*xrib in plotting panels
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Case all
       call line(psep+xequis,psey-yequis,psep+xequis-0.4*xrib*
     + dsin(-alpha),psey-yequis-0.4*xrib*dcos(-alpha),30)
       
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case laser
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xpeq=xequis+1.*xdes*dsin(-alpha)
       ypeq=yequis-1.*xdes*dcos(-alpha)

       xdesp=1.0*(0.5*(xrib-20.*xdes))/10.
c       xdesp=typm6(5)
c      REVISAR

       xdesp1x=xdesp*dsin(-alpha)
       xdesp1y=-xdesp*dcos(-alpha)
       xdesp2x=2.*xdesp*dsin(-alpha)
       xdesp2y=-2.*xdesp*dcos(-alpha)

c      Case 1: classic 3 orange points
       if (typm4(5).eq.1) then
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq+xdesp1x+2520*xkf,psey-ypeq-xdesp1y,30)
       call point (psep+xpeq+xdesp2x+2520*xkf,psey-ypeq-xdesp2y,30)
       end if

c      Case 2: Controled 3 orange points
       if (typm4(5).eq.2) then
       xpeq=xequis+1.*typm6(5)*dsin(-alpha)
       ypeq=yequis-1.*typm6(5)*dcos(-alpha)
       xdesp1x=typm5(5)*dsin(-alpha)
       xdesp1y=-typm5(5)*dcos(-alpha)
       xdesp2x=2.*typm5(5)*dsin(-alpha)
       xdesp2y=-2.*typm5(5)*dcos(-alpha)
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq+xdesp1x+2520*xkf,psey-ypeq-xdesp1y,30)
       call point (psep+xpeq+xdesp2x+2520*xkf,psey-ypeq-xdesp2y,30)
       end if

c      Case 3: triangle h mm
       if (typm4(5).eq.3) then
       xpeq=xequis-typm6(5)*dsin(alpha)
       ypeq=yequis+typm6(5)*dcos(alpha)
       call mtriangle(psep+xpeq+2520*xkf,psey-ypeq,typm5(5),-alpha,1)
       end if

       end if

       xlen=xlen+sqrt((v(i,j,9)-v(i,j-1,9))**2.+(u(i,j,9)-u(i,j-1,9))
     + **2.)
       xlenp=xlen+sqrt((v(i,j-1,9)-v(i,j-2,9))**2.+
     + (u(i,j-1,9)-u(i,j-2,9))**2.)

       end do ! j

       end do ! klz


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Right side
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,rib(i+1,15)

       xlen=0.
       j=np(i,1)
       xlenp=dsqrt((v(i,j,10)-v(i,j-1,10))**2.+(u(i,j,10)-u(i,j-1,10))
     + **2.)

       do j=np(i,1),np(i,2)+1,-1

c      Detect and draw anchor point
       if (rib(i+1,130+klz).ge.xlen.and.rib(i+1,130+klz).lt.xlenp) then

c       write (*,*) "Anchors ",i,j,klz,xlen,rib(i,130+klz),xlenp

       rib(i+1,107)=rib(i+1,130+klz)-xlen
       rib(i+1,108)=dsqrt((v(i,j,10)-v(i,j-1,10))**2.+(u(i,j,10)-
     + u(i,j-1,10))**2.)

c      Interpolate
       xequis=u(i,j,10)-(rib(i+1,107)*(u(i,j,10)-u(i,j-1,10)))/
     + rib(i+1,108)
       yequis=v(i,j,10)-(rib(i+1,107)*(v(i,j,10)-v(i,j-1,10)))/
     + rib(i+1,108)

c      Define anchor points in planar panel
       xanchorir(i,klz)=xequis
       yanchorir(i,klz)=yequis

c      Draw
       alpha=-(datan((v(i,j,10)-v(i,j-1,10))/(u(i,j,10)-u(i,j-1,10))))

       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case imp
c      Line 4*xrib in plotting panels
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(psep+xequis,psey-yequis,psep+xequis+0.4*xrib*
     + dsin(-alpha),psey-yequis+0.4*xrib*dcos(-alpha),30)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case laser
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xpeq=xequis-1.*xdes*dsin(-alpha)
       ypeq=yequis+1.*xdes*dcos(-alpha)

       xdesp=1.0*(0.5*(xrib-20.*xdes))/10.
c      REVISAR
c       xdesp=typm6(5)

       xdesp1x=xdesp*dsin(-alpha)
       xdesp1y=-xdesp*dcos(-alpha)
       xdesp2x=2.*xdesp*dsin(-alpha)
       xdesp2y=-2.*xdesp*dcos(-alpha)

c      Case 1: classic 3 orange points
       if (typm4(5).eq.1) then
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq-xdesp1x+2520*xkf,psey-ypeq+xdesp1y,30)
       call point (psep+xpeq-xdesp2x+2520*xkf,psey-ypeq+xdesp2y,30)
       end if

c      Case 2: controled 3 orange points
       if (typm4(5).eq.2) then
       xpeq=xequis+1.*typm6(5)*dsin(-alpha)
       ypeq=yequis-1.*typm6(5)*dcos(-alpha)
       xdesp1x=typm5(5)*dsin(-alpha)
       xdesp1y=-typm5(5)*dcos(-alpha)
       xdesp2x=2.*typm5(5)*dsin(-alpha)
       xdesp2y=-2.*typm5(5)*dcos(-alpha)
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq-xdesp1x+2520*xkf,psey-ypeq+xdesp1y,30)
       call point (psep+xpeq-xdesp2x+2520*xkf,psey-ypeq+xdesp2y,30)
       end if

c      Case 3: triangle 2 mm
       if (typm4(5).eq.3) then
       xpeq=xequis-typm6(5)*dsin(-alpha)
       ypeq=yequis+typm6(5)*dcos(-alpha)
       call mtriangle(psep+xpeq+2520*xkf,psey-ypeq,typm5(5),-alpha+pi,1)
       end if

       end if

       xlen=xlen+dsqrt((v(i,j,10)-v(i,j-1,10))**2.+(u(i,j,10)-
     + u(i,j-1,10))**2.)
       xlenp=xlen+dsqrt((v(i,j-1,10)-v(i,j-2,10))**2.+
     + (u(i,j-1,10)-u(i,j-2,10))**2.)

       end do ! j

       end do ! klz

       end if ! icontrol-mi

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end do ! i

c      End if control is not "ss"
       end if

       end if ! n1draw




cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12. LINES
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c        write (*,*) "pi 12. =",pi
c        pi=4.0d0*datan(1.)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.1 Write lines matrix
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do ii=1,slp

       do j=1,cam(ii)

c       write (*,*) ii,j, mc(ii,j,2), mc(ii,j,3), mc(ii,j,4), mc(ii,j,5),
c     + mc(ii,j,6), mc(ii,j,7)," - "  ,mc(ii,j,14), mc(ii,j,15)


       end do
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.2 Identifica les cordes a calcular
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       ic1=0
       ic2=1

       do ii=1,slp      ! Itera en numero de plans

       do k=2,8,2       ! Explora fins 4 nivells
       
       do j=1,cam(ii)-1 ! Itera en camins de cada pla

       if (mc(ii,j,1).le.4.and.k.le.8) then ! Detecta fins 4 nivells

       a=dfloat(mc(ii,j,k))
       b=dfloat(mc(ii,j,k+1))
       aa=dfloat(mc(ii,j+1,k))
       bb=dfloat(mc(ii,j+1,k+1))

       endif

       if (mc(ii,j,1).eq.5.and.k.eq.10) then ! Llegeix nivell 5

       a=dfloat(mc(ii,j,k))
       b=dfloat(mc(ii,j,k+1))
       aa=dfloat(mc(ii,j+1,k))
       bb=dfloat(mc(ii,j+1,k+1))

       endif


       if (a.ne.0.0d0.and.b.ne.0.0d0) then ! count pair line

c      While pair is equal, increase counter
       if (a.eq.aa.and.b.eq.bb) then

       ic2=ic2+1 ! comptabilitza cordes iguals

c      Si arribem a final del cami comptabilitzar la corda
       if (j.eq.cam(ii)-1) then

       ic1=ic1+1

       corda(ic1,1)=ii                    !planol
       corda(ic1,2)=mc(ii,j+1,k)          !nivell
       corda(ic1,3)=mc(ii,j+1,k+1)        !ordre
       corda(ic1,4)=ic2                   !punts d'acciÃ³
       corda(ic1,5)=mc(ii,j+1,1)          !ramificacions del camÃ­
       corda(ic1,6)=mc(ii,j+1,14)         !final row
       corda(ic1,7)=mc(ii,j+1,15)         !final rib
      
       ic2=1

       end if

       end if

c      Si canvia la corda al mateix nivell
       if (a.ne.aa.or.b.ne.bb) then

c       write (*,*) "Ep ",b,bb

       ic1=ic1+1

       corda(ic1,1)=ii                  !planol
       corda(ic1,2)=mc(ii,j,k)          !nivell
       corda(ic1,3)=mc(ii,j,k+1)        !ordre
       corda(ic1,4)=ic2                 !punts d'acciÃ³
       corda(ic1,5)=mc(ii,j,1)          !ramificacions del camÃ­
       corda(ic1,6)=mc(ii,j,14)         !final row
       corda(ic1,7)=mc(ii,j,15)         !final rib
       
       ic2=1

       end if

c      Si arribem a l'ultima linia i no es zero
       if (j.eq.cam(ii)-1) then

       a=dfloat(mc(ii,j,k))
       b=dfloat(mc(ii,j,k+1))
       aa=dfloat(mc(ii,j+1,k))
       bb=dfloat(mc(ii,j+1,k+1))

c      Last level
       if ((a.ne.aa.or.b.ne.bb).and.(aa.ne.0.0d0.and.bb.ne.0.0d0)) then

       ic1=ic1+1

       corda(ic1,1)=ii                    !planol
       corda(ic1,2)=mc(ii,j+1,k)          !nivell
       corda(ic1,3)=mc(ii,j+1,k+1)        !ordre
       corda(ic1,4)=ic2                   !punts d'accio
       corda(ic1,5)=mc(ii,j+1,1)          !ramificacions del camÃ­
       corda(ic1,6)=mc(ii,j+1,14)         !final row
       corda(ic1,7)=mc(ii,j+1,15)         !final rib
 
       ic2=1

       end if

       end if

       end if

       end do  ! j path
       end do  ! k level 2 4 6 8 10 
       end do  ! ii plan

       cordam=ic1 ! maxim nombre de cordes

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.3 Compute anchor points in 3D space
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Need simplification as uses same code as section 6 (!!!!!)

       do i=1,nribss+1

       tetha=rib(i,8)*pi/180.
       rot_z=rib(i,250)*pi/180.0
       pos=rib(i,5)*rib(i,251)/100.0

       do j=1,rib(i,15) ! anchor number


c      Call to subroutine xyzt
c       u_aux(i,j,1)=u(i,j,6)
c       v_aux(i,j,1)=v(i,j,6)
c       w_aux(i,j,1)=0.0d0
c       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
c       w(i,j,19)=w_aux(i,j,5)
c       u(i,j,19)=u_aux(i,j,5)
c       v(i,j,19)=v_aux(i,j,5)


c       goto 2


c      Airfoil anchor washin coordinates
c      Note the parameter -rib(i,50) and review section 6.8 (!)
       u(i,j,17)=(u(i,j,6)-(rib(i,10)/100.)*rib(i,5))*dcos(tetha)+
     + v(i,j,6)*dsin(tetha)+(rib(i,10)/100.)*rib(i,5)
       v(i,j,17)=(-u(i,j,6)+(rib(i,10)/100.)*rib(i,5))*dsin(tetha)+
     + v(i,j,6)*dcos(tetha)-rib(i,50)

c      Airfoil rotation in Z-axis. ( View section 6, MUST be the same )

       wnew(j)=-u(i,j,17)*dsin(rot_z)+pos*dsin(rot_z)
       unew(j)=u(i,j,17)*dcos(rot_z)+pos*(1-dcos(rot_z))
       vnew(j)=v(i,j,17)
       u(i,j,4)=unew(j)
       v(i,j,4)=vnew(j)
       w(i,j,4)=wnew(j)

c      Airfoil anchor (u,v,w) espace coordinates
c       u(i,j,18)=u(i,j,17)
c       v(i,j,18)=v(i,j,17)*dcos(rib(i,9)*pi/180.)
c       w(i,j,18)=-v(i,j,17)*dsin(rib(i,9)*pi/180.)

c      Airfoils rotation in Y-axis
       w(i,j,18)=-w(i,j,4)*dcos(rib(i,9)*pi/180.)-
     + v(i,j,4)*dsin(rib(i,9)*pi/180.)
       u(i,j,18)=u(i,j,4)
       v(i,j,18)=-w(i,j,4)*dsin(rib(i,9)*pi/180.)+
     + v(i,j,4)*dcos(rib(i,9)*pi/180.)

c      Airfoil anchor (x,y,z) absolute coordinates

       u(i,j,19)=rib(i,6)-w(i,j,18)
       v(i,j,19)=rib(i,3)+u(i,j,18)
       w(i,j,19)=rib(i,7)-v(i,j,18)

c 2      continue
    
       end do
       end do

       i=0
       do j=1,rib(1,15)
       u(i,j,19)=-u(1,j,19)
       v(i,j,19)=v(1,j,19)
       w(i,j,19)=w(1,j,19)
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.4 Compute singular rib points in 3D space
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=0,nribss+1

       tetha=rib(i,8)*pi/180.0d0
       rot_z=rib(i,250)*pi/180.0
       pos=rib(i,5)*rib(i,251)/100.0

       do j=6,8 ! singular point number, brakes, inlet in, inlet out

c      Airfoil anchor washin coordinates
       u(i,j,17)=(u(i,j,6)-(rib(i,10)/100.)*rib(i,5))*dcos(tetha)+
     + v(i,j,6)*dsin(tetha)+(rib(i,10)/100.)*rib(i,5)
       v(i,j,17)=(-u(i,j,6)+(rib(i,10)/100.)*rib(i,5))*dsin(tetha)+
     + v(i,j,6)*dcos(tetha)-rib(i,50)

c      Airfoil rotation in Z-axis. ( View section 6, MUST be the same )

       wnew(j)=-u(i,j,17)*dsin(rot_z)+pos*dsin(rot_z)
       unew(j)=u(i,j,17)*dcos(rot_z)+pos*(1-dcos(rot_z))
       vnew(j)=v(i,j,17)
       u(i,j,4)=unew(j)
       v(i,j,4)=vnew(j)
       w(i,j,4)=wnew(j)

c      Airfoil anchor (u,v,w) espace coordinates
c       u(i,j,18)=u(i,j,17)
c       v(i,j,18)=v(i,j,17)*dcos(rib(i,9)*pi/180.0d0)
c       w(i,j,18)=-v(i,j,17)*dsin(rib(i,9)*pi/180.0d0)

c      Airfoils rotation in Y-axis
       w(i,j,18)=-w(i,j,4)*dcos(rib(i,9)*pi/180.)-
     + v(i,j,4)*dsin(rib(i,9)*pi/180.)
       u(i,j,18)=u(i,j,4)
       v(i,j,18)=-w(i,j,4)*dsin(rib(i,9)*pi/180.)+
     + v(i,j,4)*dcos(rib(i,9)*pi/180.)

c      Airfoil anchor (x,y,z) absolute coordinates

       u(i,j,19)=rib(i,6)-w(i,j,18)
       v(i,j,19)=rib(i,3)+u(i,j,18)
       w(i,j,19)=rib(i,7)-v(i,j,18)

c      Brake distribution

       if (j.eq.6) then

       xprib=(rib(i,2)/rib(nribss,2))*100.0d0
       
       if (xprib.ge.bd(1,1).and.xprib.lt.bd(2,1)) then
       xm=(bd(2,2)-bd(1,2))/(bd(2,1)-bd(1,1))
       xb=bd(1,2)-xm*bd(1,1)
       xxl=xm*xprib+xb
       xlx=xxl*dsin(rib(i,9)*pi/180.)
       xly=xxl*dcos(rib(i,9)*pi/180.)
       end if

       if (xprib.ge.bd(2,1).and.xprib.lt.bd(3,1)) then
       xm=(bd(3,2)-bd(2,2))/(bd(3,1)-bd(2,1))
       xb=bd(2,2)-xm*bd(2,1)
       xxl=xm*xprib+xb
       xlx=xxl*dsin(rib(i,9)*pi/180.)
       xly=xxl*dcos(rib(i,9)*pi/180.)
       end if

       if (xprib.ge.bd(3,1).and.xprib.lt.bd(4,1)) then
       xm=(bd(4,2)-bd(3,2))/(bd(4,1)-bd(3,1))
       xb=bd(3,2)-xm*bd(3,1)
       xxl=xm*xprib+xb
       xlx=xxl*dsin(rib(i,9)*pi/180.)
       xly=xxl*dcos(rib(i,9)*pi/180.)
       end if

       if (xprib.ge.bd(4,1).and.xprib.le.bd(5,1)) then
       xm=(bd(5,2)-bd(4,2))/(bd(5,1)-bd(4,1))
       xb=bd(4,2)-xm*bd(4,1)
       xxl=xm*xprib+xb
       xlx=xxl*dsin(rib(i,9)*pi/180.)
       xly=xxl*dcos(rib(i,9)*pi/180.)
       end if

       u(i,j,19)=u(i,j,19)+xlx
       w(I,j,19)=w(i,j,19)-xly

       end if
    
       end do
       end do


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.4+ Redefineix punts ancoratge per a parapents tipus ss
c      Atencio als parametres atp i kaaa
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Punts tipus 19 definits a extrados
       if (atp.eq."ss") then

       do i=0,nribss
       do j=1,rib(i,15)

c      Desa ancoratges originals a vector 20       
       u(i,j,20)=u(i,j,19)
       v(i,j,20)=v(i,j,19)
       w(i,j,20)=w(i,j,19)

c      Defineix ancoratges virtuals extrados       
       jp=anccont(i,j)

       u(i,j,19)=(x(i,jp)+x(i,jp-1))/2.
       v(i,j,19)=(y(i,jp)+y(i,jp-1))/2.
       w(i,j,19)=(z(i,jp)+z(i,jp-1))/2.

c      Activar kaaa=1 nomes al fer suspentes banda A deixar morro on es
    
       if (kaaa.eq.1) then
       u(i,1,19)=u(i,1,20)
       v(i,1,19)=v(i,1,20)
       w(i,1,19)=w(i,1,20)
       end if

c       write (*,*) "19 ss ",i,j,u(i,j,19),v(i,j,19),w(i,j,19)
c       write (*,*) "20 ds ",i,j,u(i,j,20),v(i,j,20),w(i,j,20)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ESPECIAL BHL-PAMPA
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c      if rib(i,56) eq 0 not rotate triangle

       if (rib(i,56).eq.0.) then
       u(i,j,19)=u(i,j,20)
       v(i,j,19)=v(i,j,20)
       w(i,j,19)=w(i,j,20)
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ESPECIAL BHL-PAMPA
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end do
       end do
       
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.4++ Calcula carregues a cada ancoratge
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Calcula suma de ribs i suma de pesos relatius

       rib1t=0.
       rib2t=0.
       rib3t=0.
       xloadtot=0.

       do i=1,nribss

       if (rib(i,55).ne.0) then
       rib1t=rib1t+rib(i,5)
       rib2t=rib2t+rib(i,55)
       rib3t=rib3t+rib(i,5)*rib(i,55)
       end if

       end do

c       write (*,*) "rib1t, rib2t ", rib1t, rib2t

c      Assigna carregues a cada ancoratge       
       do i=1,nribss

       if (rib(i,55).ne.0) then

       do j=1,rib(i,15)
       aload(i,j)=(csusl/2.)*(cdis(int(rib(i,15)),j)/100.)*
     + (rib(i,55)*rib(i,5)/rib3t)

c       write (*,*) "A ", i, j, aload(i,j)
       xloadtot=xloadtot+aload(i,j)

       end do

       end if

       end do

c       write (*,*) "LOAD TOTAL: ",2.*xloadtot


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.5 Linies d'accio de cada corda
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Important
c      zcontrol=0 geometric action points, 
c      zcontrol=1 pondered ap
c      zcontrol=2 pondered ap 
c      comprovar les divergències

c      zcontrol=0

c      Defineix punt final de la linia d'accio de cada corda

       do i=1,cordam ! For all lines

       xcorda(i,3)=0.
       ycorda(i,3)=0.
       zcorda(i,3)=0.
       corda(i,8)=0.
       xload(i)=0.

       do ii=1,slp    !For all plans

       do k=2,8,2     ! For all levels (max=4)

       do j=1,cam(ii) ! For all paths

       if (ii.eq.corda(i,1)) then

       if (corda(i,2).eq.mc(ii,j,k).and.mc(ii,j,k+1).eq.corda(i,3)) then

       if (zcontrol.eq.0) then

c      0. Suma de les coordenades dels ancoratges finals
       xcorda(i,3)=xcorda(i,3)+u(mc(ii,j,15),mc(ii,j,14),19)
       ycorda(i,3)=ycorda(i,3)+v(mc(ii,j,15),mc(ii,j,14),19)
       zcorda(i,3)=zcorda(i,3)+w(mc(ii,j,15),mc(ii,j,14),19)

c      Carrega total a linia i
       xload(i)=xload(i)+aload(mc(ii,j,15),mc(ii,j,14))

       end if

       if(zcontrol.eq.1) then

c      1. Suma coordanades ancoratges ponderades per la long de rib
       xcorda(i,3)=xcorda(i,3)+u(mc(ii,j,15),mc(ii,j,14),19)*
     + rib(corda(i,7),5)
       ycorda(i,3)=ycorda(i,3)+v(mc(ii,j,15),mc(ii,j,14),19)*
     + rib(corda(i,7),5)
       zcorda(i,3)=zcorda(i,3)+w(mc(ii,j,15),mc(ii,j,14),19)*
     + rib(corda(i,7),5)

c      Suma longitud de ribs associats a i
       corda(i,8)=corda(i,8)+rib(corda(i,7),5)

       xload(i)=xload(i)+aload(mc(ii,j,15),mc(ii,j,14))

       end if

       if(zcontrol.eq.2) then

c      2. Coordenades ponderades per rib i pes relatiu
       xcorda(i,3)=xcorda(i,3)+u(mc(ii,j,15),mc(ii,j,14),19)*
     + rib(corda(i,7),5)*rib(corda(i,7),55)
       ycorda(i,3)=ycorda(i,3)+v(mc(ii,j,15),mc(ii,j,14),19)*
     + rib(corda(i,7),5)*rib(corda(i,7),55)
       zcorda(i,3)=zcorda(i,3)+w(mc(ii,j,15),mc(ii,j,14),19)*
     + rib(corda(i,7),5)*rib(corda(i,7),55)

       corda(i,8)=corda(i,8)+rib(corda(i,7),5)*rib(corda(i,7),55)

       xload(i)=xload(i)+aload(mc(ii,j,15),mc(ii,j,14))

       end if


       if(zcontrol.eq.3) then

c      3. Coordenades ponderades pel pes
       xcorda(i,3)=xcorda(i,3)+u(mc(ii,j,15),mc(ii,j,14),19)*
     + aload(mc(ii,j,15),mc(ii,j,14))
       ycorda(i,3)=ycorda(i,3)+v(mc(ii,j,15),mc(ii,j,14),19)*
     + aload(mc(ii,j,15),mc(ii,j,14))
       zcorda(i,3)=zcorda(i,3)+w(mc(ii,j,15),mc(ii,j,14),19)*
     + aload(mc(ii,j,15),mc(ii,j,14))

       corda(i,8)=corda(i,8)+aload(mc(ii,j,15),mc(ii,j,14))

       xload(i)=xload(i)+aload(mc(ii,j,15),mc(ii,j,14))

       end if


       end if

       end if

       end do

       end do

       end do

c      Center of gravity line i
       
       if(zcontrol.eq.0) then
       xcorda(i,3)=xcorda(i,3)/float(corda(i,4))
       ycorda(i,3)=ycorda(i,3)/float(corda(i,4))
       zcorda(i,3)=zcorda(i,3)/float(corda(i,4))
       end if

       if(zcontrol.eq.1) then
       xcorda(i,3)=xcorda(i,3)/corda(i,8)
       ycorda(i,3)=ycorda(i,3)/corda(i,8)
       zcorda(i,3)=zcorda(i,3)/corda(i,8)
       end if

       if(zcontrol.eq.2) then
       xcorda(i,3)=xcorda(i,3)/corda(i,8)
       ycorda(i,3)=ycorda(i,3)/corda(i,8)
       zcorda(i,3)=zcorda(i,3)/corda(i,8)
       end if

       if(zcontrol.eq.3) then
       xcorda(i,3)=xcorda(i,3)/xload(i)
       ycorda(i,3)=ycorda(i,3)/xload(i)
       zcorda(i,3)=zcorda(i,3)/xload(i)
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.6 Punts inicial i final de cada corda
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.6.1 LEVEL 1 (risers)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,cordam

       if (corda(i,2).eq.1) then

c      Cordes 1 tenen l'inici a mosquetons principals
       xcorda(i,1)=xkar
       ycorda(i,1)=ykar
       zcorda(i,1)=zkar

c      Equacio parametrica de la recta que passa per P1-P3

       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-
     + ycorda(i,1))**2+(zcorda(i,3)-zcorda(i,1))**2)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       t=clengr/(sqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,1,corda(i,3))=xcorda(i,1)
       y1line(ii,1,corda(i,3))=ycorda(i,1)
       z1line(ii,1,corda(i,3))=zcorda(i,1)
       x2line(ii,1,corda(i,3))=xcorda(i,2)
       y2line(ii,1,corda(i,3))=ycorda(i,2)
       z2line(ii,1,corda(i,3))=zcorda(i,2)

c      comprobacio

       disto=dsqrt((xcorda(i,2)-xcorda(i,1))**2+(ycorda(i,2)-
     + ycorda(i,1))**2+(zcorda(i,2)-zcorda(i,1))**2)

       end if

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.6.2 LEVEL 2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,cordam

       if (corda(i,2).eq.2) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      LEVEL 2 Si només dos nivells
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (corda(i,5).eq.2) then !directe a l'ancoratge

       xcorda(i,1)=x2line(corda(i,1),1,1)
       ycorda(i,1)=y2line(corda(i,1),1,1)
       zcorda(i,1)=z2line(corda(i,1),1,1)
      
       xcorda(i,2)=u(corda(i,7),corda(i,6),19)
       ycorda(i,2)=v(corda(i,7),corda(i,6),19)
       zcorda(i,2)=w(corda(i,7),corda(i,6),19)

       ii=corda(i,1)

       x1line(ii,2,corda(i,3))=xcorda(i,1)
       y1line(ii,2,corda(i,3))=ycorda(i,1)
       z1line(ii,2,corda(i,3))=zcorda(i,1)
       x2line(ii,2,corda(i,3))=xcorda(i,2)
       y2line(ii,2,corda(i,3))=ycorda(i,2)
       z2line(ii,2,corda(i,3))=zcorda(i,2)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Correccions necessaries a parapents ss (a nivell 2)
c      Calcula angles de gir phi0=phi1-phi2 a aplicar a triangles ss
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Per que es perd el valor de pi?
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c       pi=4.0d0*datan(1.)

       if (atp.eq."ss") then

       phi1(ii,2,corda(i,3))=(180./pi)*datan((x2line(ii,2,corda(i,3))-
     + x1line(ii,2,corda(i,3)))/(z1line(ii,2,corda(i,3))-
     + z2line(ii,2,corda(i,3))))

       if (kaaa.eq.1.and.corda(i,6).eq.1) then
       phi2(ii,2,corda(i,3))=0.
       else
       phi2(ii,2,corda(i,3))=(180./pi)*datan((u(corda(i,7),corda(i,6),19
     + )-u(corda(i,7),corda(i,6),20))/(w(corda(i,7),corda(i,6),20
     + )-w(corda(i,7),corda(i,6),19)))
       end if

       phi2(ii,2,corda(i,3))=rib(corda(i,7),9)

       phi0(ii,2,corda(i,3))=phi1(ii,2,corda(i,3))-phi2(ii,2,corda(i,3))

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      LEVEL 2 Si tres nivells
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (corda(i,5).eq.3) then ! tres nivells

       xcorda(i,1)=x2line(corda(i,1),1,1)
       ycorda(i,1)=y2line(corda(i,1),1,1)
       zcorda(i,1)=z2line(corda(i,1),1,1)
                    
       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-
     + ycorda(i,1))**2+(zcorda(i,3)-zcorda(i,1))**2)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       d13=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-ycorda(i,1))
     + **2+(zcorda(i,3)-zcorda(i,1))**2)
       
       t=(d13-raml(3,3))/(sqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,2,corda(i,3))=xcorda(i,1)
       y1line(ii,2,corda(i,3))=ycorda(i,1)
       z1line(ii,2,corda(i,3))=zcorda(i,1)
       x2line(ii,2,corda(i,3))=xcorda(i,2)
       y2line(ii,2,corda(i,3))=ycorda(i,2)
       z2line(ii,2,corda(i,3))=zcorda(i,2)
       
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      LEVEL 2 Si quatre nivells
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (corda(i,5).eq.4) then ! Quatre nivells

       xcorda(i,1)=x2line(corda(i,1),1,1)
       ycorda(i,1)=y2line(corda(i,1),1,1)
       zcorda(i,1)=z2line(corda(i,1),1,1)
                    
       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-
     + ycorda(i,1))**2+(zcorda(i,3)-zcorda(i,1))**2)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       d13=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-ycorda(i,1))
     + **2+(zcorda(i,3)-zcorda(i,1))**2)
       
       t=(d13-raml(4,3))/(sqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,2,corda(i,3))=xcorda(i,1)
       y1line(ii,2,corda(i,3))=ycorda(i,1)
       z1line(ii,2,corda(i,3))=zcorda(i,1)
       x2line(ii,2,corda(i,3))=xcorda(i,2)
       y2line(ii,2,corda(i,3))=ycorda(i,2)
       z2line(ii,2,corda(i,3))=zcorda(i,2)

       end if

       end if

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.6.3 LEVEL 3
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Inici al final de les cordes 2

       do i=1,cordam

       if (corda(i,2).eq.3) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Si només 3 nivells
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (corda(i,5).eq.3) then !directe a l'ancoratge

c      Explora mc i troba quin origen emprar
       do kk=1,slp
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,6).and.mc(kk,k,7).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,4)
       comp2(kk)=mc(kk,k,5)

       end if

       end do
       
       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),2,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),2,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),2,int(comp2(corda(i,1))))

c      Final
       xcorda(i,2)=u(corda(i,7),corda(i,6),19)
       ycorda(i,2)=v(corda(i,7),corda(i,6),19)
       zcorda(i,2)=w(corda(i,7),corda(i,6),19)

       ii=corda(i,1)

       x1line(ii,3,corda(i,3))=xcorda(i,1)
       y1line(ii,3,corda(i,3))=ycorda(i,1)
       z1line(ii,3,corda(i,3))=zcorda(i,1)
       x2line(ii,3,corda(i,3))=xcorda(i,2)
       y2line(ii,3,corda(i,3))=ycorda(i,2)
       z2line(ii,3,corda(i,3))=zcorda(i,2)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Correccions necessaries a parapents ss (a nivell 3)
c      Calcula angles de gir phi0=phi1-phi2 a aplicar a triangles ss
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Per que es perd el valor de pi?
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c       pi=4.0d0*datan(1.)

       if (atp.eq."ss") then

       phi1(ii,3,corda(i,3))=(180./pi)*datan((x2line(ii,3,corda(i,3))-
     + x1line(ii,3,corda(i,3)))/(z1line(ii,3,corda(i,3))-
     + z2line(ii,3,corda(i,3))))

       if (kaaa.eq.1.and.corda(i,6).eq.1) then
       phi2(ii,3,corda(i,3))=0.
       else
       phi2(ii,3,corda(i,3))=(180./pi)*datan((u(corda(i,7),corda(i,6),19
     + )-u(corda(i,7),corda(i,6),20))/(w(corda(i,7),corda(i,6),20
     + )-w(corda(i,7),corda(i,6),19)))
       end if

       phi2(ii,3,corda(i,3))=rib(corda(i,7),9)

       phi0(ii,3,corda(i,3))=phi1(ii,3,corda(i,3))-phi2(ii,3,corda(i,3))

c       write (*,*) ii, corda(i,2), corda(i,3), "phi0= ", 
c     + phi0(ii,3,corda(i,3))

c       write (*,*) "girs ",i,corda(i,1),corda(i,3),phi1(ii,4,corda(i,3))
c     + ,phi2(ii,4,corda(i,3)),phi0(ii,4,corda(i,3))

c      Fi angles de gir

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       end if

c      Si hi ha quatre nivells
       if (corda(i,5).eq.4) then

c      Explora mc i troba quin origen emprar
       do kk=1,slp
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,6).and.mc(kk,k,7).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,4)
       comp2(kk)=mc(kk,k,5)

       end if

       end do
       
       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),2,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),2,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),2,int(comp2(corda(i,1))))

       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-
     + ycorda(i,1))**2+(zcorda(i,3)-zcorda(i,1))**2)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       d13=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-ycorda(i,1))
     + **2+(zcorda(i,3)-zcorda(i,1))**2)
       
c       t=(raml(4,4)-dl3)/(sqrt(cdl*cdl+cdm*cdm+cdn*cdn))
        
        t=(raml(4,3)-raml(4,4))/(sqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,3,corda(i,3))=xcorda(i,1)
       y1line(ii,3,corda(i,3))=ycorda(i,1)
       z1line(ii,3,corda(i,3))=zcorda(i,1)
       x2line(ii,3,corda(i,3))=xcorda(i,2)
       y2line(ii,3,corda(i,3))=ycorda(i,2)
       z2line(ii,3,corda(i,3))=zcorda(i,2)
       
       end if

       end if

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.6.4 LEVEL 4
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Inici al final de les cordes 3

       do i=1,cordam

       if (corda(i,2).eq.4) then

       if (corda(i,5).eq.4) then !directe a l'ancoratge

c      Explora mc i troba quin origen emprar
       do kk=1,slp
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,8).and.mc(kk,k,9).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,6)
       comp2(kk)=mc(kk,k,7)

       end if

       end do
       
       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),3,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),3,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),3,int(comp2(corda(i,1))))

c      Final als ancoratges (parapents ds)
       xcorda(i,2)=u(corda(i,7),corda(i,6),19)
       ycorda(i,2)=v(corda(i,7),corda(i,6),19)
       zcorda(i,2)=w(corda(i,7),corda(i,6),19)

       ii=corda(i,1)

       x1line(ii,4,corda(i,3))=xcorda(i,1)
       y1line(ii,4,corda(i,3))=ycorda(i,1)
       z1line(ii,4,corda(i,3))=zcorda(i,1)
       x2line(ii,4,corda(i,3))=xcorda(i,2)
       y2line(ii,4,corda(i,3))=ycorda(i,2)
       z2line(ii,4,corda(i,3))=zcorda(i,2)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Correccions necessaries a parapents ss (a nivell 4)
c      Calcula angles de gir phi0=phi1-phi2 a aplicar a triangles ss
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Per que es perd el valor de pi?
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c       pi=4.0d0*datan(1.)

       if (atp.eq."ss") then

       phi1(ii,4,corda(i,3))=(180./pi)*datan((x2line(ii,4,corda(i,3))-
     + x1line(ii,4,corda(i,3)))/(z1line(ii,4,corda(i,3))-
     + z2line(ii,4,corda(i,3))))

       if (kaaa.eq.1.and.corda(i,6).eq.1) then
       phi2(ii,4,corda(i,3))=0.
       else
       phi2(ii,4,corda(i,3))=(180./pi)*datan((u(corda(i,7),corda(i,6),19
     + )-u(corda(i,7),corda(i,6),20))/(w(corda(i,7),corda(i,6),20
     + )-w(corda(i,7),corda(i,6),19)))
       end if

       phi2(ii,4,corda(i,3))=rib(corda(i,7),9)

       phi0(ii,4,corda(i,3))=phi1(ii,4,corda(i,3))-phi2(ii,4,corda(i,3))

c       write (*,*) "girs ",i,corda(i,1),corda(i,3),phi1(ii,4,corda(i,3))
c     + ,phi2(ii,4,corda(i,3)),phi0(ii,4,corda(i,3))

c      Fi angles de gir

       end if
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       end if

       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.7 Gir dels triangles parapents ss
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      calque = "triangles" (Note Ludovic G. 2018-05-12)

       if (atp.eq."ss") then

c      Verify thickness of last rib (escrit ja a 11.3)
       
       xsum=0.
       ic=0
       i=nribss
       do j=1,np(i,1)
       xsum=xsum+abs(v(i,j,3))
       end do
       if (xsum.ne.0.0) then
       ic=1
       end if

c      Calcula punt 4 situat al triangle 1-2-3

c      Recorre punts de l'extrados

       do i=1,cordam

c      No estabilo
       if (corda(i,7).ne.nribss*float(ic-1)*float(ic-1)) then

       ii=corda(i,1)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.7.1 Gir cordes en quart nivell
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Gir en cordes de tercer nivell
       if (corda(i,2).eq.4) then

c      write (*,*) "corda(i,2)=", corda(i,2), corda(i,5)

       if (corda(i,5).eq.4) then !directe a l'ancoratge

       jp=anccont(corda(i,7),corda(i,6))

c      MODIF Ludovic G. 2018-05-12
c      Note: do the same at "gir cordes tercer nivell"
c      New parameter idelta is a function of extradps points np(i,2)

c      idelta=np(i,2)*6/100  ! Ludovic
c      Warnig!!! BHL2-16 fails using previous!
       idelta=3 ! Previous definition by Pere

       xpt1=x(corda(i,7),jp-idelta)
       ypt1=y(corda(i,7),jp-idelta)
       zpt1=z(corda(i,7),jp-idelta)

       xpt2=x(corda(i,7),jp+idelta)
       ypt2=y(corda(i,7),jp+idelta)
       zpt2=z(corda(i,7),jp+idelta)

       xpt3=u(corda(i,7),corda(i,6),20)
       ypt3=v(corda(i,7),corda(i,6),20)
       zpt3=w(corda(i,7),corda(i,6),20)

c      Dibuixa els triangles a girar

       call line3d(xpt1,ypt1,zpt1,xpt2,ypt2,zpt2,1)
       call line3d(xpt1,ypt1,zpt1,xpt3,ypt3,zpt3,1)
       call line3d(xpt2,ypt2,zpt2,xpt3,ypt3,zpt3,1)

c      Calcula punt 4

c      Cosinus directors rectes 2-1 i 3-1

       xd21=dsqrt((xpt1-xpt2)**2.+(ypt1-ypt2)**2.+(zpt1-zpt2)**2.)
       xd31=dsqrt((xpt1-xpt3)**2.+(ypt1-ypt3)**2.+(zpt1-zpt3)**2.)
       xd32=dsqrt((xpt2-xpt3)**2.+(ypt2-ypt3)**2.+(zpt2-zpt3)**2.)

       cl21=(xpt1-xpt2)/xd21
       cm21=(ypt1-ypt2)/xd21
       cn21=(zpt1-zpt2)/xd21

       cl31=(xpt1-xpt3)/xd31
       cm31=(ypt1-ypt3)/xd31
       cn31=(zpt1-zpt3)/xd31

c      Punt 4 a recta que passa per 1-2 parametrica xt

       xt=xd31*(cl21*cl21+cm21*cm21+cn21*cn21)*
     + (cl21*cl31+cm21*cm31+cn21*cn31)

       xpt4=xpt1-cl21*xt
       ypt4=ypt1-cm21*xt
       zpt4=zpt1-cn21*xt

       call line3d(xpt4,ypt4,zpt4,xpt3,ypt3,zpt3,7)

       xd41=dsqrt((xpt1-xpt4)**2.+(ypt1-ypt4)**2.+(zpt1-zpt4)**2.)
      
       cl41=(xpt1-xpt4)/xd41
       cm41=(ypt1-ypt4)/xd41
       cn41=(zpt1-zpt4)/xd41

       xd43=dsqrt((xpt3-xpt4)**2.+(ypt3-ypt4)**2.+(zpt3-zpt4)**2.)

       cl43=(xpt3-xpt4)/xd43
       cm43=(ypt3-ypt4)/xd43
       cn43=(zpt3-zpt4)/xd43

c      Planol 1-2-3 (determinant)

       A1=(ypt2-ypt1)*(zpt3-zpt1)-(zpt2-zpt1)*(ypt3-ypt1)
       B1=(zpt2-zpt1)*(xpt3-xpt1)-(xpt2-xpt1)*(zpt3-zpt1)
       C1=(xpt2-xpt1)*(ypt3-ypt1)-(ypt2-ypt1)*(xpt3-xpt1)
       D1=-A1*xpt1-B1*ypt1-C1*zpt1

c      Punt 5 situat a la recta normal a 1-2-3 per 4

       xpt5=xpt4+A1*0.1
       ypt5=ypt4+B1*0.1
       zpt5=zpt4+C1*0.1

c      Eix normal al pla 1-2-3
c       call line3d(xpt4,ypt4,zpt4,xpt5,ypt5,zpt5,1)

       xd45=dsqrt((xpt5-xpt4)**2.+(ypt5-ypt4)**2.+(zpt5-zpt4)**2.)

       cl45=(xpt5-xpt4)/xd45
       cm45=(ypt5-ypt4)/xd45
       cn45=(zpt5-zpt4)/xd45

c       phi0(ii,corda(i,2),corda(i,3))=0.

       xptp6=xd43*dsin((pi/180.)*phi0(ii,4,corda(i,3)))
       yptp6=0.
       zptp6=-xd43*dcos((pi/180.)*phi0(ii,4,corda(i,3)))

c      "-" sign before cn41 in ypt6 be aware, review!!! however works!

       xpt6=cl45*xptp6+cm45*yptp6-cn45*zptp6+xpt4
       ypt6=cl41*xptp6+cm41*yptp6+cn41*zptp6+ypt4
       zpt6=cl43*xptp6+cm43*yptp6-cn43*zptp6+zpt4

c      Truc per ajustar posicio Y !!!!!!!!!!!!!!!!!
c      Funciona força be
c      REVISAR !!!!!!!!!!!!!!!!!!!!!!!!!!!!
c      ypt6=ypt3

c       write (*,*) "ypt6 ypt4 phi0 ", ypt6, ypt4, 
c     + phi0(ii,4,corda(i,3))

c      Segona definició, per recta perpendicular al pla 1-2-3
 
       xt=xd43*dcos((pi/180.)*phi0(ii,4,corda(i,3)))
       xpt7=xpt4+cl43*xt
       ypt7=ypt4+cm43*xt
       zpt7=zpt4+cn43*xt
c       call line3d(0.,0.,0.,xpt7,ypt7,zpt7,5)

       xt=(((xd43*xd43*(dsin((pi/180.)*phi0(ii,4,corda(i,3)))))/
     + (sqrt(A1*A1+B1*B1+C1*C1))))

c       write (*,*) "xt ", xt

c       xpt6=xpt7+A1*xt
c       ypt6=ypt7+B1*xt
c       zpt6=zpt7+C1*xt

***************************************************************
*      Codi introduit per Ludovic G. en data 20180419
*      Jo he de revisar
*      Merci!
***************************************************************

       iv=corda(i,7)
       if (rib(iv,56).eq.0.) then
       xpt6=u(corda(i,7),corda(i,6),19)
       ypt6=v(corda(i,7),corda(i,6),19)
       zpt6=w(corda(i,7),corda(i,6),19)
       end if

***************************************************************

c      Dibuixa triangles girats

       if (kaaa.eq.0.or.corda(i,6).ne.1) then
       call line3d(xpt3,ypt3,zpt3,xpt6,ypt6,zpt6,1)
       call line3d(xpt1,ypt1,zpt1,xpt6,ypt6,zpt6,2)
       call line3d(xpt2,ypt2,zpt2,xpt6,ypt6,zpt6,2)
       end if

       u(corda(i,7),corda(i,6),19)=xpt6
       v(corda(i,7),corda(i,6),19)=ypt6
       w(corda(i,7),corda(i,6),19)=zpt6

c      No gira b.a. si kaaa=1

       if (kaaa.eq.1.and.corda(i,6).eq.1) then
       u(corda(i,7),corda(i,6),19)=u(corda(i,7),corda(i,6),20)
       v(corda(i,7),corda(i,6),19)=v(corda(i,7),corda(i,6),20)
       w(corda(i,7),corda(i,6),19)=w(corda(i,7),corda(i,6),20)
       end if


       end if

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      12.7.2 Gir cordes en tercer nivell
c      opcionalment es podria fer servir rutina anterior amb corda(i,2)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Gir en cordes de tercer nivell
       if (corda(i,2).eq.3) then

c      write (*,*) "corda(i,2)=", corda(i,2), corda(i,5)

       if (corda(i,5).eq.3) then !directe a l'ancoratge

       jp=anccont(corda(i,7),corda(i,6))

       xpt1=x(corda(i,7),jp-3)
       ypt1=y(corda(i,7),jp-3)
       zpt1=z(corda(i,7),jp-3)

       xpt2=x(corda(i,7),jp+3)
       ypt2=y(corda(i,7),jp+3)
       zpt2=z(corda(i,7),jp+3)

       xpt3=u(corda(i,7),corda(i,6),20)
       ypt3=v(corda(i,7),corda(i,6),20)
       zpt3=w(corda(i,7),corda(i,6),20)

c      Dibuixa els triangles a girar

       call line3d(xpt1,ypt1,zpt1,xpt2,ypt2,zpt2,1)
       call line3d(xpt1,ypt1,zpt1,xpt3,ypt3,zpt3,1)
       call line3d(xpt2,ypt2,zpt2,xpt3,ypt3,zpt3,1)

c      Calcula punt 4

c      Cosinus directors rectes 2-1 i 3-1

       xd21=dsqrt((xpt1-xpt2)**2.+(ypt1-ypt2)**2.+(zpt1-zpt2)**2.)
       xd31=dsqrt((xpt1-xpt3)**2.+(ypt1-ypt3)**2.+(zpt1-zpt3)**2.)
       xd32=dsqrt((xpt2-xpt3)**2.+(ypt2-ypt3)**2.+(zpt2-zpt3)**2.)

       cl21=(xpt1-xpt2)/xd21
       cm21=(ypt1-ypt2)/xd21
       cn21=(zpt1-zpt2)/xd21

       cl31=(xpt1-xpt3)/xd31
       cm31=(ypt1-ypt3)/xd31
       cn31=(zpt1-zpt3)/xd31

c      Punt 4 a recta que passa per 1-2 parametrica xt

       xt=xd31*(cl21*cl21+cm21*cm21+cn21*cn21)*
     + (cl21*cl31+cm21*cm31+cn21*cn31)

       xpt4=xpt1-cl21*xt
       ypt4=ypt1-cm21*xt
       zpt4=zpt1-cn21*xt

       call line3d(xpt4,ypt4,zpt4,xpt3,ypt3,zpt3,7)

       xd41=dsqrt((xpt1-xpt4)**2.+(ypt1-ypt4)**2.+(zpt1-zpt4)**2.)
       xd43=dsqrt((xpt3-xpt4)**2.+(ypt3-ypt4)**2.+(zpt3-zpt4)**2.)

       cl43=(xpt3-xpt4)/xd43
       cm43=(ypt3-ypt4)/xd43
       cn43=(zpt3-zpt4)/xd43
      
c      Planol 1-2-3 (determinant)

       A1=(ypt2-ypt1)*(zpt3-zpt1)-(zpt2-zpt1)*(ypt3-ypt1)
       B1=(zpt2-zpt1)*(xpt3-xpt1)-(xpt2-xpt1)*(zpt3-zpt1)
       C1=(xpt2-xpt1)*(ypt3-ypt1)-(ypt2-ypt1)*(xpt3-xpt1)
       D1=-A1*xpt1-B1*ypt1-C1*zpt1

c      Punt 5 situat a la recta normal a 1-2-3 per 4

       xpt5=xpt4+A1*1.
       ypt5=ypt4+B1*1.
       zpt5=zpt4+C1*1.

c       call line3d(xpt4,ypt4,zpt4,xpt5,ypt5,zpt5,4)

       xd45=dsqrt((xpt5-xpt4)**2.+(ypt5-ypt4)**2.+(zpt5-zpt4)**2.)

       cl45=(xpt5-xpt4)/xd45
       cm45=(ypt5-ypt4)/xd45
       cn45=(zpt5-zpt4)/xd45

c      Transformacio de coordenades per traslacio i rotacio

       xptp6=xd43*dsin((pi/180.)*phi0(ii,3,corda(i,3)))
       yptp6=0.
       zptp6=xd43*dcos((pi/180.)*phi0(ii,3,corda(i,3)))

       xpt6=cl45*xptp6+cm45*yptp6+cn45*zptp6+xpt4
       ypt6=cl21*xptp6+cm21*yptp6-cn21*zptp6+ypt4
       zpt6=cl43*xptp6+cm43*yptp6+cn43*zptp6+zpt4


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ESPECIAL BHL-PAMPA
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c       iv=corda(i,7)
c       if (iv.eq.0.or.iv.eq.1.or.iv.eq.4.or.iv.eq.5.or.iv.eq.8.or.
c     + iv.eq.9) then
c       xpt6=u(corda(i,7),corda(i,6),19)
c       ypt6=v(corda(i,7),corda(i,6),19)
c       zpt6=w(corda(i,7),corda(i,6),19)
c
c       end if

       iv=corda(i,7)
       if (rib(iv,56).eq.0.) then
       xpt6=u(corda(i,7),corda(i,6),19)
       ypt6=v(corda(i,7),corda(i,6),19)
       zpt6=w(corda(i,7),corda(i,6),19)
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ESPECIAL BHL-PAMPA
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


c      Dibuixa triangles girats

       if (kaaa.eq.0.or.corda(i,6).ne.1) then
       call line3d(xpt3,ypt3,zpt3,xpt6,ypt6,zpt6,1)
       call line3d(xpt1,ypt1,zpt1,xpt6,ypt6,zpt6,2)
       call line3d(xpt2,ypt2,zpt2,xpt6,ypt6,zpt6,2)
       end if

       u(corda(i,7),corda(i,6),19)=xpt6
       v(corda(i,7),corda(i,6),19)=ypt6
       w(corda(i,7),corda(i,6),19)=zpt6

c      No gira b.a. si kaaa=1

       if (kaaa.eq.1.and.corda(i,6).eq.1) then
       u(corda(i,7),corda(i,6),19)=u(corda(i,7),corda(i,6),20)
       v(corda(i,7),corda(i,6),19)=v(corda(i,7),corda(i,6),20)
       w(corda(i,7),corda(i,6),19)=w(corda(i,7),corda(i,6),20)
       end if


       end if

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end if

       end do

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.8 Longituds de les cordes
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,cordam

       xx2=x2line(corda(i,1),corda(i,2),corda(i,3))
       xx1=x1line(corda(i,1),corda(i,2),corda(i,3))
       yy2=y2line(corda(i,1),corda(i,2),corda(i,3))
       yy1=y1line(corda(i,1),corda(i,2),corda(i,3))
       zz2=z2line(corda(i,1),corda(i,2),corda(i,3))
       zz1=z1line(corda(i,1),corda(i,2),corda(i,3))

c      Si parapent ss actualitza posicio ancoratges
       if (atp.eq."ss") then

c      Actualitza nivell 4
       if (corda(i,2).eq.4.and.corda(i,5).eq.4) then

       xx2=u(corda(i,7),corda(i,6),19)
       yy2=v(corda(i,7),corda(i,6),19)
       zz2=w(corda(i,7),corda(i,6),19)

       x2line(corda(i,1),corda(i,2),corda(i,3))=xx2
       y2line(corda(i,1),corda(i,2),corda(i,3))=yy2
       z2line(corda(i,1),corda(i,2),corda(i,3))=zz2

       end if     

c      Actualitza nivell 3
       if (corda(i,2).eq.3.and.corda(i,5).eq.3) then

       xx2=u(corda(i,7),corda(i,6),19)
       yy2=v(corda(i,7),corda(i,6),19)
       zz2=w(corda(i,7),corda(i,6),19)

       x2line(corda(i,1),corda(i,2),corda(i,3))=xx2
       y2line(corda(i,1),corda(i,2),corda(i,3))=yy2
       z2line(corda(i,1),corda(i,2),corda(i,3))=zz2

       end if     

c      Actualitza nivell 2
       if (corda(i,2).eq.2.and.corda(i,5).eq.2) then

       xx2=u(corda(i,7),corda(i,6),19)
       yy2=v(corda(i,7),corda(i,6),19)
       zz2=w(corda(i,7),corda(i,6),19)

       x2line(corda(i,1),corda(i,2),corda(i,3))=xx2
       y2line(corda(i,1),corda(i,2),corda(i,3))=yy2
       z2line(corda(i,1),corda(i,2),corda(i,3))=zz2

       end if

       end if

       xline(i)=dsqrt((xx2-xx1)**2+(yy2-yy1)**2+(zz2-zz1)**2)
       xline2(i)=dsqrt((xcorda(i,2)-xcorda(i,1))**2+
     + (ycorda(i,2)-ycorda(i,1))**2+(zcorda(i,2)-zcorda(i,1))**2)

c      write (*,*) "xline, xline2 ",i,xline(i),xline2(i)

c      write (*,*) "loads ",i, xline(i), xload(i)

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.9 Correccions elastiques
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       write(*,*) "i, xline(i), corda(i,1), corda(i,2), csus(corda(i,1),
c     + corda(i,2)), xload(i), xlide(i)"

       cttt2=0.
       cttt3=0.
       cttt4=0.

       do i=1,cordam

       xlide(i)=xline(i)*(xload(i)/10.)*csus(corda(i,1),corda(i,2))/100.

       if (corda(i,2).eq.1) then
       xlide(i)=0.
       end if

       xlifi(i)=xline(i)-xlide(i)

       if (corda(i,2).eq.2) then
       cttt2=cttt2+xload(i)
       end if

       if (corda(i,2).eq.3) then
       cttt3=cttt3+xload(i)
       end if

       if (corda(i,2).eq.4) then
       cttt4=cttt4+xload(i)
       end if

       end do

c       write (*,*) "Carrega total: ", cttt2*2., cttt3*2., cttt4*2.

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     12.10 Dibuixar cordes 2D
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       corda1=cordam

       do i=1,corda1

       x0=(1260.-160.)*xkf
       y0=1800.*xkf

       x00=1260.*xkf*float(corda(i,1)-1)

c      Colors definition (not used since 2.70 version!)
c      Use iccolor(i) vector
       if (corda(i,1).eq.1) then
       icc=1 ! line color
       end if
       if (corda(i,1).eq.2) then
       icc=30 ! line color
       end if
       if (corda(i,1).eq.3) then
       icc=3 ! line color
       end if
       if (corda(i,1).eq.4) then
       icc=4 ! line color
       end if
       if (corda(i,1).eq.5) then
       icc=5 ! line color
       end if
       if (corda(i,1).eq.6) then
       icc=6 ! line color
       end if

       call line(x1line(corda(i,1),corda(i,2),corda(i,3))+x0+x00,
     + z1line(corda(i,1),corda(i,2),corda(i,3))+y0,
     + x2line(corda(i,1),corda(i,2),corda(i,3))+x0+x00,
     + z2line(corda(i,1),corda(i,2),corda(i,3))+y0,iccolor(corda(i,1)))

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      14. BRAKE CALCULUS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      14.2 Identifica les cordes a calcular
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       ic1=cordam
       ic2=1

       ii=slp+1 ! Pla de frens

       do k=2,8,2 ! Explora fins 4 nivells
       
       do j=1,cam(ii)-1 ! Itera en camins de cada pla

       a=dfloat(mc(ii,j,k))
       b=dfloat(mc(ii,j,k+1))
       aa=dfloat(mc(ii,j+1,k))
       bb=dfloat(mc(ii,j+1,k+1))

       if (a.ne.0..and.b.ne.0.) then ! saltar cordes 0 0

c      Mentre la corda sigui igual augmentar comptador
       if (a.eq.aa.and.b.eq.bb) then

       ic2=ic2+1 ! comptabilitza cordes iguals

c      Si arribem a final del camÃ­ comptabilitzar la corda
       if (j.eq.cam(ii)-1) then

       ic1=ic1+1

c       write (*,*) "corda ", ic1, ic2, " = ", mc(ii,j,k),mc(ii,j,k+1)

       corda(ic1,1)=ii                    !planol
       corda(ic1,2)=mc(ii,j+1,k)          !nivell
       corda(ic1,3)=mc(ii,j+1,k+1)        !ordre
       corda(ic1,4)=ic2                   !punts d'acciÃ³
       corda(ic1,5)=mc(ii,j+1,1)          !ramificacions del camÃ­
       corda(ic1,6)=mc(ii,j+1,14)         !final row
       corda(ic1,7)=mc(ii,j+1,15)         !final rib
       
       ic2=1

       end if

       end if

c      Si canvia la corda al mateix nivell
       if (a.ne.aa.or.b.ne.bb) then

       ic1=ic1+1

c       write (*,*) "corda ", ic1, ic2, " = ", mc(ii,j,k),mc(ii,j,k+1)

       corda(ic1,1)=ii                  !planol
       corda(ic1,2)=mc(ii,j,k)          !nivell
       corda(ic1,3)=mc(ii,j,k+1)        !ordre
       corda(ic1,4)=ic2                 !punts d'acciÃ³
       corda(ic1,5)=mc(ii,j,1)          !ramificacions del camÃ­
       corda(ic1,6)=mc(ii,j,14)         !final row
       corda(ic1,7)=mc(ii,j,15)         !final rib
       
       ic2=1

       end if

c      Si arribem a l'ultima linia i no es zero
       if (j.eq.cam(ii)-1) then

       a=dfloat(mc(ii,j,k))
       b=dfloat(mc(ii,j,k+1))
       aa=dfloat(mc(ii,j+1,k))
       bb=dfloat(mc(ii,j+1,k+1))

       if ((a.ne.aa.or.b.ne.bb).and.(aa.ne.0..and.bb.ne.0.)) then

       ic1=ic1+1

c       write (*,*) "corda ",ic1,ic2," = ", mc(ii,j+1,k),mc(ii,j+1,k+1)

       corda(ic1,1)=ii                    !planol
       corda(ic1,2)=mc(ii,j+1,k)          !nivell
       corda(ic1,3)=mc(ii,j+1,k+1)        !ordre
       corda(ic1,4)=ic2                   !punts d'acciÃ³
       corda(ic1,5)=mc(ii,j+1,1)          !ramificacions del camÃ­
       corda(ic1,6)=mc(ii,j+1,14)         !final row
       corda(ic1,7)=mc(ii,j+1,15)         !final rib
       
       ic2=1

       end if

       end if

       end if

       end do
       end do

       cordat=ic1 ! maxim nombre de cordes inclos les de fre

c      Escriu el vector corda de fre
       do i=cordam+1,cordat

c       write(*,*) "Line ",i," Plan ", corda(i,1)," Level ", corda(i,2),
c     + " Number ", corda(i,3), " Punts A ", corda(i,4)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      14.3 Compute anchor points in 3D space
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Need simplification as uses same code as section 6 (!!!!!)

       do i=1,nribss

       tetha=rib(i,8)*pi/180.
       rot_z=rib(i,250)*pi/180.0
       pos=rib(i,5)*rib(i,251)/100.0

       do j=1,rib(i,15) ! anchor number

c      Airfoil anchor washin coordinates
       u(i,j,17)=(u(i,j,6)-(rib(i,10)/100.)*rib(i,5))*dcos(tetha)+
     + v(i,j,6)*dsin(tetha)+(rib(i,10)/100.)*rib(i,5)
       v(i,j,17)=(-u(i,j,6)+(rib(i,10)/100.)*rib(i,5))*dsin(tetha)+
     + v(i,j,6)*dcos(tetha)-rib(i,50)

c      Airfoil rotation in Z-axis. ( View section 6, MUST be the same )

       wnew(j)=-u(i,j,17)*dsin(rot_z)+pos*dsin(rot_z)
       unew(j)=u(i,j,17)*dcos(rot_z)+pos*(1-dcos(rot_z))
       vnew(j)=v(i,j,17)
       u(i,j,4)=unew(j)
       v(i,j,4)=vnew(j)
       w(i,j,4)=wnew(j)

c      Airfoil anchor (u,v,w) espace coordinates
c       u(i,j,18)=u(i,j,17)
c       v(i,j,18)=v(i,j,17)*dcos(rib(i,9)*pi/180.)
c       w(i,j,18)=-v(i,j,17)*dsin(rib(i,9)*pi/180.)

c      Airfoils rotation in Y-axis
       w(i,j,18)=-w(i,j,4)*dcos(rib(i,9)*pi/180.)-
     + v(i,j,4)*dsin(rib(i,9)*pi/180.)
       u(i,j,18)=u(i,j,4)
       v(i,j,18)=-w(i,j,4)*dsin(rib(i,9)*pi/180.)+
     + v(i,j,4)*dcos(rib(i,9)*pi/180.)

c      Airfoil anchor (x,y,z) absolute coordinates

c       Comment ???????????????????????????? !!!!!
c       u(i,j,19)=rib(i,6)-w(i,j,18)
c       v(i,j,19)=rib(i,3)+u(i,j,18)
c       w(i,j,19)=rib(i,7)-v(i,j,18) 
     

       end do
       end do

       do i=1,nribss
       do j=1,rib(i,15)

       end do

       end do
       
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     14.4 Linies d'accio de cada corda
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Recompute anchors of the brakes, for fractional option

       ii=slp+1
       do j=1,cam(ii)
       if (mc(ii,j,15).lt.nribss) then
       i=mc(ii,j,15)
       u(i,6,19)=(1-brake(j,2))*u(i,6,19)+brake(j,2)*u(i+1,6,19)
       v(i,6,19)=(1-brake(j,2))*v(i,6,19)+brake(j,2)*v(i+1,6,19)
       w(i,6,19)=(1-brake(j,2))*w(i,6,19)+brake(j,2)*w(i+1,6,19)
       end if
       end do

c      Linies d'acció

       do i=cordam+1,cordat ! For all lines

       xcorda(i,3)=0.
       ycorda(i,3)=0.
       zcorda(i,3)=0.

       ii=slp+1 !For brake plans

       do k=2,8,2 ! For all levels

       do j=1,cam(ii) ! For all paths

       if (ii.eq.corda(i,1)) then

       if (corda(i,2).eq.mc(ii,j,k).and.mc(ii,j,k+1).eq.corda(i,3)) then

c      Adaptat a punts d'ancoratge de frens (6)
       xcorda(i,3)=xcorda(i,3)+u(mc(ii,j,15),mc(ii,j,14),19)
       ycorda(i,3)=ycorda(i,3)+v(mc(ii,j,15),mc(ii,j,14),19)
       zcorda(i,3)=zcorda(i,3)+w(mc(ii,j,15),mc(ii,j,14),19)

       end if

       end if

       end do

       end do

c      Center of gravity line i
       xcorda(i,3)=xcorda(i,3)/dfloat(corda(i,4))
       ycorda(i,3)=ycorda(i,3)/dfloat(corda(i,4))
       zcorda(i,3)=zcorda(i,3)/dfloat(corda(i,4))

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      14.5 Punts inicial i final de cada corda
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Level 1 (main brake line)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=cordam+1,cordat

       if (corda(i,2).eq.1) then

c      Frens iniciats sota maillons bandes darrera
       xcorda(i,1)=x2line(slp,1,1)
       ycorda(i,1)=y2line(slp,1,1)
       zcorda(i,1)=z2line(slp,1,1)

c      Equacio parametrica de la recta que passa per P1-P3

       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2.0d0+(ycorda(i,3)-
     + ycorda(i,1))**2.0d0+(zcorda(i,3)-zcorda(i,1))**2.0d0)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necessari a la distancia objectiu

       t=clengb/(dsqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,1,corda(i,3))=xcorda(i,1)
       y1line(ii,1,corda(i,3))=ycorda(i,1)
       z1line(ii,1,corda(i,3))=zcorda(i,1)
       x2line(ii,1,corda(i,3))=xcorda(i,2)
       y2line(ii,1,corda(i,3))=ycorda(i,2)
       z2line(ii,1,corda(i,3))=zcorda(i,2)

c      comprovacio

       disto=dsqrt((xcorda(i,2)-xcorda(i,1))**2+(ycorda(i,2)-
     + ycorda(i,1))**2+(zcorda(i,2)-zcorda(i,1))**2)

       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Level 2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=cordam+1,cordat

       if (corda(i,2).eq.2) then

       if (corda(i,5).eq.2) then ! un nivell adicional


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      REVISAT 2013-05-17 !!!!!!!!!!!!!!!!!!

c      Explora mc i troba quin origen emprar
       kk=slp+1
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,4).and.mc(kk,k,5).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,2)
       comp2(kk)=mc(kk,k,3)

       end if

       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),1,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),1,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),1,int(comp2(corda(i,1))))

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc




c       xcorda(i,1)=x2line(corda(i,1),corda(i,2),corda(i,3))
c       ycorda(i,1)=y2line(corda(i,1),corda(i,2),corda(i,3))
c       zcorda(i,1)=z2line(corda(i,1),corda(i,2),corda(i,3))      

       xcorda(i,2)=u(corda(i,7),corda(i,6),19)
       ycorda(i,2)=v(corda(i,7),corda(i,6),19)
       zcorda(i,2)=w(corda(i,7),corda(i,6),19)

       ii=corda(i,1)

       x1line(ii,2,corda(i,3))=xcorda(i,1)
       y1line(ii,2,corda(i,3))=ycorda(i,1)
       z1line(ii,2,corda(i,3))=zcorda(i,1)
       x2line(ii,2,corda(i,3))=xcorda(i,2)
       y2line(ii,2,corda(i,3))=ycorda(i,2)
       z2line(ii,2,corda(i,3))=zcorda(i,2)
       
       end if

       if (corda(i,5).eq.3) then ! dos nivells adicionals

c       write (*,*) ">>> ", i, corda(i,1), corda(i,2), corda(i,3) 

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      REVISAT 2013-05-03 !!!!!!!!!!!!!!!!!!

c      Explora mc i troba quin origen emprar
       kk=slp+1
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,4).and.mc(kk,k,5).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,2)
       comp2(kk)=mc(kk,k,3)

       end if

       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),1,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),1,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),1,int(comp2(corda(i,1))))

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


c       write (*,*) ">>> ", xcorda(i,1), ycorda(i,1),zcorda(i,1)
                    
       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2.0d0+(ycorda(i,3)-
     + ycorda(i,1))**2.0d0+(zcorda(i,3)-zcorda(i,1))**2.0d0)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       d13=dsqrt((xcorda(i,3)-xcorda(i,1))**2.0d0+(ycorda(i,3)-
     + ycorda(i,1))**2.0d0+(zcorda(i,3)-zcorda(i,1))**2.0d0)
       
       t=(d13-raml(5,3))/(dsqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,2,corda(i,3))=xcorda(i,1)
       y1line(ii,2,corda(i,3))=ycorda(i,1)
       z1line(ii,2,corda(i,3))=zcorda(i,1)
       x2line(ii,2,corda(i,3))=xcorda(i,2)
       y2line(ii,2,corda(i,3))=ycorda(i,2)
       z2line(ii,2,corda(i,3))=zcorda(i,2)
       
       end if

       if (corda(i,5).eq.4) then ! Tres nivells adicionals

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      REVISAT 2013-05-03 !!!!!!!!!!!!!!!!!!

c      Explora mc i troba quin origen emprar
       kk=slp+1
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,4).and.mc(kk,k,5).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,2)
       comp2(kk)=mc(kk,k,3)

       end if

       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),1,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),1,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),1,int(comp2(corda(i,1))))


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       xcorda(i,1)=x2line(corda(i,1),corda(i,2),corda(i,3))
c       ycorda(i,1)=y2line(corda(i,1),corda(i,2),corda(i,3))
c       zcorda(i,1)=z2line(corda(i,1),corda(i,2),corda(i,3))
                    
       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-
     + ycorda(i,1))**2+(zcorda(i,3)-zcorda(i,1))**2)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       d13=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-ycorda(i,1))
     + **2+(zcorda(i,3)-zcorda(i,1))**2)
       
       t=(d13-raml(6,3))/(dsqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,2,corda(i,3))=xcorda(i,1)
       y1line(ii,2,corda(i,3))=ycorda(i,1)
       z1line(ii,2,corda(i,3))=zcorda(i,1)
       x2line(ii,2,corda(i,3))=xcorda(i,2)
       y2line(ii,2,corda(i,3))=ycorda(i,2)
       z2line(ii,2,corda(i,3))=zcorda(i,2)

       end if

       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Level 3
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Inici al final de les cordes 2

       do i=cordam+1,cordat

       if (corda(i,2).eq.3) then

       if (corda(i,5).eq.3) then !directe a l'ancoratge

c      Explora mc i troba quin origen emprar
       kk=slp+1
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,6).and.mc(kk,k,7).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,4)
       comp2(kk)=mc(kk,k,5)

       end if

       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),2,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),2,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),2,int(comp2(corda(i,1))))

       xcorda(i,2)=u(corda(i,7),corda(i,6),19)
       ycorda(i,2)=v(corda(i,7),corda(i,6),19)
       zcorda(i,2)=w(corda(i,7),corda(i,6),19)

       ii=corda(i,1)

       x1line(ii,3,corda(i,3))=xcorda(i,1)
       y1line(ii,3,corda(i,3))=ycorda(i,1)
       z1line(ii,3,corda(i,3))=zcorda(i,1)
       x2line(ii,3,corda(i,3))=xcorda(i,2)
       y2line(ii,3,corda(i,3))=ycorda(i,2)
       z2line(ii,3,corda(i,3))=zcorda(i,2)
       
       end if

c      Si hi ha quatre nivells
       if (corda(i,5).eq.4) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      LEVEL 2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      LEVEL 3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Explora mc i troba quin origen emprar
       kk=slp+1
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,6).and.mc(kk,k,7).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,4)
       comp2(kk)=mc(kk,k,5)

       end if
       
       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),2,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),2,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),2,int(comp2(corda(i,1))))

       dist=dsqrt((xcorda(i,3)-xcorda(i,1))**2+(ycorda(i,3)-
     + ycorda(i,1))**2+(zcorda(i,3)-zcorda(i,1))**2)

       cdl=(xcorda(i,3)-xcorda(i,1))/dist
       cdm=(ycorda(i,3)-ycorda(i,1))/dist
       cdn=(zcorda(i,3)-zcorda(i,1))/dist

c      Parametre necesari a la distancia objectiu

       d13=dsqrt((xcorda(i,3)-xcorda(i,1))**2.0d0+(ycorda(i,3)-
     + ycorda(i,1))**2.0d0+(zcorda(i,3)-zcorda(i,1))**2.0d0)
       
c       t=(raml(6,4)-dl3)/(sqrt(cdl*cdl+cdm*cdm+cdn*cdn))
       t=(raml(6,3)-raml(6,4))/(dsqrt(cdl*cdl+cdm*cdm+cdn*cdn))

c      Punt P2 amb equacio parametrica
       xcorda(i,2)=xcorda(i,1)+cdl*t
       ycorda(i,2)=ycorda(i,1)+cdm*t
       zcorda(i,2)=zcorda(i,1)+cdn*t

       ii=corda(i,1)

       x1line(ii,3,corda(i,3))=xcorda(i,1)
       y1line(ii,3,corda(i,3))=ycorda(i,1)
       z1line(ii,3,corda(i,3))=zcorda(i,1)
       x2line(ii,3,corda(i,3))=xcorda(i,2)
       y2line(ii,3,corda(i,3))=ycorda(i,2)
       z2line(ii,3,corda(i,3))=zcorda(i,2)
       
       end if

       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Level 4
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Inici al final de les cordes 3

       do i=cordam+1,cordat

       if (corda(i,2).eq.4) then

       if (corda(i,5).eq.4) then !directe a l'ancoratge

c      Explora mc i troba quin origen emprar
       kk=slp+1
       do k=1,cam(kk)

       if (corda(i,2).eq.mc(kk,k,8).and.mc(kk,k,9).eq.corda(i,3)) then

       comp1(kk)=mc(kk,k,6)
       comp2(kk)=mc(kk,k,7)

       end if
       
       end do

c      Origen
       xcorda(i,1)=x2line(corda(i,1),3,int(comp2(corda(i,1))))
       ycorda(i,1)=y2line(corda(i,1),3,int(comp2(corda(i,1))))
       zcorda(i,1)=z2line(corda(i,1),3,int(comp2(corda(i,1))))

       xcorda(i,2)=u(corda(i,7),corda(i,6),19)
       ycorda(i,2)=v(corda(i,7),corda(i,6),19)
       zcorda(i,2)=w(corda(i,7),corda(i,6),19)

       ii=corda(i,1)

       x1line(ii,4,corda(i,3))=xcorda(i,1)
       y1line(ii,4,corda(i,3))=ycorda(i,1)
       z1line(ii,4,corda(i,3))=zcorda(i,1)
       x2line(ii,4,corda(i,3))=xcorda(i,2)
       y2line(ii,4,corda(i,3))=ycorda(i,2)
       z2line(ii,4,corda(i,3))=zcorda(i,2)
       
       end if

       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     14.6 Longituds de les cordes
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


      do i=cordam+1,cordat

      xx2=x2line(corda(i,1),corda(i,2),corda(i,3))
      xx1=x1line(corda(i,1),corda(i,2),corda(i,3))
      yy2=y2line(corda(i,1),corda(i,2),corda(i,3))
      yy1=y1line(corda(i,1),corda(i,2),corda(i,3))
      zz2=z2line(corda(i,1),corda(i,2),corda(i,3))
      zz1=z1line(corda(i,1),corda(i,2),corda(i,3))

      xline(i)=dsqrt((xx2-xx1)**2+(yy2-yy1)**2+(zz2-zz1)**2)

      end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     14.7 Dibuixar brakes 2D
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=cordam+1,cordat

       x0=(1260.-160.)*xkf
       y0=(1800.+890.95)*xkf

       x00=1260.*xkf*float(corda(i,1)-1)

       call line(x1line(corda(i,1),corda(i,2),corda(i,3))+x0+x00,
     + z1line(corda(i,1),corda(i,2),corda(i,3))+y0,
     + x2line(corda(i,1),corda(i,2),corda(i,3))+x0+x00,
     + z2line(corda(i,1),corda(i,2),corda(i,3))+y0,iccolor(6))
c     + z2line(corda(i,1),corda(i,2),corda(i,3))+y0,corda(i,1))

       end do

c      Dibuixa distribucio de frenat

       x0=(1260.+890.)*xkf
       y0=(1800.+1000.)*xkf

       xf=rib(nribss,2)/100.

       string1="BRAKE_DISTRIBUTION"
       string2="CENTER"
       string3="WING_TIP"

       call txt(x0,y0-100.*xkf,10.0d0,0.0d0,string1,7)
       call txt(x0,y0-80.*xkf,10.0d0,0.0d0,string2,7)
       call txt(x0+100.*xf,y0-80.*xkf,10.0d0,0.0d0,string3,7)


       call line(x0,y0,x0+rib(nribss,2),y0,4)

       do k=1,5
       call line(x0+bd(k,1)*xf,y0,x0+bd(k,1)*xf,y0-bd(k,2),1)

       write (xstring,'(F6.2)') bd(k,1)
       call txt(x0+bd(k,1)*xf-20.,y0+30.*xkf,10.0d0,0.0d0,xstring,7)

       write (xstring,'(F6.2)') bd(k,2)
       call txt(x0+bd(k,1)*xf-20.,y0-50.*xkf,10.0d0,0.0d0,xstring,7)

       end do

       do k=1,4
       call line(x0+bd(k,1)*xf,y0-bd(k,2),x0+bd(k+1,1)*xf,
     + y0-bd(k+1,2),iccolor(6))
       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      15. Marques de colors
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      15.1 Extrados marks
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marques colors extrados panell i
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,npce ! ribs number with color marks

c      l=mark number in k rib
       do l=1,npc2e(k) ! marks in rib k

c      Detect if mark is exactly in the rib

       if (xpc2e(k,l).eq.0) then

       i=npc1e(k) ! rib number corresponding to k order

c      Detect segment (j,j+1) where color changes
       do j=1,np(i,2)-1

       if ((100.-(u(i,j,2)).le.xpc1e(k,l).and.
     + (100.-u(i,j+1,2)).gt.xpc1e(k,l))) then

       jcontrol=j        

       end if

       end do

c      Calcula longitud extrados fins punt j

       xle(k,l)=0.
       xleinc(k,l)=0.

       do j=1,jcontrol-1
       xle(k,l)=xle(k,l)+sqrt(((v(i,j+1,2)-v(i,j,2))**2)+
     + ((u(i,j+1,2)-u(i,j,2))**2))
       end do

c      Interpolacio punt color

       xmc=(v(i,j+1,2)-v(i,j,2))/(u(i,j+1,2)-u(i,j,2))
       xbc=v(i,j,2)-xmc*u(i,j,2)
       
       xpc3e(k,l)=100.-xpc1e(k,l)
       ypc3e(k,l)=xmc*xpc3e(k,l)+xbc

       xleinc(k,l)=dsqrt(((ypc3e(k,l)-v(i,j,2))**2)+
     + ((xpc3e(k,l)-u(i,j,2))**2))

       xle(k,l)=xle(k,l)+xleinc(k,l)
       
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa marques color esquerra panell i
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Localitza punts 
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=xyshift*xkf

       j=jcontrol

       xu=u(i,j,9)
       xv=v(i,j,9)

c      Calcula punt de color
       alp=abs(datan((v(i,j+1,9)-v(i,j,9))/(u(i,j+1,9)-u(i,j,9))))
       xu=xu+(xleinc(k,l)*(rib(i,5)/100.))*dcos(alp)
       xv=xv+(xleinc(k,l)*(rib(i,5)/100.))*dsin(alp)

c      Dibuixa creu
       call line(psep+xu-3.,-(xv)+psey,psep+xu+3.,
     + -(xv)+psey,7)
       call line(psep+xu,-(xv-3.)+psey,psep+xu,
     + -(xv+3.)+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa marques color dreta panell i-1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       if (i.eq.nribss) then


       i=i-1

c      Localitza punts 
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=xyshift*xkf

       j=jcontrol

       xu=u(i,j,10)
       xv=v(i,j,10)

c      Calcula punt de color
       alp=abs(datan((v(i,j+1,10)-v(i,j,10))/(u(i,j+1,10)-u(i,j,10))))
       xu=xu+(xleinc(k,l)*(rib(i,5)/100.))*dcos(alp)
       xv=xv+(xleinc(k,l)*(rib(i,5)/100.))*dsin(alp)

c      Dibuixa creu
       call line(psep+xu-3.,-(xv)+psey,psep+xu+3.,
     + -(xv)+psey,7)
       call line(psep+xu,-(xv-3.)+psey,psep+xu,
     + -(xv+3.)+psey,7)

c       i=i+1


       end if

       end do

       end do ! rib c colors
 


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      15.2 Intrados marks
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Control if type is not "ss"
       if (atp.ne."ss") then
       
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marques colors intrados panell i
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,npci ! ribs number with color marks

c      l=mark number in k rib
       do l=1,npc2i(k) ! marks in rib k

c      Detect if mark is exactly in the rib

       if (xpc2i(k,l).eq.0) then

       i=npc1i(k) ! rib number corresponding to k order

c      Detect segment (j,j-1) where color changes

       do j=np(i,1),np(i,2)+1,-1

       if ((100.-(u(i,j,2)).le.xpc1i(k,l).and.
     + (100.-u(i,j-1,2)).gt.xpc1i(k,l))) then

       jcontrol=j        

       end if

       end do  ! in j

c      Calcula longitud extrados fins punt j

       xli(k,l)=0.
       xliinc(k,l)=0.

       do j=np(i,1),jcontrol+1,-1
       xli(k,l)=xli(k,l)+sqrt(((v(i,j-1,2)-v(i,j,2))**2)+
     + ((u(i,j-1,2)-u(i,j,2))**2))
       end do

c      Interpolacio punt color

       xmc=(v(i,j,2)-v(i,j-1,2))/(u(i,j,2)-u(i,j-1,2))
       xbc=v(i,j-1,2)-xmc*u(i,j-1,2)
       
       xpc3i(k,l)=100.-xpc1i(k,l)
       ypc3i(k,l)=xmc*xpc3i(k,l)+xbc

       xliinc(k,l)=dsqrt(((ypc3i(k,l)-v(i,j,2))**2)+
     + ((xpc3i(k,l)-u(i,j,2))**2))

       xli(k,l)=xli(k,l)+xliinc(k,l)
       
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa marques color esquerra panell i
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Localitza punts 
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=(890.95+xyshift)*xkf

       j=jcontrol

       xu=u(i,j,9)
       xv=v(i,j,9)

c      Calcula punt de color
       alp=abs(datan((v(i,j,9)-v(i,j-1,9))/(u(i,j,9)-u(i,j-1,9))))
       xu=xu-(xliinc(k,l)*(rib(i,5)/100.))*dcos(alp)
       xv=xv-(xliinc(k,l)*(rib(i,5)/100.))*dsin(alp)

c      Dibuixa creu
       call line(psep+xu-3.,-(xv)+psey,psep+xu+3.,
     + -(xv)+psey,7)
       call line(psep+xu,-(xv-3.)+psey,psep+xu,
     + -(xv+3.)+psey,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Dibuixa marques color dreta panell i-1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=i-1

c      Localitza punts 
       psep=1970.*xkf+seppix(i)*1.0d0
       psey=(890.95+xyshift)*xkf

       j=jcontrol

       xu=u(i,j,10)
       xv=v(i,j,10)

c      Calcula punt de color
       alp=abs(datan((v(i,j,10)-v(i,j-1,10))/(u(i,j,10)-u(i,j-1,10))))
       xu=xu-(xliinc(k,l)*(rib(i,5)/100.))*dcos(alp)
       xv=xv-(xliinc(k,l)*(rib(i,5)/100.))*dsin(alp)

c      Dibuixa creu
       call line(psep+xu-3.,-(xv)+psey,psep+xu+3.,
     + -(xv)+psey,7)
       call line(psep+xu,-(xv-3.)+psey,psep+xu,
     + -(xv+3.)+psey,7)

       i=1+1

       end if

       end do

       end do ! rib c colors intra

       end if ! not "ss"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16. H V and HV ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xvrib=xvrib/10.

c       write (*,*) "xvrib=",xvrib
       
c       do i=0,nribss

c      Impressions de control
c       ii=1

c       write (*,*) "u(i,ii,6) ",i,ii,u(i,ii,6)
c       write (*,*) "np(i,2) ",i, np(i,2),np(i,1)
c       write (*,*) "jcon(i,ii,2) ",jcon(i,ii,2)

c       end do

       do k=1,nhvr

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.1 H straps Type 1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       if (hvr(k,2).eq.1) then

c      Control central cell width
       if (hvr(k,3).gt.0.or.cencell.gt.0.01) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.1.1 Line i (2)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)

c      Points 2,3,4 interpolation in rib i
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do
         

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       uinc=0.
       vinc=0.

       do j=1,21
       ucnt2(i,ii,j)=ucnt(i,ii,2)+uinc
       uinc=uinc+(ucnt(i,ii,4)-ucnt(i,ii,2))/20.

c      warning u=v
c       write (*,*) "u-v ", i,j,u(i,j,3),v(i,j,3)

c      Between 2 and jcon(i,ii,2)+1
       if (ucnt2(i,ii,j).le.u(i,jcon(i,ii,2)+1,3)) then
       xm=(v(i,jcon(i,ii,2)+1,3)-vcnt(i,ii,2))/(u(i,jcon(i,ii,2)+1,3)-
     + ucnt(i,ii,2))
       xb=vcnt(i,ii,2)-xm*ucnt(i,ii,2)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

c      Between jcon(i,ii,2)+1 and jcon(i,ii,4)

       if (ucnt2(i,ii,j).ge.u(i,jcon(i,ii,2)+1,3).and.ucnt2(i,ii,j)
     + .le.u(i,jcon(i,ii,4),3)) then
c      
       do l=jcon(i,ii,2)+1,jcon(i,ii,4)-1

c      Seleccionar tram d'interpolació

       if (ucnt2(i,ii,j).ge.u(i,l,3).and.ucnt2(i,ii,j).le.u(i,l+1,3)) 
     + then
       xm=(v(i,l+1,3)-v(i,l,3))/(u(i,l+1,3)-u(i,l,3))
       xb=v(i,l,3)-xm*u(i,l,3)
       end if
       end do
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
c       write (*,*) "xm, xb ", xm,xb
       end if

c      Between jcon(i,ii,4) and 4       
       if (ucnt2(i,ii,j).gt.u(i,jcon(i,ii,4),3)) then
       xm=(vcnt(i,ii,4)-v(i,jcon(i,ii,4),3))/(ucnt(i,ii,4)-
     + u(i,jcon(i,ii,4),3))
       xb=vcnt(i,ii,4)-xm*ucnt(i,ii,4)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

c       write (*,*) "Line 2 ",i,j,ucnt2(i,ii,j),vcnt2(i,ii,j)

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.1.2 Line i+1 (3)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,5)
       ii=hvr(k,6)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,2)=ucnt(i,ii,3)-(hvr(k,7)+hvr(k,20))
       ucnt(i,ii,4)=ucnt(i,ii,3)+(hvr(k,7)+hvr(k,20))

c       write (*,*) "> ",i,ii,hvr(k,20)

c      Points 2,3,4 interpolation in rib i
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do
         
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       uinc=0.
       vinc=0.

       do j=1,21
       ucnt3(i,ii,j)=ucnt(i,ii,2)+uinc
       uinc=uinc+(ucnt(i,ii,4)-ucnt(i,ii,2))/20.

c      Between 2 and jcon(i,ii,2)+1
       if (ucnt3(i,ii,j).le.u(i,jcon(i,ii,2)+1,3)) then
       xm=(v(i,jcon(i,ii,2)+1,3)-vcnt(i,ii,2))/(u(i,jcon(i,ii,2)+1,3)-
     + ucnt(i,ii,2))
       xb=vcnt(i,ii,2)-xm*ucnt(i,ii,2)
       vcnt3(i,ii,j)=xm*ucnt3(i,ii,j)+xb
       end if

c      Between jcon(i,ii,2)+1 and jcon(i,ii,4)

       if (ucnt3(i,ii,j).ge.u(i,jcon(i,ii,2)+1,3).and.ucnt3(i,ii,j)
     + .le.u(i,jcon(i,ii,4),3)) then
c      
       do l=jcon(i,ii,2)+1,jcon(i,ii,4)-1

c      Seleccionar tram d'interpolació

       if (ucnt3(i,ii,j).ge.u(i,l,3).and.ucnt3(i,ii,j).le.u(i,l+1,3)) 
     + then
       xm=(v(i,l+1,3)-v(i,l,3))/(u(i,l+1,3)-u(i,l,3))
       xb=v(i,l,3)-xm*u(i,l,3)
       end if
       end do
       vcnt3(i,ii,j)=xm*ucnt3(i,ii,j)+xb
       end if

c      Between jcon(i,ii,4) and 4       
       if (ucnt3(i,ii,j).gt.u(i,jcon(i,ii,4),3)) then
       xm=(vcnt(i,ii,4)-v(i,jcon(i,ii,4),3))/(ucnt(i,ii,4)-
     + u(i,jcon(i,ii,4),3))
       xb=vcnt(i,ii,4)-xm*ucnt(i,ii,4)
       vcnt3(i,ii,j)=xm*ucnt3(i,ii,j)+xb
       end if

       end do ! j

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.1.3 Lines 2 and 3 transportation on the space
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Rib i (Line 2)

       i=hvr(k,3)
       ii=hvr(k,4)

       tetha=rib(i,8)*pi/180.
       rot_z=rib(i,250)*pi/180.0
       pos=rib(i,5)*rib(i,251)/100.0

  
       do j=1,21
       ru(i,j,3)=ucnt2(i,ii,j)
       rv(i,j,3)=vcnt2(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       hx2(i,j,ii)=rx(i,j)
       hy2(i,j,ii)=ry(i,j)
       hz2(i,j,ii)=rz(i,j)

       end do


c       write(*,*) "Ep: ",hx2(0,1,1)

c      Rib i+1 (Line 3)

       i=hvr(k,5)
       ii=hvr(k,6)

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt3(i,ii,j)
       rv(i,j,3)=vcnt3(i,ii,j)-rib(i,50)
c      COMPTE AMB el rib(i,50) A ESTUDIAR       
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       hx3(i-1,j,ii)=rx(i,j)
       hy3(i-1,j,ii)=ry(i,j)
       hz3(i-1,j,ii)=rz(i,j)

       end do


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.1.4 H-rib 2-3 in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*tan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Tensa cintes. Calcula i imprimeix distancies...
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       j=10


       hdist(i)=dsqrt((pl1y(i,j)-pr1y(i,j))**2.+
     + (pl1x(i,j)-pr1x(i,J))**2.)
       hangle(i)=datan((pr1y(i,j)-pl1y(i,j))/(pr1x(i,j)-pl1x(i,j)))

c      Ajusta tensió de la cinta

c      Note: if use variable htens not work, I renamed htensi

       htens=htensi

       do j=1,21

       pr1x(i,j)=pr1x(i,j)-htensi*hdist(i)*dcos(hangle(i))
       pr1y(i,j)=pr1y(i,j)-htensi*hdist(i)*dsin(hangle(i))
       pr2x(i,j)=pr2x(i,j)-htensi*hdist(i)*dcos(hangle(i))
       pr2y(i,j)=pr2y(i,j)-htensi*hdist(i)*dsin(hangle(i))

       end do

c      Cintes tensades
       j=10

       hdist(i)=dsqrt((pl1y(i,j)-pr1y(i,j))**2.+
     + (pl1x(i,j)-pr1x(i,J))**2.)
       hangle(i)=datan((pr1y(i,j)-pl1y(i,j))/(pr1x(i,j)-pl1x(i,j)))

c       write (*,*) "dist tensades ", i, "-", i+1, hdist(i), hangle(i)

c      Drawing in 2D model
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

c       write (*,*) i,ii,psep,psey

       j=1

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),30)

       j=21

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),30)

       do j=1,21-1

c      Dibuixa limit esquerre
c       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pl2x(i,j),
c     + psey+pl2y(i,j),1)

c      Dibuixa limit dret
c       call line(psep+pr1x(i,j),psey+pr1y(i,j),psep+pr2x(i,j),
c     + psey+pr2y(i,j),1)


c       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
c     + psey+pr1y(i,j),4)


c      Vores de costura esquerra
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xvrib*dcos(alpl)

c      Vores de costura dreta
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xvrib*dcos(alpr)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + -xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),30)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + +xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),30)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + -xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),30)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + +xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),30)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)
       
       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

       end do

c      Dibuixa punt central de control de costura AD

       alpl=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       xpx=(pl1x(i,1)+pl2x(i,20))/2.-xdes*dsin(alpl)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-xdes*dcos(alpl)

       call point(psep+xpx,psey+xpy,3)

       alpr=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)-pr2x(i,20))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpr)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpr)

       call point(psep+xpx,psey+xpy,1)


c      Etiqueta cintes en romans AD

       pi=4.0d0*datan(1.0d0)

       xpx=(pl1x(i,1)+pl2x(i,20))/2.-xdes*dsin(alpl)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-xdes*dcos(alpl)

c       alpl=(datan((pl2y(i,20)-pl1y(i,1))/(pl2x(i,20)-pl1x(i,1))))

c      write (*,*) "romano", hvr(k,3), hvr(k,4), xvrib, alpl

       xpx2=psep+xpx+0.4*hvr(k,7)*dcos(alpl)-0.6*xvrib*dsin(alpl)
       xpy2=psey+xpy-0.4*hvr(k,7)*dsin(alpl)-0.6*xvrib*dcos(alpl)
       
       call romano(int(hvr(k,3)),xpx2,xpy2,alpl,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.6*hvr(k,7)*dcos(alpl)-0.6*xvrib*dsin(alpl)
       xpy2=psey+xpy+0.6*hvr(k,7)*dsin(alpl)-0.6*xvrib*dcos(alpl)
       
       call romano(int(hvr(k,4)),xpx2,xpy2,alpl,typm6(10)*0.1,7)

c       call line(psep+xpx,psey+xpy,psep+xpx+4.*dcos(alpl),
c     + psey+xpy+4.*dsin(alpl),1)

c      H-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)
     
c      Numera cintes H en decimals (VH type 1)
       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),psey-10,
     + typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)

       pi=4.0d0*datan(1.0d0)

c      Dibuixa vores amb segments completament enllaçats       

       do j=1,20

       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),30)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),30)

       end do

       end if

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2 V ribs partial (Type 2)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,2).eq.2) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.1 Rib i
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Define main points

       i=hvr(k,3)    ! rib i
       ii=hvr(k,4)   ! row ii

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,8)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)


c      Points 2,3,4 interpolation in rib i
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       uinc=0.
       vinc=0.

       do j=1,21
       ucnt2(i,ii,j)=ucnt(i,ii,2)+uinc
       uinc=uinc+(ucnt(i,ii,4)-ucnt(i,ii,2))/20.

c      Between 2 and jcon(i,ii,2)+1
       if (ucnt2(i,ii,j).le.u(i,jcon(i,ii,2)+1,3)) then
       xm=(v(i,jcon(i,ii,2)+1,3)-vcnt(i,ii,2))/(u(i,jcon(i,ii,2)+1,3)-
     + ucnt(i,ii,2))
       xb=vcnt(i,ii,2)-xm*ucnt(i,ii,2)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Between jcon(i,ii,2)+1 and jcon(i,ii,4)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ucnt2(i,ii,j).ge.u(i,jcon(i,ii,2)+1,3).and.ucnt2(i,ii,j)
     + .le.u(i,jcon(i,ii,4),3)) then
c      
       do l=jcon(i,ii,2)+1,jcon(i,ii,4)-1

c      Seleccionar tram d'interpolació

       if (ucnt2(i,ii,j).ge.u(i,l,3).and.ucnt2(i,ii,j).le.u(i,l+1,3)) 
     + then
       xm=(v(i,l+1,3)-v(i,l,3))/(u(i,l+1,3)-u(i,l,3))
       xb=v(i,l,3)-xm*u(i,l,3)
       end if
       end do
c       xm=(v(i,jcon(i,ii,2)+j,3)-v(i,jcon(i,ii,2)+j-1,3))/
c     + (u(i,jcon(i,ii,2)+j,3)-u(i,jcon(i,ii,2)+j-1,3))
c       xb=v(i,jcon(i,ii,2)+j-1,3)-xm*u(i,jcon(i,ii,2)+j-1,3)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

c      Between jcon(i,ii,4) and 4       
       if (ucnt2(i,ii,j).gt.u(i,jcon(i,ii,4),3)) then
       xm=(vcnt(i,ii,4)-v(i,jcon(i,ii,4),3))/(ucnt(i,ii,4)-
     + u(i,jcon(i,ii,4),3))
       xb=vcnt(i,ii,4)-xm*ucnt(i,ii,4)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.2 Rib i-1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)-1
       ii=hvr(k,4)

       hvr(k,19)=hvr(k,8)+hvr(k,15)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,19)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,19)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 1,3,5 interpolation in rib i-1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,1).and.u(i,j+1,3).ge.ucnt(i,ii,1)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,1)=xm*ucnt(i,ii,1)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,5).and.u(i,j+1,3).ge.ucnt(i,ii,5)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,5)=xm*ucnt(i,ii,5)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i-1
       do j=1,np(i,2)

       if (u(i,j,3).ge.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       end if

       end do

c      Calculus of 6,7,8 points in rib i-1
       vcnt(i,ii,6)=(vcnt(i,ii,9)-vcnt(i,ii,1))*(hvr(k,9)/100.)+
     + vcnt(i,ii,1)
       vcnt(i,ii,7)=(vcnt(i,ii,10)-vcnt(i,ii,3))*(hvr(k,9)/100.)+
     + vcnt(i,ii,3)
       vcnt(i,ii,8)=(vcnt(i,ii,11)-vcnt(i,ii,5))*(hvr(k,9)/100.)+
     + vcnt(i,ii,5)

c      Redefinition of points 6,8 if angle is not 90 

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      AQUÍ ÉS EL PROBLEMA!!!!!!!!!!!!!!
c      no és hvr(k,8) ans una valor afectat per hvr(k,17).... o similar!!!!
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

    
       if (hvr(k,10).ne.90.) then
       ucnt(i,ii,6)=ucnt(i,ii,7)-hvr(k,19)*dcos((pi/180.)*hvr(k,10))
       ucnt(i,ii,8)=ucnt(i,ii,7)+hvr(k,19)*dcos((pi/180.)*hvr(k,10))
       vcnt(i,ii,6)=vcnt(i,ii,7)-hvr(k,19)*dsin((pi/180.)*hvr(k,10))
       vcnt(i,ii,8)=vcnt(i,ii,7)+hvr(k,19)*dsin((pi/180.)*hvr(k,10))
       end if

c      Divide line 6-8 in n segments

       uinc=0.
       vinc=0.
       do j=1,21
       ucnt1(i,ii,j)=ucnt(i,ii,6)+uinc
       uinc=uinc+(ucnt(i,ii,8)-ucnt(i,ii,6))/20.
       vcnt1(i,ii,j)=vcnt(i,ii,6)+vinc
       vinc=vinc+(vcnt(i,ii,8)-vcnt(i,ii,6))/20.
       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.3 Rib i+1
cccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)+1
       ii=hvr(k,4)

       hvr(k,19)=hvr(k,8)+hvr(k,17)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,19)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,19)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      NOTE: uso hvr(k,17) car hvr(k,16) no donava be
c       write (*,*) "2>",hvr(k,1),hvr(k,15),hvr(k,8),hvr(k,17)


c      Points 1,3,5 interpolation in rib i+1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,1).and.u(i,j+1,3).ge.ucnt(i,ii,1)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,1)=xm*ucnt(i,ii,1)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,5).and.u(i,j+1,3).ge.ucnt(i,ii,5)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,5)=xm*ucnt(i,ii,5)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i+1
       do j=1,np(i,2)

       if (u(i,j,3).ge.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       end if

       end do

c      Calculus of 6,7,8 points in rib i+1
       vcnt(i,ii,6)=(vcnt(i,ii,9)-vcnt(i,ii,1))*(hvr(k,9)/100.)+
     + vcnt(i,ii,1)
       vcnt(i,ii,7)=(vcnt(i,ii,10)-vcnt(i,ii,3))*(hvr(k,9)/100.)+
     + vcnt(i,ii,3)
       vcnt(i,ii,8)=(vcnt(i,ii,11)-vcnt(i,ii,5))*(hvr(k,9)/100.)+
     + vcnt(i,ii,5)

c      Redefinition of points 6,8 if angle is not 90     
       if (hvr(k,10).ne.90.) then
       ucnt(i,ii,6)=ucnt(i,ii,7)-hvr(k,19)*dcos((pi/180.)*hvr(k,10))
       ucnt(i,ii,8)=ucnt(i,ii,7)+hvr(k,19)*dcos((pi/180.)*hvr(k,10))
       vcnt(i,ii,6)=vcnt(i,ii,7)-hvr(k,19)*dsin((pi/180.)*hvr(k,10))
       vcnt(i,ii,8)=vcnt(i,ii,7)+hvr(k,19)*dsin((pi/180.)*hvr(k,10))
       end if

c      Divide line 6-8 in n segments

       uinc=0.
       vinc=0.
       do j=1,21
       ucnt3(i,ii,j)=ucnt(i,ii,6)+uinc
       uinc=uinc+(ucnt(i,ii,8)-ucnt(i,ii,6))/20.
       vcnt3(i,ii,j)=vcnt(i,ii,6)+vinc
       vinc=vinc+(vcnt(i,ii,8)-vcnt(i,ii,6))/20.
       end do

c      Rib localisation
       i=hvr(k,3)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.4 V-ribs lines 1 2 3 transportation to 3D espace
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Rib i-1 (Line 1)

       i=hvr(k,3)-1

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt1(i,ii,j)
       rv(i,j,3)=vcnt1(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx1(i+1,j,ii)=rx(i,j)
       ry1(i+1,j,ii)=ry(i,j)
       rz1(i+1,j,ii)=rz(i,j)

       end do

c      Rib i (Line 2)

       i=hvr(k,3)

       tetha=rib(i,8)*pi/180.
       
       do j=1,21
       ru(i,j,3)=ucnt2(i,ii,j)
       rv(i,j,3)=vcnt2(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx2(i,j,ii)=rx(i,j)
       ry2(i,j,ii)=ry(i,j)
       rz2(i,j,ii)=rz(i,j)

       end do

c      Rib i+1 (Line 3)

       i=hvr(k,3)+1

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt3(i,ii,j)
       rv(i,j,3)=vcnt3(i,ii,j)-rib(i,50)
c      COMPTE AMB el rib(i,50) A ESTUDIAR       
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx3(i-1,j,ii)=rx(i,j)
       ry3(i-1,j,ii)=ry(i,j)
       rz3(i-1,j,ii)=rz(i,j)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.5.X V-ribs 1-2 and 2-3 in 3D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Return to rib i
       i=hvr(k,3)

c      Rib 1-2 (blue)

       if (hvr(k,5).eq.1) then
       do j=1,21
       call line3d(rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),
     + rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),5)
       call line3d(-rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),
     + -rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),5)
       end do
       end if

c      Rib 2-3 (red)
       if (hvr(k,6).eq.1) then
       do j=1,21
       call line3d(rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),
     + rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),1)
       call line3d(-rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),
     + -rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),1)
       end do
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.5 V-ribs calculus and drawing in 3D and 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.5.1 V-rib 1-2 in 2D model (blue)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)-1

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do

c      Drawing in 2D model
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       if (hvr(k,5).eq.1) then

       j=1

c      Costat vora atac
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),5)

       j=21
c      Costat fuga
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),5)

c      Marca punts MC a l'esquerra

       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pl1x(i,1)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pl1y(i,1)-xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pl1x(i,21)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pl1y(i,21)-xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp7,psey+yp7,1)
       call point(psep+xp8,psey+yp8,1)

c     Romano costat esquerra

      sl=1.
       
      xpx=(pl1x(i,1)+pl2x(i,20))/2.-xdes*dsin(alpha)
      xpy=(pl1y(i,1)+pl2y(i,20))/2.-xdes*dcos(alpha)

      xpx2=psep+xpx+0.5*hvr(k,8)*dcos(alpha)-0.3*xvrib*dsin(alpha)
      xpy2=psey+xpy-0.5*hvr(k,8)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

      call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

      xpx2=psep+xpx-0.5*hvr(k,8)*dcos(alpha)-0.3*xvrib*dsin(alpha)
      xpy2=psey+xpy+0.5*hvr(k,8)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

      call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)


c      Marca punts MC a la dreta

       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)-pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp7=0.5*(pr1x(i,1)+pr2x(i,20))+xdes*dsin(alpha)
       yp7=0.5*(pr1y(i,1)+pr2y(i,20))+xdes*dcos(alpha)

       call point(psep+xp7,psey+yp7,3)


c     Romano costat dret

      sr=1.
       
      xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
      xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

      xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)+0.3*xvrib*dsin(alpha)
      xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

      call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)
       
       do j=1,21-1

c      Vores de costura esquerra
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xvrib*dcos(alpl)

c      Vores de costura dreta
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xvrib*dcos(alpr)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + -xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),5)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + +xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),5)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + -xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),5)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + +xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),5)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)

c      Numera cintes V (Type 2 left side, blue)
       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),psey-10,
     + typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)
   
       end do

c      Dibuixa vores amb segments completament enllaçats       
       do j=1,20

       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),5)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),5)

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.5.2 V-rib 2-3 in 2D model (red)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       if (hvr(k,6).eq.1) then

       j=1

c      Costat vora d'atac
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)

       j=21
c      Costat fuga
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)


c      Marca punts MC a l'esquerra

       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp7=0.5*(pl1x(i,1)+pl1x(i,21))-xdes*dsin(alpha)
       yp7=0.5*(pl1y(i,1)+pl1y(i,21))-xdes*dcos(alpha)

       call point(psep+xp7,psey+yp7,1)

c      Romano costat esquerra

       sl=1.
       
       xpx=(pl1x(i,1)+pl2x(i,20))/2.-sl*xdes*dsin(alpha)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-sl*xdes*dcos(alpha)

       xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)-0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Marca punts MC a la dreta

       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)
     + -pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pr1x(i,1)+xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pr1y(i,1)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pr1x(i,21)+xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pr1y(i,21)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp7,psey+yp7,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat dret

       sr=1.
       
       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

       xpx2=psep+xpx+0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy+0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Vores de costura

       do j=1,21-1

c      Vores de costura esquerra
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xvrib*dcos(alpl)

c      Vores de costura dreta
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xvrib*dcos(alpr)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + -xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),1)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + +xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),1)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + -xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),1)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + +xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),1)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

c      Numera cintes V
c       call itxt(psep-20-xrsep,psey-10,10.0d0,0.0d0,i,7)
c       call itxt(psep+20-xrsep,psey-10,10.0d0,0.0d0,i+1,7)

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)

c      Numera cintes V (Type 2 right side, red)
       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)

       end do

c      Dibuixa vores amb segments completament enllaçats       
       do j=1,20

       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),1)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),1)

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.2.5.3 Drawing V-ribs in 2D ribs, Print and MC
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

c      Rib i-1
       kx=int((float(i-2)/6.))
       ky=i-1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,5).eq.1) then

c      Segment
       call line(sepx+ucnt(i-1,ii,6),-vcnt(i-1,ii,6)+sepy,
     + sepx+ucnt(i-1,ii,8),-vcnt(i-1,ii,8)+sepy,1)
       call line(sepx+2530.*xkf+ucnt(i-1,ii,6),-vcnt(i-1,ii,6)+sepy,
     + sepx+2530.*xkf+ucnt(i-1,ii,8),-vcnt(i-1,ii,8)+sepy,1)

c      Punts marcatge V-rib
       alpha=datan((vcnt(i-1,ii,8)-vcnt(i-1,ii,6))/
     + (ucnt(i-1,ii,8)-ucnt(i-1,ii,6)))
       xp6=ucnt(i-1,ii,6)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp6=vcnt(i-1,ii,6)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=ucnt(i-1,ii,8)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp8=vcnt(i-1,ii,8)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)
       call point(sepx+xp6,sepy-yp6,1)
       call point(sepx+xp7,sepy-yp7,1)
       call point(sepx+xp8,sepy-yp8,1)
       call point(sepx+2530.*xkf+xp6,sepy-yp6,1)
       call point(sepx+2530.*xkf+xp7,sepy-yp7,1)
       call point(sepx+2530.*xkf+xp8,sepy-yp8,1)

       end if

c      Rib i (center)

       kx=int((float(i-1)/6.))
       ky=i-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       call line(sepx+ucnt(i,ii,2),-vcnt(i,ii,2)+sepy,
     + sepx+ucnt(i,ii,4),-vcnt(i,ii,4)+sepy,4)

c      Rib i+1
       kx=int((float(i)/6.))
       ky=i+1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,6).eq.1) then

c      Segment
       call line(sepx+ucnt(i+1,ii,6),-vcnt(i+1,ii,6)+sepy,
     + sepx+ucnt(i+1,ii,8),-vcnt(i+1,ii,8)+sepy,5)
       call line(sepx+2530.*xkf+ucnt(i+1,ii,6),-vcnt(i+1,ii,6)+sepy,
     + sepx+2530.*xkf+ucnt(i+1,ii,8),-vcnt(i+1,ii,8)+sepy,5)

c      Punts marcatge V-rib
       alpha=datan((vcnt(i+1,ii,8)-vcnt(i+1,ii,6))/
     + (ucnt(i+1,ii,8)-ucnt(i+1,ii,6)))
       xp6=ucnt(i+1,ii,6)-xdes*dsin(alpha)
       yp6=vcnt(i+1,ii,6)+xdes*dcos(alpha)
       xp8=ucnt(i+1,ii,8)-xdes*dsin(alpha)
       yp8=vcnt(i+1,ii,8)+xdes*dcos(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)
       call point(sepx+xp6,sepy-yp6,1)
       call point(sepx+xp7,sepy-yp7,1)
       call point(sepx+xp8,sepy-yp8,1)
       call point(sepx+2530.*xkf+xp6,sepy-yp6,1)
       call point(sepx+2530.*xkf+xp7,sepy-yp7,1)
       call point(sepx+2530.*xkf+xp8,sepy-yp8,1)

       end if

       end if ! Type 2



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3 V ribs full Type 3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1 V-ribs full but independent strips
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.1 Rib i
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,2).eq.3) then

c      Define main points 2,3,4,9,10,11

       i=hvr(k,3)    ! rib i
       ii=hvr(k,4)   ! row ii

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,8)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 2,3,4 interpolation in rib i
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       uinc=0.
       vinc=0.

       do j=1,21
       ucnt2(i,ii,j)=ucnt(i,ii,2)+uinc
       uinc=uinc+(ucnt(i,ii,4)-ucnt(i,ii,2))/20.

c      Between 2 and jcon(i,ii,2)+1
       if (ucnt2(i,ii,j).le.u(i,jcon(i,ii,2)+1,3)) then
       xm=(v(i,jcon(i,ii,2)+1,3)-vcnt(i,ii,2))/(u(i,jcon(i,ii,2)+1,3)-
     + ucnt(i,ii,2))
       xb=vcnt(i,ii,2)-xm*ucnt(i,ii,2)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

c      Between jcon(i,ii,2)+1 and jcon(i,ii,4)

       if (ucnt2(i,ii,j).ge.u(i,jcon(i,ii,2)+1,3).and.ucnt2(i,ii,j)
     + .le.u(i,jcon(i,ii,4),3)) then
c      
       do l=jcon(i,ii,2)+1,jcon(i,ii,4)-1

c      Seleccionar tram d'interpolació

       if (ucnt2(i,ii,j).ge.u(i,l,3).and.ucnt2(i,ii,j).le.u(i,l+1,3)) 
     + then
       xm=(v(i,l+1,3)-v(i,l,3))/(u(i,l+1,3)-u(i,l,3))
       xb=v(i,l,3)-xm*u(i,l,3)
       end if
       end do
c       xm=(v(i,jcon(i,ii,2)+j,3)-v(i,jcon(i,ii,2)+j-1,3))/
c     + (u(i,jcon(i,ii,2)+j,3)-u(i,jcon(i,ii,2)+j-1,3))
c       xb=v(i,jcon(i,ii,2)+j-1,3)-xm*u(i,jcon(i,ii,2)+j-1,3)
c      !!!!!!!!!!!!!Revisar
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

c      Between jcon(i,ii,4) and 4       
       if (ucnt2(i,ii,j).gt.u(i,jcon(i,ii,4),3)) then
       xm=(vcnt(i,ii,4)-v(i,jcon(i,ii,4),3))/(ucnt(i,ii,4)-
     + u(i,jcon(i,ii,4),3))
       xb=vcnt(i,ii,4)-xm*ucnt(i,ii,4)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

       end do



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.2 Rib i-1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)-1
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-(hvr(k,8)+hvr(k,15))
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+(hvr(k,8)+hvr(k,15))
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 1,3,5 interpolation in rib i-1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,1).and.u(i,j+1,3).ge.ucnt(i,ii,1)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,1)=xm*ucnt(i,ii,1)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,5).and.u(i,j+1,3).ge.ucnt(i,ii,5)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,5)=xm*ucnt(i,ii,5)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i-1
       do j=1,np(i,2)

       if (u(i,j,3).gt.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       jcon(i,ii,9)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       jcon(i,ii,10)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       jcon(i,ii,11)=j+1
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat 9-10-11 in n spaces (rib i-1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
   
c      Reformat in 20 spaces

       n1vr=jcon(i,ii,9)-jcon(i,ii,11)+1    
       n2vr=20+1

c      Load data polyline
       xlin1(1)=ucnt(i,ii,9)
       ylin1(1)=vcnt(i,ii,9)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon(i,ii,9)-j+1,3)
       ylin1(j)=v(i,jcon(i,ii,9)-j+1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=ucnt(i,ii,11)
       ylin1(n1vr)=vcnt(i,ii,11)

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt1(i,ii,j)=xlin3(j)
       vcnt1(i,ii,j)=ylin3(j)
       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.3 Rib i+1
cccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)+1
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-(hvr(k,8)+hvr(k,16))
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+(hvr(k,8)+hvr(k,16))
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 1,3,5 interpolation in rib i+1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,1).and.u(i,j+1,3).ge.ucnt(i,ii,1)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,1)=xm*ucnt(i,ii,1)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,5).and.u(i,j+1,3).ge.ucnt(i,ii,5)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,5)=xm*ucnt(i,ii,5)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i+1
       do j=1,np(i,2)

       if (u(i,j,3).gt.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       jcon(i,ii,9)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       jcon(i,ii,10)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       jcon(i,ii,11)=j+1
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat 9-10-11 in n spaces (rib i+1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Experimental version     
c      Reformat in 20 spaces

       n1vr=jcon(i,ii,9)-jcon(i,ii,11)+1
       n2vr=20+1

c      Load data polyline
       xlin1(1)=ucnt(i,ii,9)
       ylin1(1)=vcnt(i,ii,9)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon(i,ii,9)-j+1,3)
       ylin1(j)=v(i,jcon(i,ii,9)-j+1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=ucnt(i,ii,11)
       ylin1(n1vr)=vcnt(i,ii,11)

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt3(i,ii,j)=xlin3(j)
       vcnt3(i,ii,j)=ylin3(j)
       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib localisation
       i=hvr(k,3)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.4 V-ribs lines 1 2 3 transportation to 3D espace
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Rib i-1 (Line 1)

       i=hvr(k,3)-1

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt1(i,ii,j)
       rv(i,j,3)=vcnt1(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx1(i+1,j,ii)=rx(i,j)
       ry1(i+1,j,ii)=ry(i,j)
       rz1(i+1,j,ii)=rz(i,j)

       end do

c      Rib i (Line 2)

       i=hvr(k,3)

       tetha=rib(i,8)*pi/180.
       
       do j=1,21
       ru(i,j,3)=ucnt2(i,ii,j)
       rv(i,j,3)=vcnt2(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx2(i,j,ii)=rx(i,j)
       ry2(i,j,ii)=ry(i,j)
       rz2(i,j,ii)=rz(i,j)

       end do

c      Rib i+1 (Line 3)

       i=hvr(k,3)+1

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt3(i,ii,j)
       rv(i,j,3)=vcnt3(i,ii,j)-rib(i,50)
c      COMPTE AMB el rib(i,50) A ESTUDIAR       
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx3(i-1,j,ii)=rx(i,j)
       ry3(i-1,j,ii)=ry(i,j)
       rz3(i-1,j,ii)=rz(i,j)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.5 V-ribs calculus and drawing in 3D and 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.5.1 V-rib 1-2 in 2D model (blue)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)-1

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do

c      Drawing in 2D model
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       if (hvr(k,5).eq.1) then

       j=1
c      Costat vora atac
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),5)

       j=21
c      Costat fuga
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),5)

c      Marca punts MC a l'esquerra

       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pl1x(i,1)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pl1y(i,1)-xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pl1x(i,21)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pl1y(i,21)-xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
c       call point(psep+xp7,psey+yp7,1)
       call point(psep+xp8,psey+yp8,1)

c     Romano costat esquerra

      sl=1.
       
      xpx=(pl1x(i,1)+pl2x(i,20))/2.-xdes*dsin(alpha)
      xpy=(pl1y(i,1)+pl2y(i,20))/2.-xdes*dcos(alpha)

      xpx2=psep+xpx+0.5*hvr(k,8)*dcos(alpha)-0.3*xvrib*dsin(alpha)
      xpy2=psey+xpy-0.5*hvr(k,8)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

      call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

      xpx2=psep+xpx-0.5*hvr(k,8)*dcos(alpha)-0.3*xvrib*dsin(alpha)
      xpy2=psey+xpy+0.5*hvr(k,8)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

      call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)


c      Marca punts MC a la dreta

       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)-pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp7=0.5*(pr1x(i,1)+pr2x(i,20))+xdes*dsin(alpha)
       yp7=0.5*(pr1y(i,1)+pr2y(i,20))+xdes*dcos(alpha)

       call point(psep+xp7,psey+yp7,3)


c     Romano costat dret

      sr=1.
       
      xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
      xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

      xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)+0.3*xvrib*dsin(alpha)
      xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

      call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)
       
       do j=1,21-1

c      Vores de costura esquerra
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xvrib*dcos(alpl)

c      Vores de costura dreta
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xvrib*dsin(alpr)
       rvcy(I,j)=psey+pr1y(i,j)+xvrib*dcos(alpr)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + -xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),5)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + +xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),5)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + -xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),5)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + +xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),5)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)

c      Numera cintes V Type 3
       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)
       
       end do

c      Dibuixa vores amb segments completament enllaçats       
       do j=1,20

       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),5)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),5)

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.5.2 V-rib 2-3 in 2D model (red)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       if (hvr(k,6).eq.1) then

       j=1

c      Costat vora d'atac
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)

       j=21
c      Costat fuga
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)


c      Marca punts MC a l'esquerra

       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp7=0.5*(pl1x(i,1)+pl1x(i,21))-xdes*dsin(alpha)
       yp7=0.5*(pl1y(i,1)+pl1y(i,21))-xdes*dcos(alpha)

       call point(psep+xp7,psey+yp7,1)

c      Romano costat esquerra

       sl=1.
       
       xpx=(pl1x(i,1)+pl2x(i,20))/2.-sl*xdes*dsin(alpha)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-sl*xdes*dcos(alpha)

       xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)-0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Marca punts MC a la dreta

       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)
     + -pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pr1x(i,1)+xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pr1y(i,1)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pr1x(i,21)+xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pr1y(i,21)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
c       call point(psep+xp7,psey+yp7,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat dret

       sr=1.
       
       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

       xpx2=psep+xpx+0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy+0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Vores de costura

       do j=1,21-1

c      Vores de costura esquerra
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xvrib*dcos(alpl)

c      Vores de costura dreta
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xvrib*dcos(alpr)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + -xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),1)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + +xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),1)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + -xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),1)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + +xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),1)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)

c      Numera cintes V Type 3
       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)

       end do

c      Dibuixa vores amb segments completament enllaçats       
       do j=1,20

       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),1)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),1)

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.1.5.3 Drawing V-ribs marks in 2D ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing in 2D ribs printing
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

c      Rib i-1
       kx=int((float(i-2)/6.))
       ky=i-1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,5).eq.1) then
       call line(sepx+ucnt(i-1,ii,9),-vcnt(i-1,ii,9)+sepy,
     + sepx+ucnt(i-1,ii,11),-vcnt(i-1,ii,11)+sepy,4)

c      Draw 3 point in 9 and 11

       alpha=(datan((v(i-1,jcon(i-1,ii,9)-1,3)-v(i-1,jcon(i-1,ii,9)+1,
     + 3))/(u(i-1,jcon(i-1,ii,9)-1,3)-u(i-1,jcon(i-1,ii,9)+1,3))))
       if (alpha.lt.0.) then
c       alpha=alpha+pi
       end if

       xpeq=ucnt(i-1,ii,9)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i-1,ii,9)+1.*xdes*dcos(alpha)

       call point(sepx+xpeq,sepy-ypeq,92)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),92)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),92)

       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,2)
       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),92)
       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),92)


       alpha=(datan((v(i-1,jcon(i-1,ii,11)-1,3)-v(i-1,jcon(i-1,ii,11)+1,
     + 3))/(u(i-1,jcon(i-1,ii,11)-1,3)-u(i-1,jcon(i-1,ii,11)+1,3))))
       if (alpha.lt.0.) then
c       alpha=alpha+pi
       end if

       xpeq=ucnt(i-1,ii,11)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i-1,ii,11)+1.*xdes*dcos(alpha)

       call point(sepx+xpeq,sepy-ypeq,92)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),92)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),92)

       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,92)
       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),92)
       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),92)

c      Marks in V-rib
       alpha=datan((vcnt(i-1,ii,11)-vcnt(i-1,ii,9))/
     + (ucnt(i-1,ii,11)-ucnt(i-1,ii,9)))

       xp9=ucnt(i-1,ii,9)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp9=vcnt(i-1,ii,9)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)

       xp11=ucnt(i-1,ii,11)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp11=vcnt(i-1,ii,11)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)

       xu=sepx+xp9
       xv=-sepy+yp9
c       call pointg(xu,xv,xcir,1)
       xu=sepx+xp11
       xv=-sepy+yp11
c       call pointg(xu,xv,xcir,1)

       end if

c      Rib i (center)
       kx=int((float(i-1)/6.))
       ky=i-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       call line(sepx+ucnt(i,ii,2),-vcnt(i,ii,2)+sepy,
     + sepx+ucnt(i,ii,4),-vcnt(i,ii,4)+sepy,4)

c      Rib i+1
       kx=int((float(i)/6.))
       ky=i+1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,6).eq.1) then
       call line(sepx+ucnt(i+1,ii,9),-vcnt(i+1,ii,9)+sepy,
     + sepx+ucnt(i+1,ii,11),-vcnt(i+1,ii,11)+sepy,3)

c      Punts marcatge V-rib
       alpha=datan((vcnt(i+1,ii,11)-vcnt(i+1,ii,9))/
     + (ucnt(i+1,ii,11)-ucnt(i+1,ii,9)))

       xp9=ucnt(i+1,ii,9)-xdes*dsin(alpha)
       yp9=vcnt(i+1,ii,9)+xdes*dcos(alpha)

       xp11=ucnt(i+1,ii,11)-xdes*dsin(alpha)
       yp11=vcnt(i+1,ii,11)+xdes*dcos(alpha)

       xu=sepx+xp9
       xv=-sepy+yp9
c       call pointg(xu,xv,xcir,1)
       xu=sepx+xp11
       xv=-sepy+yp11
c       call pointg(xu,xv,xcir,1)

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing V-ribs in 2D ribs mesa corte
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

c      Rib i-1
       kx=int((float(i-2)/6.))
       ky=i-1-kx*6

       sepx=2530.*xkf+sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,5).eq.1) then
c      Segment               
       call line(sepx+ucnt(i-1,ii,9),-vcnt(i-1,ii,9)+sepy,
     + sepx+ucnt(i-1,ii,11),-vcnt(i-1,ii,11)+sepy,4)

c      Punts marcatge V-rib
       alpha=datan((vcnt(i-1,ii,11)-vcnt(i-1,ii,9))/
     + (ucnt(i-1,ii,11)-ucnt(i-1,ii,9)))

       xp9=ucnt(i-1,ii,9)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp9=vcnt(i-1,ii,9)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)

       xp11=ucnt(i-1,ii,11)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp11=vcnt(i-1,ii,11)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)

       call point(sepx+xp9,sepy-yp9,3)
       call point(sepx+xp11,sepy-yp11,3)

       end if


c      Rib i+1
       kx=int((float(i)/6.))
       ky=i+1-kx*6

       sepx=2530.*xkf+sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,6).eq.1) then
c      Segment  
       call line(sepx+ucnt(i+1,ii,9),-vcnt(i+1,ii,9)+sepy,
     + sepx+ucnt(i+1,ii,11),-vcnt(i+1,ii,11)+sepy,3)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Draw 3 point in 9 and 11

       alpha=(datan((v(i+1,jcon(i+1,ii,9)-1,3)-v(i+1,jcon(i+1,ii,9)+1,
     + 3))/(u(i+1,jcon(i+1,ii,9)-1,3)-u(i+1,jcon(i+1,ii,9)+1,3))))
       if (alpha.lt.0.) then
c       alpha=alpha+pi
       end if

       xpeq=ucnt(i+1,ii,9)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,9)+1.*xdes*dcos(alpha)

       call point(sepx+xpeq,sepy-ypeq,92)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),92)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),92)

       call point(-2530.*xkf+sepx+xpeq,sepy-ypeq,92)
       call point(-2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),92)
       call point(-2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),92)


       alpha=(datan((v(i+1,jcon(i+1,ii,11)-1,3)-v(i+1,jcon(i+1,ii,11)+1,
     + 3))/(u(i+1,jcon(i+1,ii,11)-1,3)-u(i+1,jcon(i+1,ii,11)+1,3))))
       if (alpha.lt.0.) then
c       alpha=alpha+pi
       end if

       xpeq=ucnt(i+1,ii,11)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,11)+1.*xdes*dcos(alpha)

       call point(sepx+xpeq,sepy-ypeq,92)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),92)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),92)

       call point(-2530.*xkf+sepx+xpeq,sepy-ypeq,5)
       call point(-2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),92)
       call point(-2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),92)



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

           
c      Punts marcatge V-rib
       alpha=datan((vcnt(i+1,ii,11)-vcnt(i+1,ii,9))/
     + (ucnt(i+1,ii,11)-ucnt(i+1,ii,9)))

       xp9=ucnt(i+1,ii,9)-xdes*dsin(alpha)
       yp9=vcnt(i+1,ii,9)+xdes*dcos(alpha)

       xp11=ucnt(i+1,ii,11)-xdes*dsin(alpha)
       yp11=vcnt(i+1,ii,11)+xdes*dcos(alpha)

       call point(sepx+xp9,sepy-yp9,3)
       call point(sepx+xp11,sepy-yp11,3)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw V-rib type 3 in 3D model
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Left rib
       if (hvr(k,5).eq.1) then

       do j=1,21
       call line3d(rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),4)
       call line3d(-rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + -rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),4)
       end do

       end if


c      Right rib
       if (hvr(k,6).eq.1) then

       do j=1,21
       call line3d(rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),3)
       call line3d(-rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + -rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),3)
       end do

       end if


c      end if V-rib type 3

       end if




ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2 Continuous full V-rib type-5
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,2).eq.5) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2.1 Rib i points 2,3,4
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Define main points 2,3,4,9,10,11
c      See schema for points interpretation

       i=hvr(k,3)    ! rib i
c      PLEASE make max hvr(k,4)=rib(i,15)
       ii=hvr(k,4)   ! row ii
      
       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,10)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,10)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Points 2,3,4 interpolation in rib i
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j

c      First 2
       if (ii.eq.1) then
       xtu2(i)=ucnt(i,ii,2)
       xtv2(i)=vcnt(i,ii,2)
       jcon2(i,ii,2)=jcon(i,ii,2)

c      Calcule te-2, variable rib(i,102)
       rib(i,102)=0.
       do jj=np(i,1),jcon2(i,ii,2)+2,-1
       rib(i,102)=rib(i,102)+sqrt((u(i,jj-1,3)-u(i,jj,3))**2+
     + (v(i,jj-1,3)-v(i,jj,3))**2)
       end do
       rib(i,102)=rib(i,102)+sqrt((u(i,jcon2(i,ii,2)+1,3)-ucnt(i,ii,2))
     + **2+(v(i,jcon2(i,ii,2)+1,3)-vcnt(i,ii,2))**2)

       end if

       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j

c      Last 4
       if (ii.eq.rib(i,15)) then
       xtu4(i)=ucnt(i,ii,4)
       xtv4(i)=vcnt(i,ii,4)
       jcon4(i,ii,4)=jcon(i,ii,4)

c      Calcule te-4
       rib(i,104)=0.
       do jj=np(i,1),jcon4(i,ii,4)+2,-1
       rib(i,104)=rib(i,104)+sqrt((u(i,jj-1,3)-u(i,jj,3))**2+
     + (v(i,jj-1,3)-v(i,jj,3))**2)
       end do
       rib(i,104)=rib(i,104)+sqrt((u(i,jcon4(i,ii,4)+1,3)-ucnt(i,ii,4))
     + **2+(v(i,jcon4(i,ii,4)+1,3)-vcnt(i,ii,4))**2)
c      Verificar graficament que OK

       end if

       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Continue calculus c ii max
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,4).eq.rib(i,15)) then

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line "2" in n spaces
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Reformat in 120 spaces
       n1vr=jcon4(i,int(rib(i,15)),4)-jcon2(i,1,2)+1
       n2vr=121

c      Load data polyline
       xlin1(1)=xtu2(i)
       ylin1(1)=xtv2(i)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon2(i,1,2)+j-1,3)
       ylin1(j)=v(i,jcon2(i,1,2)+j-1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=xtu4(i)
       ylin1(n1vr)=xtv4(i)
      
c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt2(i,ii,j)=xlin3(j)
       vcnt2(i,ii,j)=ylin3(j)
c       write (*,*) "Line 2f: ", j, xlin3(j),ylin3(j)
       end do
       
       end if ! Enf if in ii max
   

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2.2 Points 9-10-11 in Rib i-1 and reformat
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      We only need first "9" and last "11"

       i=hvr(k,3)-1
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,10)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,10)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,10)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,10)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 2,3,4 interpolation in rib i-1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i-1 (not used)
       do j=1,np(i,2)

       if (u(i,j,3).gt.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       jcon(i,ii,9)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       jcon(i,ii,10)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       jcon(i,ii,11)=j+1
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Detect first 9 and last 11 (rib i-1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      First 9
       if (ii.eq.1) then

c      Line "r"
       xru(1)=ucnt(i,ii,2)
       xrv(1)=vcnt(i,ii,2)
       xru(2)=ucnt(i,ii,2)-1.
       xrv(2)=vcnt(i,ii,2)+dtan(hvr(k,7)*pi/180.)

c      Look at segments near "A"
       do ki=jcon(i,ii,10),np(i,2)

c      Line "s"
       xsu(1)=u(i,ki,3)
       xsv(1)=v(i,ki,3)
       xsu(2)=u(i,ki+1,3)
       xsv(2)=v(i,ki+1,3)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (xsu(1).ge.xtu.and.xsu(2).lt.xtu.and.xsv(2).ge.0.) then
       xtu9(i)=xtu
       xtv9(i)=xtv
       jcon9(i,ii,2)=ki+1
       end if
     
       end do

c      Dibuix provisional, but in vertical rib!    
c       call line(xru(1),-300-xrv(1),xtu9(i),-300-xtv9(i),7)

       end if   ! First 9

       
c      Last 11
       if (ii.eq.rib(i,15)) then

c      Line "r"
       xru(1)=ucnt(i,ii,4)
       xrv(1)=vcnt(i,ii,4)
       xru(2)=ucnt(i,ii,4)+1.
       xrv(2)=vcnt(i,ii,4)+dtan(hvr(k,8)*pi/180.)

c      Look at segments near "A"
       do ki=1,np(i,2)

c      Line "s"
       xsu(1)=u(i,ki,3)
       xsv(1)=v(i,ki,3)
       xsu(2)=u(i,ki+1,3)
       xsv(2)=v(i,ki+1,3)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (xsu(1).ge.xtu.and.xsu(2).lt.xtu.and.xsv(2).ge.0.) then
       xtu11(i)=xtu
       xtv11(i)=xtv
       jcon11(i,ii,2)=ki+1

c      Calcule te-11
       rib(i,105)=0.
       do jj=1,jcon11(i,ii,2)-2

       rib(i,105)=rib(i,105)+sqrt((u(i,jj+1,3)-u(i,jj,3))**2+
     + (v(i,jj+1,3)-v(i,jj,3))**2)
       end do
ccccccc Ep! rib(1,105) NO.........!ccccccccccccccccccccccccccccccccccc
c       Error corregit 2018-05-12
c       rib(i,105)=rib(1,105)+sqrt((u(i,jcon11(i,ii,2)-1,3)-xtu11(i))
c     + **2+(v(i,jcon11(i,ii,2)-1,3)-xtv11(i))**2)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       rib(i,105)=rib(i,105)+sqrt((u(i,jcon11(i,ii,2)-1,3)-xtu11(i))
     + **2+(v(i,jcon11(i,ii,2)-1,3)-xtv11(i))**2)


       end if
     
       end do

c      Dibuix provisional, but in vertical rib!
c       call line(xru(1),-300-xrv(1),xtu11(i),-300-xtv11(i),7)

       end if   ! Last 11

       end do   ! in points upper surface

c      Calculus of partial lengths in rib i-1

c      Calculus of te-11 length
       if (ii.eq.rib(i,15)) then
       xlte11(i)=0.
       do kl=1,jcon11(i,ii,2)-2
       xlte11(i)=xlte11(i)+sqrt((u(i,kl+1,3)-u(i,kl,3))**2+
     + (v(i,kl+1,3)-v(i,kl,3))**2)
       end do 
       kl=jcon11(i,ii,2)-1
       xlte11(i)=xlte11(i)+sqrt((u(i,kl,3)-xtu11(i))**2+
     + (v(i,kl,3)-xtv11(i))**2)
       end if

c      Calculus of le-9 length
       if (ii.eq.1) then
c       write (*,*) "Epppp   ", jcon9(i,ii,2),np(i,2)
       xlle9(i)=0.
       do kl=jcon9(i,ii,2),np(i,2)-1
       xlle9(i)=xlle9(i)+sqrt((u(i,kl+1,3)-u(i,kl,3))**2+
     + (v(i,kl+1,3)-v(i,kl,3))**2)
       end do 
       kl=jcon9(i,ii,2)
       xlle9(i)=xlle9(i)+sqrt((u(i,kl,3)-xtu9(i))**2+
     + (v(i,kl,3)-xtv9(i))**2)
       end if


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 1 (9-11) in n spaces (rib i-1)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       if (ii.eq.rib(i+1,15)) then ! why i+1?
       if (ii.eq.rib(i,15)) then


c      Reformat in 120 spaces

       n1vr=jcon9(i,1,2)-jcon11(i,int(rib(i,15)),2)+1    
       n2vr=121

c      Load data polyline
       xlin1(1)=xtu9(i)
       ylin1(1)=xtv9(i)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon9(i,1,2)-j+1,3)
       ylin1(j)=v(i,jcon9(i,1,2)-j+1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=xtu11(i)
       ylin1(n1vr)=xtv11(i)

c      Esborrar?       
       do j=1,n1vr-1
c       call line(xlin1(j),-300-ylin1(j),xlin1(j+1),-300-ylin1(j+1),3)
       end do

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt1(i,ii,j)=xlin3(j)
       vcnt1(i,ii,j)=ylin3(j)
       end do

       end if ! ii=rib(i+1,15)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2.3 Points 9-10-11 in Rib i+1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      We only need first "9" and last "11"

       i=hvr(k,3)+1
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,10)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,10)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,10)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,10)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 2,3,4 interpolation in rib i+1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i+1 (not used)
       do j=1,np(i,2)

       if (u(i,j,3).gt.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       jcon(i,ii,9)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       jcon(i,ii,10)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       jcon(i,ii,11)=j+1
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Detect first 9 and last 11 (rib i+1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      First 9
       if (ii.eq.1) then

c      Line "r"
       xru(1)=ucnt(i,ii,2)
       xrv(1)=vcnt(i,ii,2)
       xru(2)=ucnt(i,ii,2)-1.
       xrv(2)=vcnt(i,ii,2)+dtan(hvr(k,7)*pi/180.)

c      Look at segments near "A"
       do ki=jcon(i,ii,10),np(i,2)

c      Line "s"
       xsu(1)=u(i,ki,3)
       xsv(1)=v(i,ki,3)
       xsu(2)=u(i,ki+1,3)
       xsv(2)=v(i,ki+1,3)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (xsu(1).ge.xtu.and.xsu(2).lt.xtu.and.xsv(2).ge.0.) then
       xtu9(i)=xtu
       xtv9(i)=xtv
       jcon9(i,ii,2)=ki+1
       end if
     
       end do

       end if   ! First 9

c      Last 11
       if (ii.eq.rib(i,15)) then

c      Line "r"
       xru(1)=ucnt(i,ii,4)
       xrv(1)=vcnt(i,ii,4)
       xru(2)=ucnt(i,ii,4)+1.
       xrv(2)=vcnt(i,ii,4)+dtan(hvr(k,8)*pi/180.)

c      Look at segments near "A"
       do ki=1,np(i,2)

c      Line "s"
       xsu(1)=u(i,ki,3)
       xsv(1)=v(i,ki,3)
       xsu(2)=u(i,ki+1,3)
       xsv(2)=v(i,ki+1,3)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (xsu(1).ge.xtu.and.xsu(2).lt.xtu.and.xsv(2).ge.0.) then
       xtu11(i)=xtu
       xtv11(i)=xtv
       jcon11(i,ii,2)=ki+1

c      Calcule te-11
       rib(i,105)=0.
       do jj=1,jcon11(i,ii,2)-2
       rib(i,105)=rib(i,105)+sqrt((u(i,jj+1,3)-u(i,jj,3))**2+
     + (v(i,jj+1,3)-v(i,jj,3))**2)
       end do
       rib(i,105)=rib(i,105)+sqrt((u(i,jcon11(i,ii,2)-1,3)-xtu11(i))
     + **2+(v(i,jcon11(i,ii,2)-1,3)-xtv11(i))**2)

       end if
     
       end do

       end if   ! Last 11

       end do

c      Calculus of partial lengths in rib i+1

c      Calculus of te-11 length
       if (ii.eq.rib(i,15)) then
       xrte11(i)=0.
       do kl=1,jcon11(i,ii,2)-2
       xrte11(i)=xrte11(i)+sqrt((u(i,kl+1,3)-u(i,kl,3))**2+
     + (v(i,kl+1,3)-v(i,kl,3))**2)
       end do 
       kl=jcon11(i,ii,2)-1
       xrte11(i)=xrte11(i)+sqrt((u(i,kl,3)-xtu11(i))**2+
     + (v(i,kl,3)-xtv11(i))**2)
       end if

c      Calculus of le-9 length
       if (ii.eq.1) then
c       write (*,*) "Epppp   ", jcon9(i,ii,2),np(i,2)
       xrle9(i)=0.
       do kl=jcon9(i,ii,2),np(i,2)-1
       xrle9(i)=xrle9(i)+sqrt((u(i,kl+1,3)-u(i,kl,3))**2+
     + (v(i,kl+1,3)-v(i,kl,3))**2)
       end do 
       kl=jcon9(i,ii,2)
       xrle9(i)=xrle9(i)+sqrt((u(i,kl,3)-xtu9(i))**2+
     + (v(i,kl,3)-xtv9(i))**2)
c       write (*,*) "xrle9 ok ",i,xrle9(i)
       end if

c      Calculus of partial lengths in rib i (intrados)

c      Calculus of te-4 length
       if (ii.eq.rib(i,15)) then

             end if

c      Calculus of le-2 length
       if (ii.eq.1) then

             end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 3 9-11 in n spaces (rib i+1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      if (ii.eq.rib(i-1,15)) then ! why i-1?
       if (ii.eq.rib(i,15)) then

c      Reformat in 120 spaces

       n1vr=jcon9(i,1,2)-jcon11(i,int(rib(i,15)),2)+1    
       n2vr=121

c      Load data polyline
       xlin1(1)=xtu9(i)
       ylin1(1)=xtv9(i)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon9(i,1,2)-j+1,3)
       ylin1(j)=v(i,jcon9(i,1,2)-j+1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=xtu11(i)
       ylin1(n1vr)=xtv11(i)

       do j=1,n1vr-1
c       call line(xlin1(j),-312-ylin1(j),xlin1(j+1),-312-ylin1(j+1),6)
       end do

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

       do j=1,n2vr-1
c       call line(xlin3(j),-310-ylin3(j),xlin3(j+1),-310-ylin3(j+1),4)
       end do

c      Load result polyline

       do j=1,n2vr
       ucnt3(i,ii,j)=xlin3(j)
       vcnt3(i,ii,j)=ylin3(j)
       end do

       end if ! ii=rib(i-1,15)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib localisation
       i=hvr(k,3)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ii.eq.rib(i,15)) then
       i=hvr(k,3)-1
       do j=1,121
c       write (*,*) "C2: ",ucnt1(i,ii,j),vcnt1(i,ii,j)
       end do
c       write (*,*) "control ", i,ii,j,n2vr
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2.4 Lines 1 2 3 transportation to 3D espace
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ii.eq.rib(i,15)) then

c      Rib i-1 (Line 1)

       i=hvr(k,3)-1

       tetha=rib(i,8)*pi/180.

       do j=1,121
       ru(i,j,3)=ucnt1(i,ii,j)
       rv(i,j,3)=vcnt1(i,ii,j)-rib(i,50)
c       write (*,*) "C3: ",ucnt1(i,ii,j),vcnt1(i,ii,j)
       end do
c       write (*,*) "control ", i,ii,j,n2vr

c      ESBORRAR
c       do j=1,n2vr-1
c       call line(300+ru(i,j,3),-300-rv(i,j,3),
c     + 300+ru(i,j+1,3),-300-rv(i,j+1,3),1)
c       end do


       do j=1,121

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx1(i+1,j,ii)=rx(i,j)
       ry1(i+1,j,ii)=ry(i,j)
       rz1(i+1,j,ii)=rz(i,j)

c       write (*,*) j, rx(i,j),ry(i,j),rz(i,j)


       end do

c      Rib i (Line 2)

       i=hvr(k,3)

       tetha=rib(i,8)*pi/180.
       
       do j=1,121
       ru(i,j,3)=ucnt2(i,ii,j)
       rv(i,j,3)=vcnt2(i,ii,j)-rib(i,50)
       end do

       do j=1,121

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx2(i,j,ii)=rx(i,j)
       ry2(i,j,ii)=ry(i,j)
       rz2(i,j,ii)=rz(i,j)

       end do

c      Rib i+1 (Line 3)

       i=hvr(k,3)+1

       tetha=rib(i,8)*pi/180.

       do j=1,121
       ru(i,j,3)=ucnt3(i,ii,j)
       rv(i,j,3)=vcnt3(i,ii,j)-rib(i,50)
c      COMPTE AMB el rib(i,50) A ESTUDIAR       
       end do

       do j=1,121

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx3(i-1,j,ii)=rx(i,j)
       ry3(i-1,j,ii)=ry(i,j)
       rz3(i-1,j,ii)=rz(i,j)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2.5 V-ribs full Type 5 calculus and drawing in 3D and 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc       
c      16.3.2.5.1 Left rib Type 5 (blue) 1-2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      AQUEST IF es tanca al final del rib 15??????????????????
       if (ii.eq.rib(i,15)) then

       i=hvr(k,3)-1

c      Call flattening subroutine

       call flatt(i,n2vr,rx,ry,rz,
     + pl1x,pl1y,pl2x,pl2y,pr1x,pr1y,pr2x,pr2y)

c      Rotate ribs in 2D
c      Align using right side
       angle=datan((pr1x(i,121)-pr1x(i,1))/(pr1y(i,121)-pr1y(i,1)))
       angle=angle*180./pi
       angle2=angle

       xc=dcos(angle*pi/180.0d0)
       xs=dsin(angle*pi/180.0d0)
      
       do j=1,n2vr
       px9o(j)=xc*pl1x(i,j)-xs*pl1y(i,j)
       py9o(j)=xs*pl1x(i,j)+xc*pl1y(i,j)
       end do
       do j=1,n2vr
       pl1x(i,j)=px9o(j)
       pl1y(i,j)=py9o(j)
       end do

       do j=1,n2vr
       px9o(j)=xc*pl2x(i,j)-xs*pl2y(i,j)
       py9o(j)=xs*pl2x(i,j)+xc*pl2y(i,j)
       end do
       do j=1,n2vr
       pl2x(i,j)=px9o(j)
       pl2y(i,j)=py9o(j)
       end do

       do j=1,n2vr
       px9o(j)=xc*pr1x(i,j)-xs*pr1y(i,j)
       py9o(j)=xs*pr1x(i,j)+xc*pr1y(i,j)
       end do
       do j=1,n2vr
       pr1x(i,j)=px9o(j)
       pr1y(i,j)=py9o(j)
       end do

       do j=1,n2vr
       px9o(j)=xc*pr2x(i,j)-xs*pr2y(i,j)
       py9o(j)=xs*pr2x(i,j)+xc*pr2y(i,j)
       end do
       do j=1,n2vr
       pr2x(i,j)=px9o(j)
       pr2y(i,j)=py9o(j)
       end do
      
c      Drawing in 2D model (BOX 2,7)
       
       psep=5820.*xkf+xrsep*1.6*float(i)-150
       psey=800.*xkf+yrsep*float(ii)-500.

       if (hvr(k,5).eq.1) then

c      Draw basic contour, left and right
       do j=1,120
       call line(psep+pl1x(i,j),psey+pl1y(i,j),
     + psep+pl1x(i,j+1),psey+pl1y(i,j+1),5)
       call line(psep+pr1x(i,j),psey+pr1y(i,j),
     + psep+pr1x(i,j+1),psey+pr1y(i,j+1),5)
       end do

       j=1
       call line(psep+pl1x(i,j),psey+pl1y(i,j),
     + psep+pr1x(i,j),psey+pr1y(i,j),5)

c      xsegment definition
       xsegment=dsqrt((pl1x(i,j)-pr1x(i,j))**2+
     + (pl1y(i,j)-pr1y(i,j))**2)
c      xrvlen
       xrvlen=dsqrt((pr1x(i,1)-pr1x(i,121))**2+
     + (pr1y(i,1)-pr1y(i,121))**2)

       j=121
       call line(psep+pl1x(i,j),psey+pl1y(i,j),
     + psep+pr1x(i,j),psey+pr1y(i,j),5)


c      External edges calculus and drawing

       do j=1,121

c      Edges left
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if
c      Correction in alpl
       if (j.eq.120) then
       alpl120=alpl
       end if
       if (j.eq.121) then
       alpl=alpl120
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xrib*0.1*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xrib*0.1*dcos(alpl)

c      Edges right
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if
c      Correction in alpr
       if (j.eq.120) then
       alpr120=alpr
       end if
       if (j.eq.121) then
       alpr=alpr120
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xrib*0.1*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xrib*0.1*dcos(alpr)

       end do

c      Edges drawing       
       do j=1,120
       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),5)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),5)
       end do

c      Segments drawing

       j=1
       call line(lvcx(i,j),lvcy(i,j),psep+pl1x(i,j),psey+pl1y(i,j),5)
       call line(rvcx(i,j),rvcy(i,j),psep+pr1x(i,j),psey+pr1y(i,j),5)
       j=121
       call line(lvcx(i,j),lvcy(i,j),psep+pl1x(i,j),psey+pl1y(i,j),5)
       call line(rvcx(i,j),rvcy(i,j),psep+pr1x(i,j),psey+pr1y(i,j),5)

c      Calculus of 9-11 length in planar rib i-1
        
       xl911(i)=0.
       do j=1,120
       xl911(i)=xl911(i)+sqrt((pl1x(i,j)-pl1x(i,j+1))**2+
     + (pl1y(i,j)-pl1y(i,j+1))**2)
       end do 

c      Calculus of 2-4 length in planar rib i-1 (rib i)
        
       xc24(i+1)=0.
       do j=1,120
       xc24(i+1)=xc24(i+1)+sqrt((pr1x(i,j)-pr1x(i,j+1))**2+
     + (pr1y(i,j)-pr1y(i,j+1))**2)
       end do 


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      VERIFICATION left     
c       write (*,*) "Rib i-1 ",i,xlle9(i),xl911(i),xlte11(i),rib(i,31),
c     + xlle9(i)+xl911(i)+xlte11(i) !OK
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Naming and marks in V-rib full continous (left-blue)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)

c      Naming ribs with number

       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10.,typm3(10),0.0d0,i,7)
       call itxt(psep-xrsep+hvr(k,15)+83.*xkf-120.*(typm3(10)/10.),
     + psey-10.,typm3(10),0.0d0,i+1,7)


c      Mark rib at left (roman number) 

       alpha=-(datan((pl1y(i,1)-pr1y(i,1))/(pl1x(i,1)-pr1x(i,1))))

       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       sl=1.
       
       xpx=pl1x(i,1)*0.8+pr1x(i,1)*0.2-0.2*xrib*dsin(alpha) !double xrib
       xpy=pl1y(i,1)*0.8+pr1y(i,1)*0.2-0.2*xrib*dcos(alpha)
       xpx2=psep+xpx
       xpy2=psey+xpy

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Mark rib at right (roman number) 

       alpha=-(datan((pl1y(i,1)-pr1y(i,1))/(pl1x(i,1)-pr1x(i,1))))

       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       sr=1.
       
       xpx=pl1x(i,1)*0.2+pr1x(i,1)*0.8-0.2*xrib*dsin(alpha)
       xpy=pl1y(i,1)*0.2+pr1y(i,1)*0.8-0.2*xrib*dcos(alpha) 
       xpx2=psep+xpx
       xpy2=psey+xpy

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Mark equidistant points in left rib (upper surface)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       jcontrol=1

       do jm=1,60 ! Till 60 marks

       xmarkjm=xmark*float(jm)

c      Draw only in rib
       if (xmarkjm.ge.rib(i,105).and.xmarkjm.le.rib(i,105)+xl911(i)) 
     + then

c      Define rib(i,106) only for first mark
       if (jcontrol.eq.1) then
       rib(i,106)=xmarkjm-rib(i,105)
       end if
       jcontrol=0

       xlen=0.
       xlenp=dsqrt((pl1x(i,121)-pl1x(i,120))**2+
     + (pl1y(i,121)-pl1y(i,120))**2)  ! Acumulated length

       do j=121,3,-1
       
c      Detect and draw equidistant point
       if (xmarkjm-rib(i,105).ge.xlen.and.xmarkjm-rib(i,105).lt.xlenp) 
     + then

       rib(i,107)=xmarkjm-xlen-rib(i,105)
       rib(i,108)=dsqrt((pl1x(i,j-1)-pl1x(i,j))**2+
     + (pl1y(i,j-1)-pl1y(i,j))**2)

c      Interpolate
       xequis=pl1x(i,j)-(rib(i,107)*(pl1x(i,j)-pl1x(i,j-1)))/rib(i,108)
       yequis=pl1y(i,j)-(rib(i,107)*(pl1y(i,j)-pl1y(i,j-1)))/rib(i,108)

c      Draw
       alpha=-(datan((pl1y(i,j)-pl1y(i,j-1))/(pl1x(i,j)-pl1x(i,j-1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xpeq=xequis-1.*xdes*dsin(alpha)
       ypeq=yequis+1.*xdes*dcos(alpha)

       call point (psep+xpeq,psey+ypeq,3)

       end if ! detect point

c      Set xlen, xlenp for next segment
       xlen=xlen+sqrt((pl1x(i,j)-pl1x(i,j-1))**2+
     + (pl1y(i,j)-pl1y(i,j-1))**2)
       xlenp=xlen+sqrt((pl1x(i,j-1)-pl1x(i,j-2))**2+
     + (pl1y(i,j-1)-pl1y(i,j-2))**2)

       end do ! contour V-rib

       end if ! marks zone

       end do ! marks jm

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Mark equidistant points in bottom surface (rib i+1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Move to rib i+1

       jcontrol=1

       do jm=1,60 ! Till 50 marks

       xmarkjm=xmark*float(jm)

c      Draw only in rib
       if (xmarkjm.ge.rib(i+1,104).and.xmarkjm.le.rib(i+1,104)+
     + xc24(i+1)) then

c      Define rib(i,106) only for first mark
       if (jcontrol.eq.1) then
       rib(i+1,106)=xmarkjm-rib(i+1,104)
       end if
       jcontrol=0

       xlen=0.
       xlenp=dsqrt((pr1x(i,121)-pr1x(i,120))**2+
     + (pr1y(i,121)-pr1y(i,120))**2)

       do j=121,3,-1
       
c      Detect and draw equidistant point
       if (xmarkjm-rib(i+1,104).ge.xlen.and.xmarkjm-rib(i+1,104).lt.
     + xlenp) then

       rib(i+1,107)=xmarkjm-xlen-rib(i+1,104)
       rib(i+1,108)=dsqrt((pr1x(i,j-1)-pr1x(i,j))**2+
     + (pr1y(i,j-1)-pr1y(i,j))**2)

c      Interpolate
       xequis=pr1x(i,j)-(rib(i+1,107)*(pr1x(i,j)-pr1x(i,j-1)))/
     + rib(i+1,108)
       yequis=pr1y(i,j)-(rib(i+1,107)*(pr1y(i,j)-pr1y(i,j-1)))/
     + rib(i+1,108)

c      Draw
       alpha=-(datan((pr1y(i,j)-pr1y(i,j-1))/(pr1x(i,j)-pr1x(i,j-1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xpeq=xequis+1.*xdes*dsin(alpha)
       ypeq=yequis-1.*xdes*dcos(alpha)

       call point (psep+xpeq,psey+ypeq,3)

       end if ! detect point

       xlen=xlen+sqrt((pr1x(i,j)-pr1x(i,j-1))**2+
     + (pr1y(i,j)-pr1y(i,j-1))**2)
       xlenp=xlen+sqrt((pr1x(i,j-1)-pr1x(i,j-2))**2+
     + (pr1y(i,j-1)-pr1y(i,j-2))**2)

       end do ! contour V-rib

       end if ! marks zone

       end do ! marks jm

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Mark anchor points in left rib
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,rib(i+1,15)

       xlen=0.
       xlenp=dsqrt((pr1x(i,121)-pr1x(i,120))**2+
     + (pr1y(i,121)-pr1y(i,120))**2)

       do j=121,3,-1

c      Detect and draw anchor point
       if (rib(i+1,130+klz)-rib(i+1,104).ge.xlen.and.
     + rib(i+1,130+klz)-rib(i+1,104).lt.
     + xlenp) then

    
       rib(i+1,107)=rib(i+1,130+klz)-xlen-rib(i+1,104)
       rib(i+1,108)=dsqrt((pr1x(i,j-1)-pr1x(i,j))**2+
     + (pr1y(i,j-1)-pr1y(i,j))**2)

c      Interpolate
       xequis=pr1x(i,j)-(rib(i+1,107)*(pr1x(i,j)-pr1x(i,j-1)))/
     + rib(i+1,108)
       yequis=pr1y(i,j)-(rib(i+1,107)*(pr1y(i,j)-pr1y(i,j-1)))/
     + rib(i+1,108)

c      Define anchor points in planar V-rib
       xanchor(i+1,klz)=xequis
       yanchor(i+1,klz)=yequis

c      Draw
       alpha=-(datan((pr1y(i,j)-pr1y(i,j-1))/(pr1x(i,j)-pr1x(i,j-1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xpeq=xequis+1.*xdes*dsin(alpha)
       ypeq=yequis-1.*xdes*dcos(alpha)

c      Girar angle
       call point (psep+xpeq,psey+ypeq,30)
       call point (psep+xpeq-1.,psey+ypeq,30)
       call point (psep+xpeq-2.,psey+ypeq,30)

       end if ! detect point

       xlen=xlen+sqrt((pr1x(i,j)-pr1x(i,j-1))**2+
     + (pr1y(i,j)-pr1y(i,j-1))**2)
       xlenp=xlen+sqrt((pr1x(i,j-1)-pr1x(i,j-2))**2+
     + (pr1y(i,j-1)-pr1y(i,j-2))**2)

       end do ! in contour

       end do ! in anchors

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw parabolic holes in left rib
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       do klz=1,rib(i+1,15)-1

       xprb(i+1,klz,0)=(xanchor(i+1,klz)+xanchor(i+1,klz+1))/2.
       yprb(i+1,klz,0)=(yanchor(i+1,klz)+yanchor(i+1,klz+1))/2.

       do j=1,120

c      Point 5
       if (pl1y(i,j).le.yprb(i+1,klz,0).and.pl1y(i,j+1).gt.
     + yprb(i+1,klz,0)) then

       xm=(pl1y(i,j+1)-pl1y(i,j))/(pl1x(i,j+1)-pl1x(i,j))
       xb=pl1y(i,j)-xm*pl1x(i,j)

       yprb(i+1,klz,5)=yprb(i+1,klz,0)
       xprb(i+1,klz,5)=(yprb(i+1,klz,5)-xb)/xm
       
c      Point 6
       dist05=xprb(i+1,klz,0)-xprb(i+1,klz,5)
       dist06=dist05*hvr(k,9)/100.
       yprb(i+1,klz,6)=yprb(i+1,klz,0)
       xprb(i+1,klz,6)=xprb(i+1,klz,0)-dist06
       end if

c      Point 1

       if (pr1y(i,j).le.yanchor(i+1,klz)+hvr(k,10).and.pr1y(i,j+1).gt.
     + yanchor(i+1,klz)+hvr(k,10)) then

       xm=(pr1y(i,j+1)-pr1y(i,j))/(pr1x(i,j+1)-pr1x(i,j))
       xb=pr1y(i,j)-xm*pr1x(i,j)

       yprb(i+1,klz,1)=yanchor(i+1,klz)+hvr(k,10)
       xprb(i+1,klz,1)=(yprb(i+1,klz,1)-xb)/xm
       end if

       end do ! end j

       end do ! end klz


       do klz=1,rib(i+1,15)-1

       do j=1,120

c      Point 2 Intersection right side parabola with airfoil contour

       if (pr1y(i,j).ge.yprb(i+1,klz,0).and.pr1y(i,j).lt.
     + yanchor(i+1,klz+1)) then

c      Line "r" (parabola)

       xkprb(klz)=(xprb(i+1,klz,1)-xprb(i+1,klz,6))/
     + ((yprb(i+1,klz,1)-yprb(i+1,klz,6))**2.)

       xru(1)=xkprb(klz)*((pr1y(i,j)-yprb(i+1,klz,6))**2.)+
     + xprb(i+1,klz,6)
       xrv(1)=pr1y(i,j)
       xru(2)=xkprb(klz)*((pr1y(i,j+1)-yprb(i+1,klz,6))**2.)+
     + xprb(i+1,klz,6)
       xrv(2)=pr1y(i,j+1)

c      Line "s" (bottom surface)

       xsu(1)=pr1x(i,j)
       xsv(1)=pr1y(i,j)
       xsu(2)=pr1x(i,j+1)
       xsv(2)=pr1y(i,j+1)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)


       if (xsv(1).le.xtv.and.xsv(2).gt.xtv) then  !!REVISAR
       yprb(i+1,klz,2)=xtv
       xprb(i+1,klz,2)=xtu
       end if  


       end if   

       end do ! in j

      
c       call line(psep+xprb(i+1,klz,0),psey+yprb(i+1,klz,0),
c     + psep+xprb(i+1,klz,6),psey+yprb(i+1,klz,6),2)

c       call line(psep+xprb(i+1,klz,1),psey+yprb(i+1,klz,1),
c     + psep+xprb(i+1,klz,6),psey+yprb(i+1,klz,6),3)

c       call line(psep+xprb(i+1,klz,2),psey+yprb(i+1,klz,2),
c     + psep+xprb(i+1,klz,6),psey+yprb(i+1,klz,6),1)

c      Draw parabolas


c      Detect extremal points
       do j=1,120

       if (pr1y(i,j).le.yprb(i+1,klz,1).and.pr1y(i,j+1).gt.
     + yprb(i+1,klz,1)) then
       jconi(klz)=j+1
       end if
       if (pr1y(i,j).le.yprb(i+1,klz,2).and.pr1y(i,j+1).gt.
     + yprb(i+1,klz,2)) then
       jconf(klz)=j
       end if

       end do

c      Draw parabolas

       if (hvr(k,9).le.100.) then

       j=jconi(klz)
       xpa1=xkprb(klz)*((pr1y(i,j)-yprb(i+1,klz,6))**2.)+
     + xprb(i+1,klz,6)
       call line(psep+xprb(i+1,klz,1),psey+yprb(i+1,klz,1),
     + psep+xpa1,psey+pr1y(i,j),5)
       do j=jconi(klz),jconf(klz)-1
       xpa1=xkprb(klz)*((pr1y(i,j)-yprb(i+1,klz,6))**2.)+
     + xprb(i+1,klz,6)
       xpa2=xkprb(klz)*((pr1y(i,j+1)-yprb(i+1,klz,6))**2.)+
     + xprb(i+1,klz,6)
       call line(psep+xpa1,psey+pr1y(i,j),
     + psep+xpa2,psey+pr1y(i,j+1),5)
       end do
       j=jconf(klz)
       xpa1=xkprb(klz)*((pr1y(i,j)-yprb(i+1,klz,6))**2.)+
     + xprb(i+1,klz,6)
       call line(psep+xprb(i+1,klz,2),psey+yprb(i+1,klz,2),
     + psep+xpa1,psey+pr1y(i,j),5)

       end if

       
c      Draw ellipses

       if (hvr(k,9).gt.100) then

       xprb(i+1,klz,7)=(xprb(i+1,klz,0)+xprb(i+1,klz,5))/2.
       yprb(i+1,klz,7)=yprb(i+1,klz,0)
       
       xa=0.5d0*((xprb(i+1,klz,0)-xprb(i+1,klz,5))*
     + (1.0d0-(2.0d0*(hvr(k,9)-100.0d0)/100.0d0)))
       xb=0.5d0*(yprb(i+1,klz,2)-yprb(i+1,klz,1)-2.*hvr(k,10))

       xgir=0.0d0

       do j=1,100-2.*pi/100.

       xsu(1)=xprb(i+1,klz,7)+xa*dcos(xgir)
       xsv(1)=yprb(i+1,klz,7)+xb*dsin(xgir)
       xsu(2)=xprb(i+1,klz,7)+xa*dcos(xgir+2.*pi/100.)
       xsv(2)=yprb(i+1,klz,7)+xb*dsin(xgir+2.*pi/100.)

       call line(psep+xsu(1),psey+xsv(1),psep+xsu(2),psey+xsv(2),5)

       xgir=xgir+2.0d0*pi/100.0d0

       end do

       end if

       end do ! in klz

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw left diagonal in 3D space
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ii.eq.rib(i,15)) then
       
       do j=1,121
       call line3d(rx2(i+1,j,ii),ry2(i+1,j,ii),rz2(i+1,j,ii),
     + rx1(i+1,j,ii),ry1(i+1,j,ii),rz1(i+1,j,ii),5)
       call line3d(-rx2(i+1,j,ii),ry2(i+1,j,ii),rz2(i+1,j,ii),
     + -rx1(i+1,j,ii),ry1(i+1,j,ii),rz1(i+1,j,ii),5)
       end do
       end if

       end if ! Draw left diagonal


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc       
c      16.3.2.5.2 Right rib (red) 2-3
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      i=hvr(k,3)+1 ? NO
       i=hvr(k,3)

c      Call flattening subroutine

       call flatt(i,n2vr,rx,ry,rz,
     + pl1x,pl1y,pl2x,pl2y,pr1x,pr1y,pr2x,pr2y)

c      Rotate ribs in 2D
c      Align using left side
       angle=datan((pr1x(i,121)-pr1x(i,1))/(pr1y(i,121)-pr1y(i,1)))
       angle=angle*180./pi

       xc=dcos(angle*pi/180.)
       xs=dsin(angle*pi/180.)

c      And do displacement using xsegment and angle2 defined in left rib
       xdx=xsegment*dcos(angle2*pi/180)
       xdy=xsegment*dsin(angle2*pi/180)

       do j=1,n2vr
       px9o(j)=xc*pl1x(i,j)-xs*pl1y(i,j)
       py9o(j)=xs*pl1x(i,j)+xc*pl1y(i,j)+xdy
       end do
       do j=1,n2vr
       pl1x(i,j)=px9o(j)
       pl1y(i,j)=py9o(j)
       end do

       do j=1,n2vr
       px9o(j)=xc*pl2x(i,j)-xs*pl2y(i,j)
       py9o(j)=xs*pl2x(i,j)+xc*pl2y(i,j)+xdy
       end do
       do j=1,n2vr
       pl2x(i,j)=px9o(j)
       pl2y(i,j)=py9o(j)
       end do

       do j=1,n2vr
       px9o(j)=xc*pr1x(i,j)-xs*pr1y(i,j)
       py9o(j)=xs*pr1x(i,j)+xc*pr1y(i,j)+xdy
       end do
       do j=1,n2vr
       pr1x(i,j)=px9o(j)
       pr1y(i,j)=py9o(j)
       end do

       do j=1,n2vr
       px9o(j)=xc*pr2x(i,j)-xs*pr2y(i,j)
       py9o(j)=xs*pr2x(i,j)+xc*pr2y(i,j)+xdy
       end do
       do j=1,n2vr
       pr2x(i,j)=px9o(j)
       pr2y(i,j)=py9o(j)
       end do


c      Drawing in 2D model
       
       psep=5820.*xkf+xrsep*1.6*float(i-1)+1.5*xsegment-150
       psey=800.*xkf+yrsep*float(ii)-500.

       if (hvr(k,6).eq.1) then

c      Draw basic contour
       do j=1,120
       call line(psep+pl1x(i,j),psey+pl1y(i,j),
     + psep+pl1x(i,j+1),psey+pl1y(i,j+1),1)
       call line(psep+pr1x(i,j),psey+pr1y(i,j),
     + psep+pr1x(i,j+1),psey+pr1y(i,j+1),1)
       end do

       j=1
       call line(psep+pl1x(i,j),psey+pl1y(i,j),
     + psep+pr1x(i,j),psey+pr1y(i,j),1)
       j=121
       call line(psep+pl1x(i,j),psey+pl1y(i,j),
     + psep+pr1x(i,j),psey+pr1y(i,j),1)


c      External edges calculus and drawing

       do j=1,121

c      Edges left
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

c      Correction in alpl
       if (j.eq.120) then
       alpl120=alpl
       end if
       if (j.eq.121) then
       alpl=alpl120
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xrib*0.1*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xrib*0.1*dcos(alpl)

c      Edges right
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if
c      Correction in alpr
       if (j.eq.120) then
       alpr120=alpr
       end if
       if (j.eq.121) then
       alpr=alpr120
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xrib*0.1*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xrib*0.1*dcos(alpr)

       end do

c      Edges drawing       
       do j=1,120
       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),1)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),1)
       end do

c      Segments drawing
       j=1
       call line(lvcx(i,j),lvcy(i,j),psep+pl1x(i,j),psey+pl1y(i,j),1)
       call line(rvcx(i,j),rvcy(i,j),psep+pr1x(i,j),psey+pr1y(i,j),1)
       j=121
       call line(lvcx(i,j),lvcy(i,j),psep+pl1x(i,j),psey+pl1y(i,j),1)
       call line(rvcx(i,j),rvcy(i,j),psep+pr1x(i,j),psey+pr1y(i,j),1)


c      Calculus of 9-11 length in planar rib i+1
        
       xr911(i+1)=0.
       do j=1,120
       xr911(i+1)=xr911(i+1)+sqrt((pr1x(i,j)-pr1x(i,j+1))**2+
     + (pr1y(i,j)-pr1y(i,j+1))**2)
       end do 

c      Calculus of 2-4 length in planar rib i
        
       xc24i=xc24(i) ! Left side
       xc24(i)=0.
       do j=1,120
       xc24(i)=xc24(i)+sqrt((pl1x(i,j)-pl1x(i,j+1))**2+
     + (pl1y(i,j)-pl1y(i,j+1))**2)
       end do 

c       write (*,*) "xc24(i) ",i,xc24i,xc24(i)
c      Petites diferencies 1 mm a corregir


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      VERIFICATION right     
c       write (*,*) "Rib i+1 ",i+1,xrle9(i+1),xr911(i+1),xrte11(i+1),
c     + rib(i+1,31),xrle9(i+1)+xr911(i+1)+xrte11(i+1) !
c      Hi ha petit error de 1 mm, a revisar (potser calcul r influ)
c      menys exacte r que l? a rutina planar
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Naming and marks in V-rib (right-red)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.+
     + (lvcy(i,1)-rvcy(i,1))**2.)

c      Naming ribs with number

       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i,7)
       call itxt(psep-xrsep+hvr(k,15)+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)

       
c      Mark rib at left (roman number) 

       alpha=-(datan((pl1y(i,1)-pr1y(i,1))/(pl1x(i,1)-pr1x(i,1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       sl=1.
       
       xpx=pl1x(i,1)*0.8+pr1x(i,1)*0.2+0.2*xrib*dsin(alpha) !double xrib
       xpy=pl1y(i,1)*0.8+pr1y(i,1)*0.2+0.2*xrib*dcos(alpha) 
       xpx2=psep+xpx
       xpy2=psey+xpy

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Mark rib at right (roman number) 

       alpha=-(datan((pl1y(i,1)-pr1y(i,1))/(pl1x(i,1)-pr1x(i,1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       sr=1.
       
       xpx=pl1x(i,1)*0.2+pr1x(i,1)*0.8+0.2*xrib*dsin(alpha)
       xpy=pl1y(i,1)*0.2+pr1y(i,1)*0.8+0.2*xrib*dcos(alpha)
       xpx2=psep+xpx
       xpy2=psey+xpy

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Mark equidistant points in right rib (upper surface) rib i+1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       jcontrol=1

       do jm=1,60 ! Till 50 marks

       xmarkjm=xmark*float(jm)

c      Draw only in rib
       if (xmarkjm.ge.rib(i+1,105).and.xmarkjm.le.rib(i+1,105)+
     + xr911(i+1)) then

c      Define rib(i+1,106) only for first mark
       if (jcontrol.eq.1) then
       rib(i+1,106)=xmarkjm-rib(i+1,105)
       end if
       jcontrol=0

       xlen=0.
       xlenp=dsqrt((pr1x(i,121)-pr1x(i,120))**2+
     + (pr1y(i,121)-pr1y(i,120))**2)

       do j=121,3,-1  !!!!! REVISAR !!!!!!!!!!!!!!
c       do j=120,3,-1
       
c      Detect and draw equidistant point
       if (xmarkjm-rib(i+1,105).ge.xlen.and.xmarkjm-rib(i+1,105).lt.
     + xlenp) then

       rib(i+1,107)=xmarkjm-xlen-rib(i+1,105)
       rib(i+1,108)=dsqrt((pr1x(i,j-1)-pr1x(i,j))**2+
     + (pr1y(i,j-1)-pr1y(i,j))**2)

c      Interpolate
       xequis=pr1x(i,j)-(rib(i+1,107)*(pr1x(i,j)-pr1x(i,j-1)))/
     + rib(i+1,108)
       yequis=pr1y(i,j)-(rib(i+1,107)*(pr1y(i,j)-pr1y(i,j-1)))/
     + rib(i+1,108)

c      Draw
       alpha=-(datan((pr1y(i,j)-pr1y(i,j-1))/(pr1x(i,j)-pr1x(i,j-1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xpeq=xequis+1.*xdes*dsin(alpha)
       ypeq=yequis-1.*xdes*dcos(alpha)

       call point (psep+xpeq,psey+ypeq,3)

       end if ! detect point

       xlen=xlen+sqrt((pr1x(i,j)-pr1x(i,j-1))**2+
     + (pr1y(i,j)-pr1y(i,j-1))**2)
       xlenp=xlen+sqrt((pr1x(i,j-1)-pr1x(i,j-2))**2+
     + (pr1y(i,j-1)-pr1y(i,j-2))**2)

       end do ! contour V-rib

       end if ! marks zone

       end do ! marks jm

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Mark equidistant points in bottom surface (rib i)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Move to rib i

       jcontrol=1

       do jm=1,60 ! Till 50 marks

       xmarkjm=xmark*float(jm)

c      Draw only in rib
       if (xmarkjm.ge.rib(i,104).and.xmarkjm.le.rib(i,104)+
     + xc24(i)) then

c      Define rib(i,106) only for first mark
       if (jcontrol.eq.1) then
       rib(i,106)=xmarkjm-rib(i,104)
       end if
       jcontrol=0

       xlen=0.
       xlenp=dsqrt((pl1x(i,121)-pl1x(i,120))**2+
     + (pl1y(i,121)-pl1y(i,120))**2)

       do j=121,3,-1
       
c      Detect and draw equidistant point
       if (xmarkjm-rib(i,104).ge.xlen.and.xmarkjm-rib(i,104).lt.
     + xlenp) then

       rib(i,107)=xmarkjm-xlen-rib(i,104)
       rib(i,108)=dsqrt((pl1x(i,j-1)-pl1x(i,j))**2+
     + (pl1y(i,j-1)-pl1y(i,j))**2)

c      Interpolate
       xequis=pl1x(i,j)-(rib(i,107)*(pl1x(i,j)-pl1x(i,j-1)))/
     + rib(i,108)
       yequis=pl1y(i,j)-(rib(i,107)*(pl1y(i,j)-pl1y(i,j-1)))/
     + rib(i,108)

c      Draw
       alpha=-(datan((pl1y(i,j)-pl1y(i,j-1))/(pl1x(i,j)-pl1x(i,j-1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xpeq=xequis-1.*xdes*dsin(alpha)
       ypeq=yequis+1.*xdes*dcos(alpha)

       call point (psep+xpeq,psey+ypeq,3)

       end if ! detect point

       xlen=xlen+sqrt((pl1x(i,j)-pl1x(i,j-1))**2+
     + (pl1y(i,j)-pl1y(i,j-1))**2)
       xlenp=xlen+sqrt((pl1x(i,j-1)-pl1x(i,j-2))**2+
     + (pl1y(i,j-1)-pl1y(i,j-2))**2)

       end do ! contour V-rib

       end if ! marks zone

       end do ! marks jm


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Mark anchor points in right rib
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,rib(i,15)

       xlen=0.
       xlenp=dsqrt((pl1x(i,121)-pl1x(i,120))**2+
     + (pl1y(i,121)-pl1y(i,120))**2)

       do j=121,3,-1

c      Detect and draw anchor point
       if (rib(i,130+klz)-rib(i,104).ge.xlen.and.
     + rib(i,130+klz)-rib(i,104).lt.
     + xlenp) then

    
       rib(i,107)=rib(i,130+klz)-xlen-rib(i,104)
       rib(i,108)=dsqrt((pl1x(i,j-1)-pl1x(i,j))**2+
     + (pl1y(i,j-1)-pl1y(i,j))**2)

c      Interpolate
       xequis=pl1x(i,j)-(rib(i,107)*(pl1x(i,j)-pl1x(i,j-1)))/
     + rib(i,108)
       yequis=pl1y(i,j)-(rib(i,107)*(pl1y(i,j)-pl1y(i,j-1)))/
     + rib(i,108)

c      Define anchor points in planar V-rib
       xanchor(i,klz)=xequis
       yanchor(i,klz)=yequis

c      Draw
       alpha=-(datan((pl1y(i,j)-pl1y(i,j-1))/(pl1x(i,j)-pl1x(i,j-1))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xpeq=xequis+1.*xdes*dsin(alpha)
       ypeq=yequis-1.*xdes*dcos(alpha)

c      Girar angle
       call point (psep+xpeq,psey+ypeq,30)
       call point (psep+xpeq+1.,psey+ypeq,30)
       call point (psep+xpeq+2.,psey+ypeq,30)

       end if ! detect point

       xlen=xlen+sqrt((pl1x(i,j)-pl1x(i,j-1))**2+
     + (pl1y(i,j)-pl1y(i,j-1))**2)
       xlenp=xlen+sqrt((pl1x(i,j-1)-pl1x(i,j-2))**2+
     + (pl1y(i,j-1)-pl1y(i,j-2))**2)


       end do ! in contour


       end do ! in anchors



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw parabolic holes in right rib
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       do klz=1,rib(i,15)-1

       xprb(i,klz,0)=(xanchor(i,klz)+xanchor(i,klz+1))/2.
       yprb(i,klz,0)=(yanchor(i,klz)+yanchor(i,klz+1))/2.

       do j=1,120

c      Point 5
       if (pr1y(i,j).le.yprb(i,klz,0).and.pr1y(i,j+1).gt.
     + yprb(i,klz,0)) then

       xm=(pr1y(i,j+1)-pr1y(i,j))/(pr1x(i,j+1)-pr1x(i,j))
       xb=pr1y(i,j)-xm*pr1x(i,j)

       yprb(i,klz,5)=yprb(i,klz,0)
       xprb(i,klz,5)=(yprb(i,klz,5)-xb)/xm

c       call line(psep+xprb(i,klz,5),psey+yprb(i,klz,5),
c     + psep+xprb(i,klz,5)+30,psey+yprb(i,klz,5),2)

       
c      Point 6
       dist05=-xprb(i,klz,0)+xprb(i,klz,5)
       dist06=dist05*hvr(k,9)/100.
       yprb(i,klz,6)=yprb(i,klz,0)
       xprb(i,klz,6)=xprb(i,klz,0)+dist06
       end if

c      Point 1

       if (pl1y(i,j).le.yanchor(i,klz)+hvr(k,10).and.pl1y(i,j+1).gt.
     + yanchor(i,klz)+hvr(k,10)) then

       xm=(pl1y(i,j+1)-pl1y(i,j))/(pl1x(i,j+1)-pl1x(i,j))
       xb=pl1y(i,j)-xm*pl1x(i,j)

       yprb(i,klz,1)=yanchor(i,klz)+hvr(k,10)
       xprb(i,klz,1)=(yprb(i,klz,1)-xb)/xm
       end if

       end do ! end j

       end do ! end klz


       do klz=1,rib(i+1,15)-1

       do j=1,120

c      Point 2 Intersection right side parabola with airfoil contour

       if (pl1y(i,j).ge.yprb(i,klz,0).and.pl1y(i,j).lt.
     + yanchor(i,klz+1)) then

c      Line "r" (parabola)

       xkprb(klz)=(xprb(i,klz,1)-xprb(i,klz,6))/
     + ((yprb(i,klz,1)-yprb(i,klz,6))**2.)

       xru(1)=xkprb(klz)*((pl1y(i,j)-yprb(i,klz,6))**2.)+
     + xprb(i,klz,6)
       xrv(1)=pl1y(i,j)
       xru(2)=xkprb(klz)*((pl1y(i,j+1)-yprb(i,klz,6))**2.)+
     + xprb(i,klz,6)
       xrv(2)=pl1y(i,j+1)

c      Line "s" (bottom surface)

       xsu(1)=pl1x(i,j)
       xsv(1)=pl1y(i,j)
       xsu(2)=pl1x(i,j+1)
       xsv(2)=pl1y(i,j+1)

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)


       if (xsv(1).le.xtv.and.xsv(2).gt.xtv) then  !!REVISAR
       yprb(i,klz,2)=xtv
       xprb(i,klz,2)=xtu
       end if  


       end if   

       end do ! in j

      
c       call line(psep+xprb(i,klz,0),psey+yprb(i,klz,0),
c     + psep+xprb(i,klz,6),psey+yprb(i,klz,6),2)

c       call line(psep+xprb(i,klz,1),psey+yprb(i,klz,1),
c     + psep+xprb(i,klz,6),psey+yprb(i,klz,6),3)

c       call line(psep+xprb(i,klz,2),psey+yprb(i,klz,2),
c     + psep+xprb(i,klz,6),psey+yprb(i,klz,6),1)

c      Draw parabolas


c      Detect extremal points
       do j=1,120

       if (pl1y(i,j).le.yprb(i,klz,1).and.pl1y(i,j+1).gt.
     + yprb(i,klz,1)) then
       jconi(klz)=j+1
       end if
       if (pl1y(i,j).le.yprb(i,klz,2).and.pl1y(i,j+1).gt.
     + yprb(i,klz,2)) then
       jconf(klz)=j
       end if

       end do

c      Draw parabolas

       if (hvr(k,9).le.100.) then

       j=jconi(klz)
       xpa1=xkprb(klz)*((pl1y(i,j)-yprb(i,klz,6))**2.)+
     + xprb(i,klz,6)
       call line(psep+xprb(i,klz,1),psey+yprb(i,klz,1),
     + psep+xpa1,psey+pl1y(i,j),1)
       do j=jconi(klz),jconf(klz)-1
       xpa1=xkprb(klz)*((pl1y(i,j)-yprb(i,klz,6))**2.)+
     + xprb(i,klz,6)
       xpa2=xkprb(klz)*((pl1y(i,j+1)-yprb(i,klz,6))**2.)+
     + xprb(i,klz,6)
       call line(psep+xpa1,psey+pl1y(i,j),
     + psep+xpa2,psey+pl1y(i,j+1),1)
       end do
       j=jconf(klz)
       xpa1=xkprb(klz)*((pl1y(i,j)-yprb(i,klz,6))**2.)+
     + xprb(i,klz,6)
       call line(psep+xprb(i,klz,2),psey+yprb(i,klz,2),
     + psep+xpa1,psey+pl1y(i,j),1)

       end if


c      Draw ellipses

       if (hvr(k,9).gt.100) then

       xprb(i,klz,7)=(xprb(i,klz,5)+xprb(i,klz,0))/2.
       yprb(i,klz,7)=yprb(i,klz,0)
       
       xa=0.5*((xprb(i,klz,5)-xprb(i,klz,0))*
     + (1.-(2.*(hvr(k,9)-100.)/100.)))
       xb=0.5*(yprb(i,klz,2)-yprb(i,klz,1)-2.*hvr(k,10))

       xgir=0.

       do j=1,100-2.*pi/100.

       xsu(1)=xprb(i,klz,7)+xa*dcos(xgir)
       xsv(1)=yprb(i,klz,7)+xb*dsin(xgir)
       xsu(2)=xprb(i,klz,7)+xa*dcos(xgir+2.*pi/100.)
       xsv(2)=yprb(i,klz,7)+xb*dsin(xgir+2.*pi/100.)

       call line(psep+xsu(1),psey+xsv(1),psep+xsu(2),psey+xsv(2),1)

       xgir=xgir+2.*pi/100.

       end do

       end if

       end do ! in klz

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw right diagonal in 3D space
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ii.eq.rib(i,15)) then
       do j=1,121
       call line3d(rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),1)
       call line3d(-rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + -rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),1)
       end do
       end if

       end if ! Draw right diagonal

       end if  ! rigth


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.3.2.5.3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marks in main ribs (rib i, bottom surface) plott and MC
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       sepxx=700.*xkf
       sepyy=100.*xkf

c      Rib i (center)
       kx=int((float(i-1)/6.))
       ky=i-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       do klz=1,3
      
       alpha=-datan((xtv9(i-1)-vcnt(i-1,1,2))/(xtu9(i-1)-ucnt(i-1,1,2)))
c       if (rib(i,149).le.0.1d0) then ! Verify if airfoil thicknees = 0
c       alpha=pi/2.0d0
c       end if
       xp22=xtu2(i)+(1-klz+xdes)*dcos(alpha)
       yp22=xtv2(i)-(1-klz+xdes)*dsin(alpha)
       xu=sepx+xp22
       xv=-sepy+yp22
       call pointg(xu,-xv,xcir,6) ! Box (1,2)
       call point(xu+2530.*xkf,-xv,6) ! Box (1,4)

       alpha=datan((xtv11(i-1)-vcnt(i-1,ii,4))/
     + (xtu11(i-1)-ucnt(i-1,ii,4)))
c       if (rib(i,149).le.0.1d0) then ! Verify if airfoil thicknees = 0
c       alpha=pi/2.0d0
c       end if
       xp44=xtu4(i)-(1-klz+xdes)*dcos(alpha)
       yp44=xtv4(i)-(1-klz+xdes)*dsin(alpha)
       xu=sepx+xp44
       xv=-sepy+yp44
       call pointg(xu,-xv,xcir,6) ! Box (1,2)
       call point(xu+2530.*xkf,-xv,6) ! Box (1,4)

       end do

       if (ii.eq.rib(i,15)) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Full V-ribs marks in ribs plotting and MC
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

c      Rib i-1 Left side
       kx=int((float(i-2)/6.))
       ky=i-1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)       

       if (hvr(k,5).eq.1) then
       call line(sepx+xtu9(i-1),-xtv9(i-1)+sepy,
     + sepx+ucnt(i-1,1,2),-vcnt(i-1,1,2)+sepy,5)
       call line(sepx+xtu11(i-1),-xtv11(i-1)+sepy,
     + sepx+ucnt(i-1,ii,4),-vcnt(i-1,ii,4)+sepy,5)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marks 9-10 in V-rib left
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,3
      
       alpha=-datan((xtv9(i-1)-vcnt(i-1,1,2))/(xtu9(i-1)-ucnt(i-1,1,2)))
       xp9=xtu9(i-1)-(1-klz+xdes)*dcos(alpha)
       yp9=xtv9(i-1)+(1-klz+xdes)*dsin(alpha)
       xu=sepx+xp9
       xv=-sepy+yp9
       call pointg(xu,-xv,xcir,6) ! Box (1,2)
       call point(xu+2530.*xkf,-xv,6) ! Box (1,4)

       alpha=datan((xtv11(i-1)-vcnt(i-1,ii,4))/
     + (xtu11(i-1)-ucnt(i-1,ii,4)))
       xp11=xtu11(i-1)+(1-klz+xdes)*dcos(alpha)
       yp11=xtv11(i-1)+(1-klz+xdes)*dsin(alpha)
       xu=sepx+xp11
       xv=-sepy+yp11
       call pointg(xu,-xv,xcir,6) ! Box (1,2)
       call point(xu+2530.*xkf,-xv,6) ! Box (1,4)

       end do

       end if  ! Left side


c      Rib i+1 Right side

       kx=int((float(i)/6.))
       ky=i+1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,6).eq.1) then
       call line(sepx+xtu9(i+1),-xtv9(i+1)+sepy,
     + sepx+ucnt(i+1,1,2),-vcnt(i+1,1,2)+sepy,1)
       call line(sepx+xtu11(i+1),-xtv11(i+1)+sepy,
     + sepx+ucnt(i+1,ii,4),-vcnt(i+1,ii,4)+sepy,1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marks 9-11 in V-rib right
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,3 ! Tree points
      
       alpha=-datan((xtv9(i+1)-vcnt(i+1,1,2))/(xtu9(i+1)-ucnt(i+1,1,2)))
       xp9=xtu9(i+1)-(1-klz+xdes)*dcos(alpha)
       yp9=xtv9(i+1)+(1-klz+xdes)*dsin(alpha)
       xu=sepx+xp9
       xv=-sepy+yp9
       call pointg(xu,-xv,xcir,6)
       call point(xu+2530.*xkf,-xv,6) ! Box (1,4)

       alpha=datan((xtv11(i+1)-vcnt(i+1,ii,4))/
     + (xtu11(i+1)-ucnt(i+1,ii,4)))
       xp11=xtu11(i+1)+(1-klz+xdes)*dcos(alpha)
       yp11=xtv11(i+1)+(1-klz+xdes)*dsin(alpha)
       xu=sepx+xp11
       xv=-sepy+yp11
       call pointg(xu,-xv,xcir,6)
       call point(xu+2530.*xkf,-xv,6) ! Box (1,4)

       end do

       end if  ! Right side

       end if  ! rib(i,15)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       end if ! ii=rib(i,15)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       end if ! end type 5

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

 



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4 HV ribs Type 4
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,2).eq.4) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4.1 Rib i-1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)-1
       ii=hvr(k,4) ! row

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)
       ucnt(i,ii,2)=ucnt(i,ii,3)-(hvr(k,7)+hvr(k,15))
       ucnt(i,ii,4)=ucnt(i,ii,3)+(hvr(k,7)+hvr(k,15))
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,8)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)


c      Points 2,3,4 interpolation in rib i-1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       uinc=0.
       vinc=0.

       do j=1,21
       ucnt2(i,ii,j)=ucnt(i,ii,2)+uinc
       uinc=uinc+(ucnt(i,ii,4)-ucnt(i,ii,2))/20.

c      Between 2 and jcon(i,ii,2)+1
       if (ucnt2(i,ii,j).le.u(i,jcon(i,ii,2)+1,3)) then
       xm=(v(i,jcon(i,ii,2)+1,3)-vcnt(i,ii,2))/(u(i,jcon(i,ii,2)+1,3)-
     + ucnt(i,ii,2))
       xb=vcnt(i,ii,2)-xm*ucnt(i,ii,2)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Between jcon(i,ii,2)+1 and jcon(i,ii,4)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ucnt2(i,ii,j).ge.u(i,jcon(i,ii,2)+1,3).and.ucnt2(i,ii,j)
     + .le.u(i,jcon(i,ii,4),3)) then
c      
       do l=jcon(i,ii,2)+1,jcon(i,ii,4)-1

c      Seleccionar tram d'interpolació

       if (ucnt2(i,ii,j).ge.u(i,l,3).and.ucnt2(i,ii,j).le.u(i,l+1,3)) 
     + then
       xm=(v(i,l+1,3)-v(i,l,3))/(u(i,l+1,3)-u(i,l,3))
       xb=v(i,l,3)-xm*u(i,l,3)
       end if
       end do
c       xm=(v(i,jcon(i,ii,2)+j,3)-v(i,jcon(i,ii,2)+j-1,3))/
c     + (u(i,jcon(i,ii,2)+j,3)-u(i,jcon(i,ii,2)+j-1,3))
c       xb=v(i,jcon(i,ii,2)+j-1,3)-xm*u(i,jcon(i,ii,2)+j-1,3)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

c      Between jcon(i,ii,4) and 4       
       if (ucnt2(i,ii,j).gt.u(i,jcon(i,ii,4),3)) then
       xm=(vcnt(i,ii,4)-v(i,jcon(i,ii,4),3))/(ucnt(i,ii,4)-
     + u(i,jcon(i,ii,4),3))
       xb=vcnt(i,ii,4)-xm*ucnt(i,ii,4)
       vcnt2(i,ii,j)=xm*ucnt2(i,ii,j)+xb
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4.2 Rib i
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,8)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 1,3,5 interpolation in rib i
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,1).and.u(i,j+1,3).ge.ucnt(i,ii,1)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,1)=xm*ucnt(i,ii,1)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,5).and.u(i,j+1,3).ge.ucnt(i,ii,5)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,5)=xm*ucnt(i,ii,5)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i
       do j=1,np(i,2)

       if (u(i,j,3).ge.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       end if

       end do

c      Calculus of 6,7,8 points in rib i
       vcnt(i,ii,6)=(vcnt(i,ii,9)-vcnt(i,ii,1))*(hvr(k,9)/100.)+
     + vcnt(i,ii,1)
       vcnt(i,ii,7)=(vcnt(i,ii,10)-vcnt(i,ii,3))*(hvr(k,9)/100.)+
     + vcnt(i,ii,3)
       vcnt(i,ii,8)=(vcnt(i,ii,11)-vcnt(i,ii,5))*(hvr(k,9)/100.)+
     + vcnt(i,ii,5)

c      Redefinition of points 6,8 if angle is not 90     
       if (hvr(k,10).ne.90.) then
       ucnt(i,ii,6)=ucnt(i,ii,7)-hvr(k,8)*dcos((pi/180.)*hvr(k,10))
       ucnt(i,ii,8)=ucnt(i,ii,7)+hvr(k,8)*dcos((pi/180.)*hvr(k,10))
       vcnt(i,ii,6)=vcnt(i,ii,7)-hvr(k,8)*dsin((pi/180.)*hvr(k,10))
       vcnt(i,ii,8)=vcnt(i,ii,7)+hvr(k,8)*dsin((pi/180.)*hvr(k,10))
       end if

c      Divide line 6-8 in n segments

       uinc=0.
       vinc=0.
       do j=1,21
       ucnt1(i,ii,j)=ucnt(i,ii,6)+uinc
       uinc=uinc+(ucnt(i,ii,8)-ucnt(i,ii,6))/20.
       vcnt1(i,ii,j)=vcnt(i,ii,6)+vinc
       vinc=vinc+(vcnt(i,ii,8)-vcnt(i,ii,6))/20.
       end do


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4.3 Rib i+1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)+1
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,7)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,8)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)

c      Points 1,3,5 interpolation in rib i+1
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,1).and.u(i,j+1,3).ge.ucnt(i,ii,1)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,1)=xm*ucnt(i,ii,1)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       end if

       if (u(i,j,3).le.ucnt(i,ii,5).and.u(i,j+1,3).ge.ucnt(i,ii,5)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,5)=xm*ucnt(i,ii,5)+xb
       end if

       end do

c      Points 9,10,11 interpolation in rib i+1
       do j=1,np(i,2)

       if (u(i,j,3).ge.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       end if

       if (u(i,j,3).ge.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       end if

       end do

c      Calculus of 6,7,8 points in rib i+1
       vcnt(i,ii,6)=(vcnt(i,ii,9)-vcnt(i,ii,1))*(hvr(k,9)/100.)+
     + vcnt(i,ii,1)
       vcnt(i,ii,7)=(vcnt(i,ii,10)-vcnt(i,ii,3))*(hvr(k,9)/100.)+
     + vcnt(i,ii,3)
       vcnt(i,ii,8)=(vcnt(i,ii,11)-vcnt(i,ii,5))*(hvr(k,9)/100.)+
     + vcnt(i,ii,5)

c      Redefinition of points 7,8 if angle is not 90     
       if (hvr(k,10).ne.90.) then
       ucnt(i,ii,6)=ucnt(i,ii,7)-hvr(k,8)*dcos((pi/180.)*hvr(k,10))
       ucnt(i,ii,8)=ucnt(i,ii,7)+hvr(k,8)*dcos((pi/180.)*hvr(k,10))
       vcnt(i,ii,6)=vcnt(i,ii,7)-hvr(k,8)*dsin((pi/180.)*hvr(k,10))
       vcnt(i,ii,8)=vcnt(i,ii,7)+hvr(k,8)*dsin((pi/180.)*hvr(k,10))
       end if

c      Divide line 6-8 in n segments

       uinc=0.
       vinc=0.
       do j=1,21
       ucnt3(i,ii,j)=ucnt(i,ii,6)+uinc
       uinc=uinc+(ucnt(i,ii,8)-ucnt(i,ii,6))/20.
       vcnt3(i,ii,j)=vcnt(i,ii,6)+vinc
       vinc=vinc+(vcnt(i,ii,8)-vcnt(i,ii,6))/20.
       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4.4 Rib i+2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)+2
       ii=hvr(k,4)

       ucnt(i,ii,3)=u(i,ii,6)
       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)
       ucnt(i,ii,2)=ucnt(i,ii,3)-(hvr(k,7)+hvr(k,16))
       ucnt(i,ii,4)=ucnt(i,ii,3)+(hvr(k,7)+hvr(k,16))
       ucnt(i,ii,5)=ucnt(i,ii,3)+hvr(k,8)
       ucnt(i,ii,6)=ucnt(i,ii,1)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,5)
       ucnt(i,ii,9)=ucnt(i,ii,1)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,5)


c      Points 2,3,4 interpolation in rib i+2
       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       uinc=0.
       vinc=0.

       do j=1,21
       ucnt4(i,ii,j)=ucnt(i,ii,2)+uinc
       uinc=uinc+(ucnt(i,ii,4)-ucnt(i,ii,2))/20.

c      Between 2 and jcon(i,ii,2)+1
       if (ucnt4(i,ii,j).le.u(i,jcon(i,ii,2)+1,3)) then
       xm=(v(i,jcon(i,ii,2)+1,3)-vcnt(i,ii,2))/(u(i,jcon(i,ii,2)+1,3)-
     + ucnt(i,ii,2))
       xb=vcnt(i,ii,2)-xm*ucnt(i,ii,2)
       vcnt4(i,ii,j)=xm*ucnt4(i,ii,j)+xb
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Between jcon(i,ii,2)+1 and jcon(i,ii,4)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ucnt4(i,ii,j).ge.u(i,jcon(i,ii,2)+1,3).and.ucnt4(i,ii,j)
     + .le.u(i,jcon(i,ii,4),3)) then
c      
       do l=jcon(i,ii,2)+1,jcon(i,ii,4)-1

c      Seleccionar tram d'interpolació

       if (ucnt4(i,ii,j).ge.u(i,l,3).and.ucnt4(i,ii,j).le.u(i,l+1,3)) 
     + then
       xm=(v(i,l+1,3)-v(i,l,3))/(u(i,l+1,3)-u(i,l,3))
       xb=v(i,l,3)-xm*u(i,l,3)
       end if
       end do
c       xm=(v(i,jcon(i,ii,2)+j,3)-v(i,jcon(i,ii,2)+j-1,3))/
c     + (u(i,jcon(i,ii,2)+j,3)-u(i,jcon(i,ii,2)+j-1,3))
c       xb=v(i,jcon(i,ii,2)+j-1,3)-xm*u(i,jcon(i,ii,2)+j-1,3)
       vcnt4(i,ii,j)=xm*ucnt4(i,ii,j)+xb
       end if

c      Between jcon(i,ii,4) and 4       
       if (ucnt4(i,ii,j).gt.u(i,jcon(i,ii,4),3)) then
       xm=(vcnt(i,ii,4)-v(i,jcon(i,ii,4),3))/(ucnt(i,ii,4)-
     + u(i,jcon(i,ii,4),3))
       xb=vcnt(i,ii,4)-xm*ucnt(i,ii,4)
       vcnt4(i,ii,j)=xm*ucnt4(i,ii,j)+xb
       end if

       end do


c      Rib localisation
       i=hvr(k,3)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4.4 VH-ribs lines 1 2 3 4 transportation to 3D espace
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Rib i (Line 1)

       i=hvr(k,3)

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt1(i,ii,j)
       rv(i,j,3)=vcnt1(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       sx1(i,j,ii)=rx(i,j)
       sy1(i,j,ii)=ry(i,j)
       sz1(i,j,ii)=rz(i,j)

       end do

c      Rib i-1 (Line 2)

       i=hvr(k,3)-1

       tetha=rib(i,8)*pi/180.
       
       do j=1,21
       ru(i,j,3)=ucnt2(i,ii,j)
       rv(i,j,3)=vcnt2(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       sx2(i,j,ii)=rx(i,j)
       sy2(i,j,ii)=ry(i,j)
       sz2(i,j,ii)=rz(i,j)

       end do

c      Rib i+1 (Line 3)

       i=hvr(k,3)+1

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt3(i,ii,j)
       rv(i,j,3)=vcnt3(i,ii,j)-rib(i,50)
c      COMPTE AMB el rib(i,50) A ESTUDIAR       
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       sx3(i,j,ii)=rx(i,j)
       sy3(i,j,ii)=ry(i,j)
       sz3(i,j,ii)=rz(i,j)

       end do

c      Rib i+2 (Line 4)

       i=hvr(k,3)+2

       tetha=rib(i,8)*pi/180.
       
       do j=1,21
       ru(i,j,3)=ucnt4(i,ii,j)
       rv(i,j,3)=vcnt4(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       sx4(i,j,ii)=rx(i,j)
       sy4(i,j,ii)=ry(i,j)
       sz4(i,j,ii)=rz(i,j)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing VH Type 4 in 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       do j=1,21

c      Rib i-1 to i+2

       i=hvr(k,3)

       if (hvr(k,5).eq.1) then
       call line3d(sx2(i-1,j,ii),sy2(i-1,j,ii),sz2(i-1,j,ii),
     + sx1(i,j,ii),sy1(i,j,ii),sz1(i,j,ii),3)
       call line3d(-sx2(i-1,j,ii),sy2(i-1,j,ii),sz2(i-1,j,ii),
     + -sx1(i,j,ii),sy1(i,j,ii),sz1(i,j,ii),3)
       end if

       call line3d(sx1(i,j,ii),sy1(i,j,ii),sz1(i,j,ii),
     + sx3(i+1,j,ii),sy3(i+1,j,ii),sz3(i+1,j,ii),2)
       call line3d(-sx1(i,j,ii),sy1(i,j,ii),sz1(i,j,ii),
     + -sx3(i+1,j,ii),sy3(i+1,j,ii),sz3(i+1,j,ii),2)

       if (hvr(k,6).eq.1) then
       call line3d(sx3(i+1,j,ii),sy3(i+1,j,ii),sz3(i+1,j,ii),
     + sx4(i+2,j,ii),sy4(i+2,j,ii),sz4(i+2,j,ii),1)
       call line3d(-sx3(i+1,j,ii),sy3(i+1,j,ii),sz3(i+1,j,ii),
     + -sx4(i+2,j,ii),sy4(i+2,j,ii),sz4(i+2,j,ii),1)
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.4.5 VH-ribs calculus and drawing in 2D and 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      VH-rib 1-2 in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)-1 ! color green

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do

c      Drawing in 2D model
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       if (hvr(k,5).eq.1) then

       j=1

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),3)

       j=21

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),3)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marca punts MC a l'esquerra
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pl1x(i,1)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pl1y(i,1)-xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pl1x(i,21)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pl1y(i,21)-xdes*dcos(alpha)-2.*xdes*dsin(alpha)
c       xp7=0.5*(pl1x(i,1)+pl1x(i,21))-xdes*dsin(alpha)
c       yp7=0.5*(pl1y(i,1)+pl1y(i,21))-xdes*dcos(alpha)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat esquerra
       sl=1.
       
       xpx=(pl1x(i,1)+pl2x(i,20))/2.-sl*xdes*dsin(alpha)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-sl*xdes*dcos(alpha)

       xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)-0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marca punts MC a la dreta
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)
     + -pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pr1x(i,1)+xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pr1y(i,1)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pr1x(i,21)+xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pr1y(i,21)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat dret
       sr=1.
       
       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

       xpx2=psep+xpx+0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy+0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vores de costura
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do j=1,21-1

c       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pl2x(i,j),
c     + psey+pl2y(i,j),30)

c       call line(psep+pr1x(i,j),psey+pr1y(i,j),psep+pr2x(i,j),
c     + psey+pr2y(i,j),2)

c      Vores de costura esquerra
       alpl=abs(datan((pl2y(i,j)-pl1y(i,j))/(pl2x(i,j)-pl1x(i,j))))

       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + +xvrib*dcos(alpl),psep+pl2x(i,j)-xvrib*dsin(alpl),
     + psey+pl2y(i,j)+xvrib*dcos(alpl),3)

c      Vores de costura dreta
       alpr=abs(datan((pr2y(i,j)-pr1y(i,j))/(pr2x(i,j)-pr1x(i,j))))
c       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then ! Revisar cases atès que hi ha qualque no OK!!!!!!!!!!!!!
       alpr=alpr+pi
       end if

       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + -xvrib*dcos(alpr),psep+pr2x(i,j)+xvrib*dsin(alpr),
     + psey+pr2y(i,j)-xvrib*dcos(alpr),3)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + +xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),3)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + -xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),3)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + +xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),3)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + -xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),3)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

       
       end do ! J

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,21)-rvcx(i,21))**2.+
     + (lvcy(i,21)-rvcy(i,21))**2.)

c      Numera cintes Type 4 V (i to i-1)
       call itxt(psep-0.-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)


       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      VH-rib 3-4 in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)+1 ! color red

       px0=0.0d0
       py0=0.0d0
       ptheta=0.0d0

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       
       end do

c      Drawing in 2D model
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       if (hvr(k,6).eq.1) then

       j=1

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)

       j=21

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marca punts MC a l'esquerra
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pl1x(i,1)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pl1y(i,1)-xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pl1x(i,21)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pl1y(i,21)-xdes*dcos(alpha)-2.*xdes*dsin(alpha)
c       xp7=0.5*(pl1x(i,1)+pl1x(i,21))-xdes*dsin(alpha)
c       yp7=0.5*(pl1y(i,1)+pl1y(i,21))-xdes*dcos(alpha)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat esquerra
       sl=1.
       
       xpx=(pl1x(i,1)+pl2x(i,20))/2.-sl*xdes*dsin(alpha)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-sl*xdes*dcos(alpha)

       xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)-0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marca punts MC a la dreta
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)
     + -pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pr1x(i,1)+xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pr1y(i,1)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pr1x(i,21)+xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pr1y(i,21)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat dret
       sr=1.
       
       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

       xpx2=psep+xpx+0.2*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.2*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.2*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy+0.2*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vores de costura
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do j=1,21-1

c       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pl2x(i,j),
c     + psey+pl2y(i,j),1)

c       call line(psep+pr1x(i,j),psey+pr1y(i,j),psep+pr2x(i,j),
c     + psey+pr2y(i,j),1)

c      Vores de costura esquerra
       alpl=abs(datan((pl2y(i,j)-pl1y(i,j))/(pl2x(i,j)-pl1x(i,j))))

       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + +xvrib*dcos(alpl),psep+pl2x(i,j)-xvrib*dsin(alpl),
     + psey+pl2y(i,j)+xvrib*dcos(alpl),1)

c      Vores de costura dreta
       alpr=abs(datan((pr2y(i,j)-pr1y(i,j))/(pr2x(i,j)-pr1x(i,j))))

       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + -xvrib*dcos(alpr),psep+pr2x(i,j)+xvrib*dsin(alpr),
     + psey+pr2y(i,j)-xvrib*dcos(alpr),1)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + +xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),1)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + -xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),1)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + +xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),1)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + -xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),1)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if


       end do ! j

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,21)-rvcx(i,21))**2.+
     + (lvcy(i,21)-rvcy(i,21))**2.)

c      REVISAR PRESENTACIO

c      Numera cintes V TYpe 4 i+1 to i+2
       call itxt(psep-0.-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      VH-rib 1-3 in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3) ! color yellow

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.0d0)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.0d0*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.0d0*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.0d0*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       
       end do

c      Drawing in 2D model
       
       psep=3300.*xkf+xrsep*float(i)
       psey=800.*xkf+yrsep*float(ii)

       j=1

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),30)

       j=21

       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),30)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marca punts MC a l'esquerra
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pl1x(i,1)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pl1y(i,1)-xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pl1x(i,21)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pl1y(i,21)-xdes*dcos(alpha)-2.*xdes*dsin(alpha)
c       xp7=0.5*(pl1x(i,1)+pl1x(i,21))-xdes*dsin(alpha)
c       yp7=0.5*(pl1y(i,1)+pl1y(i,21))-xdes*dcos(alpha)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat esquerra
       sl=1.
       
       xpx=(pl1x(i,1)+pl2x(i,20))/2.-sl*xdes*dsin(alpha)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-sl*xdes*dcos(alpha)

       xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)-0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Marca punts MC a la dreta
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)
     + -pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pr1x(i,1)+xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pr1y(i,1)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pr1x(i,21)+xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pr1y(i,21)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat dret
       sr=1.
       
       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

       xpx2=psep+xpx+0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.5*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy+0.5*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(int(hvr(k,4)),xpx2,xpy2,alpha,typm6(10)*0.1,7)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Vores de costura
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do j=1,21-1

c       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pl2x(i,j),
c     + psey+pl2y(i,j),1)

c       call line(psep+pr1x(i,j),psey+pr1y(i,j),psep+pr2x(i,j),
c     + psey+pr2y(i,j),1)


c      Vores de costura esquerra
       alpl=abs(datan((pl2y(i,j)-pl1y(i,j))/(pl2x(i,j)-pl1x(i,j))))

       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + +xvrib*dcos(alpl),psep+pl2x(i,j)-xvrib*dsin(alpl),
     + psey+pl2y(i,j)+xvrib*dcos(alpl),30)

c      Vores de costura dreta
       alpr=abs(datan((pr2y(i,j)-pr1y(i,j))/(pr2x(i,j)-pr1x(i,j))))

       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + -xvrib*dcos(alpr),psep+pr2x(i,j)+xvrib*dsin(alpr),
     + psey+pr2y(i,j)-xvrib*dcos(alpr),30)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + +xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),30)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + -xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),30)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + +xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),30)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + -xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),30)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

       end do

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,21)-rvcx(i,21))**2.+
     + (lvcy(i,21)-rvcy(i,21))**2.)

c      Numera cintes H Type 4 i to i+1
       call itxt(psep-0.-xrsep+83.*xkf-120.*(typm3(10)/10.),psey-10,
     + typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing VH-ribs in 2D ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib i-1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       kx=int((float(i-2)/6.))
       ky=i-1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

c       write (*,*) "i,kx,ky ",i,kx,ky,sepx,sepy

       if (hvr(k,5).eq.1) then

c      Segment
       call line(sepx+ucnt(i-1,ii,2),-vcnt(i-1,ii,2)+sepy,
     + sepx+ucnt(i-1,ii,4),-vcnt(i-1,ii,4)+sepy,3)
       call line(sepx+2530.*xkf+ucnt(i-1,ii,2),-vcnt(i-1,ii,2)+sepy,
     + sepx+2530.*xkf+ucnt(i-1,ii,4),-vcnt(i-1,ii,4)+sepy,3)

c      Points in 2
       alpha=(datan((v(i-1,jcon(i-1,ii,2)-1,3)-v(i-1,jcon(i-1,ii,2)+1,
     + 3))/(u(i-1,jcon(i-1,ii,2)-1,3)-u(i-1,jcon(i-1,ii,2)+1,3))))
       xpeq=ucnt(i-1,ii,2)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i-1,ii,2)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,3)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),1)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,3)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),1)

c      Points in 4
       alpha=(datan((v(i-1,jcon(i-1,ii,4)-1,3)-v(i-1,jcon(i-1,ii,4)+1,
     + 3))/(u(i-1,jcon(i-1,ii,4)-1,3)-u(i-1,jcon(i-1,ii,4)+1,3))))
       xpeq=ucnt(i-1,ii,4)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i-1,ii,4)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,3)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),1)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,3)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),1)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib i (center)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       kx=int((float(i-1)/6.))
       ky=i-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

c      Segment
       call line(sepx+ucnt(i,ii,6),-vcnt(i,ii,6)+sepy,
     + sepx+ucnt(i,ii,8),-vcnt(i,ii,8)+sepy,30)
       call line(sepx+2530.*xkf+ucnt(i,ii,6),-vcnt(i,ii,6)+sepy,
     + sepx+2530.*xkf+ucnt(i,ii,8),-vcnt(i,ii,8)+sepy,30)

c      Points in 6
       alpha=(datan((v(i,jcon(i,ii,6)-1,3)-v(i,jcon(i,ii,6)+1,
     + 3))/(u(i,jcon(i,ii,6)-1,3)-u(i,jcon(i,ii,6)+1,3))))
       xpeq=ucnt(i,ii,6)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i,ii,6)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,1)
c       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),1)
c       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,1)
c       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
c     + 1*dcos(alpha),1)
c       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
c     + 2*dcos(alpha),1)

c      Points in 8
       alpha=(datan((v(i,jcon(i,ii,8)-1,3)-v(i,jcon(i,ii,8)+1,
     + 3))/(u(i,jcon(i,ii,8)-1,3)-u(i,jcon(i,ii,8)+1,3))))
       xpeq=ucnt(i,ii,8)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i,ii,8)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,30)
c       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),1)
c       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,30)
c       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
c     + 1*dcos(alpha),1)
c       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
c     + 2*dcos(alpha),1)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib i+1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       kx=int((float(i)/6.))
       ky=i+1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,6).eq.1) then
       
c      Segment
       call line(sepx+ucnt(i+1,ii,6),-vcnt(i+1,ii,6)+sepy,
     + sepx+ucnt(i+1,ii,8),-vcnt(i+1,ii,8)+sepy,30)
       call line(sepx+2530.*xkf+ucnt(i+1,ii,6),-vcnt(i+1,ii,6)+sepy,
     + sepx+2530.*xkf+ucnt(i+1,ii,8),-vcnt(i+1,ii,8)+sepy,30)

c      Points in 6
       alpha=(datan((v(i+1,jcon(i+1,ii,6)-1,3)-v(i+1,jcon(i+1,ii,6)+1,
     + 3))/(u(i+1,jcon(i+1,ii,6)-1,3)-u(i+1,jcon(i+1,ii,6)+1,3))))
       xpeq=ucnt(i+1,ii,6)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,6)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,30)
c       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),1)
c       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,30)
c       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
c     + 1*dcos(alpha),1)
c       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
c     + 2*dcos(alpha),1)

c      Points in 8
       alpha=(datan((v(i+1,jcon(i+1,ii,8)-1,3)-v(i+1,jcon(i+1,ii,8)+1,
     + 3))/(u(i+1,jcon(i+1,ii,8)-1,3)-u(i+1,jcon(i+1,ii,8)+1,3))))
       xpeq=ucnt(i+1,ii,8)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,8)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,1)
c       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),1)
c       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,1)
c       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
c     + 1*dcos(alpha),1)
c       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
c     + 2*dcos(alpha),1)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib i+2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       kx=int((float(i+1)/6.))
       ky=i+2-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

       if (hvr(k,6).eq.1) then

c      Segment
       call line(sepx+ucnt(i+2,ii,2),-vcnt(i+2,ii,2)+sepy,
     + sepx+ucnt(i+2,ii,4),-vcnt(i+2,ii,4)+sepy,1)
       call line(sepx+2530.*xkf+ucnt(i+2,ii,2),-vcnt(i+2,ii,2)+sepy,
     + sepx+2530.*xkf+ucnt(i+2,ii,4),-vcnt(i+2,ii,4)+sepy,1)

c      Points in 2
       alpha=(datan((v(i+2,jcon(i+2,ii,2)-1,3)-v(i+2,jcon(i+2,ii,2)+1,
     + 3))/(u(i+2,jcon(i+2,ii,2)-1,3)-u(i+2,jcon(i+2,ii,2)+1,3))))
       xpeq=ucnt(i+2,ii,2)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i+2,ii,2)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,3)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),1)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,3)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),1)

c      Points in 4
       alpha=(datan((v(i+2,jcon(i+2,ii,4)-1,3)-v(i+2,jcon(i+2,ii,4)+1,
     + 3))/(u(i+2,jcon(i+2,ii,4)-1,3)-u(i+2,jcon(i+2,ii,4)+1,3))))
       xpeq=ucnt(i+2,ii,4)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i+2,ii,4)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,3)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),1)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,3)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),1)

       end if

       end if   ! end type VH



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6 V-rib Type 6 GENERAL TYPE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.1 Rib i
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Now ii is virtual row, assigned automatically for each rib
       iii=1

       if (hvr(k,2).eq.6) then

c      Define types 6 along rib
       if (k.ge.2.and.hvr(k-1,2).eq.6.and.hvr(k-1,3).eq.hvr(k,3)) then
       iii=iii+1
       end if

c      Define main points 2,3,4,9,10,11

       i=hvr(k,3)    ! rib i
       ii=iii       ! virtual row ii, in rib i

       ucnt(i,ii,3)=rib(i,5)*hvr(k,4)/100.0d0
       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,6)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,7)
       ucnt(i,ii,6)=ucnt(i,ii,2)
       ucnt(i,ii,7)=ucnt(i,ii,3)
       ucnt(i,ii,8)=ucnt(i,ii,4)
       ucnt(i,ii,9)=ucnt(i,ii,2)
       ucnt(i,ii,10)=ucnt(i,ii,3)
       ucnt(i,ii,11)=ucnt(i,ii,4)

c      Points 2,3,4 interpolation in rib i

       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do

c      Points 9,10,11 interpolation in rib i

       do j=1,np(i,2)

       if (u(i,j,3).gt.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       jcon(i,ii,9)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       jcon(i,ii,10)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       jcon(i,ii,11)=j+1
       end if

       end do

c      Points 6,8 interpolation in rib i

       vcnt(i,ii,6)=(vcnt(i,ii,9)-vcnt(i,ii,2))*(hvr(k,5)/100.)+
     + vcnt(i,ii,2)
       vcnt(i,ii,8)=(vcnt(i,ii,11)-vcnt(i,ii,4))*(hvr(k,5)/100.)+
     + vcnt(i,ii,4)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h1=0.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (hvr(k,5).eq.0.) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Experimental version     
c      Reformat in 20 spaces

       n1vr=jcon(i,ii,4)-jcon(i,ii,2)+1
       n2vr=20+1

c      Load data polyline
       xlin1(1)=ucnt(i,ii,2)
       ylin1(1)=vcnt(i,ii,2)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon(i,ii,2)+j-1,3)
       ylin1(j)=v(i,jcon(i,ii,2)+j-1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=ucnt(i,ii,4)
       ylin1(n1vr)=vcnt(i,ii,4)

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt2(i,ii,j)=xlin3(j)
       vcnt2(i,ii,j)=ylin3(j)
       end do

       end if ! case h1=0.

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 0. < h1 < 100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Redefine line 2: ucnt2(i,ii,j) - vcnt2(i,ii,j)
c      Divide line 6-8 in n segments

       uinc=0.
       vinc=0.
       do j=1,21
       ucnt2(i,ii,j)=ucnt(i,ii,6)+uinc
       uinc=uinc+(ucnt(i,ii,8)-ucnt(i,ii,6))/20.
       vcnt2(i,ii,j)=vcnt(i,ii,6)+vinc
       vinc=vinc+(vcnt(i,ii,8)-vcnt(i,ii,6))/20.
       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h1=100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,5).eq.100.) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat 9-10-11 in n spaces (rib i)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
   
c      Reformat in 20 spaces

       n1vr=jcon(i,ii,9)-jcon(i,ii,11)+1    
       n2vr=20+1

c      Load data polyline
       xlin1(1)=ucnt(i,ii,9)
       ylin1(1)=vcnt(i,ii,9)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon(i,ii,9)-j+1,3)
       ylin1(j)=v(i,jcon(i,ii,9)-j+1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=ucnt(i,ii,11)
       ylin1(n1vr)=vcnt(i,ii,11)

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt2(i,ii,j)=xlin3(j)
       vcnt2(i,ii,j)=ylin3(j)
       end do
 
       end if ! Case h1=100.


cccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.2 Rib i+1
cccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,8)   ! rib i+1
c      ii use virtial row 

       ucnt(i,ii,3)=rib(i,5)*hvr(k,9)/100.0d0

c       ucnt(i,ii,1)=ucnt(i,ii,3)-hvr(k,8)

       ucnt(i,ii,2)=ucnt(i,ii,3)-hvr(k,11)
       ucnt(i,ii,4)=ucnt(i,ii,3)+hvr(k,12)
       ucnt(i,ii,6)=ucnt(i,ii,2)
       ucnt(i,ii,8)=ucnt(i,ii,4)
       ucnt(i,ii,9)=ucnt(i,ii,2)
       ucnt(i,ii,11)=ucnt(i,ii,4)

c      Points 2,3,4 interpolation in rib i+1

       do j=np(i,2),np(i,1)

       if (u(i,j,3).le.ucnt(i,ii,2).and.u(i,j+1,3).ge.ucnt(i,ii,2)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,2)=xm*ucnt(i,ii,2)+xb
       jcon(i,ii,2)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,3).and.u(i,j+1,3).ge.ucnt(i,ii,3)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,3)=xm*ucnt(i,ii,3)+xb
       jcon(i,ii,3)=j
       end if

       if (u(i,j,3).le.ucnt(i,ii,4).and.u(i,j+1,3).ge.ucnt(i,ii,4)) then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,4)=xm*ucnt(i,ii,4)+xb
       jcon(i,ii,4)=j
       end if

       end do

c      Points 9,10,11 interpolation in rib i+1

       do j=1,np(i,2)

       if (u(i,j,3).gt.ucnt(i,ii,9).and.u(i,j+1,3).le.ucnt(i,ii,9)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,9)=xm*ucnt(i,ii,9)+xb
       jcon(i,ii,9)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,10).and.u(i,j+1,3).le.ucnt(i,ii,10)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,10)=xm*ucnt(i,ii,10)+xb
       jcon(i,ii,10)=j+1
       end if

       if (u(i,j,3).gt.ucnt(i,ii,11).and.u(i,j+1,3).le.ucnt(i,ii,11)) 
     + then
       xm=(v(i,j+1,3)-v(i,j,3))/(u(i,j+1,3)-u(i,j,3))
       xb=v(i,j,3)-xm*u(i,j,3)
       vcnt(i,ii,11)=xm*ucnt(i,ii,11)+xb
       jcon(i,ii,11)=j+1
       end if

       end do

c      Points 6,8 interpolation in rib i+1

       vcnt(i,ii,6)=(vcnt(i,ii,9)-vcnt(i,ii,2))*(hvr(k,10)/100.)+
     + vcnt(i,ii,2)
       vcnt(i,ii,8)=(vcnt(i,ii,11)-vcnt(i,ii,4))*(hvr(k,10)/100.)+
     + vcnt(i,ii,4)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h2=0.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,10).eq.0.) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat line 2-3-4 in n regular spaces   
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Experimental version     
c      Reformat in 20 spaces

       n1vr=jcon(i,ii,4)-jcon(i,ii,2)+1
       n2vr=20+1

c      Load data polyline
       xlin1(1)=ucnt(i,ii,2)
       ylin1(1)=vcnt(i,ii,2)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon(i,ii,2)+j-1,3)
       ylin1(j)=v(i,jcon(i,ii,2)+j-1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=ucnt(i,ii,4)
       ylin1(n1vr)=vcnt(i,ii,4)

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt3(i,ii,j)=xlin3(j)
       vcnt3(i,ii,j)=ylin3(j)
       end do

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 0. < h2 < 100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Redefine line 2: ucnt3(i,ii,j) - vcnt3(i,ii,j)
c      Divide line 6-8 in n segments

       uinc=0.
       vinc=0.
       do j=1,21
       ucnt3(i,ii,j)=ucnt(i,ii,6)+uinc
       uinc=uinc+(ucnt(i,ii,8)-ucnt(i,ii,6))/20.
       vcnt3(i,ii,j)=vcnt(i,ii,6)+vinc
       vinc=vinc+(vcnt(i,ii,8)-vcnt(i,ii,6))/20.
       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h2=100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,10).eq.100.) then

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Reformat 9-10-11 in n spaces (rib i+1)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Experimental version     
c      Reformat in 20 spaces

       n1vr=jcon(i,ii,9)-jcon(i,ii,11)+1
       n2vr=20+1

c      Load data polyline
       xlin1(1)=ucnt(i,ii,9)
       ylin1(1)=vcnt(i,ii,9)
       do j=2,n1vr-1
       xlin1(j)=u(i,jcon(i,ii,9)-j+1,3)
       ylin1(j)=v(i,jcon(i,ii,9)-j+1,3)
c      MIRAR SI CAL +-1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       end do
       xlin1(n1vr)=ucnt(i,ii,11)
       ylin1(n1vr)=vcnt(i,ii,11)

c      Call subroutine vector redistribution

       call vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)

c      Load result polyline

       do j=1,n2vr
       ucnt3(i,ii,j)=xlin3(j)
       vcnt3(i,ii,j)=ylin3(j)
       end do

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib localisation
       i=hvr(k,3)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.3 V-ribs lines 2 3 transportation to 3D espace
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Rib i (Line 2)

       i=hvr(k,3)

       tetha=rib(i,8)*pi/180.
       
       do j=1,21
       ru(i,j,3)=ucnt2(i,ii,j)
       rv(i,j,3)=vcnt2(i,ii,j)-rib(i,50)
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx2(i,j,ii)=rx(i,j)
       ry2(i,j,ii)=ry(i,j)
       rz2(i,j,ii)=rz(i,j)

       end do

c      Rib i+1 (Line 3)

       i=hvr(k,8)

       tetha=rib(i,8)*pi/180.

       do j=1,21
       ru(i,j,3)=ucnt3(i,ii,j)
       rv(i,j,3)=vcnt3(i,ii,j)-rib(i,50)      
       end do

       do j=1,21

       u_aux(i,j,1)=ru(i,j,3)
       v_aux(i,j,1)=rv(i,j,3)
       w_aux(i,j,1)=0.0d0
       call xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)
       rx(i,j)=w_aux(i,j,5)
       ry(i,j)=u_aux(i,j,5)
       rz(i,j)=v_aux(i,j,5)

       rx3(i-1,j,ii)=rx(i,j)
       ry3(i-1,j,ii)=ry(i,j)
       rz3(i-1,j,ii)=rz(i,j)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.4 V-ribs calculus and drawing in 3D and 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.4 V-rib 2-3 in 2D model (red)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       i=hvr(k,3)

       px0=0.
       py0=0.
       ptheta=0.

       do j=1,21

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.+(ry(i+1,j)-ry(i,j))**2.+
     + (rz(i+1,j)-rz(i,j))**2.)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.+(ry(i+1,j+1)-ry(i,j))**2.+
     + (rz(i+1,j+1)-rz(i,j))**2.)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.+(ry(i+1,j+1)-ry(i+1,j))**2.+
     + (rz(i+1,j+1)-rz(i+1,j))**2.)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.+(ry(i+1,j)-ry(i,j+1))**2.+
     + (rz(i+1,j)-rz(i,j+1))**2.)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.+(ry(i,j+1)-ry(i,j))**2.+
     + (rz(i,j+1)-rz(i,j))**2.)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.+(ry(i+1,j+1)-ry(i,j+1))**2.+
     + (rz(i+1,j+1)-rz(i,j+1))**2.)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.0d0*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.0d0*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.0d0*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing Type-6 in 2D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       

c      Draw in BOX(2,6)

       psep=(3300.+1260.+1260.)*xkf+xrsep*float(i)
       psey=(800.+890.85+100.)*xkf+(hvr(k,4)+hvr(k,9))*0.5*
     + rib(int(hvr(k,3)),5)*3.0/100.

c       write (*,*) "i,ii ",i,ii

       j=1

c      Costat vora d'atac
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)

       j=21
c      Costat fuga
       call line(psep+pl1x(i,j),psey+pl1y(i,j),psep+pr1x(i,j),
     + psey+pr1y(i,j),1)


c      Marca punts MC a l'esquerra

       alpha=-(datan((pl1y(i,1)-pl2y(i,20))/(pl1x(i,1)-pl2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pl1x(i,1)-xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pl1y(i,1)-xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pl1x(i,21)-xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pl1y(i,21)-xdes*dcos(alpha)-2.*xdes*dsin(alpha)
c       xp7=0.5*(pl1x(i,1)+pl1x(i,21))-xdes*dsin(alpha)
c       yp7=0.5*(pl1y(i,1)+pl1y(i,21))-xdes*dcos(alpha)

c       call point(psep+xp7,psey+yp7,2)

       call point(psep+xp6,psey+yp6,1)
c       call point(psep+xp7,psey+yp7,1)
       call point(psep+xp8,psey+yp8,1)


c      Romano costat esquerra

       sl=1.
       
       xpx=(pl1x(i,1)+pl2x(i,20))/2.-sl*xdes*dsin(alpha)
       xpy=(pl1y(i,1)+pl2y(i,20))/2.-sl*xdes*dcos(alpha)

       xpx2=psep+xpx+0.3*hvr(k,7)*dcos(alpha)-0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.3*hvr(k,7)*dsin(alpha)-0.3*xvrib*dcos(alpha) 

       call romano(i,xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Marca punts MC a la dreta

       alpha=-(datan((pr1y(i,1)-pr2y(i,20))/(pr1x(i,1)
     + -pr2x(i,20))))
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

       xp6=pr1x(i,1)+xdes*dsin(alpha)-2.*xdes*dcos(alpha)
       yp6=pr1y(i,1)+xdes*dcos(alpha)+2.*xdes*dsin(alpha)
       xp8=pr1x(i,21)+xdes*dsin(alpha)+2.*xdes*dcos(alpha)
       yp8=pr1y(i,21)+xdes*dcos(alpha)-2.*xdes*dsin(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)

       call point(psep+xp6,psey+yp6,1)
c       call point(psep+xp7,psey+yp7,1)
       call point(psep+xp8,psey+yp8,1)

c      Romano costat dret

       sr=1.
       
       xpx=(pr1x(i,1)+pr2x(i,20))/2.+xdes*dsin(alpha)
       xpy=(pr1y(i,1)+pr2y(i,20))/2.+xdes*dcos(alpha)

       xpx2=psep+xpx+0.2*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy-0.2*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

       call romano(i+1,xpx2,xpy2,alpha,typm6(10)*0.1,7)

       xpx2=psep+xpx-0.2*hvr(k,8)*dcos(alpha)+0.3*xvrib*dsin(alpha)
       xpy2=psey+xpy+0.2*hvr(k,8)*dsin(alpha)+0.3*xvrib*dcos(alpha) 

c      Numbering of Type 6 pieces now fron 0 t 10 according the %
       call romano(int(hvr(k,4)*0.1),xpx2,xpy2,alpha,typm6(10)*0.1,7)

c      Vores de costura

       do j=1,21-1

c      Vores de costura esquerra
       alpl=-(datan((pl1y(i,j)-pl2y(i,j))/(pl1x(i,j)-pl2x(i,j))))
       if (alpl.lt.0.) then
       alpl=alpl+pi
       end if

       lvcx(i,j)=psep+pl1x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j)=psey+pl1y(i,j)-xvrib*dcos(alpl)

c      Vores de costura dreta
       alpr=-(datan((pr1y(i,j)-pr2y(i,j))/(pr1x(i,j)-pr2x(i,j))))
       if (alpr.lt.0.) then
       alpr=alpr+pi
       end if

       rvcx(i,j)=psep+pr1x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j)=psey+pr1y(i,j)+xvrib*dcos(alpr)

c      Tancament lateral inici
       if (j.eq.1) then
       call line(psep+pl1x(i,j)-xvrib*dsin(alpl),psey+pl1y(i,j)
     + -xvrib*dcos(alpl),psep+pl1x(i,j),psey+pl1y(i,j),1)
       call line(psep+pr1x(i,j)+xvrib*dsin(alpr),psey+pr1y(i,j)
     + +xvrib*dcos(alpr),psep+pr1x(i,j),psey+pr1y(i,j),1)
       end if

c      Tancament lateral fi
       if (j.eq.20) then
       call line(psep+pl2x(i,j)-xvrib*dsin(alpl),psey+pl2y(i,j)
     + -xvrib*dcos(alpl),psep+pl2x(i,j),psey+pl2y(i,j),1)
       call line(psep+pr2x(i,j)+xvrib*dsin(alpr),psey+pr2y(i,j)
     + +xvrib*dcos(alpr),psep+pr2x(i,j),psey+pr2y(i,j),1)

       lvcx(i,j+1)=psep+pl2x(i,j)-xvrib*dsin(alpl)
       lvcy(i,j+1)=psey+pl2y(i,j)-xvrib*dcos(alpl)

       rvcx(i,j+1)=psep+pr2x(i,j)+xvrib*dsin(alpr)
       rvcy(i,j+1)=psey+pr2y(i,j)+xvrib*dcos(alpr)

       end if

       end do ! j

c      V-rib length
       hvr(k,15)=dsqrt((lvcx(i,1)-rvcx(i,1))**2.0d0+
     + (lvcy(i,1)-rvcy(i,1))**2.0d0)

c      Numera cintes V Type 6
       call itxt(psep-xrsep+83.*xkf-120.*(typm3(10)/10.),psey-10,
     + typm3(10),0.0d0,i,7)
       call itxt(psep+hvr(k,15)-xrsep+83.*xkf-120.*(typm3(10)/10.),
     + psey-10,typm3(10),0.0d0,i+1,7)

c      Dibuixa vores amb segments completament enllaçats       
       do j=1,20

       call line(lvcx(i,j),lvcy(i,j),lvcx(i,j+1),lvcy(i,j+1),1)
       call line(rvcx(i,j),rvcy(i,j),rvcx(i,j+1),rvcy(i,j+1),1)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.5 Drawing V-ribs marks in 2D ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Drawing in 2D ribs printing and MC (+2530.xkf)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Box (1,2)

       sepxx=700.*xkf
       sepyy=100.*xkf

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib i (center)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       kx=int((float(i-1)/6.))
       ky=i-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h1=0.
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,5).eq.0.) then

c      Segment
       call line(sepx+ucnt(i,ii,2),-vcnt(i,ii,2)+sepy,
     + sepx+ucnt(i,ii,4),-vcnt(i,ii,4)+sepy,1)
       call line(sepx+2530.*xkf+ucnt(i,ii,2),-vcnt(i,ii,2)+sepy,
     + sepx+2530.*xkf+ucnt(i,ii,4),-vcnt(i,ii,4)+sepy,1)

c      Points in 2 and 4 (Experimental)

c      Points in 2
       alpha=(datan((v(i,jcon(i,ii,2)-1,3)-v(i,jcon(i,ii,2)+1,
     + 3))/(u(i,jcon(i,ii,2)-1,3)-u(i,jcon(i,ii,2)+1,3))))
       xpeq=ucnt(i,ii,2)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i,ii,2)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,1)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),1)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,1)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),1)

c      Points in 4
       alpha=(datan((v(i,jcon(i,ii,4)-1,3)-v(i,jcon(i,ii,4)+1,
     + 3))/(u(i,jcon(i,ii,4)-1,3)-u(i,jcon(i,ii,4)+1,3))))
       xpeq=ucnt(i,ii,4)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i,ii,4)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,1)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),1)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,1)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),1)

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 0. < h1 < 100.
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,5).gt.0.and.hvr(k,5).lt.100.) then

c      Segment
       call line(sepx+ucnt(i,ii,6),-vcnt(i,ii,6)+sepy,
     + sepx+ucnt(i,ii,8),-vcnt(i,ii,8)+sepy,1)
       call line(sepx+2530.*xkf+ucnt(i,ii,6),-vcnt(i,ii,6)+sepy,
     + sepx+2530.*xkf+ucnt(i,ii,8),-vcnt(i,ii,8)+sepy,1)

c      Punts marcatge V-rib
       alpha=datan((vcnt(i,ii,8)-vcnt(i,ii,6))/
     + (ucnt(i,ii,8)-ucnt(i,ii,6)))
       xp6=ucnt(i,ii,6)-xdes*dsin(alpha)
       yp6=vcnt(i,ii,6)+xdes*dcos(alpha)
       xp8=ucnt(i,ii,8)-xdes*dsin(alpha)
       yp8=vcnt(i,ii,8)+xdes*dcos(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)
       call point(sepx+xp6,sepy-yp6,1)
       call point(sepx+xp7,sepy-yp7,1)
       call point(sepx+xp8,sepy-yp8,1)
       call point(sepx+2530.*xkf+xp6,sepy-yp6,1)
       call point(sepx+2530.*xkf+xp7,sepy-yp7,1)
       call point(sepx+2530.*xkf+xp8,sepy-yp8,1)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h1=100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,5).eq.100.) then

c      Segment
       call line(sepx+ucnt(i,ii,9),-vcnt(i,ii,9)+sepy,
     + sepx+ucnt(i,ii,11),-vcnt(i,ii,11)+sepy,1)
       call line(sepx+2530.*xkf+ucnt(i,ii,9),-vcnt(i,ii,9)+sepy,
     + sepx+2530.*xkf+ucnt(i,ii,11),-vcnt(i,ii,11)+sepy,1)

c      Points in 9
       alpha=(datan((v(i,jcon(i,ii,9)-1,3)-v(i,jcon(i,ii,9)+1,
     + 3))/(u(i,jcon(i,ii,9)-1,3)-u(i,jcon(i,ii,9)+1,3))))
       xpeq=ucnt(i,ii,9)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i,ii,9)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,1)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),1)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,1)
       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),1)

c      Points in 11
       alpha=(datan((v(i,jcon(i,ii,11)-1,3)-v(i,jcon(i,ii,11)+1,
     + 3))/(u(i,jcon(i,ii,11)-1,3)-u(i,jcon(i,ii,11)+1,3))))
       xpeq=ucnt(i,ii,11)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i,ii,11)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,1)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),1)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,1)
       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),1)
       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),1)

       end if


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Rib i+1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       kx=int((float(i)/6.))
       ky=i+1-kx*6

       sepx=sepxx+seprix*float(kx)
       sepy=sepyy+sepriy*float(ky-1)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h2=0.
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,10).eq.0.) then

c      Segments
       call line(sepx+ucnt(i+1,ii,2),-vcnt(i+1,ii,2)+sepy,
     + sepx+ucnt(i+1,ii,4),-vcnt(i+1,ii,4)+sepy,4)
       call line(sepx+2530.*xkf+ucnt(i+1,ii,2),-vcnt(i+1,ii,2)+sepy,
     + sepx+2530.*xkf+ucnt(i+1,ii,4),-vcnt(i+1,ii,4)+sepy,4)

c      Draw 3 point in 2 and 4

c      Points in 2 and 4 (Experimental)

c      Points in 2
       alpha=(datan((v(i+1,jcon(i+1,ii,2)-1,3)-v(i+1,jcon(i+1,ii,2)+1,
     + 3))/(u(i+1,jcon(i+1,ii,2)-1,3)-u(i+1,jcon(i+1,ii,2)+1,3))))
       xpeq=ucnt(i+1,ii,2)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,2)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,4)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),4)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,4)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),4)

c      Points in 4
       alpha=(datan((v(i+1,jcon(i+1,ii,4)-1,3)-v(i+1,jcon(i+1,ii,4)+1,
     + 3))/(u(i+1,jcon(i+1,ii,4)-1,3)-u(i+1,jcon(i+1,ii,4)+1,3))))
       xpeq=ucnt(i+1,ii,4)+1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,4)-1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,4)
       call point(sepx+xpeq-1*dsin(alpha),sepy-ypeq-1*dcos(alpha),4)
       call point(sepx+xpeq-2*dsin(alpha),sepy-ypeq-2*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,4)
       call point(2530.*xkf+sepx+xpeq-1*dsin(alpha),sepy-ypeq-
     + 1*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq-2*dsin(alpha),sepy-ypeq-
     + 2*dcos(alpha),4)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 0. < h2 < 100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,10).gt.0.and.hvr(k,10).lt.100.) then

c      Segments
       call line(sepx+ucnt(i+1,ii,6),-vcnt(i+1,ii,6)+sepy,
     + sepx+ucnt(i+1,ii,8),-vcnt(i+1,ii,8)+sepy,4)
       call line(sepx+2530.*xkf+ucnt(i+1,ii,6),-vcnt(i+1,ii,6)+sepy,
     + sepx+2530.*xkf+ucnt(i+1,ii,8),-vcnt(i+1,ii,8)+sepy,4)

c      Punts marcatge V-rib
       alpha=datan((vcnt(i+1,ii,8)-vcnt(i+1,ii,6))/
     + (ucnt(i+1,ii,8)-ucnt(i+1,ii,6)))
       xp6=ucnt(i+1,ii,6)-xdes*dsin(alpha)
       yp6=vcnt(i+1,ii,6)+xdes*dcos(alpha)
       xp8=ucnt(i+1,ii,8)-xdes*dsin(alpha)
       yp8=vcnt(i+1,ii,8)+xdes*dcos(alpha)
       xp7=0.5*(xp6+xp8)
       yp7=0.5*(yp6+yp8)
       call point(sepx+xp6,sepy-yp6,4)
       call point(sepx+xp7,sepy-yp7,4)
       call point(sepx+xp8,sepy-yp8,4)
       call point(sepx+2530.*xkf+xp6,sepy-yp6,4)
       call point(sepx+2530.*xkf+xp7,sepy-yp7,4)
       call point(sepx+2530.*xkf+xp8,sepy-yp8,4)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case h2=100.
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,10).eq.100.) then

c      Segements
       call line(sepx+ucnt(i+1,ii,9),-vcnt(i+1,ii,9)+sepy,
     + sepx+ucnt(i+1,ii,11),-vcnt(i+1,ii,11)+sepy,4)
       call line(sepx+2530.*xkf+ucnt(i+1,ii,9),-vcnt(i+1,ii,9)+sepy,
     + sepx+2530.*xkf+ucnt(i+1,ii,11),-vcnt(i+1,ii,11)+sepy,4)

c      Draw 3 point in 9 and 11

c      Points in 9
       alpha=(datan((v(i+1,jcon(i+1,ii,9)-1,3)-v(i+1,jcon(i+1,ii,9)+1,
     + 3))/(u(i+1,jcon(i+1,ii,9)-1,3)-u(i+1,jcon(i+1,ii,9)+1,3))))
       xpeq=ucnt(i+1,ii,9)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,9)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,4)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),4)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,4)
       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),4)

c      Points in 11
       alpha=(datan((v(i+1,jcon(i+1,ii,11)-1,3)-v(i+1,jcon(i+1,ii,11)+1,
     + 3))/(u(i+1,jcon(i+1,ii,11)-1,3)-u(i+1,jcon(i+1,ii,11)+1,3))))
       xpeq=ucnt(i+1,ii,11)-1.*xdes*dsin(alpha)
       ypeq=vcnt(i+1,ii,11)+1.*xdes*dcos(alpha)
       call point(sepx+xpeq,sepy-ypeq,4)
       call point(sepx+xpeq+1*dsin(alpha),sepy-ypeq+1*dcos(alpha),4)
       call point(sepx+xpeq+2*dsin(alpha),sepy-ypeq+2*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq,sepy-ypeq,4)
       call point(2530.*xkf+sepx+xpeq+1*dsin(alpha),sepy-ypeq+
     + 1*dcos(alpha),4)
       call point(2530.*xkf+sepx+xpeq+2*dsin(alpha),sepy-ypeq+
     + 2*dcos(alpha),4)

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      16.6.6 Draw V-rib type 6 in 3D model
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Colors definition if even or odd
       control=((hvr(k,3))/2.)-float(int((hvr(k,3))/2.))
       if (control.ne.0) then
       icolor=4
       else
       icolor=30
       end if

c      Draw in 3D model
       do j=1,21
       call line3d(rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),icolor)
       call line3d(-rx2(i,j,ii),ry2(i,j,ii),rz2(i,j,ii),
     + -rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),icolor)
       end do

c      end if V-rib type 6
       end if


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c   End type 6
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


c      Seguent dispositiu

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     17. CALAGE CALCULUS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Speed
c      do i=1,n128

       
c      end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     18. TXT OUTPUT lep-out.txt
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     18.1 Main output
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Customized header
       if (ich.eq.1) then
       write (23,*) 
       write (23,*) "**************************************************"
       write (23,'(1x,A72)') lepuser
       write (23,*) "**************************************************"
       else
       write (23,*)
       end if

       write (23,'(A31,1x,A6,1x,A7,1x,A50)') 
     + " LABORATORI D'ENVOL PARAGLIDING",lepv,"version",lepc
       write (23,*) "by Pere Casellas 2010-2021"
       write (23,*) "http://www.laboratoridenvol.com"
       write (23,*) "General Public License GNU/GPL 3.0"
       write (23,*)
       write (23,*) "Brand: ", bname
       if (atp.eq."pc") then
       write (23,*) "Parachute model: ", wname
       else
       write (23,*) "Paraglider model: ", wname
       end if
       write (23,'(A9,3x,F7.5)') "scale: ", xwf

c      Area

       farea=(rib(1,4)-rib(1,3))*rib(1,2)

       parea=(rib(1,4)-rib(1,3))*rib(1,6)

       do i=1,nribss-1

       farea=farea+(rib(i,4)-rib(i,3)+rib(i+1,4)-rib(i+1,3))*0.5*
     + (rib(i+1,2)-rib(i,2))

       parea=parea+(rib(i,4)-rib(i,3)+rib(i+1,4)-rib(i+1,3))*0.5*
     + (rib(i+1,6)-rib(i,6))

       end do

       farea=farea*2./10000.
       parea=parea*2./10000.

c      Span

       fspan=2.*rib(nribss,2)/100.
       pspan=2.*rib(nribss,6)/100.

c      A/R Aspect Ratio

       faratio=fspan*fspan/farea
       paratio=pspan*pspan/parea

       write (23,*)
       write (23,*) "1. MAIN PARAMETERS:"
       write (23,*) "-------------------------------------------------"
       write (23,'(A,1x,F5.2,A,F6.1,A)') "Flat area = ", farea, " m2 ",
     + farea*10.7639," ft2"
       write (23,'(A,1x,F5.2,A,F6.1,A)') "Flat span = ",fspan, " m  ",
     + fspan/0.3048," ft" 
       write (23,'(A,1x,F4.2)') "Flat A/R = ", faratio
       write (23,*)
       write (23,'(A,1x,F5.2,A,F6.1,A)') "Projected area = ", parea, 
     + " m2 ",parea*10.7639," ft2"
       write (23,'(A,1x,F5.2,A,F6.1,A)') "Projected span = ",pspan, 
     + " m  ",pspan/0.3048," ft" 
       write (23,'(A,1x,F4.2)') "Projected A/R = ", paratio
       write (23,'(A,1x,F5.2)') "Flattening = ", ((farea-parea)/farea)*100.

c      More geometric parameters
       write (23,*)
       write (23,'(A)') "More geometric parameters:"
       varrow=(rib(nribss,7)-rib(1,7))*xwf/100
       write (23,'(A,1x,F5.2,A)') "Vault arrow = ", varrow, " m"
       write (23,'(A,1x,F5.2)') "Proj_span/arrow = ", pspan/varrow
       write (23,'(A,1x,F5.2,A)') "Line heigth (included risers) = ", 
     + (clengr+clengl)/100, " m"
       write (23,'(A,1x,F5.2)') "Proj_span/Line_heigth = ", 
     + pspan*100/(clengl)
       clli=(dsqrt((clengl-rib(nribss,7)*xwf)*(clengl-rib(nribss,7)*
     + xwf)+(pspan*0.50d0*100.0d0)*(pspan*0.5d0*100.0d0)))/100.0d0
       write (23,'(A,1x,F5.2,A)') "Karabiners - wingtip = ", clli, " m"
       write (23,'(A,1x,F5.2)') "Proj_span/(Karabiners - wingtip) = ",
     + pspan/clli

c      Wing type
       write (23,*) 
       write (23,'(A,A)') "Wing type is: ", atp
       write (23,*)

c      Center of gravity

       write (23,'(A,F5.2,A)') "Planform center of gravity at ", cdg, 
     + " % from leading edge"

c      Calage properties     

       write (23,*)
       write (23,*) "2. CALAGE PROPERTIES:"
       write (23,*) "-------------------------------------------------"
       write (23,'(A,1x,F5.2)') "finesse GR ", planeig
       write (23,'(A,1x,F5.2)') "glide angle ", afinesse
       write (23,'(A,1x,F5.2)') "AoA ", aoa
       write (23,'(A,1x,F5.2)') "assiette ", assiette
       write (23,'(A,1x,F6.0,A)') "total height hcp (inc risers)", 
     + hcp, " cm"
       write (23,'(A,1x,F6.0,A)') "risers", clengr, " cm"
       write (23,'(A,1x,F6.2,2x,F6.2)') "calage, pilot centering % cm"
     + , calage, calag
       write (23,'(2A,1x,F6.2,2x,F6.2)') "center pressure (estimation)",
     + " cm", cpress, cple
       write (23,'(A,3(3x,F7.2))') "karabiners (x,y,z) ",xkar,ykar,zkar
       write (23,*)

c      Rib properties

       write (23,*) "3. RIB PROPERTIES:"
       write (23,*) "-------------------------------------------------"
       write (23,*) "Ribs number = ", nribss*2
       write (23,*) "Cells number = ", nribss*2-1
       if (rib(1,2).lt.0.01) then
       write (23,*) "Zero-thickness central cell"
       end if
       write (23,*)

       write (23,*) "Rib - Chord - washin - beta - Rot_z"
       write (23,*) "-------------------------------------------------"

       do i=1,nribss

       write (23,'(I2,5x,F6.2,2x,F6.3,2x,F5.2,2x,F5.2)') i,rib(i,5), 
     + rib(i,8),rib(i,9),rib(i,250)

       end do

c      Cell properties

       write(23,*)

       write (23,*) "Cell   width (cm)"
      
       write (23,'(I2,7x,F5.2)') 0, 2.*rib(1,2)
       
       do i=1,nribss-1

       write (23,'(I2,5x,F5.2)') i, rib(i+1,2)-rib(i,2)

       end do

c      Anchor points

c      Lines

       xlength=0.

       write (23,*)
       write (23,*) "4. LINE MATRIX, LINE LENGTHS,AND LINE LOADS:"
       write (23,*) "Line-plan- level- order- ap  - r - row - rib -  L  
     +  -   length -length_e - load (Kg)"
       write (23,*) "------------------------------------------------",
     + "--------------------------"

       do i=1,cordat

       write (23,'(8(I3,3x),A,3x,2(F6.2,3x),F7.2)') i,corda(i,1),
     + corda(i,2),corda(i,3),corda(i,4),corda(i,5),corda(i,6),
     + corda(i,7)," L = ",xline(i), xlifi(i), xload(i)

       if (corda(i,2).ne.1) then
       xlength=xlength+xline(i)
       end if

       end do

       write (23,*)
       write (23,'(A,1x,F8.2)') "Total line lengths (without loops) = " 
     + , xlength*2./100.

      write (23,'(A,1x,F8.2)') "Total line lengths (with loops) = " 
     + , xlength*2./100.+(10.*2.*cordat*2)/100.
      write (23,*) "(estimation of 10 cm additional per loop)"

       write (23,*)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     18.2 ADJUSTEMENT SEAM PARAMETERS
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
  
c      Ajust de costura

       write (23,*)
       write (23,*) "5. Adjustment seam parameters on the inner side" 
       write (23,*) "of extrados panels (fig. 10 of the manual)"
       write (23,*) "-------------------------------------------------"

       if (ndif.eq.1000) then
       write (23,*) "Not used ( ndif=1000 )"
       else
       write (23,*) "Points number= ", ndif, "  scale= ",xndif
       do i=1,nribss-1
       write (23,*) "Rib= ", i, " dif= ", rib(i,81)
       end do
       end if

       write (23,*)

c      Panels and rib differences report

       write (23,*)
       write (23,*) "6. VERIFICATION Panels and rib differences (mm):"
       write (23,*) "-------------------------------------------------"
       write (23,*) "NOTE: Maximal accuracy ",
     + "<< 0.02 mm in extrados and intrados panels"
       write (23,*)
       write (23,*) "Number - Panel at left - Rib - Panel at right -", 
     + " max dif (mm)"

       if (atp.eq."ss") then
       do i=1,nribss-1
       xmax=max(abs(rib(i,30)-rib(i,31)),abs(rib(i,32)-rib(i,31)))
       write(23,'(I2,3x,F10.2,F10.2,F10.2,F10.2,F10.2)') 
     + i,10.*rib(i,30)+10.*rib(i,26),10.*rib(i,31)+10.*rib(i,26),
     + 10.*rib(i,32)+10.*rib(i,26),10.*xmax
       end do
       end if

       if (atp.ne."ss") then

c      Ribs 1 to nribss-1
       do i=1,nribss-1
       xmaxe=max(abs(rib(i,30)-rib(i,31)),abs(rib(i,32)-rib(i,31)))
       xmaxi=max(abs(rib(i,33)-rib(i,34)),abs(rib(i,35)-rib(i,34)))
       write (23,*)
       write (23,'(I2,2x,F10.2,F10.2,F10.2,F10.3,A6)') 
     + i,10*rib(i,30),10*rib(i,31),10*rib(i,32),10.*xmaxe," extra"
       write (23,'(I2,2x,F10.2,F10.2,F10.2,F10.3,A6)') 
     + i,10*rib(i,33),10*rib(i,34),10*rib(i,35),10.*xmaxi," intra"
       end do

c      Last rib
       i=nribss
       xmaxe=abs(rib(i,30)-rib(i,31))
       xmaxi=abs(rib(i,33)-rib(i,34))
       write (23,*)
       write (23,'(I2,2x,F10.2,F10.2,A10,F10.3,A6)') 
     + i,10*rib(i,30),10*rib(i,31),"   -    ",10.*xmaxe," extra"
       write (23,'(I2,2x,F10.2,F10.2,A10,F10.3,A6)') 
     + i,10*rib(i,33),10*rib(i,34),"   -    ",10.*xmaxi," intra"

       end if

       write (23,*)

c      Print distorsions

       write (23,*) "Panel distorsions in the leading edge (mm):"
       write (23,*) "-------------------------------------------"
       write (23,*) "Panel   D. extra   D. intra"
       do i=0,nribss-1
       write (23,'(I3,2x,F10.4,F10.4)')
     + i,(rib(i,97)-rib(i,96))*10.,(rib(i,99)-rib(i,98))*10.
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.3 Speed system amb trim calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k28p.eq.1) then
       
       write(23,*)
       write(23,*) "7. CALAGE AND RISERS VARIATIONS WITH ANGLE"

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.3.1 a) Speed system pivot in last riser
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       a1281=a128/dfloat(n128)

       do j=1,n128+1 ! itera en angles

       alpha28(j)=a1281*dfloat(j-1) 

c      Initial and final lengths
       
       do k=1,nriser28

       x1=p28(k)*rib(1,5)/100.0d0
       y1=0.0d0
       x2=calage*rib(1,5)/100.0d0
       y2=clengl+clengr
       lini28(j,k)=dsqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

       hhh=(p28(nriser28)-p28(k))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       x3=x1+hhh-xxx
       y3=yyy
       lfin28(j,k)=dsqrt(((x2-x3)*(x2-x3))+((y2-y3)*(y2-y3)))

       end do

c      New calage, use values k=nriser28

       xru(1)=p28(nriser28)*rib(1,5)/100.0d0
       xrv(1)=0.0d0
       hhh=(p28(nriser28)-p28(1))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       xru(2)=(p28(1)*rib(1,5)/100.0d0)+hhh-xxx
       xrv(2)=-yyy

       xsu(1)=calage*rib(1,5)/100.0d0
       xsv(1)=clengl+clengr
       xsu(2)=xsu(1)+100.0d0*dtan(alpha28(j)*pi/180.0d0)
       xsv(2)=xsv(1)-100.0d0

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (alpha28(j).eq.0.0d0) then
       xtu=calage*rib(1,5)/100.0d0
       xtv=0.0d0
       end if
       
       p28max=(p28(nriser28))*rib(i,5)/100.0d0
       xru(3)=p28max*(1.0d0-dcos(alpha28(j)*pi/180.0d0))
       xrv(3)=-p28max*sin(alpha28(j)*pi/180.0d0)

       calagnew(j)=(dsqrt(((xtu-xru(3))*(xtu-xru(3)))+
     + ((xtv-xrv(3))*(xtv-xrv(3)))))*100.0d0/rib(1,5)

       cnewtps(j)=calagnew(j)
       cnewcms(j)=lini28(j,1)-lfin28(j,1)

       end do

c      Print case 2 risers
       if (nriser28.eq.2) then
       write(23,*)
       write(23,*) "a) Speed system pivot in last riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","Calage"
       do j=1,n128+1
       write(*,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lini28(j,1)-lfin28(j,1),
     + lini28(j,2)-lfin28(j,2), calagnew(j)
       end do
       end if

c      Print case 3 risers
       if (nriser28.eq.3) then
       write(23,*)
       write(23,*) "a) Speed system pivot in last riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","Calage"
       do j=1,n128+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lini28(j,1)-lfin28(j,1),
     + lini28(j,2)-lfin28(j,2),lini28(j,3)-lfin28(j,3), calagnew(j)
       end do
       end if

c      Print case 4 risers
       if (nriser28.eq.4) then
       write(23,*)
       write(23,*) "a) Speed system pivot in last riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","D","Calage"
       do j=1,n128+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F5.2,2x,
     + A6)') j,alpha28(j),lini28(j,1)-lfin28(j,1),lini28(j,2)-lfin28
     + (j,2),lini28(j,3)-lfin28(j,3),lini28(j,4)-lfin28(j,4),calagnew(j)
       end do
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.3.2 b) Speed system pivot in first riser
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       a1281=a128/dfloat(n128)

       do j=1,n128+1 ! itera en angles

       alpha28(j)=a1281*dfloat(j-1) 

c      Initial and final lengths
       
       do k=1,nriser28

       x1=p28(k)*rib(1,5)/100.0d0
       y1=0.0d0
       x2=calage*rib(1,5)/100.0d0
       y2=clengl+clengr
       lini28(j,k)=dsqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

       hhh=(p28(k)-p28(1))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       x3=(p28(1)*rib(1,5)/100.0d0)+xxx
       y3=yyy
       lfin28(j,k)=dsqrt(((x2-x3)*(x2-x3))+((y2-y3)*(y2-y3)))

       end do

c      New calage, use values k=nriser28

       xru(1)=p28(1)*rib(1,5)/100.0d0
       xrv(1)=0.0d0
       hhh=(p28(nriser28)-p28(1))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       xru(2)=xru(1)+xxx
       xrv(2)=yyy

       xsu(1)=calage*rib(1,5)/100.0d0
       xsv(1)=clengl+clengr
       xsu(2)=xsu(1)+100.0d0*dtan(alpha28(j)*pi/180.0d0)
       xsv(2)=xsv(1)-100.0d0

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (alpha28(j).eq.0.0d0) then
       xtu=calage*rib(1,5)/100.0d0
       xtv=0.0d0
       end if

       xru(3)=xru(1)*(1.0d0-dcos(alpha28(j)*pi/180.0d0))
       xrv(3)=-xru(1)*dsin(alpha28(j)*pi/180.0d0)

       calagnew(j)=(dsqrt(((xtu-xru(3))*(xtu-xru(3)))+
     + ((xtv-xrv(3))*(xtv-xrv(3)))))*100.0d0/rib(1,5)

       end do

c      Print case 2 risers
       if (nriser28.eq.2) then
       write(23,*)
       write(23,*) "b) Speed system pivot in first riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","Calage"
       do j=1,n128+1
       write(*,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lfin28(j,1)-lini28(j,1),
     + lfin28(j,2)-lini28(j,2), calagnew(j)
       end do
       end if

c      Print case 3 risers
       if (nriser28.eq.3) then
       write(23,*)
       write(23,*) "b) Speed system pivot in first riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","Calage"
       do j=1,n128+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lfin28(j,1)-lini28(j,1),
     + lfin28(j,2)-lini28(j,2),lfin28(j,3)-lini28(j,3), calagnew(j)
       end do
       end if

c      Print case 4 risers
       if (nriser28.eq.4) then
       write(23,*)
       write(23,*) "b) Speed system pivot in first riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","D","Calage"
       do j=1,n128+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,
     + A6)') j,alpha28(j),lfin28(j,1)-lini28(j,1),lfin28(j,2)-lini28
     + (j,2),lfin28(j,3)-lini28(j,3),lfin28(j,4)-lini28(j,4),calagnew(j)
       end do
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.3.3 c) Trimer system pivot in first riser
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       a2282=a228/dfloat(n228)

       do j=1,n228+1 ! itera en angles

       alpha28(j)=a2282*dfloat(j-1) 

c      Initial and final lengths
       
       do k=1,nriser28

       x1=p28(k)*rib(1,5)/100.0d0
       y1=0.0d0
       x2=calage*rib(1,5)/100.0d0
       y2=clengl+clengr
       lini28(j,k)=dsqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

       hhh=(p28(k)-p28(1))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       x3=(p28(1)*rib(1,5)/100.0d0)+xxx
       y3=yyy
       lfin28(j,k)=dsqrt(((x2-x3)*(x2-x3))+((y2-y3)*(y2-y3)))

       end do

c      New calage, use values k=nriser28

       xru(1)=p28(1)*rib(1,5)/100.0d0
       xrv(1)=0.0d0
       hhh=(p28(nriser28)-p28(1))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       xru(2)=xru(1)+xxx
       xrv(2)=yyy

       xsu(1)=calage*rib(1,5)/100.0d0
       xsv(1)=clengl+clengr
       xsu(2)=xsu(1)+100.0d0*dtan(alpha28(j)*pi/180.0d0)
       xsv(2)=xsv(1)-100.0d0

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (alpha28(j).eq.0.0d0) then
       xtu=calage*rib(1,5)/100.0d0
       xtv=0.0d0
       end if

       xru(3)=xru(1)*(1.0d0-dcos(alpha28(j)*pi/180.0d0))
       xrv(3)=-xru(1)*dsin(alpha28(j)*pi/180.0d0)

       calagnew(j)=(dsqrt(((xtu-xru(3))*(xtu-xru(3)))+
     + ((xtv-xrv(3))*(xtv-xrv(3)))))*100.0d0/rib(1,5)

       cnewtpt(j)=calagnew(j)
       cnewcmt(j)=lini28(j,nriser28)-lfin28(j,nriser28)

       end do

c      Print case 2 risers
       if (nriser28.eq.2) then
       write(23,*)
       write(23,*) "c) Trimer system pivot in first riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","Calage"
       do j=1,n228+1
       write(*,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lfin28(j,1)-lini28(j,1),
     + lfin28(j,2)-lini28(j,2), calagnew(j)
       end do
       end if

c      Print case 3 risers
       if (nriser28.eq.3) then
       write(23,*)
       write(23,*) "c) Trimer system pivot in first riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","Calage"
       do j=1,n228+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lfin28(j,1)-lini28(j,1),
     + lfin28(j,2)-lini28(j,2),lfin28(j,3)-lini28(j,3), calagnew(j)
       end do
       end if

c      Print case 4 risers
       if (nriser28.eq.4) then
       write(23,*)
       write(23,*) "b) Trimer system pivot in first riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","D","Calage"
       do j=1,n228+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,
     + A6)') j,alpha28(j),lfin28(j,1)-lini28(j,1),lfin28(j,2)-lini28
     + (j,2),lfin28(j,3)-lini28(j,3),lfin28(j,4)-lini28(j,4),calagnew(j)
       end do
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.3.4 d) Trimer system pivot in last riser
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

    
       a2282=a228/dfloat(n228)

       do j=1,n228+1 ! itera en angles

       alpha28(j)=a2282*dfloat(j-1) 

c      Initial and final lengths
       
       do k=1,nriser28

       x1=p28(k)*rib(1,5)/100.0d0
       y1=0.0d0
       x2=calage*rib(1,5)/100.0d0
       y2=clengl+clengr
       lini28(j,k)=dsqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))

       hhh=(p28(nriser28)-p28(k))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       x3=x1+hhh-xxx
       y3=yyy
       lfin28(j,k)=dsqrt(((x2-x3)*(x2-x3))+((y2-y3)*(y2-y3)))

       end do

c      New calage, use values k=nriser28

       xru(1)=p28(nriser28)*rib(1,5)/100.0d0
       xrv(1)=0.0d0
       hhh=(p28(nriser28)-p28(1))*rib(1,5)/100.0d0
       xxx=hhh*dcos(alpha28(j)*pi/180.0d0)
       yyy=hhh*dsin(alpha28(j)*pi/180.0d0)
       xru(2)=(p28(1)*rib(1,5)/100.0d0)+hhh-xxx
       xrv(2)=-yyy

       xsu(1)=calage*rib(1,5)/100.0d0
       xsv(1)=clengl+clengr
       xsu(2)=xsu(1)+100.0d0*dtan(alpha28(j)*pi/180.0d0)
       xsv(2)=xsv(1)-100.0d0

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       if (alpha28(j).eq.0.0d0) then
       xtu=calage*rib(1,5)/100.0d0
       xtv=0.0d0
       end if

       p28max=(p28(nriser28))*rib(i,5)/100.0d0
       xru(3)=p28max*(1.0d0-dcos(alpha28(j)*pi/180.0d0))
       xrv(3)=-p28max*dsin(alpha28(j)*pi/180.0d0)

       calagnew(j)=(dsqrt(((xtu-xru(3))*(xtu-xru(3)))+
     + ((xtv-xrv(3))*(xtv-xrv(3)))))*100.0d0/rib(1,5)

       end do

c      Print case 2 risers
       if (nriser28.eq.2) then
       write(23,*)
       write(23,*) "d) Trimer system pivost in last riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","Calage"
       do j=1,n228+1
       write(*,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lini28(j,1)-lfin28(j,1),
     + lini28(j,2)-lfin28(j,2), calagnew(j)
       end do
       end if

c      Print case 3 risers
       if (nriser28.eq.3) then
       write(23,*)
       write(23,*) "d) Trimer system pivot in last riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","Calage"
       do j=1,n228+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,A6)') 
     + j,alpha28(j),lini28(j,1)-lfin28(j,1),
     + lini28(j,2)-lfin28(j,2),lini28(j,3)-lfin28(j,3), calagnew(j)
       end do
       end if

c      Print case 4 risers
       if (nriser28.eq.4) then
       write(23,*)
       write(23,*) "d) Trimer system pivot in last riser:"
       write (23,*) "-------------------------------------------"
       write(23,'(A2,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6,2x,A6)') "i","alpha",
     + "A","B","C","D","Calage"
       do j=1,n228+1
       write(23,'(I2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,F6.2,2x,
     + A6)') j,alpha28(j),lini28(j,1)-lfin28(j,1),lini28(j,2)-lfin28
     + (j,2),lini28(j,3)-lfin28(j,3),lini28(j,4)-lfin28(j,4),calagnew(j)
       end do
       end if






cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.3.5 Draw calage variations
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


c     Box (2,1)

       x0=0.-400.0*xkf
       y0=900.*xkf+600.*xkf

c      Draw box

       xakk=2.*xkf
       yakk=2.*xkf
       xa=100.*xakk
       ya=100.*yakk

       call line(x0,y0,x0+xa,y0,7)
       call line(x0,y0,x0,y0-ya,7)
       call line(x0+xa,y0,x0+xa,y0-ya,7)
       call line(x0,y0-ya,x0+xa,y0-ya,7)

       do j=1,9
       call line(x0+10.*float(j)*xakk,y0,x0+10.*float(j)*xakk,y0-ya,8)
       end do

       do j=1,19
       call line(x0,y0-5.*float(j)*yakk,x0+xa,y0-5.*float(j)*yakk,9)
       end do

       xtext="Calage %"
       call txt(x0+xa/2.0d0-10.0d0,y0+25.0d0,8.0d0,0.0d0,xtext,7)
       xtext="0 %"
       call txt(x0-10.,y0+12.,8.0d0,0.0d0,xtext,7)
       write (xtext,'(F5.2)') calage
       call txt(x0+calage*xakk-10.,y0+12.,8.0d0,0.0d0,xtext,7)
       xtext="100 %"
       call txt(x0+xa,y0+12.,8.0d0,0.0d0,xtext,7)

       xtext="Speed system (cm)"
       call txt(x0-20.,y0-20,8.0d0,90.0d0,xtext,1)
       xtext="0"
       call txt(x0-10.,y0,8.0d0,0.0d0,xtext,1)
       xtext="20"
       call txt(x0-10.,y0-ya,8.0d0,0.0d0,xtext,1)

       xtext="Trimer system (cm)"
       call txt(x0+xa+20.,y0-20,8.0d0,90.0d0,xtext,5)
       xtext="0"
       call txt(x0+xa+10.,y0,8.0d0,0.0d0,xtext,5)
       xtext="20"
       call txt(x0+xa+10.,y0-ya,8.0d0,0.0d0,xtext,5)

       do j=1,n128

       call line(x0+cnewtps(j)*xakk,y0+cnewcms(j)*5.*yakk,
     + x0+cnewtps(j+1)*xakk,y0+cnewcms(j+1)*5.*yakk,1)

       end do

       do j=1,n228

       call line(x0+cnewtpt(j)*xakk,y0-cnewcmt(j)*5.*yakk,
     + x0+cnewtpt(j+1)*xakk,y0-cnewcmt(j+1)*5.*yakk,5)

       end do

       end if ! Case k28p=1


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.4 Print joncs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (k21d.ge.1) then
       x1=0.
       write (23,*)
       write (23,*) "8. NYLON RODS (JONCS)"
       write (23,*) "-------------------------------------------"
       do m=1,k21blocs
       write (23,'(A5,I3,A8,I2)') "BLOC ",m,"   TYPE ",k21blocf(m,2) 
       write (23,*) "-------------------------------------------"
       do ng=1,k21blocf(m,3)
       write (23,'(A5,I3)') "Group",ng
       write (23,*) "----------------------------"
       do i=ngoo(m,ng,2),ngoo(m,ng,3)
       x1=x1+joncf(i,m,ng,2)
       write (23,'(A5,I3,2x,F7.1)') "Jonc ",i,joncf(i,m,ng,2)
       end do
       write (23,*) "----------------------------"

       end do
       end do
       write (23,'(A,F8.2)') "Joncs total length m (both sides) ",
     + x1*2./100.
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.5 Print 3D-shaping details
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

 
c      Case k29d=0     
       if (k29d.eq.0) then
       write (23,*)
       write (23,*) "9. 3D-SHAPING DETAILS"
       write (23,*) "-------------------------------------------"
       write (23,*) 
       end if

c      Case k29d=1
       if (k29d.eq.1) then
       write (23,*)
       write (23,*) "9. 3D-SHAPING DETAILS"
       write (23,*) "-------------------------------------------"
       write (23,*) 

       ng=rib(i,169)

       do i=1,nribss

       if (uppcuts(ng).ge.1.or.lowcuts(ng).ge.1) then
       write (23,*) "-------------------------------------"
       write (23,*) "zone   rib      d1       d2    d2-d1 "
       write (23,*) "-------------------------------------"
       end if

       if (uppcuts(ng).eq.1) then
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z1 ",i,zinf(i,1,1),zinf(i,2,1),zinf(i,5,1)
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z3 ",i,zinf(i,1,3),zinf(i,2,3),zinf(i,5,3)
       write (23,'(A4,3x,I3,3x,F6.2)') "f13 ",i,zinf(i,6,1)
       end if

       if (uppcuts(ng).eq.2) then
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z1 ",i,zinf(i,1,1),zinf(i,2,1),zinf(i,5,1)
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z2 ",i,zinf(i,1,2),zinf(i,2,2),zinf(i,5,2)
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z3 ",i,zinf(i,1,3),zinf(i,2,3),zinf(i,5,3)
       write (23,'(A4,3x,I3,3x,F6.2)') "f12 ",i,zinf(i,6,1)
       write (23,'(A4,3x,I3,3x,F6.2)') "f23 ",i,zinf(i,6,2)
       end if

       if (uppcuts(ng).ge.1) then
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z4 ",i,zinf(i,1,4),zinf(i,2,4),zinf(i,5,4)
       end if

       if (lowcuts(ng).eq.1) then
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z5 ",i,zinf(i,1,5),zinf(i,2,5),zinf(i,5,5)
       write (23,'(A4,3x,I3,3x,F6.2,3x,F6.2,3x,F6.2)') 
     + "z6 ",i,zinf(i,1,6),zinf(i,2,6),zinf(i,5,6)
       write (23,'(A4,3x,I3,3x,F6.2)') "f56 ",i,zinf(i,6,4)
       end if
       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.6 Print informative extrados and intrados coeeficents
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
 
       write (23,*)
       write (23,*) "10. INFORMATIVE EXTRADOS AND INTRADOS COEFFICIENTS"
       write (23,*) "-------------------------------------------"
c       write (23,*) 

       write (23,*) "Rib             panel/rib (left) panel/rib (right)"
       do i=0,nribss-1
       write (23,'(I3,3x,A11,5x,F7.5,9x,F7.5)') i,"extrados ",
     + rib(i,194),rib(i,195)
       end do
       write (23,*) 
       do i=0,nribss-1
       write (23,'(I3,3x,A11,5x,F7.5,9x,F7.5)') i,"intrados ",
     + rib(i,200),rib(i,201)
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.7 Print information about profil points
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
 
       write (23,*)
       write (23,*) "11. INFORMATION ABOUT AIRFOIL POINTS"
       write (23,*) "-------------------------------------------"
c       write (23,*) 

       write (23,*) "Rib  Total Extra Vents Intra"
       do i=0,nribss
       write (23,'(I3,3x,I3,3x,I3,3x,I3,3x,I3)') i,np(i,1),np(i,2),
     + np(i,3),np(i,4)
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      18.8 Print angles between airfoil plane and glidepath
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       write (23,*)
       write (23,*) "12. ANGLES BETWEEN AIRFOIL PLANE AND GLIDEPATH LINE
     +  (phi) and local AoA (chi)"
       write (23,*) "---------------------------------------------------
     + -------------------------"
c       write (23,*) 
       write (23,*) "Informative angles. Change rotation values"
       write (23,*) "in column 10 of SECTION 1, using phi to improve the 
     + results"
       write (23,*) "phi=angle between airfoil plane and glidepath line"
       write (23,*) 'chi=angle between chord line and glidepath line (lo
     +cal AoA)'
       write (23,*)
       write (23,*) "Rib    phi      chi"
       do i=1,nribss
       write (23,'(I3,3x,F6.2,3x,F6.2)') i,-phii(i)*180.0d0/pi,
     + chii(i)*180.0d0/pi
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      19. lines.txt List of lines - labels in human readable format
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       write (30,*) "LEparagliding"
       write (30,*) "List of lines, human readable format"
       write (30,*) "Ready also to import in .ods or .xls formats"
       write (30,*)
       write (30,*) "Line number - Label - Lenght (cm)"
       write (30,*) 

       do i=1, cordat

c      Select letter as final row of the line
       write (ln1,'(I1)') corda (i,2)

       if (corda(i,6).eq.1) ln2="A"
       if (corda(i,6).eq.2) ln2="B"
       if (corda(i,6).eq.3) ln2="C"
       if (corda(i,6).eq.4) ln2="D"
       if (corda(i,6).eq.5) ln2="E"
       if (corda(i,6).eq.6) ln2="F"

c      If only two levels
c      Is OK

c      If tree levels
c      1 and 2 level will be named acording lineplan

c      Renames letters if levels 1 or 2

       if (corda(i,2).le.2.and.corda(i,5).ge.3) then

       if (corda(i,1).eq.1) ln2="A"
       if (corda(i,1).eq.2) ln2="B"
       if (corda(i,1).eq.3) ln2="C"
       if (corda(i,1).eq.4) ln2="D"
       if (corda(i,1).eq.5) ln2="E"
       if (corda(i,1).eq.6) ln2="F"

       end if

       if (corda(i,2).eq.1.and.corda(i,5).eq.2) then

       if (corda(i,1).eq.1) ln2="A"
       if (corda(i,1).eq.2) ln2="B"
       if (corda(i,1).eq.3) ln2="C"
       if (corda(i,1).eq.4) ln2="D"
       if (corda(i,1).eq.5) ln2="E"
       if (corda(i,1).eq.6) ln2="F"

       end if

c      Adjust brake letter to F

       if (i.gt.cordam) ln2="F"

c      Put 2 characters
       
c       if (corda(i,3).le.9)  write (ln3,'(I,I)') 0,corda(i,3)
c       if (corda(i,3).gt.9)  write (ln3,'(I2)') corda(i,3)

c       write (ln3,'(I2)') corda(i,3)

       if (corda(i,3).ge.10) then
       write (ln3,'(I2)') corda(i,3)
       end if

       if (corda(i,3).lt.10) then
       write (ln3,'(I1)') corda(i,3)
       end if


c      Change line order by final rib if upper line

       if (corda(i,2).eq.corda(i,5)) then

c       if (corda(i,7).le.9)  write (ln3,'(I,I)') 0,corda(i,7)
c       if (corda(i,7).gt.9)  write (ln3,'(I2)') corda(i,7)

       if (corda(i,7).ge.10) then
       write (ln3,'(I2)') corda(i,7)
       end if

       if (corda(i,7).lt.10) then
       write (ln3,'(I1)') corda(i,7)
       end if


       end if

c      Write line labels

       write (ln4(i),'(A1,A1,A2)') ln1,ln2,ln3
c       write (ln4(i),'(A1,A1)') ln1,ln2


       if (corda(i,6).eq.6) xlifi(i)=xline(i)

c      Row plan A

       if (i.eq.1) then 
       slpi(1)=i
       write (30,*)
       write (30,*) "Plan A"
       write (30,*) 
       end if

c      Rows plan B,C,D,E,F

       if(i.ge.2.and.corda(i-1,1).lt.corda(i,1)) then

       if (corda(i,1).eq.2) then
       slpi(2)=i
       write (30,*)
       write (30,*) "Plan B"
       write (30,*) 
       end if

       if (corda(i,1).eq.3) then
       slpi(3)=i
       write (30,*)
       write (30,*) "Plan C"
       write (30,*) 
       end if

       if (corda(i,1).eq.4.and.i.le.cordam) then
       slpi(4)=i
       write (30,*)
       write (30,*) "Plan D"
       write (30,*) 
       end if

       if (corda(i,1).eq.5.and.i.le.cordam) then
       slpi(5)=i
       write (30,*)
       write (30,*) "Plan E"
       write (30,*) 
       end if

       end if

c      Plan F

       if (i.eq.cordam+1) then
       slpi(6)=i
       write (30,*)
       write (30,*) "Brake lines"
       write (30,*) 
       end if

       write (30,'(I3,3x,A4,3x,F5.1)')  i, ln4(i), xlifi(i)

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     20. Draw labels in 2D (in tree of lines)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Labels in lines
       corda1=cordam

       do i=1,corda1

       x0=(1260.-160.)*xkf
       y0=1800.*xkf

       x00=1260.*xkf*float(corda(i,1)-1)

       xxk=0.7 ! controls label positions

       xlabel=x1line(corda(i,1),corda(i,2),corda(i,3))+
     + (x2line(corda(i,1),corda(i,2),corda(i,3))-
     + x1line(corda(i,1),corda(i,2),corda(i,3)))*xxk+x0+x00

       zlabel=z1line(corda(i,1),corda(i,2),corda(i,3))+
     + (z2line(corda(i,1),corda(i,2),corda(i,3))-
     + z1line(corda(i,1),corda(i,2),corda(i,3)))*xxk+y0

c       xlabel=((x1line(corda(i,1),corda(i,2),corda(i,3))+x0+x00)+
c     + (x2line(corda(i,1),corda(i,2),corda(i,3))+x0+x00))*0.5d0

c       zlabel=((z1line(corda(i,1),corda(i,2),corda(i,3))+y0)+
c     + (z2line(corda(i,1),corda(i,2),corda(i,3))+y0))*0.5d0

c      Text size = typm3(9)
       xtext=ln4(i)
       call txt(xlabel,zlabel,typm3(9),0.0d0,xtext,7)

       end do
   
c      Labels in brakes
       do i=cordam+1,cordat

       x0=(1260.-160.)*xkf
       y0=(1800.+890.95)*xkf

       x00=1260.*xkf*float(corda(i,1)-1)

       xlabel=((x1line(corda(i,1),corda(i,2),corda(i,3))+x0+x00)+
     + (x2line(corda(i,1),corda(i,2),corda(i,3))+x0+x00))*0.5d0

       zlabel=((z1line(corda(i,1),corda(i,2),corda(i,3))+y0)+
     + (z2line(corda(i,1),corda(i,2),corda(i,3))+y0))*0.5d0

c      Text size = typm3(9)   
       xtext=ln4(i)
       call txt(xlabel,zlabel,typm3(9),0.0d0,xtext,7)

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21. 3D model DXF drawing
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c       call dxfinit(25)

       do i=1,nribss

c      21.1 Extrados airfoil blue

       do j=1,np(i,2)-1

       p1x=x(i,j)
       p1y=y(i,j)
       p1z=z(i,j)
       p2x=x(i,j+1)
       p2y=y(i,j+1)
       p2z=z(i,j+1)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(11))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(11))

       end do

c      Draw extrados, straight line

       if (i.le.nribss.and.ele3d(11).eq.1) then

       do j=1,np(i,2)-1
       p1x=x(i-1,j)
       p1y=y(i-1,j)
       p1z=z(i-1,j)
       p2x=x(i,j)
       p2y=y(i,j)
       p2z=z(i,j)
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(11))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(11))
       end do

       end if

c      21.2 Vents

c      Case "ds" or "ss"
       if (atp.eq."ds".or.atp.eq."ss") then

       do j=np(i,2),np(i,2)+np(i,3)-2

       p1x=x(i,j)
       p1y=y(i,j)
       p1z=z(i,j)
       p2x=x(i,j+1)
       p2y=y(i,j+1)
       p2z=z(i,j+1)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))

       end do

c      Draw vents, straight line

       if (i.le.nribss.and.ele3d(12).eq.1) then

       do j=np(i,2),np(i,2)+np(i,3)-2
       p1x=x(i-1,j)
       p1y=y(i-1,j)
       p1z=z(i-1,j)
       p2x=x(i,j)
       p2y=y(i,j)
       p2z=z(i,j)
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       end do

       end if

       end if ! ds or ss

c      Case "pc"
       if (atp.eq."pc") then

       j1=np(i,2)
       j2=np(i,2)+np(i,3)-1

       p1x=x(i,j1)
       p1y=y(i,j1)
       p1z=z(i,j1)
       p2x=x(i,j2)
       p2y=y(i,j2)
       p2z=z(i,j2)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3d(12))

       end if

c      21.3 Intrados 

       do j=np(i,2)+np(i,3)-1,np(i,1)-1

       p1x=x(i,j)
       p1y=y(i,j)
       p1z=z(i,j)
       p2x=x(i,j+1)
       p2y=y(i,j+1)
       p2z=z(i,j+1)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(13))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(13))

       end do

c      Draw intrados, straight line

       if (i.le.nribss.and.ele3d(13).eq.1) then

       do j=np(i,2)+np(i,3)-1,np(i,1)-1
       p1x=x(i-1,j)
       p1y=y(i-1,j)
       p1z=z(i-1,j)
       p2x=x(i,j)
       p2y=y(i,j)
       p2z=z(i,j)
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(13))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(13))
       end do

       end if


       end do

c      21.4 Trailing edge

       do i=1,nribss-1

       p1x=x(i,1)
       p1y=y(i,1)
       p1z=z(i,1)
       p2x=x(i+1,1)
       p2y=y(i+1,1)
       p2z=z(i+1,1)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(11))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(11))

       end do

       p1x=x(1,1)
       p1y=y(1,1)
       p1z=z(1,1)
       p2x=-x(1,1)
       p2y=y(1,1)
       p2z=z(1,1)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(11))

c      21.5 Leading edge

c      Case classic
       if (k26d.eq.0) then

c      Vent in

       do i=1,nribss

       p1x=x(i-1,np(i,2))
       p1y=y(i-1,np(i,2))
       p1z=z(i-1,np(i,2))
       p2x=x(i,np(i,2))
       p2y=y(i,np(i,2))
       p2z=z(i,np(i,2))

       if (rib(i,14).eq.1) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       end if
       if (rib(i,14).eq.0) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,9)
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,9)
       end if


       end do

c       p1x=x(1,np(i,2))
c       p1y=y(1,np(i,2))
c       p1z=z(1,np(i,2))
c       p2x=-x(1,np(i,2))
c       p2y=y(1,np(i,2))
c       p2z=z(1,np(i,2))

c       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,1)

c      Vent out

       do i=1,nribss

       j=np(i,2)+np(i,3)-1

       p1x=x(i-1,j)
       p1y=y(i-1,j)
       p1z=z(i-1,j)
       p2x=x(i,j)
       p2y=y(i,j)
       p2z=z(i,j)

       if (rib(i,14).eq.1) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       end if
       if (rib(i,14).eq.4) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,9)
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,9)
       end if

       end do

       end if ! k26d=0


c      Case new vents
       if (k26d.eq.1) then

c      Vent in

       do i=1,nribss

       p1x=x(i-1,np(i,2))
       p1y=y(i-1,np(i,2))
       p1z=z(i-1,np(i,2))
       p2x=x(i,np(i,2))
       p2y=y(i,np(i,2))
       p2z=z(i,np(i,2))

       j=np(i,2)+np(i,3)-1

       p3x=x(i-1,j)
       p3y=y(i-1,j)
       p3z=z(i-1,j)
       p4x=x(i,j)
       p4y=y(i,j)
       p4z=z(i,j)

       if (rib(i,165).eq.0) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       call line3d(p3x,p3y,p3z,p4x,p4y,p4z,ele3dc(12))
       call line3d(-p3x,p3y,p3z,-p4x,p4y,p4z,ele3dc(12))
       end if

       if (rib(i,165).eq.1.or.rib(i,165).eq.6) then
       call line3d(p3x,p3y,p3z,p4x,p4y,p4z,ele3dc(12))
       call line3d(-p3x,p3y,p3z,-p4x,p4y,p4z,ele3dc(12))
       end if

       if (rib(i,165).eq.-1.or.rib(i,165).eq.-6) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       end if

       if (rib(i,165).eq.-2) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       call line3d(p3x,p3y,p3z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p3x,p3y,p3z,-p2x,p2y,p2z,ele3dc(12))
       end if

       if (rib(i,165).eq.-3) then
       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,ele3dc(12))
       call line3d(p1x,p1y,p1z,p4x,p4y,p4z,ele3dc(12))
       call line3d(-p1x,p1y,p1z,-p4x,p4y,p4z,ele3dc(12))
       end if


c      Vents type 4,-4,-5
       if (rib(i,165).eq.4.or.rib(i,165).eq.-4.or.rib(i,165).eq.-5) then

c      Interpolate new vent init

c      Load vent polyline
c      Left side
       do j=np(i,2),np(i,2)+np(i,3)-1
       xpoly(j)=x(i-1,j)
       ypoly(j)=y(i-1,j)
       zpoly(j)=z(i-1,j)
       end do
       npo=np(i,3)

c      Length vent left
       xlenl=0.0d0
       do j=np(i,2),np(i,2)+np(i,3)-2
       xlenl=xlenl+dsqrt((xpoly(j+1)-xpoly(j))*(xpoly(j+1)-xpoly(j))+
     + (ypoly(j+1)-ypoly(j))*(ypoly(j+1)-ypoly(j))+
     + (zpoly(j+1)-zpoly(j))*(zpoly(j+1)-zpoly(j)))  
       end do
       xlenlr=xlenl*(1.-csi(i,19)/100.)

c      Interpole point
       call interpoly3d(xpoly,ypoly,zpoly,x_poly,y_poly,z_poly,
     + xlenlr,np(i,2),np(i,2)+np(i,3)-1,npolyl,distrel)
       x_poly1=x_poly
       y_poly1=y_poly
       z_poly1=z_poly
       distrel1=distrel

c      Right side
       do j=np(i,2),np(i,2)+np(i,3)-1
       xpoly(j)=x(i,j)
       ypoly(j)=y(i,j)
       zpoly(j)=z(i,j)
       end do
       npo=np(i,3)

c      Length vent right
       xlenr=0.0d0
       do j=np(i,2),np(i,2)+np(i,3)-2
       xlenr=xlenr+dsqrt((xpoly(j+1)-xpoly(j))*(xpoly(j+1)-xpoly(j))+
     + (ypoly(j+1)-ypoly(j))*(ypoly(j+1)-ypoly(j))+
     + (zpoly(j+1)-zpoly(j))*(zpoly(j+1)-zpoly(j)))  
       end do
       xlenrr=xlenr*(1.-csi(i,20)/100.)

c      Interpole point
       call interpoly3d(xpoly,ypoly,zpoly,x_poly,y_poly,z_poly,
     + xlenrr,np(i,2),np(i,2)+np(i,3)-1,npolyl,distrel)
       x_poly2=x_poly
       y_poly2=y_poly
       z_poly2=z_poly
       distrel2=distrel

c      Case 4,-4,-5
c      Draw line vent
       call line3d(x_poly1,y_poly1,z_poly1,x_poly2,y_poly2,z_poly2,
     + ele3dc(12))
       call line3d(-x_poly1,y_poly1,z_poly1,-x_poly2,y_poly2,z_poly2,
     + ele3dc(12))

c      Case -5 still not drawn

c      Draw line extrados
       if (rib(i,165).eq.-4.or.rib(i,165).eq.-5) then
       j=np(i,2)
       call line3d(x(i-1,j),y(i-1,j),z(i-1,j),x(i,j),y(i,j),z(i,j),
     + ele3dc(12))
       call line3d(-x(i-1,j),y(i-1,j),z(i-1,j),-x(i,j),y(i,j),z(i,j),
     + ele3dc(12))
       end if

c      Draw line intrados
       if (rib(i,165).eq.4.or.rib(i,165).eq.5) then
       j=np(i,2)+np(i,3)-1
       call line3d(x(i-1,j),y(i-1,j),z(i-1,j),x(i,j),y(i,j),z(i,j),
     + ele3dc(12))
       call line3d(-x(i-1,j),y(i-1,j),z(i-1,j),-x(i,j),y(i,j),z(i,j),
     + ele3dc(12))
       end if

       end if ! vents 4,-4,-5

       end do ! i


       end if ! k26d=1


c      21.6 lines 3D

c      Lines A,B,C,D,...

       do i=1,cordam

       p2x=x2line(corda(i,1),corda(i,2),corda(i,3))
       p1x=x1line(corda(i,1),corda(i,2),corda(i,3))
       p2y=y2line(corda(i,1),corda(i,2),corda(i,3))
       p1y=y1line(corda(i,1),corda(i,2),corda(i,3))
       p2z=z2line(corda(i,1),corda(i,2),corda(i,3))
       p1z=z1line(corda(i,1),corda(i,2),corda(i,3))

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,iccolor(10+corda(i,1)))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,iccolor(10+corda(i,1)))

       end do

c      21.7 Brakes

       do i=cordam+1,cordat

       p2x=x2line(corda(i,1),corda(i,2),corda(i,3))
       p1x=x1line(corda(i,1),corda(i,2),corda(i,3))
       p2y=y2line(corda(i,1),corda(i,2),corda(i,3))
       p1y=y1line(corda(i,1),corda(i,2),corda(i,3))
       p2z=z2line(corda(i,1),corda(i,2),corda(i,3))
       p1z=z1line(corda(i,1),corda(i,2),corda(i,3))

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,iccolor(16))
       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,iccolor(16))

       end do


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.8 H-V-ribs 3D drawing
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do k=1,nhvr

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.8.1 H-ribs
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (hvr(k,2).eq.1) then
       i=hvr(k,3)
c      warning
       ii=hvr(k,4)

       do j=1,21

       p1x=hx3(i,j,ii)
       p1y=hy3(i,j,ii)
       p1z=hz3(i,j,ii)
       p2x=hx2(i,j,ii)
       p2y=hy2(i,j,ii)
       p2z=hz2(i,j,ii)

       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,2)

       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,2)

       if (j.lt.21) then

       call line3d(-hx2(i,j,ii),hy2(i,j,ii),hz2(i,j,ii),
     + -hx2(i,j+1,ii),hy2(i,j+1,ii),hz2(i,j+1,ii),2)
       call line3d(-hx3(i,j,ii),hy3(i,j,ii),hz3(i,j,ii),
     + -hx3(i,j+1,ii),hy3(i,j,ii),hz3(i,j+1,ii),2)

       call line3d(hx2(i,j,ii),hy2(i,j,ii),hz2(i,j,ii),
     + hx2(i,j+1,ii),hy2(i,j+1,ii),hz2(i,j+1,ii),2)
       call line3d(hx3(i,j,ii),hy3(i,j,ii),hz3(i,j,ii),
     + hx3(i,j+1,ii),hy3(i,j,ii),hz3(i,j+1,ii),2)

       end if

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.8.2 V-ribs partial
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Obsolete, erased

       if (hvr(k,2).eq.2) then
       i=hvr(k,3)
       ii=hvr(k,4)

       do j=1,21

       p1x=rx1(i,j,ii)
       p1y=ry1(i,j,ii)
       p1z=rz1(i,j,ii)
       p2x=rx2(i,j,ii)
       p2y=ry2(i,j,ii)
       p2z=rz2(i,j,ii)

c      Diagonal i-1 to i
       if (hvr(k,5).eq.1) then
c       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,5)
c       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,5)
       end if

       if (j.lt.21) then
       if (hvr(k,5).eq.1) then
c       call line3d(rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),
c     + rx1(i,j+1,ii),ry1(i,j+1,ii),rz1(i,j+1,ii),5)
c       call line3d(-rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),
c     + -rx1(i,j+1,ii),ry1(i,j+1,ii),rz1(i,j+1,ii),5)
       end if
       end if

       p1x=rx3(i,j,ii)
       p1y=ry3(i,j,ii)
       p1z=rz3(i,j,ii)
       p2x=rx2(i,j,ii)
       p2y=ry2(i,j,ii)
       p2z=rz2(i,j,ii)

c      Diagonal i to i+1
       if (hvr(k,6).eq.1) then
c       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,1)
c       call line3d(-p1x,p1y,p1z,-p2x,p2y,p2z,1)
       end if

       if (j.lt.21) then
       if (hvr(k,6).eq.1) then
c       call line3d(rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),
c     + rx3(i,j+1,ii),ry3(i,j+1,ii),rz3(i,j+1,ii),1)
c       call line3d(-rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),
c     + -rx3(i,j+1,ii),ry3(i,j+1,ii),rz3(i,j+1,ii),1)
       end if
       end if

       end do

       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.8.4 VH-ribs
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      OBSOLETE, draw before. ERASE

       if (hvr(k,2).eq.4) then
       i=hvr(k,3)-1
       ii=hvr(k,4)

       do j=1,21

c      Diagonal i-1 to i

       p1x=sx1(i,j,ii)
       p1y=sy1(i,j,ii)
       p1z=sz1(i,j,ii)
       p2x=sx2(i,j,ii)
       p2y=sy2(i,j,ii)
       p2z=sz2(i,j,ii)

       if (hvr(k,5).eq.1) then
c       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,4)
       end if

       if (j.lt.21) then
       if (hvr(k,5).eq.1) then
c       call line3d(rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),
c     + rx1(i,j+1,ii),ry1(i,j+1,ii),rz1(i,j+1,ii),4)
       end if
       end if

c      Horizontal i to i+1

       p1x=sx1(i,j,ii)
       p1y=sy1(i,j,ii)
       p1z=sz1(i,j,ii)
       p2x=sx3(i,j,ii)
       p2y=sy3(i,j,ii)
       p2z=sz3(i,j,ii)

       if (hvr(k,5).eq.1.or.hvr(k,6).eq.1) then
c       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,4)
       end if

       if (j.lt.21) then
       if (hvr(k,5).eq.1) then
c       call line3d(rx1(i,j,ii),ry1(i,j,ii),rz1(i,j,ii),
c     + rx1(i,j+1,ii),ry1(i,j+1,ii),rz1(i,j+1,ii),4)
       end if
       end if

c      Diagonal i+1 to i+2

       p1x=sx3(i,j,ii)
       p1y=sy3(i,j,ii)
       p1z=sz3(i,j,ii)
       p2x=sx4(i,j,ii)
       p2y=sy4(i,j,ii)
       p2z=sz4(i,j,ii)

       if (hvr(k,6).eq.1) then
c       call line3d(p1x,p1y,p1z,p2x,p2y,p2z,4)
       end if

       if (j.lt.21) then
       if (hvr(k,6).eq.1) then
c       call line3d(rx3(i,j,ii),ry3(i,j,ii),rz3(i,j,ii),
c     + rx3(i,j+1,ii),ry3(i,j+1,ii),rz3(i,j+1,ii),4)
       end if
       end if

       end do

       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.9 Draw the intermediate and ovalized airfoil in 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss

c      All airfoil points
       if (atp.ne."ss") then
       jfin=np(i,1)-1
       end if

c      Limite the number of points in single skin
       if (atp.eq."ss") then
       jfin=np(i,2)+np(i,3)-2
       end if

c      Intermediate airfoil (48)
       if (pp29(1,1).eq.1) then
       if (i.ge.pp29(1,2).and.i.le.pp29(1,3)) then
       do j=1,jfin
       call line3d(u(i,j,48),v(i,j,48),w(i,j,48),
     + u(i,j+1,48),v(i,j+1,48),w(i,j+1,48),7)
       if (pp29(1,4).eq.0) then
       call line3d(-u(i,j,48),v(i,j,48),w(i,j,48),
     + -u(i,j+1,48),v(i,j+1,48),w(i,j+1,48),7)
       end if
       end do
       end if
       end if

c      Ovalized airfoil (49)
       if (pp29(2,1).eq.1) then
       if (i.ge.pp29(2,2).and.i.le.pp29(2,3)) then
       do j=1,jfin
       call line3d(u(i,j,49),v(i,j,49),w(i,j,49),u(i,j+1,49),v(i,j+1,49)
     + ,w(i,j+1,49),4)
       if (pp29(2,4).eq.0) then
       call line3d(-u(i,j,49),v(i,j,49),w(i,j,49),-u(i,j+1,49),
     + v(i,j+1,49),w(i,j+1,49),4)
       end if
       end do
       end if
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.10 Draw tessellation in 3D model
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       if (pp29(3,1).eq.1) then
       if (i.ge.pp29(3,2).and.i.le.pp29(3,3)) then

       end if
       end if

       end do ! i

       call dxfend(25)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.11 Draw external 3D DXF tessellation (CFD analysis)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss

       if (pp29(4,1).eq.1) then
       if (i.ge.pp29(4,2).and.i.le.pp29(4,3)) then

c      Write new DXF file

       end if
       end if

       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      21.12 Draw tessellation in 3D model (OpenSCAD view)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do i=1,nribss

       if (pp29(5,1).eq.1) then
       if (i.ge.pp29(5,2).and.i.le.pp29(5,3)) then

c      Write STL file

       end if
       end if

       end do

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      22. TEXT NOTES
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      22.1 Text in boxes

       xtext=bname
       call txt(-630.*xkf,-100.*xkf,50.0d0,0.0d0,xtext,3)
   
       xtext=wname
       call txt(600.*xkf,-100.*xkf,50.0d0,0.0d0,xtext,1)

       xtext=lepv
       call txt(1400.*xkf,-100.*xkf,50.0d0,0.0d0,xtext,3)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (n1draw.eq.1) then
c      Row -1

       xpos=1260.*2*xkf
       ypos=-(91.+891.)*xkf
       xtext="-1-3 EXTRADOS PANELS WITH 3D-PARTS (PRINTER)"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=1260.*4*xkf
       ypos=-(91.+891.)*xkf
       xtext="-1-5 EXTRADOS PANELS WITH 3D-PARTS (LASER)"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Row 0

       xpos=1260.*2*xkf
       ypos=-91.*xkf
       xtext="0-3 INTRADOS PANELS WITH 3D-PARTS (PRINTER)"
       call txt(xpos,ypos,10.0d0,0.0d0,xtext,7)

       xpos=1260.*4*xkf
       ypos=-91.*xkf
       xtext="0-5 INTRADOS PANELS WITH 3D-PARTS (LASER)"
       call txt(xpos,ypos,10.0d0,0.0d0,xtext,7)
       end if ! n1draw
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Row 1

       xpos=0.*xkf
       ypos=800.*xkf
       xtext="1-1 PLANFORM AND VAULT"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)
       xtext=bname
       call txt(xpos,ypos-300.*xkf,10.0d0,0.0d0,xtext,7)
       xtext=wname
       call txt(xpos+190.,ypos-300.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Flat area (m2) : "
       call txt(xpos,ypos-280.*xkf,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') farea
       call txt(xpos+170.,ypos-280.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Flat span (m) : "
       call txt(xpos,ypos-260.*xkf,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') fspan
       call txt(xpos+170.,ypos-260.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Flat aspect ratio : "
       call txt(xpos,ypos-240.*xkf,10.0d0,0.0d0,xtext,7)
       write (xtext, '(F5.2)') faratio
       call txt(xpos+170.,ypos-240.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Cells number : "
       call txt(xpos,ypos-220.*xkf,10.0d0,0.0d0,xtext,7)
       write (xtext, '(I3)') nribss*2-1
       if (rib(1,2).le.0.01) then
       write (xtext, '(I3)') nribss*2-2
       end if
       call txt(xpos+170.,ypos-220.*xkf,10.0d0,0.0d0,xtext,7)


       xpos=xpos+1260.*xkf
       xtext="1-2 RIBS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="1-3 EXTRADOS PANELS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)
       xtext="Leading edge"
       call txt(xpos,ypos-810.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Trailing edge"
       call txt(xpos,ypos-160.*xkf,10.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="1-4 RIBS (FOR CUTTING TABLE)"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="1-5 EXTRADOS PANELS (FOR CUTTING TABLE)"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)
       xtext="Leading edge"
       call txt(xpos,ypos-810.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Trailing edge"
       call txt(xpos,ypos-160.*xkf,10.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="1-6 MIDDLE UNLOADED RIBS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="1-7 NYLON RODS POCKETS, NOSE MYLARS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Print joncs in BOX(1,7)
c      ACTUALITZAR BLOCS m !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
c      Print blocs separate
c      Define jonc lenghts in each bloc
       if (k21d.ge.1) then
       xqw=0.

       do m=1,k21blocs

       y1=40.*float(m-1) ! Desplacement in Y for each bloc

       write (xtext,'(A25,I2,A1)') "List of nylon rods (bloc ",
     + m,")"

       ng21=k21blocf(m,3)
       call txt(xpos+400.*xkf,ypos+y1+(-700.+xqw)*
     + xkf,xmida1,0.0d0,xtext,7)
       do ng=1,ng21
       xqw=xqw+15.
       write (xtext,'(A5,I3)') "Group ",ng
       call txt(xpos+400*xkf,ypos+y1+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       ngo(ng,2)=ngoo(m,ng,2)
       ngo(ng,3)=ngoo(m,ng,3)
       do i=ngo(ng,2),ngo(ng,3)
       xqw=xqw+15.
       write (xtext,'(A5,I3,2x,F7.1)') "Jonc ",i,joncf(i,m,ng,2)
       call txt(xpos+400*xkf,ypos+y1+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       end do ! ngo
       end do ! ng

       end do ! m
       end if

       xpos=xpos+1260.*xkf
       xtext="1-8 MIDDLE AND MIDDLE OVALIZED AIRFOILS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Row 2

       xpos=0.*xkf
       ypos=ypos+890.95*xkf
       xtext="2-1 CALAGE ESTIMATION"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="2-2 RIBS WASHIN ANGLE"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="2-3 INTRADOS PANELS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)
       xtext="Trailing edge"
       call txt(xpos,ypos-810.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Leading edge"
       call txt(xpos,ypos-160.*xkf,10.0d0,0.0d0,xtext,7)


       xpos=xpos+1260.*xkf
       xtext="2-4 MINI-RIBS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="2-5 INTRADOS PANELS (FOR CUTTING TABLE)"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)
       xtext="Trailing edge"
       call txt(xpos,ypos-810.*xkf,10.0d0,0.0d0,xtext,7)
       xtext="Leading edge"
       call txt(xpos,ypos-160.*xkf,10.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="2-6 FULL DIAGONAL RIBS"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="2-7"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="2-8"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Row 3

       xpos=0.*xkf
       ypos=ypos+890.95*xkf
       xtext="3-1 UPPER VIEW"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="3-2 LINES A"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Write lines in plan A,B,C,D,E,F
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      write lines in plan A
       if (slp.ge.1) then
       xqw=0.
       xtext="Line - Label - Length"
       call txt(xpos-500.*xkf,ypos+(-718.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       do i=1,slpi(2)-1
       xqw=xqw+18.
       write (xtext,'(I3,3x,A4,3x,F5.1)') i,ln4(i),xlifi(i)
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       end do
       end if

       xpos=xpos+1260.*xkf
       xtext="3-3 LINES B"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      write lines in plan B
       if (slp.ge.2) then
       if (slp.eq.2) slpi(3)=cordam+1
       xqw=0.
       xtext="Line - Label - Length"
       call txt(xpos-500.*xkf,ypos+(-718.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       do i=slpi(2),slpi(3)-1
       xqw=xqw+18.
       write (xtext,'(I3,3x,A4,3x,F5.1)') i,ln4(i),xlifi(i)
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       end do
       end if

       xpos=xpos+1260.*xkf
       xtext="3-4 LINES C"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      write lines in plan C
       if (slp.ge.3) then
       if (slp.eq.3) slpi(4)=cordam+1
       xqw=0.
       xtext="Line - Label - Length"
       call txt(xpos-500.*xkf,ypos+(-718.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       do i=slpi(3),slpi(4)-1
       xqw=xqw+18.
       write (xtext,'(I3,3x,A4,3x,F5.1)') i,ln4(i),xlifi(i)
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       end do
       end if

       xpos=xpos+1260.*xkf
       xtext="3-5 LINES D"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      write lines in plan D
       if (slp.ge.4) then
       if (slp.eq.4) slpi(5)=cordam+1
       xqw=0.
       xtext="Line - Label - Length"
       call txt(xpos-500.*xkf,ypos+(-718.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       do i=slpi(4),slpi(5)-1
       xqw=xqw+18.
       write (xtext,'(I3,3x,A4,3x,F5.1)') i,ln4(i),xlifi(i)
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       end do
       end if

c      Box for V-rib Type-6

       xpos=xpos+1260.*xkf
       xtext="3-6 V-rib Type-6"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Box(3,7)

       xpos=xpos+1260.*xkf
       xtext="3-7"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="3-8"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Row 4

       xpos=0.*xkf
       ypos=ypos+890.95*xkf
       xtext="4-1 VAULT VIEW"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="4-2 LATERAL VIEW"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="4-3 BRAKE DISTRIBUTION"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="4-4"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="4-5 BRAKES"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      write lines in brakes
       xqw=0.
       xtext="Line - Label - Length"
       call txt(xpos-500.*xkf,ypos+(-718.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       do i=cordam+1,cordat
       xqw=xqw+18.
       write (xtext,'(I3,3x,A4,3x,F5.1)') i,ln4(i),xlifi(i)
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,typm3(9),0.0d0,xtext,7)
       end do

       xpos=xpos+1260.*xkf
       xtext="4-6"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

       xpos=xpos+1260.*xkf
       xtext="4-7 GENERAL NOTES"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

c      Print general notes BOX(4,7)

c      Notes about plans, first column

       xqw=0.
       xtext="1-1: 111111111111111111111111111111111111111111111"  

       xtext="PLANS GENERAL NOTES"
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida1,0.0d0,xtext,7)
       xqw=xqw+30.

       xtext="1-1: Planform and vault view (informative)"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-2: Ribs for plotter, one side"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-3: Extrados panels for plotter, one side"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-4: Ribs for laser cutting, one side. Units cm"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-5: Extrados for laser cutting, one side.Units cm"  
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-6: Middle unloaded ribs for laser cutting, "
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="     one side Units cm"  
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-7: Rods pockets and nylons lengths, mylars"  
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="1-8: Intermediate and ovalized airfoils"  
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)

       xqw=xqw+30.
       xtext="2-1: Calage estimation, speed and trim systems"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="2-2: Ribs printed with washin angle (informative)"
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="2-3: Intrados panels for plotter, one side"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="2-4: Mini-ribs horizontal and diagonal"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="2-5: Intrados for laser cutting, one side"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="2-6: Full diagonal ribs laser, one side"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="2-7: Free"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)

       xqw=xqw+30.
       xtext="3-1: Upper view 3D (informative)"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="3-2: Lines A"
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="3-3: Lines B"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="3-4: Lines C"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="3-5: Lines D"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="3-6: V-rib type-6"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="3-7: Free"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)

       xqw=xqw+30.
       xtext="4-1: Vault view (informative)"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="4-2: Lateral view (informative)"
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="4-3: Brake distribution (informative)"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="4-4: Free"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="4-5: Brake lines"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="4-6: Free"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext="4-7: General notes"       
       call txt(xpos-500.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)

c      Notes, second column

       xqw=0.
       xtext="1-1: 111111111111111111111111111111111111111111111"    

       xtext="UNITS"
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida1,0.0d0,xtext,7)
       xqw=xqw+30.

       xtext="Main units are centimeters. Scale x10 to use in mm"
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+30.

       xtext="WIDTHS FOR SEWING AND OFFSETS "
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida1,0.0d0,xtext,7)
       xqw=xqw+30.

       write (xtext,'(A32,F6.2)') "Lateral width in extrados (mm): ",
     + xupp
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A31,F6.2)') "Width in leading edge ex (mm): ",
     + xupple
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A32,F6.2)') "Width in trailing edge ex (mm): ",
     + xuppte
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A32,F6.2)') "Lateral width in intrados (mm): ",
     + xlow
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A31,F6.2)') "Width in leading edge in (mm): ",
     + xlowle
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A32,F6.2)') "Width in trailing edge in (mm): ",
     + xlowte
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A28,F6.2)') "Lateral width in ribs (mm): ",
     + xrib
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       write (xtext,'(A30,F6.2)') "Lateral width in V-ribs (mm): ",
     + xvrib*10.
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.
       
       write(xtext,'(A35,F6.2)') "General offset lateral points (mm): ",
     + typm6(1)
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+30.

       write(xtext,'(A28,A14,F6.2)') "Distance between equidistant",
     + " points (cm): ",xmark
       call txt(xpos-100.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       xqw=xqw+15.


c      Notes, third column

       xqw=0.
       xtext="1-1: 111111111111111111111111111111111111111111111"    

       xtext='"ROMAN" NUMBERS CODIFICATION'
       call txt(xpos+300.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida1,0.0d0,xtext,7)
       xqw=xqw+15.
       xtext='Numbering panels, ribs, mini-ribs, V-ribs'
       call txt(xpos+300.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida1,0.0d0,xtext,7)
       xqw=xqw+30.

       do i=1,nribss
       write (xtext,'(A7,I3,A3)') "Number ",i," = "
       call txt(xpos+300.*xkf,ypos+(-700.+xqw)*
     + xkf,xmida2,0.0d0,xtext,7)
       call romano(i,xpos+400.*xkf,ypos+(-700.+xqw)*xkf,0.0d0,3.0d0,7)
       xqw=xqw+15.
       end do

       xpos=xpos+1260.*xkf
       xtext="4-8"
       call txt(xpos,ypos,12.0d0,0.0d0,xtext,7)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      23. END OF MAIN PROGRAM
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc   

       call dxfend(20)

       write (*,*)

       if (atp.eq."pc") then
       write (*,'(A,1x,F6.2,A,F7.1,A)') " Total line length = ",
     + xlength*2./100.," m ",(xlength*2./100.)/0.3048," ft"
       write (*,*)
       else
       write (*,'(A,1x,F6.2,A)') " Total line length = ",
     + xlength*2./100.," m"
       write (*,*)
       end if

       if (atp.eq."ds".or.atp.eq."ss") then
       write (*,*) "OK, paraglider calculated !"
       end if
       if (atp.eq."pc") then
       write (*,*) "OK, parachute calculated !"
       end if
       write (*,*)
       write (*,*) "Please open the following files:" 
       write (*,*)
       write (*,*) "   leparagliding.dxf"
       write (*,*) "   lep-3d.dxf"
       write (*,*) "   lep-out.txt"
       write (*,*) "   lines.txt"
       write (*,*)


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc       
c      Verificació de subrutines
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       punt1(1)=0.0
       punt1(2)=0.0
       punt1(3)=0.0
       punt2(1)=1.0
       punt2(2)=0.0
       punt2(3)=0.0
       punt3(1)=0.0
       punt3(2)=2.0
       punt3(3)=0.0

c       call planeby123(punt1,punt2,punt3,aplane,bplane,cplane,
c     + dplane)

c       write (*,*) "A B C D"
c       write (*,*) aplane,bplane,cplane,dplane

       dp0=-20.0
       punt0(1)=1.0
       punt0(2)=2.0
       punt0(3)=1.0

c       call pointp(punt0,aplane,bplane,cplane,dp0,punt4)

c       write (*,*) punt4(1),punt4(2),punt4(3)











ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      END MAIN PROGRAM
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc 

       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      24. GRAPHICAL SUBROUTINES
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE pointg (radius xcir)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE pointg(xu,xv,xcir,pointcolor)

       integer pointcolor

       real*8 pi,angle1,angle2,xu,xv,xcir

       integer typm1(50),typm4(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50)
       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

       pi=4.0d0*datan(1.0d0)
       xcir=0.1*typm2(1)

c      Case 1: Draw constructed points
       if (typm1(1).eq.1) then
       xv=-xv
c      Draw cross
       call line(xu-xcir,-(xv),xu+xcir,-(xv),pointcolor)
       call line(xu,-(xv-xcir),xu,-(xv+xcir),pointcolor)

c      Draw circle
       do l=1,8

       angle1=float(l-1)*2.*pi/8.
       xlu1=xcir*dcos(angle1)
       xlv1=xcir*dsin(angle1)
       angle2=float(l)*2.*pi/8.
       xlu2=xcir*dcos(angle2)
       xlv2=xcir*dsin(angle2)

       call line(xu+xlu1,-(xv+xlv1),xu+xlu2,-(xv+xlv2),pointcolor)

       end do
       end if

c      Case 2: Draw minicircles
       if (typm1(1).eq.2) then
       write(20,'(A,/,I1,/,A)') "CIRCLE",8,"mcircles"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,xu,20,-xv
       write(20,'(I2,/,F12.3,/,I2,/,I3,/,I2)') 40,0.1*typm2(1),62,
     + pointcolor,0
       end if

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE POINT 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE point(x1,y1,pointcolor)
c      line P1-P2

       character*50 lyname(50)
       real*8 x1,y1
       integer pointcolor,typepoint
       integer typm1(50),typm4(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50)

       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

       lyname(4)="A"
       lyname(5)="points"
       typepoint=typm4(1)

c       write (*,*) typepoint,lyname(4)

c      Euclidean point
       if (typepoint.eq.1) then
       write(20,'(A,/,I1,/,A)') "POINT",8,"points"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,x1,20,-y1
       write(20,'(I2,/,I2,/,I2,/,I3,/,I2)') 39,0,62,pointcolor,0
       end if

c      Point defined as circle diameter 0.4 mm
       if (typepoint.eq.2) then
       write(20,'(A,/,I1,/,A)') "CIRCLE",8,"mcircles"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,x1,20,-y1
       write(20,'(I2,/,F12.3,/,I2,/,I3,/,I2)') 40,0.1*typm5(1),62,
     + pointcolor,0
       end if

       return
       end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE POINTLAYER 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE poinc(x1,y1,xrad,gname,pointcolor)
c      Point as minicicle radius xrad in layer gname

       character*50 gname
       real*8 x1,y1,xrad
       integer pointcolor

c      Point defined as circle radius xrad (0.2 mm)
       write(20,'(A,/,I1,/,A)') "CIRCLE",8,gname
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,x1,20,-y1
       write(20,'(I2,/,F12.3,/,I2,/,I3,/,I2)') 40,xrad,62,pointcolor,0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE POINTLAYER 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE poinl(x1,y1,gname,pointcolor)
c      Euclidean point in layer gname

       character*50 gname
       real*8 x1,y1
       integer pointcolor

       write(20,'(A,/,I1,/,A)') "POINT",8,gname
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,x1,20,-y1
       write(20,'(I2,/,I2,/,I2,/,I3,/,I2)') 39,0,62,pointcolor,0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE CIRCLE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE circle(x1,y1,radc,gname,pointcolor)
c      Circle radius radc in layer gname

       character*50 gname
       real*8 x1,y1,radc
       integer pointcolor

       write(20,'(A,/,I1,/,A)') "CIRCLE",8,gname
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,x1,20,-y1
       write(20,'(I2,/,F12.3,/,I2,/,I3,/,I2)') 40,radc,62,pointcolor,0

       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE MTRIANGLE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE mtriangle(p1x,p1y,xh,xrot,linecolor)
c      line P1-P2

       real*8 p1x,p1y

       real*8 xh,xrot,pi

       pi=4.0d0*datan(1.0d0)

c       write (*,*) i,xrot

       x1=p1x
       y1=p1y
       xx2=xh*dtan((pi/6.))
       yy2=xh
       xx3=-xh*dtan((pi/6.))
       yy3=xh

c      Rotation matrix in xrot
       x2=p1x+xx2*dcos(xrot)+yy2*sin(xrot)
       y2=p1y-xx2*dsin(xrot)+yy2*cos(xrot)
       x3=p1x+xx3*dcos(xrot)+yy3*sin(xrot)
       y3=p1y-xx3*dsin(xrot)+yy3*cos(xrot)

       write(20,'(A,/,I1,/,A)') "LINE",8,"triangles"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,x1,20,-y1
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,x2,21,-y2
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0

       write(20,'(A,/,I1,/,A)') "LINE",8,"triangles"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,x2,20,-y2
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,x3,21,-y3
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0
       
       write(20,'(A,/,I1,/,A)') "LINE",8,"triangles"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,x3,20,-y3
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,x1,21,-y1
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINEVENT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE linevent(p1x,p1y,p2x,p2y,linecolor)
c      line P1-P2

       real*8 p1x,p1y,p2x,p2y

       write(20,'(A,/,I1,/,A)') "LINE",8,"vents"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,p1x,20,-p1y
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,p2x,21,-p2y
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE SEGMENT101
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE segment101(p1x,p1y,p2x,p2y,linecolor)
c      line P1-P2

       real*8 p1x,p1y,p2x,p2y

       x3=p1x+(p2x-p1x)/3.
       y3=p1y+(p2y-p1y)/3.
       x4=p1x+(p2x-p1x)*(2./3.)
       y4=p1y+(p2y-p1y)*(2./3.)

       write(20,'(A,/,I1,/,A)') "LINE",8,"segment101"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,p1x,20,-p1y
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,x3,21,-y3
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0

       write(20,'(A,/,I1,/,A)') "LINE",8,"segment101"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,x4,20,-y4
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,p2x,21,-p2y
       write(20,'(I2,/,I2,/,I2,/,I2,/,I2)') 39,0,62,linecolor,0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINE 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE line(p1x,p1y,p2x,p2y,linecolor)
c      line P1-P2

       real*8 p1x,p1y,p2x,p2y

       write(20,'(A,/,I1,/,A)') "LINE",8,"default"
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 10,p1x,20,-p1y
       write(20,'(I2,/,F14.4,/,I2,/,F14.4)') 11,p2x,21,-p2y
       write(20,'(I2,/,I2,/,I2,/,I3,/,I2)') 39,0,62,linecolor,0
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc        
c     SUBROUTINE LINE 3D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE line3d(p1x,p1y,p1z,p2x,p2y,p2z,linecolor)
c      line P1-P2

       real*8 p1x,p1y,p1z,p2x,p2y,p2z

       write(25,'(A,/,I1,/,A)') "LINE",8,"default"
c       write(25,'(I3,/,A)') 100,"AcDbLine"
       write(25,'(I1,/,A)') 6,"CONTINUOUS"
       write(25,'(I2,/,F8.3,/,I2,/,F8.3,/,I2,/,F8.3)') 
     + 10,p1x,20,p1y,30,p1z
       write(25,'(I2,/,F8.3,/,I2,/,F8.3,/,I2,/,F8.3)') 
     + 11,p2x,21,p2y,31,p2z
       write(25,'(I2,/,I2,/,I2,/,I3,/,I2)') 39,0,62,linecolor,0
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      POLYLINE 2D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE poly2d(plx,ply,nvertex,linecolor)

       real*8 plx(500),ply(500)

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

c       write (*,'(A,/,I1,/,I1,/,I2)') "POLYLINE",8,0,62
c       write (*,'(I3,/,I2,/,I1)') linecolor,66,1
c       write (*,'(I2,/,F3.1,/,I2,/,F3.1,/,I2,/,F3.1,/,I1)') 
c     + 10,0.0,20,0.0,30,0.0,0
       
c       do k=1,nvertex

c       write (*,'(A,/,I1,/,I1,/,I2)') "VERTEX",8,0,62
c       write (*,'(I3,/,I2,/,I1)') linecolor,66,1 
c       write (*,'(I2,/,F9.3,/,I2,/,F9.3,/,I2,/,F9.3,/,I1)') 
c     + 10,plx(k),20,ply(k),30,0.0,0

c       end do

c       write (*,'(A,/,I1,/,I1,/,I2)') "SEQEND",8,0,62
c       write (*,'(I3,/,I1)') linecolor,0 

       return

       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      ELLIPSE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE ellipse(u0,v0,a,b,tet0,linecolor)

       real*8 xe(500),ye(500)

       real*8 pi,u0,v0,a,b,tet,tet0

       real*8 p1x,p1y,p2x,p2y

       pi=4.0d0*datan(1.0d0)

       do ll=1,40

       tet=2.*pi*((float(ll)-1.)/39.)

c      write (*,*) ll,float(ll),tet," ",pi,"---"

       xe(ll)=u0+a*dcos(tet)*dcos(tet0)-b*dsin(tet)*dsin(tet0)
       ye(ll)=v0+a*dcos(tet)*dsin(tet0)+b*dsin(tet)*dcos(tet0)

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
       real*8 rx0, ry0, ralp, requi, dx
        
c      AQUI ES EL PROBLEMA!!!!!!!!!!!!!!!!!!!!!!!!!!!
c      Points separation in romano

c      requi=0.350d0

       dx=0.0d0

       rn1=int(float(rn)/10)
       rn2=int((float(rn)-10*float(rn1))/5)
       rn3=rn-10*rn1-5*rn2

c      write (*,*) "rn1= ", rn, rn1, rn2, rn3

       do i=1,rn1

       call point(rx0+dx*dcos(ralp),ry0-dx*dsin(ralp),rcolor)
       call point(rx0+dx*dcos(ralp)+requi*dsin(ralp),
     + ry0-dx*dsin(ralp)+requi*dcos(ralp),rcolor)
       dx=dx+requi
       call point(rx0+dx*dcos(ralp),ry0-dx*dsin(ralp),rcolor)
       call point(rx0+dx*dcos(ralp)+requi*dsin(ralp),
     + ry0-dx*dsin(ralp)+requi*dcos(ralp),rcolor)
       dx=dx+requi

       end do

       do i=1,rn2

       call point(rx0+dx*dcos(ralp),ry0-dx*dsin(ralp),rcolor)
       call point(rx0+(dx+0.5d0*requi)*dcos(ralp)+requi*dsin(ralp),
     + ry0-(dx+0.5d0*requi)*dsin(ralp)+requi*dcos(ralp),rcolor)
       dx=dx+requi
       call point(rx0+dx*dcos(ralp),ry0-dx*dsin(ralp),rcolor)
       dx=dx+requi

       end do

       do i=1,rn3

       call point(rx0+dx*dcos(ralp),ry0-dx*dsin(ralp),rcolor)
       dx=dx+requi

       end do

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE TEXT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE txt(p1x,p1y,htext,atext,xtext,txtcolor)
c      line P1-P2

       real*8 atext,htext,p1x,p1y
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

       real*8 atext,htext,p1x,p1y
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

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE ITEXT2
c      Only format two digits
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE itxt2(p1x,p1y,htext,atext,itext,txtcolor)
c      line P1-P2

       real*8 atext,htext,p1x,p1y
       integer itext, txtcolor

       write(20,'(A,/,I1,/,A)') "TEXT",5,"10A38"
       write(20,'(I1,/,I1)') 8, 0
       write(20,'(I1,/,A)') 6,"CONTINUOUS"
       write(20,'(I2,/,I3)') 62, txtcolor
       write(20,'(I2,/,F12.2,/,I2,/,F12.2)') 10,p1x,20,-p1y
       write(20,'(I2,/,F12.2)') 30,0.0
       write(20,'(I2,/,F12.2)') 40, htext
       write(20,'(I2,/,I2)') 1, itext
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
       write(nunit,'(I2,/,F12.3,/,I2,/,F12.3)') 10,-670.,20,-3630.
       write(nunit,'(I1,/,A)') 9,"$EXTMIN"
       write(nunit,'(I2,/,F12.3,/,I2,/,F12.3)') 10,7000.,20,120.
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

 
cccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE vectors redistribution             c
c                                                    c
c      Read polyline (xlin1,ylin1) in n1vr points    c
c      and redistribute in polyline                  c
c      (xlin3,ylin3) in n2vr points                  c
cccccccccccccccccccccccccccccccccccccccccccccccccccccc

       subroutine vredis(xlin1,ylin1,xlin3,ylin3,n1vr,n2vr)  

       real*8 xlin1(5000),ylin1(5000)
       real*8 xlin2(50000),ylin2(50000)
       real*8 xlin3(5000),ylin3(5000)
   

c      Case n1vr > 3

c      j2vr counter in x10 multiplied vector
       j2vr=0

c      Define local vector
       do j1vr=1,n1vr-1

       xj=xlin1(j1vr)
       yj=ylin1(j1vr)
       xjm1=xlin1(j1vr+1)
       yjm1=ylin1(j1vr+1)

       do kvr=0,10
       stvr=float(kvr)/10.
       j2vr=j2vr+1
c      Parametric equation in each segment
       xlin2(j2vr)=xj+stvr*(xjm1-xj)
       ylin2(j2vr)=yj+stvr*(yjm1-yj)
       end do
       j2vr=j2vr-1

       end do

       j2max=j2vr+1
      
       icount=int(float((10*n1vr-1)/(n2vr-1)))
       iespai=icount*(n2vr-1)
       isobra=10*(n1vr-1)-iespai

       itotes=10*(n1vr-1)

c      Assign vector 3

c      j3 counter in final vector
       j3vr=1
       j2vr=1
       do j22vr=1,j2max

       xlin3(j3vr)=xlin2(j2vr)
       ylin3(j3vr)=ylin2(j2vr)

c      Ajust exactly the final point
       if (j3vr.eq.n2vr) then
       xlin3(j3vr)=xlin1(n1vr)
       ylin3(j3vr)=ylin1(n1vr)
       end if

c      Assign excess of spaces
       iplus=0
       if (j3vr.le.isobra) then
       iplus=1
       end if

c      Count
       do ijkvr=1,icount+iplus
       j2vr=j2vr+1
       end do
      
       j3vr=j3vr+1

       end do

c      Special case n1vr=2
       if (n1vr.eq.2) then 
             
       disx=(xlin1(2)-xlin1(1))/float(n2vr-1)
       disy=(ylin1(2)-ylin1(1))/float(n2vr-1)

       do j=1,n2vr
       xlin3(j)=xlin1(1)+disx*float(j-1)
       ylin3(j)=ylin1(1)+disy*float(j-1)
       end do

       end if

       return

       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c
c     SUBROUTINE r and s lines 2D intersection
c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE xrxs(xru,xrv,xsu,xsv,xtu,xtv)

      real*8 xru(2),xrv(2),xsu(2),xsv(2)

      xmr=(xrv(2)-xrv(1))/(xru(2)-xru(1))
      xbr=xrv(1)-xmr*xru(1)
c      if (dabs((xru(2)-xru(1))).le.0.0001) then
c      xmr=(xrv(2)-xrv(1))/0.000001
c      end if

      xms=(xsv(2)-xsv(1))/(xsu(2)-xsu(1))
      xbs=xsv(1)-xms*xsu(1)
c      if (dabs((xsu(2)-xsu(1))).le.0.0001) then
c      xms=(xsv(2)-xsv(1))/0.000001
c      end if

      xtu=(xbs-xbr)/(xmr-xms)
      xtv=xmr*xtu+xbr

c     Case xsu(1)=xsu(2)
      if (dabs((xsu(2)-xsu(1))).le.0.0001d0) then
      xtu=xsu(1)
      xtv=xmr*xsu(1)+xbr
      end if

c     Case xru(1)=xru(2)
      if (dabs((xru(2)-xru(1))).le.0.0001d0) then
      xtu=xru(1)
      xtv=xms*xru(1)+xbs
      end if

c      write (*,*) "Z ", xru(1),xrv(1),xmr,xms,xtu,xtv

      return

      end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE  flattening
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE flatt(ni,npunts,rx,ry,rz,
     + pl1x,pl1y,pl2x,pl2y,pr1x,pr1y,pr2x,pr2y)

       real*8 rx(0:100,500),ry(0:100,500),rz(0:100,500)

       real*8 pl1x(0:100,500),pl1y(0:100,500),pl2x(0:100,500),
     + pl2y(0:100,500)
       real*8 pr1x(0:100,500),pr1y(0:100,500),pr2x(0:100,500),
     + pr2y(0:100,500)

       real*8 phr,pa1r,pa2r,phl,pa1l,pa2l,px0,py0,ptheta,pw1
       real*8 pa,pb,pc,pd,pe,pf

       i=ni

       px0=0.0d0
       py0=0.0d0
       ptheta=0.0d0

       do j=1,npunts

c       write (*,*) "rx ry rx ", j, rx(i,j),ry(i,j),rz(i,j)

c      Distances between points
       pa=dsqrt((rx(i+1,j)-rx(i,j))**2.0d0+(ry(i+1,j)-ry(i,j))**2.0d0+
     + (rz(i+1,j)-rz(i,j))**2.0d0)
       pb=dsqrt((rx(i+1,j+1)-rx(i,j))**2.0d0+(ry(i+1,j+1)-ry(i,j))**
     + 2.0d0+(rz(i+1,j+1)-rz(i,j))**2.0d0)
       pc=dsqrt((rx(i+1,j+1)-rx(i+1,j))**2.0d0+(ry(i+1,j+1)-ry(i+1,j))
     + **2.+(rz(i+1,j+1)-rz(i+1,j))**2.0d0)
       pd=dsqrt((rx(i+1,j)-rx(i,j+1))**2.0d0+(ry(i+1,j)-ry(i,j+1))**
     + 2.0d0+(rz(i+1,j)-rz(i,j+1))**2.0d0)
       pe=dsqrt((rx(i,j+1)-rx(i,j))**2.0d0+(ry(i,j+1)-ry(i,j))**2.0d0+
     + (rz(i,j+1)-rz(i,j))**2.0d0)
       pf=dsqrt((rx(i+1,j+1)-rx(i,j+1))**2.0d0+(ry(i+1,j+1)-ry(i,j+1))
     + **2.0d0+(rz(i+1,j+1)-rz(i,j+1))**2.0d0)
       
       pa2r=(pa*pa-pb*pb+pc*pc)/(2.0d0*pa)
       pa1r=pa-pa2r
       phr=dsqrt(pc*pc-pa2r*pa2r)

       pa2l=(pa*pa-pe*pe+pd*pd)/(2.0d0*pa)
       pa1l=pa-pa2l
       phl=dsqrt(pd*pd-pa2l*pa2l)

       pb2t=(pb*pb-pe*pe+pf*pf)/(2.0d0*pb)
       pb1t=pb-pb2t
       pht=dsqrt(pf*pf-pb2t*pb2t)
       
       pw1=datan(phr/pa1r)
       phu=pb1t*dtan(pw1)

c      Quadrilater coordinates
       pl1x(i,j)=px0
       pl1y(i,j)=py0

       pr1x(i,j)=pa*dcos(ptheta)+px0
       pr1y(i,j)=pa*dsin(ptheta)+py0

       pl2x(i,j)=pa1l*dcos(ptheta)-phl*dsin(ptheta)+px0
       pl2y(i,j)=pa1l*dsin(ptheta)+phl*dcos(ptheta)+py0
       
       pr2x(i,j)=pa1r*dcos(ptheta)-phr*dsin(ptheta)+px0
       pr2y(i,j)=pa1r*dsin(ptheta)+phr*dcos(ptheta)+py0

c      Iteration
       px0=pl2x(i,j)
       py0=pl2y(i,j)
       ptheta=datan((pr2y(i,j)-pl2y(i,j))/(pr2x(i,j)-pl2x(i,j)))
       
       end do

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE  axisch
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE axisch(npunts,angle,px9i,py9i,px9o,py9o)

       real*8 px9i(500),py9i(500)
       real*8 px9o(500),py9o(500)

       real*8 angle,xc,xs,pi

       pi=4.0d0*datan(1.0d0)
       angle=0.0d0

       do j=1,npunts

       xc=dcos(angle*pi/180.0d0)
       xs=dsin(angle*pi/180.0d0)

       px9o(j)=xc*px9i(j)-xs*py9i(j)
       py9o(j)=xs*px9i(j)+xc*py9i(j)

       end do

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE angdis1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE angdis2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      ES FA SERVIR??????????????
c      REVISAR el double precision:
c
c      gfortran-8 -g -fbacktrace -fdefault-real-8 
c      -falign-commons -fno-automatic -finit-local-zero 
c      -mcmodel=medium leparagliding.f 
c 

       SUBROUTINE angdis2(p1u,p1v,p2u,p2v,p3u,p3v,angl,dist)

       real*8 du,dv,angl

       real*8 p1u,p1v,p2u,p2v,p3u,p3v,dist

       du=p2u-p1u
       dv=p2v-p1v

c       write (*,*) "sub ",p1u,p1v,p2u,p2v
      
       if (du.ne.0.) then 
c       angl=dabs(datan(dv/du))
       end if
ccccccccccccccccc       if (du.eq.0.) then angl=2.0d0*datan(1.0d0)
c       write (*,*) "sub dv du",dv,du,angl

c      Case 1
       if (du.ge.0.and.dv.ge.0) then
c       p3u=p1u-dist*dsin(angl)
c       p3v=p1v+dist*dcos(angl)
       end if

c      Case 2
       if (du.lt.0.and.dv.ge.0) then
c       p3u=p1u-dist*dsin(angl)
c       p3v=p1v-dist*dcos(angl)
       end if

c      Case 3
       if (du.ge.0.and.dv.le.0) then
c       p3u=p1u+dist*dsin(angl)
c       p3v=p1v+dist*dcos(angl)
       end if

c      Case 4
       if (du.lt.0.and.dv.le.0) then
c       p3u=p1u+dist*dsin(angl)
c       p3v=p1v-dist*dcos(angl)
       end if

c       write(*,*) "4444 ",angl,p3u,p3v

      
       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE angdis3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE d3p
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE EXTERNAL POINTS IN A PANEL
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Computes external points 11-24-14 and 12-25-15
c      in a panel from 1 to npo
c      but draws nothing
c
c      WARNING IN REDEFINITION VARIABLES u, v !!!
c      ISOLATE THEM!

       SUBROUTINE extpoints(i,uf,vf,npo,xpal,xpale,xpate,icase)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 xupp,xupple,xpale,xpate,xpal,xuppte,alple,alpte
       real*8 xru(2),xrv(2),xsu(2),xsv(2)
c       integer icase

       xupple=xpale
       xuppte=xpate
       xupp=xpal
c      WARNING!!! xupp NOT USED

c       icase=1 ! Tangent
c       icase=2 ! Orthogonal

c       icase=1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case tangent
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Points LE 14,15,24,25

       if (icase.eq.1) then

       alple=-(datan((vf(i,npo,10)-vf(i,npo,9))/
     + (uf(i,npo,10)-uf(i,npo,9))))

       uf(i,npo,14)=uf(i,npo,9)+xupple*0.1*dsin(alple)
       vf(i,npo,14)=vf(i,npo,9)+xupple*0.1*dcos(alple)

       uf(i,npo,15)=uf(i,npo,10)+xupple*0.1*dsin(alple)
       vf(i,npo,15)=vf(i,npo,10)+xupple*0.1*dcos(alple)

c      recta r (14-15)

       xru(1)=uf(i,npo,14)
       xrv(1)=vf(i,npo,14)
       xru(2)=uf(i,npo,15)
       xrv(2)=vf(i,npo,15)

c      recta s left (11)

       xsu(1)=uf(i,npo-1,11)
       xsv(1)=vf(i,npo-1,11)
       xsu(2)=uf(i,npo,11)
       xsv(2)=vf(i,npo,11)

c      Intersection 24
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       uf(i,npo,24)=xtu
       vf(i,npo,24)=xtv

c      recta s right (11)

       xsu(1)=uf(i,npo-1,12)
       xsv(1)=vf(i,npo-1,12)
       xsu(2)=uf(i,npo,12)
       xsv(2)=vf(i,npo,12)

c      Intersection 24
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       uf(i,npo,25)=xtu
       vf(i,npo,25)=xtv

c      Points TE 14,15,24,25

       alpte=-(datan((vf(i,1,10)-vf(i,1,9))/
     + (uf(i,1,10)-uf(i,1,9))))

       uf(i,1,14)=uf(i,1,9)-xuppte*0.1*dsin(alpte)
       vf(i,1,14)=vf(i,1,9)-xuppte*0.1*dcos(alpte)

       uf(i,1,15)=uf(i,1,10)-xuppte*0.1*dsin(alpte)
       vf(i,1,15)=vf(i,1,10)-xuppte*0.1*dcos(alpte)

c      recta r (14-15)

       xru(1)=uf(i,1,14)
       xrv(1)=vf(i,1,14)
       xru(2)=uf(i,1,15)
       xrv(2)=vf(i,1,15)

c      recta s left (11)

       xsu(1)=uf(i,1,11)
       xsv(1)=vf(i,1,11)
       xsu(2)=uf(i,2,11)
       xsv(2)=vf(i,2,11)

c      Intersection 24
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       uf(i,1,24)=xtu
       vf(i,1,24)=xtv

c      recta s right (11)

       xsu(1)=uf(i,1,12)
       xsv(1)=vf(i,1,12)
       xsu(2)=uf(i,2,12)
       xsv(2)=vf(i,2,12)

c      Intersection 25
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       uf(i,1,25)=xtu
       vf(i,1,25)=xtv

       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case orthogonal
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (icase.eq.2) then

       alple=-(datan((vf(i,npo,10)-vf(i,npo,9))/
     + (uf(i,npo,10)-uf(i,npo,9))))

       uf(i,npo,14)=uf(i,npo,9)+xupple*0.1*dsin(alple)
       vf(i,npo,14)=vf(i,npo,9)+xupple*0.1*dcos(alple)

       uf(i,npo,15)=uf(i,npo,10)+xupple*0.1*dsin(alple)
       vf(i,npo,15)=vf(i,npo,10)+xupple*0.1*dcos(alple)

       uf(i,npo,24)=uf(i,npo,14)-xupp*0.1*dcos(alple)
       vf(i,npo,24)=vf(i,npo,14)+xupp*0.1*dsin(alple)

       uf(i,npo,25)=uf(i,npo,15)+xupp*0.1*dcos(alple)
       vf(i,npo,25)=vf(i,npo,15)-xupp*0.1*dsin(alple)

c      Points TE 14,15,24,25,26,27
c      TE case orthogonal

       alpte=-(datan((vf(i,1,10)-vf(i,1,9))/(uf(i,1,10)-uf(i,1,9))))

       uf(i,1,14)=uf(i,1,9)-xuppte*0.1*dsin(alpte)
       vf(i,1,14)=vf(i,1,9)-xuppte*0.1*dcos(alpte)

       uf(i,1,15)=uf(i,1,10)-xuppte*0.1*dsin(alpte)
       vf(i,1,15)=vf(i,1,10)-xuppte*0.1*dcos(alpte)

       uf(i,1,24)=uf(i,1,14)-xupp*0.1*dcos(alpte)
       vf(i,1,24)=vf(i,1,14)+xupp*0.1*dsin(alpte)
 
       uf(i,1,25)=uf(i,1,15)+xupp*0.1*dcos(alpte)
       vf(i,1,25)=vf(i,1,15)-xupp*0.1*dsin(alpte)

       end if

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL COMPLETE
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelc(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1
c      Sobreamples esquerra

       call line(psep+uf(i,j,9),psey-vf(i,j,9),psep+uf(i,j+1,9),
     + psey-vf(i,j+1,9),1)

c      Sobreamples dreta

       call line(psep+uf(i,j,10),psey-vf(i,j,10),psep+uf(i,j+1,10),
     + psey-vf(i,j+1,10),1)

c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      Four horizontal segments 11-9, 10-12

       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,9),psey-vf(i,npo,9),3)

       call line(psep+uf(i,npo,10),psey-vf(i,npo,10),
     + psep+uf(i,npo,12),psey-vf(i,npo,12),3)

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,9),psey-vf(i,1,9),3)

       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,12),psey-vf(i,1,12),3)

c      Four vertical segments 10-15, 9-14

       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)

       call line(psep+uf(i,npo,10),psey-vf(i,npo,10),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)
       
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,14),psey-vf(i,1,14),3)

       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),
     + psep+uf(i,npo,14),psey-vf(i,npo,14),3)

c      Two horizontal lines 14-15

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)

c      Draw eight corner segments

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,15),psey-vf(i,1,15),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
     
       call line(psep+uf(i,1,12),psey-vf(i,1,12),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,15),psey-vf(i,npo,15),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
     
       call line(psep+uf(i,npo,12),psey-vf(i,npo,12),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)

c      Trailing edge extrados
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,10),psey-vf(i,1,10),1)
       
c      Init extrados
       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),
     + psep+uf(i,npo,10),psey-vf(i,npo,10),1)
            
       return
       end



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL COMPLETE WITH CONTROL (ic)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelcc(i,uf,vf,npo,psep,psey,ic)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey
       integer icont(10),ic

       do k=1,8
       icont(k)=0
       end do

c      case ic=1
       if (ic.eq.1) then ! Vores laterals exteriors
       icont(1)=1
       icont(4)=1
       end if

c      case ic=2
       if (ic.eq.2) then ! Vores laterals exteriors sense LE
       icont(1)=1
       icont(2)=1
       icont(4)=1
       icont(5)=1
       icont(7)=1
       end if

c      case ic=3
       if (ic.eq.3) then ! Vores laterals exteriors tot
       icont(1)=1
       icont(2)=1
       icont(3)=1
       icont(4)=1
       icont(5)=1
       icont(6)=1
       icont(7)=1
       icont(8)=1
       end if

c      case ic=4
       if (ic.eq.4) then ! Vores laterals exteriors sense TE
       icont(1)=1
       icont(3)=1
       icont(4)=1
       icont(6)=1
       icont(8)=1
       end if

c      case ic=5
       if (ic.eq.5) then ! Vores laterals exteriors
       icont(1)=1
       end if

c      case ic=6
       if (ic.eq.6) then ! Vores laterals exteriors sense TE
       icont(1)=1
       icont(2)=1
       end if

c      case ic=7
       if (ic.eq.7) then ! Vores laterals exteriors sense TE
       icont(1)=1
       icont(2)=1
       icont(3)=1
       end if

c      case ic=8
       if (ic.eq.8) then ! Vores laterals exteriors sense TE
       icont(1)=1
       icont(3)=1
       end if

       do j=1,npo-1

       if (icont(4).eq.1) then
c      Sobreamples esquerra
       call line(psep+uf(i,j,9),psey-vf(i,j,9),psep+uf(i,j+1,9),
     + psey-vf(i,j+1,9),1)
c      Sobreamples dreta
       call line(psep+uf(i,j,10),psey-vf(i,j,10),psep+uf(i,j+1,10),
     + psey-vf(i,j+1,10),1)
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      MULTIBAT
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (icont(1).eq.1) then
c      Vores de costura esquerra
       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)
c      Vores de costura dreta
       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)
       end if

       end do

       if (icont(8).eq.1) then
c      Corners fin 11-9-14 and 12-10-15
       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,9),psey-vf(i,npo,9),3)
       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),
     + psep+uf(i,npo,14),psey-vf(i,npo,14),3)
       call line(psep+uf(i,npo,10),psey-vf(i,npo,10),
     + psep+uf(i,npo,12),psey-vf(i,npo,12),3)
       call line(psep+uf(i,npo,10),psey-vf(i,npo,10),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)
       end if

       if (icont(7).eq.1) then
c      Corners init 11-9-14 and 12-10-15
       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,9),psey-vf(i,1,9),3)
       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,12),psey-vf(i,1,12),3)
       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)     
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,14),psey-vf(i,1,14),3)
       end if

       if (icont(2).eq.1) then
c      Init bracket
c      Lines 14-15
       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)
c      Segments 14-24-11 and 15-25-12
       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)
       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)
       call line(psep+uf(i,1,15),psey-vf(i,1,15),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
       call line(psep+uf(i,1,12),psey-vf(i,1,12),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
       end if

       if (icont(3).eq.1) then
c      Final bracket
c      Lines 14-15
       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)
c      Segments 14-24-11 and 15-25-12
       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)
       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)
       call line(psep+uf(i,npo,15),psey-vf(i,npo,15),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
       call line(psep+uf(i,npo,12),psey-vf(i,npo,12),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
       end if

       if (icont(5).eq.1) then
c      Initial segment
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,10),psey-vf(i,1,10),1)
       end if

       if (icont(6).eq.1) then
c      Final segment
       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),
     + psep+uf(i,npo,10),psey-vf(i,npo,10),1)
       end if
            
       return

       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW ARC BY 3 POINTS WITH CONTROL (ic)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE arc3p(i,npunt,uf,vf,dfle,is,psep,psey,ic,xupp)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey,dfle,sfle,tetha,omega,puntu(0:10),puntv(0:10)
       real*8 a,b,c,d,e,f,ep,eps,ep1,ep3,radi,epinc,bv,cv,xupp
       real*8 g,mu,xi,parcu(0:21),parcv(0:21),parcul(0:21),parcvl(0:21)
       real*8 parcve(0:21),parcue(0:21)
       real*8 xru(2),xrv(2),xsu(2),xsv(2)
       integer npunt,ic,is

c      is = convexitat (1) o concavitat (-1) de l'arc

       j=npunt

c      Evita radi infinit
       if (dabs(dfle).lt.0.000001d0) then
       dfle=0.00001d0 ! :)
       end if

c      Sign control (use negative 3D shaping)
       ii=1
       if (dfle.lt.0.) then
       ii=-1
       end if
       is=is*ii

c      ic=1 draw complete borders
c      ic=2 draw only external borders

c      Set basic points 1-2-3-4

       puntu(1)=uf(i,j,9)
       puntv(1)=vf(i,j,9)
       puntu(3)=uf(i,j,10)
       puntv(3)=vf(i,j,10)
       puntu(4)=0.5d0*(puntu(1)+puntu(3))
       puntv(4)=0.5d0*(puntv(1)+puntv(3))
       puntu(9)=puntu(3)
       puntv(9)=puntv(3)

       sfle=0.5d0*dsqrt((puntu(1)-puntu(3))**2.+(puntv(1)-puntv(3))**2.)
       tetha=datan(dfle/sfle)
       omega=datan((puntv(1)-puntv(3))/(puntu(3)-puntu(1)))
       if (is.eq.1) then
       puntu(2)=puntu(4)+dfle*dsin(omega)
       puntv(2)=puntv(4)+dfle*dcos(omega)
       end if
       if (is.eq.-1) then
       puntu(2)=puntu(4)-dfle*dsin(omega)
       puntv(2)=puntv(4)-dfle*dcos(omega)
       end if

c      Draw two segments
c       call line(psep+puntu(1),psey-puntv(1),
c     + psep+puntu(2),psey-puntv(2),1)
c       call line(psep+puntu(3),psey-puntv(3),
c     + psep+puntu(2),psey-puntv(2),1)

c      Circle by 1-2-3 analytical solution

       a=2.0d0*(puntu(2)-puntu(1))
       b=2.0d0*(puntv(2)-puntv(1))
       c=puntu(1)*puntu(1)-puntu(2)*puntu(2)+
     + puntv(1)*puntv(1)-puntv(2)*puntv(2)
       d=2.0d0*(puntu(3)-puntu(2))
       e=2.0d0*(puntv(3)-puntv(2))
       f=puntu(2)*puntu(2)-puntu(3)*puntu(3)+
     + puntv(2)*puntv(2)-puntv(3)*puntv(3)
       puntv(0)=((c*d/a)-f)/(e-(b*d/a))
       puntu(0)=-(puntv(0)*b+c)/a
       radi=dsqrt((puntu(1)-puntu(0))**2.+(puntv(1)-puntv(0))**2.)

c      Draw basic radius
c       call line(psep+puntu(1),psey-puntv(1),
c     + psep+puntu(0),psey-puntv(0),7)
c       call line(psep+puntu(3),psey-puntv(3),
c     + psep+puntu(0),psey-puntv(0),7)

c      Consider points in an horizontal segment 1-3

       if (dabs(puntu(3)-puntu(1)).ge.0.01d0) then
       xi=datan((puntv(1)-puntv(3))/(puntu(1)-puntu(3)))
       end if

       g=dsqrt(radi*radi-sfle*sfle)
       mu=datan(sfle/g)

       puntu(3)=puntu(1)+2.0d0*sfle
       puntv(3)=puntv(1)
       puntu(0)=puntu(1)+sfle
       puntv(0)=puntv(1)-g

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Arc internal
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Arc global coordinates (u,v) using 21 points
       do k=1,21
       ep=mu-(2.0d0*mu/20.0d0)*dfloat(k-1)
       parcu(k-1)=puntu(0)-radi*dsin(ep)
       parcv(k-1)=puntv(0)+radi*dcos(ep)
       end do

c      Arc local coordinates (u',v')
       do k=0,20
       parcul(k)=parcu(k)-puntu(1)
       parcvl(k)=dfloat(is)*(parcv(k)-puntv(1))
       end do

c      Rotate local coordinates around punt 1
       do k=0,20
       parcu(k)=parcul(k)*dcos(xi)-parcvl(k)*dsin(xi)+puntu(1)
       parcv(k)=parcul(k)*dsin(xi)+parcvl(k)*dcos(xi)+puntv(1)
       end do

c      Draw rotated arc
       if (ic.ne.2) then
       do k=1,20
       call line(psep+parcu(k-1),psey-parcv(k-1),
     + psep+parcu(k),psey-parcv(k),1)
       end do
       end if

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Arc external
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Arc global coordinates (u,v) using 21 points
       do k=1,21
       ep=mu-(2.0d0*mu/20.0d0)*dfloat(k-1)
       parcu(k-1)=puntu(0)-(radi+dfloat(ii)*xupp*0.1d0)*dsin(ep)
       parcv(k-1)=puntv(0)+(radi+dfloat(ii)*xupp*0.1d0)*dcos(ep)
       end do

c      Arc local coordinates (u',v')
       do k=0,20
       parcul(k)=parcu(k)-puntu(1)
       parcvl(k)=dfloat(is)*(parcv(k)-puntv(1))
       end do

c      Rotate local coocrdinates around punt 1
       do k=0,20
       parcue(k)=parcul(k)*dcos(xi)-parcvl(k)*dsin(xi)+puntu(1)
       parcve(k)=parcul(k)*dsin(xi)+parcvl(k)*dcos(xi)+puntv(1)
       end do

c      Draw rotated arc
       do k=1,20
       call line(psep+parcue(k-1),psey-parcve(k-1),
     + psep+parcue(k),psey-parcve(k),3)
       end do

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Intersection points
c      Points of intersection of arcs with external borders
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Intersection left
       xru(1)=parcue(0)
       xrv(1)=parcve(0)
       xru(2)=parcue(1)
       xrv(2)=parcve(1)

       if (is*ii.eq.1) then
       xsu(1)=uf(i,j,11)
       xsv(1)=vf(i,j,11)
       xsu(2)=uf(i,j-1,11)
       xsv(2)=vf(i,j-1,11)
       end if

       if (is*ii.eq.-1) then 
       xsu(1)=uf(i,j,11)
       xsv(1)=vf(i,j,11)
       xsu(2)=uf(i,j+1,11)
       xsv(2)=vf(i,j+1,11)
       end if

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       call line(psep+xsu(1),psey-xsv(1),psep+xtu,psey-xtv,3)
       call line(psep+xru(1),psey-xrv(1),psep+xtu,psey-xtv,3)
       if (ic.ne.2) then
       call line(psep+puntu(1),psey-puntv(1),psep+xtu,psey-xtv,3)
       call line(psep+puntu(1),psey-puntv(1),psep+xsu(1),psey-xsv(1),3)
       call line(psep+puntu(1),psey-puntv(1),psep+xru(1),psey-xrv(1),3)
       end if

c      Intersection right
       xru(1)=parcue(20)
       xrv(1)=parcve(20)
       xru(2)=parcue(19)
       xrv(2)=parcve(19)

       if (is*ii.eq.1) then
       xsu(1)=uf(i,j,12)
       xsv(1)=vf(i,j,12)
       xsu(2)=uf(i,j-1,12)
       xsv(2)=vf(i,j-1,12)
       end if

       if (is*ii.eq.-1) then
       xsu(1)=uf(i,j,12)
       xsv(1)=vf(i,j,12)
       xsu(2)=uf(i,j+1,12)
       xsv(2)=vf(i,j+1,12)
       end if

       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)

       call line(psep+xsu(1),psey-xsv(1),psep+xtu,psey-xtv,3)
       call line(psep+xru(1),psey-xrv(1),psep+xtu,psey-xtv,3)
       if (ic.ne.2) then
       call line(psep+puntu(9),psey-puntv(9),psep+xtu,psey-xtv,3)
       call line(psep+puntu(9),psey-puntv(9),psep+xsu(1),psey-xsv(1),3)
       call line(psep+puntu(9),psey-puntv(9),psep+xru(1),psey-xrv(1),3)
       end if

       return
       end



ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW ARC BY 3 POINTS WITH CONTROL (ic) 
c      SPECIAL!!!!!
c      USED ONLY FOR OBTAINIG SOME POINTS FOR ROMAN PRINTING....
c      INTEGRAR DINS romanoparc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE arc3parc(i,npunt,uf,vf,dfle,is,psep,psey,ic,xupp)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey,dfle,sfle,tetha,omega,puntu(0:10),puntv(0:10)
       real*8 a,b,c,d,e,f,ep,eps,ep1,ep3,radi,epinc,bv,cv,xupp
       real*8 g,mu,xi,parcu(0:21),parcv(0:21),parcul(0:21),parcvl(0:21)
       real*8 parcve(0:21),parcue(0:21)
       real*8 xru(2),xrv(2),xsu(2),xsv(2)
       real*8 uu1,vv1,uu2,vv2,xlen1,xlen2
       integer npunt,ic,is,kini,kfin

       j=npunt

c      Evita radi infinit
       if (dfle.lt.0.000001d0) then
       dfle=0.00001d0 ! :)
       end if

c      ic=1 draw complete borders
c      ic=2 draw only external borders

c      Set basic points 1-2-3-4

       puntu(1)=uf(i,j,9)
       puntv(1)=vf(i,j,9)
       puntu(3)=uf(i,j,10)
       puntv(3)=vf(i,j,10)
       puntu(4)=0.5d0*(puntu(1)+puntu(3))
       puntv(4)=0.5d0*(puntv(1)+puntv(3))
       puntu(9)=puntu(3)
       puntv(9)=puntv(3)

       sfle=0.5d0*dsqrt((puntu(1)-puntu(3))**2.+(puntv(1)-puntv(3))**2.)
       tetha=datan(dfle/sfle)
       omega=datan((puntv(1)-puntv(3))/(puntu(3)-puntu(1)))
       if (is.eq.1) then
       puntu(2)=puntu(4)+dfle*dsin(omega)
       puntv(2)=puntv(4)+dfle*dcos(omega)
       end if
       if (is.eq.-1) then
       puntu(2)=puntu(4)-dfle*dsin(omega)
       puntv(2)=puntv(4)-dfle*dcos(omega)
       end if

c      Circle by 1-2-3 analytical solution
       a=2.0d0*(puntu(2)-puntu(1))
       b=2.0d0*(puntv(2)-puntv(1))
       c=puntu(1)*puntu(1)-puntu(2)*puntu(2)+
     + puntv(1)*puntv(1)-puntv(2)*puntv(2)
       d=2.0d0*(puntu(3)-puntu(2))
       e=2.0d0*(puntv(3)-puntv(2))
       f=puntu(2)*puntu(2)-puntu(3)*puntu(3)+
     + puntv(2)*puntv(2)-puntv(3)*puntv(3)
       puntv(0)=((c*d/a)-f)/(e-(b*d/a))
       puntu(0)=-(puntv(0)*b+c)/a
       radi=dsqrt((puntu(1)-puntu(0))**2.+(puntv(1)-puntv(0))**2.)

c      Consider points in an horizontal segment 1-3
       if (dabs(puntu(3)-puntu(1)).ge.0.01d0) then
       xi=datan((puntv(1)-puntv(3))/(puntu(1)-puntu(3)))
       end if

       g=dsqrt(radi*radi-sfle*sfle)
       mu=datan(sfle/g)

       puntu(3)=puntu(1)+2.0d0*sfle
       puntv(3)=puntv(1)
       puntu(0)=puntu(1)+sfle
       puntv(0)=puntv(1)-g

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Arc internal
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Case extrados
c      Arc global coordinates (u,v) using 21 points
       do k=1,21
       ep=mu-(2.0d0*mu/20.0d0)*dfloat(k-1)
       parcu(k-1)=puntu(0)-radi*dsin(ep)
       parcv(k-1)=puntv(0)+radi*dcos(ep)
       end do

c      Case intrados
       if (ii.eq.-1) then
       do k=21,1,-1

       end do
       end if

c      Arc local coordinates (u',v')
       do k=0,20
       parcul(k)=parcu(k)-puntu(1)
       parcvl(k)=dfloat(is)*(parcv(k)-puntv(1))
       end do

c      Rotate local coordinates around punt 1
       do k=0,20
       parcu(k)=parcul(k)*dcos(xi)-parcvl(k)*dsin(xi)+puntu(1)
       parcv(k)=parcul(k)*dsin(xi)+parcvl(k)*dcos(xi)+puntv(1)
       end do

c      Draw rotated arc
       if (ic.ne.2) then
       do k=1,20
c       call line(psep+parcu(k-1),psey-parcv(k-1),
c     + psep+parcu(k),psey-parcv(k),1)
       end do
       end if

c      Arc length
       xlen1=0.0d0
       do k=0,20-1
       xlen1=xlen1+dsqrt((parcu(k+1)-parcu(k))**2.+
     + (parcv(k+1)-parcv(k))**2)
       end do

c      Detect kini and kfin
       xlen2=0.0d0
       do k=0,20-1
       xlen2=xlen+dsqrt((parcu(k+1)-parcu(k))**2.+
     + (parcv(k+1)-parcv(k))**2)
       if (len2.le.len1*xlenco) then
       kini=k
       kfin=k+2
       end if
       end do
c      Some arrangements...
       if (kini.ge.19) then
       kfin=20
       end if
       if (kfin.eq.20) then
       kini=18
       end if

c      Define especial points in the arc
       uu1=parcu(kini)
       vv1=parcv(kini)
       uu2=parcu(kfin)
       vv2=parcv(kfin)

       return
       end    ! ARC3P special


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW VENT WITH CONTROLS
c      Draw vent panels types
c      ic1=1 > print; ic1=2 > laser
c      ic2= vent type 1,0,-1,-2,-3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc     
       SUBROUTINE drwvent(i,np,uf,vf,ufv,vfv,psep,psey,xupp,xupple,
     + xuppte,xkf,ic1,ic2,csi)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 ufv(0:100,500,50),vfv(0:100,500,50)
       real*8 ufa(0:100,500,50),vfa(0:100,500,50) !auxiliar
       real*8 ufb(0:100,500,50),vfb(0:100,500,50) !auxiliar
       integer np(0:100,9)
       real*8 psep,psey,xupp,xupple,xuppte,xkf,xcsi,ycsi
       real*8 cs2x,cs2y,cs1x,cs1y,alpha,alpha1,alpha2,csi(0:100,60)
       integer npi,npf,np0,npo1,i,ic1,ic2
       real*8 xru(2),xrv(2),xsu(2),xsv(2)
       real*8 xlenl,xlenlr,xlenr,xlenrr
       real*8 xcir,xdes
       real*8 pgx(100),pgy(100),param1,param2,param3
       real*8 distrel,distrel1,distrel2
       integer npol,npr,npoly,npolyl,npolyr

       real*8 xpoly(500),ypoly(500)
       real*8 x_poly,y_poly,x_poly1,y_poly1,x_poly2,y_poly2
       real*8 x_poly11,y_poly11,x_poly12,y_poly12
       real*8 xu,xv,alp
       real*8 xupplenew

c      Vent points
       npi=np(i,2)
       npf=np(i,2)+np(i,3)-1
       npo=npf-npi+1

c      Parameters
       xdes=csi(i,51)
       xcir=csi(i,50)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Parameters for translation and rotation ic2 ge 1
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (ic2.ge.1) then
       npo1=np(i,2)
       cs1x=(uf(i,npo1,9)+uf(i,npo1,10))*0.5
       cs1y=(vf(i,npo1,9)+vf(i,npo1,10))*0.5
       cs2x=(ufv(i,1,9)+ufv(i,1,10))*0.5
       cs2y=(vfv(i,1,9)+vfv(i,1,10))*0.5
       alpha=(datan((vf(i,npo1,10)-vf(i,npo1,9))/
     + (uf(i,npo1,10)-uf(i,npo1,9))))

c      Translation -cs2x
       do j=1,npo
       ufb(i,j,9)=ufv(i,j,9)-cs2x
       ufb(i,j,10)=ufv(i,j,10)-cs2x
       ufb(i,j,11)=ufv(i,j,11)-cs2x
       ufb(i,j,12)=ufv(i,j,12)-cs2x
       vfb(i,j,9)=vfv(i,j,9)
       vfb(i,j,10)=vfv(i,j,10)
       vfb(i,j,11)=vfv(i,j,11)
       vfb(i,j,12)=vfv(i,j,12)
       end do

c      Rotation alpha and traslation csx1,cs1y
       do j=1,npo
       ufa(i,j,9)=ufb(i,j,9)*dcos(alpha)-vfv(i,j,9)*dsin(alpha)+
     + cs1x
       ufa(i,j,10)=ufb(i,j,10)*dcos(alpha)-vfv(i,j,10)*dsin(alpha)+
     + cs1x
       ufa(i,j,11)=ufb(i,j,11)*dcos(alpha)-vfv(i,j,11)*dsin(alpha)+
     + cs1x
       ufa(i,j,12)=ufb(i,j,12)*dcos(alpha)-vfv(i,j,12)*dsin(alpha)+
     + cs1x
       vfa(i,j,9)=ufb(i,j,9)*dsin(alpha)+vfv(i,j,9)*dcos(alpha)+
     + cs1y
       vfa(i,j,10)=ufb(i,j,10)*dsin(alpha)+vfv(i,j,10)*dcos(alpha)+
     + cs1y
       vfa(i,j,11)=ufb(i,j,11)*dsin(alpha)+vfv(i,j,11)*dcos(alpha)+
     + cs1y
       vfa(i,j,12)=ufb(i,j,12)*dsin(alpha)+vfv(i,j,12)*dcos(alpha)+
     + cs1y
       end do

c      BRUTE FORCE redefine
       ufa(i,1,9)=csi(i,21)
       vfa(i,1,9)=csi(i,22)
       ufa(i,1,10)=csi(i,23)
       vfa(i,1,10)=csi(i,24)
       ufa(i,1,11)=csi(i,25)
       vfa(i,1,11)=csi(i,26)
       ufa(i,1,12)=csi(i,27)
       vfa(i,1,12)=csi(i,28)

       call extpoints(i,ufa,vfa,npo,xupp,xupple,xuppte,1)

       end if ! ic2 ge 1

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Parameters for translation and rotation ic2 le -1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       If (ic2.le.-1) then

       do j=1,npo
       ufb(i,j,9)=ufv(i,j,9)
       ufb(i,j,10)=ufv(i,j,10)
       ufb(i,j,11)=ufv(i,j,11)
       ufb(i,j,12)=ufv(i,j,12)
       vfb(i,j,9)=vfv(i,j,9)
       vfb(i,j,10)=vfv(i,j,10)
       vfb(i,j,11)=vfv(i,j,11)
       vfb(i,j,12)=vfv(i,j,12)
       end do

       cs1x=(ufv(i,npo,9)+ufv(i,npo,10))*0.5
       cs1y=(vfv(i,npo,9)+vfv(i,npo,10))*0.5
       cs2x=(ufv(i,1,9)+ufv(i,1,10))*0.5
       cs2y=(vfv(i,1,9)+vfv(i,1,10))*0.5

       alpha1=(datan((vfv(i,npo,10)-vfv(i,npo,9))/
     + (ufv(i,npo,10)-ufv(i,npo,9))))
       alpha2=(datan((vfb(i,1,10)-vfb(i,1,9))/
     + (ufb(i,npo,10)-ufb(i,1,9))))

c      Translate vents from point 2 to (0,0)
             
       do j=1,npo
       ufb(i,j,9)=ufv(i,j,9)-cs1x
       ufb(i,j,10)=ufv(i,j,10)-cs1x
       ufb(i,j,11)=ufv(i,j,11)-cs1x
       ufb(i,j,12)=ufv(i,j,12)-cs1x
       vfb(i,j,9)=vfv(i,j,9)-cs1y
       vfb(i,j,10)=vfv(i,j,10)-cs1y
       vfb(i,j,11)=vfv(i,j,11)-cs1y
       vfb(i,j,12)=vfv(i,j,12)-cs1y
       end do

c      Rotation angle alpha
c      Translation using brute force (section 8.5.5) variable csi
c      TRY ANOTHER METHOD!!!!!!!!!!!!!!
c      Force last point

       alpha=-alpha1+csi(i,9)
       xcsi=(csi(i,1)+csi(i,3))*0.5
       ycsi=(csi(i,2)+csi(i,4))*0.5

       do j=1,npo
       ufa(i,j,9)=ufb(i,j,9)*dcos(alpha)-vfb(i,j,9)*dsin(alpha)+xcsi
       ufa(i,j,10)=ufb(i,j,10)*dcos(alpha)-vfb(i,j,10)*dsin(alpha)+
     + xcsi
       ufa(i,j,11)=ufb(i,j,11)*dcos(alpha)-vfb(i,j,11)*dsin(alpha)+
     + xcsi
       ufa(i,j,12)=ufb(i,j,12)*dcos(alpha)-vfb(i,j,12)*dsin(alpha)+
     + xcsi
       vfa(i,j,9)=ufb(i,j,9)*dsin(alpha)+vfb(i,j,9)*dcos(alpha)+ycsi
       vfa(i,j,10)=ufb(i,j,10)*dsin(alpha)+vfb(i,j,10)*dcos(alpha)+
     + ycsi
       vfa(i,j,11)=ufb(i,j,11)*dsin(alpha)+vfb(i,j,11)*dcos(alpha)+
     + ycsi
       vfa(i,j,12)=ufb(i,j,12)*dsin(alpha)+vfb(i,j,12)*dcos(alpha)+
     + ycsi
       end do

c      BRUTE FORCE redefine
       ufa(i,npo,9)=csi(i,1)
       vfa(i,npo,9)=csi(i,2)
       ufa(i,npo,10)=csi(i,3)
       vfa(i,npo,10)=csi(i,4)
       ufa(i,npo,11)=csi(i,5)
       vfa(i,npo,11)=csi(i,6)
       ufa(i,npo,12)=csi(i,7)
       vfa(i,npo,12)=csi(i,8)

c      USE LOW!!!
       call extpoints(i,ufa,vfa,npo,csi(i,10),csi(i,11),csi(i,12),1)

       end if ! ic1=-1

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw complete vent case ic2=1,6
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic2.eq.1.or.ic2.eq.6) then

c      Subcase ic1=1 (Print)
c      Points vent
       if (ic1.eq.1) then
       j9=npo
       j10=npo
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,1,9),psey-vfa(i,1,9),psep+ufa(i,1,10),
     + psey-vfa(i,1,10),1)
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),psep+ufa(i,npo,10),
     + psey-vfa(i,npo,10),1)
       call line(psep+ufa(i,npo,24),psey-vfa(i,npo,24),
     + psep+ufa(i,npo,25),psey-vfa(i,npo,25),3)
c      Lateral unions       
       call line(psep+ufa(i,npo,24),psey-vfa(i,npo,24),
     + psep+ufa(i,npo,11),psey-vfa(i,npo,11),3)
       call line(psep+ufa(i,npo,25),psey-vfa(i,npo,25),
     + psep+ufa(i,npo,12),psey-vfa(i,npo,12),3)
c      Corners
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),
     + psep+ufa(i,npo,11),psey-vfa(i,npo,11),3)
       call line(psep+ufa(i,npo,10),psey-vfa(i,npo,10),
     + psep+ufa(i,npo,12),psey-vfa(i,npo,12),3)
       call line(psep+ufa(i,npo,14),psey-vfa(i,npo,14),
     + psep+ufa(i,npo,9),psey-vfa(i,npo,9),3)
       call line(psep+ufa(i,npo,15),psey-vfa(i,npo,15),
     + psep+ufa(i,npo,10),psey-vfa(i,npo,10),3)
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,9),psey-vfa(i,j,9),psep+ufa(i,j+1,9),
     + psey-vfa(i,j+1,9),1)
       call line(psep+ufa(i,j,10),psey-vfa(i,j,10),psep+ufa(i,j+1,10),
     + psey-vfa(i,j+1,10),1)
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Case ic2=6 draw elliptical inlets
       if (ic2.eq.6) then
       pgx(1)=psep+ufa(i,1,9)
       pgy(1)=psey-vfa(i,1,9)
       pgx(2)=psep+ufa(i,1,10)
       pgy(2)=psey-vfa(i,1,10)
       pgx(4)=psep+ufa(i,npo,9)
       pgy(4)=psey-vfa(i,npo,9)
       pgx(3)=psep+ufa(i,npo,10)
       pgy(3)=psey-vfa(i,npo,10)
       param1=csi(i+1,19)
       param2=csi(i+1,20)
       call elliquad(pgx,pgy,param1,param2)
       end if

       end if ! ic1=1

c      Subcase ic1=2 (Laser)
       if (ic1.eq.2) then
c      Punts vent
c      Revisar
c      xcir,xdes aquí ja està destrossat!!!!!!!!!
c       write (*,*) "HERE IS 1 ",i,csi(i,50),csi(i,51)
c       write (*,*) "HERE IS 2 ",i,xcir,xdes
c      Note csi(i,50)=xcir
c      Note csi(i,51)=xdes
       j9=npo
       j10=npo
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,npo,24),psey-vfa(i,npo,24),
     + psep+ufa(i,npo,25),psey-vfa(i,npo,25),3)
c      Lateral unions       
       call line(psep+ufa(i,npo,24),psey-vfa(i,npo,24),
     + psep+ufa(i,npo,11),psey-vfa(i,npo,11),3)
       call line(psep+ufa(i,npo,25),psey-vfa(i,npo,25),
     + psep+ufa(i,npo,12),psey-vfa(i,npo,12),3)
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Case ic2=6 draw elliptical inlets
       if (ic2.eq.6) then
       pgx(1)=psep+ufa(i,1,9)
       pgy(1)=psey-vfa(i,1,9)
       pgx(2)=psep+ufa(i,1,10)
       pgy(2)=psey-vfa(i,1,10)
       pgx(4)=psep+ufa(i,npo,9)
       pgy(4)=psey-vfa(i,npo,9)
       pgx(3)=psep+ufa(i,npo,10)
       pgy(3)=psey-vfa(i,npo,10)
       param1=csi(i+1,19)
       param2=csi(i+1,20)
       call elliquad(pgx,pgy,param1,param2)
       end if

       end if ! ic1=2

       end if ! ic2=1,6

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw complete vent case ic2=-1,-6 (intrados)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic2.eq.-1.or.ic2.eq.-6) then

c      Subcase ic1=1 (Print)
       if (ic1.eq.1) then
c      Points vent
       j9=1
       j10=1
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,1,9),psey-vfa(i,1,9),psep+ufa(i,1,10),
     + psey-vfa(i,1,10),1)
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),
     + psep+ufa(i,npo,10),psey-vfa(i,npo,10),1)
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Lateral unions       
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,11),psey-vfa(i,1,11),3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,1,12),psey-vfa(i,1,12),3)
c      Corners
       call line(psep+ufa(i,1,9),psey-vfa(i,1,9),
     + psep+ufa(i,1,11),psey-vfa(i,1,11),3)
       call line(psep+ufa(i,1,10),psey-vfa(i,1,10),
     + psep+ufa(i,1,12),psey-vfa(i,1,12),3)
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,9),psey-vfa(i,1,9),3)
       if (ufa(i,1,25).ge.ufa(i,1,15)) then ! segment correction
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,1,10),psey-vfa(i,1,10),3)
       else
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,1,10),psey-vfa(i,1,10),3)
       end if
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,9),psey-vfa(i,j,9),psep+ufa(i,j+1,9),
     + psey-vfa(i,j+1,9),1)
       call line(psep+ufa(i,j,10),psey-vfa(i,j,10),psep+ufa(i,j+1,10),
     + psey-vfa(i,j+1,10),1)
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Case ic2=-6 draw elliptical inlets
       if (ic2.eq.-6) then
       pgx(1)=psep+ufa(i,1,9)
       pgy(1)=psey-vfa(i,1,9)
       pgx(2)=psep+ufa(i,1,10)
       pgy(2)=psey-vfa(i,1,10)
       pgx(4)=psep+ufa(i,npo,9)
       pgy(4)=psey-vfa(i,npo,9)
       pgx(3)=psep+ufa(i,npo,10)
       pgy(3)=psey-vfa(i,npo,10)
       param1=csi(i+1,19)
       param2=csi(i+1,20)
       call elliquad(pgx,pgy,param1,param2)
       end if

       end if ! ic1=1

c      Subcase ic1=2 (Laser)
       if (ic1.eq.2) then
c      Points vent
       j9=1
       j10=1
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Lateral unions       
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,11),psey-vfa(i,1,11),3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,1,12),psey-vfa(i,1,12),3)
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Case ic2=-6 draw elliptical inlets
       if (ic2.eq.-6) then
       pgx(1)=psep+ufa(i,1,9)
       pgy(1)=psey-vfa(i,1,9)
       pgx(2)=psep+ufa(i,1,10)
       pgy(2)=psey-vfa(i,1,10)
       pgx(4)=psep+ufa(i,npo,9)
       pgy(4)=psey-vfa(i,npo,9)
       pgx(3)=psep+ufa(i,npo,10)
       pgy(3)=psey-vfa(i,npo,10)
       param1=csi(i+1,19)
       param2=csi(i+1,20)
       call elliquad(pgx,pgy,param1,param2)
       end if

       end if ! ic1=2

       end if ! ic2=-1,-6

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw complete vent case ic2=-2 (intrados)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic2.eq.-2) then

c      Redefine 24,14,15,25
       alpha=datan((vfa(i,npo,9)-vfa(i,1,10))/
     + (ufa(i,1,10)-ufa(i,npo,9)))
       ufa(i,1,14)=ufa(i,npo,9)-csi(i,12)*0.1*dsin(alpha)
       vfa(i,1,14)=vfa(i,npo,9)-csi(i,12)*0.1*dcos(alpha)
       ufa(i,1,15)=ufa(i,1,10)-csi(i,12)*0.1*dsin(alpha)
       vfa(i,1,15)=vfa(i,1,10)-csi(i,12)*0.1*dcos(alpha)

c      Point 24
       xru(1)=ufa(i,npo,11)
       xrv(1)=vfa(i,npo,11)
       xru(2)=ufa(i,npo-1,11)
       xrv(2)=vfa(i,npo-1,11)
       xsu(1)=ufa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(1)=vfa(i,1,14)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,24)=xtu
       vfa(i,1,24)=xtv

c      Point 25
       xru(1)=ufa(i,1,12)
       xru(2)=ufa(i,2,12)
       xrv(1)=vfa(i,1,12)
       xrv(2)=vfa(i,2,12)
       xsu(1)=ufa(i,1,14)
       xsv(1)=vfa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,25)=xtu
       vfa(i,1,25)=xtv

c      Subcase ic1=1 (Print)
       if (ic1.eq.1) then
c      Points vent
       j9=npo
       j10=1
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),psep+ufa(i,npo,10),
     + psey-vfa(i,npo,10),1)
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),psep+ufa(i,1,10),
     + psey-vfa(i,1,10),1)
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Lateral unions       
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,npo,11),psey-vfa(i,npo,11),3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,1,12),psey-vfa(i,1,12),3)
c      Corners
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),
     + psep+ufa(i,npo,11),psey-vfa(i,npo,11),3)
       call line(psep+ufa(i,1,10),psey-vfa(i,1,10),
     + psep+ufa(i,1,12),psey-vfa(i,1,12),3)
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,npo,9),psey-vfa(i,npo,9),3)
       if (ufa(i,1,25).ge.ufa(i,1,15)) then ! segment correction
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,1,10),psey-vfa(i,1,10),3)
       else
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,1,10),psey-vfa(i,1,10),3)
       end if
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,10),psey-vfa(i,j,10),psep+ufa(i,j+1,10),
     + psey-vfa(i,j+1,10),1)
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
       end if ! ic1=1

c      Subcase ic1=2 (Laser)
       if (ic1.eq.2) then
c      Points vent
       j9=npo
       j10=1
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Lateral unions       
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,npo,11),psey-vfa(i,npo,11),3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,1,12),psey-vfa(i,1,12),3)
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
       end if ! ic1=2

       end if ! ic2=-2

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw complete vent case ic2=-3 (intrados)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic2.eq.-3) then

c      !!!!!!!!!!!!!!!! RECALCULAR !!!!!!!!!!!!!!!!!!!!!!!!

c      Redefine 24,14,15,25
       alpha=datan((vfa(i,1,9)-vfa(i,npo,10))/
     + (ufa(i,npo,10)-ufa(i,1,9)))
       ufa(i,1,14)=ufa(i,1,9)-csi(i,12)*0.1*dsin(alpha)
       vfa(i,1,14)=vfa(i,1,9)-csi(i,12)*0.1*dcos(alpha)
       ufa(i,1,15)=ufa(i,npo,10)-csi(i,12)*0.1*dsin(alpha)
       vfa(i,1,15)=vfa(i,npo,10)-csi(i,12)*0.1*dcos(alpha)

c      Point 24
       xru(1)=ufa(i,1,11)
       xrv(1)=vfa(i,1,11)
       xru(2)=ufa(i,2,11)
       xrv(2)=vfa(i,2,11)
       xsu(1)=ufa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(1)=vfa(i,1,14)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,24)=xtu
       vfa(i,1,24)=xtv

c      Point 25
       xru(1)=ufa(i,npo,12)
       xru(2)=ufa(i,npo-1,12)
       xrv(1)=vfa(i,npo,12)
       xrv(2)=vfa(i,npo-1,12)
       xsu(1)=ufa(i,1,14)
       xsv(1)=vfa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,25)=xtu
       vfa(i,1,25)=xtv

c      Subcase ic1=1 (Print)
       if (ic1.eq.1) then
c      Points vent
       j9=1
       j10=npo
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),psep+ufa(i,npo,10),
     + psey-vfa(i,npo,10),1)
       call line(psep+ufa(i,1,9),psey-vfa(i,1,9),psep+ufa(i,npo,10),
     + psey-vfa(i,npo,10),1)
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Lateral unions       
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,11),psey-vfa(i,1,11),3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,npo,12),psey-vfa(i,npo,12),3)
c      Corners
       call line(psep+ufa(i,1,9),psey-vfa(i,1,9),
     + psep+ufa(i,1,11),psey-vfa(i,1,11),3)
       call line(psep+ufa(i,npo,10),psey-vfa(i,npo,10),
     + psep+ufa(i,npo,12),psey-vfa(i,npo,12),3)
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,9),psey-vfa(i,1,9),3)
       if (ufa(i,1,15).ge.ufa(i,1,25)) then ! segment correction
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,npo,10),psey-vfa(i,npo,10),3)
       else
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,npo,10),psey-vfa(i,npo,10),3)
       end if
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,9),psey-vfa(i,j,9),psep+ufa(i,j+1,9),
     + psey-vfa(i,j+1,9),1)
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       end do
       end if ! ic1=1

c      Subcase ic1=2 (Laser)
       if (ic1.eq.2) then
c      Points vent
       j9=1
       j10=npo
       call prinfpv(i,j9,j10,ufa,vfa,psep,psey,csi(i,50),csi(i,51),xkf,
     + ic1,ic2)
c      Segments
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Lateral unions       
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+ufa(i,1,11),psey-vfa(i,1,11),3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+ufa(i,npo,12),psey-vfa(i,npo,12),3)
c      Laterals
       do j=1,npo-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       end do
       end if ! ic1=2

       end if ! ic2=-3

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw complete vent case ic2=-4,-5 (intrados)
c      Advanced generic vent...
c      Use vector csi(i,k) for transport additional interpolation data
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic2.eq.-4.or.ic2.eq.-5) then

       if (ic2.eq.-4) then
c      Length vent left
       xlenl=0.0d0
       do j=1,npo-1
       xlenl=xlenl+dsqrt((ufa(i,j,9)-ufa(i,j+1,9))**2.+
     + (vfa(i,j,9)-vfa(i,j+1,9))**2.)
       end do
       xlenlr=xlenl*(1.-csi(i+1,19)/100.)

c      Length vent rigth
       xlenr=0.0d0
       do j=1,npo-1
       xlenr=xlenr+dsqrt((ufa(i,j,10)-ufa(i,j+1,10))**2.+
     + (vfa(i,j,10)-vfa(i,j+1,10))**2.)
       end do
       xlenrr=xlenr*(1.-csi(i+1,20)/100.)
       end if

       if (ic2.eq.-5) then
c      Length vent left
       xlenl=0.0d0
       do j=1,npo-1
       xlenl=xlenl+dsqrt((ufa(i,j,9)-ufa(i,j+1,9))**2.+
     + (vfa(i,j,9)-vfa(i,j+1,9))**2.)
       end do
       xlenlr=xlenl*(1.-csi(i+1,19)/100.)

c      Length vent rigth
       xlenr=0.0d0
       do j=1,npo-1
       xlenr=xlenr+dsqrt((ufa(i,j,10)-ufa(i,j+1,10))**2.+
     + (vfa(i,j,10)-vfa(i,j+1,10))**2.)
       end do
       xlenrr=xlenr*(1.-csi(i+1,20)/100.)

c      Deflection parameter (vent type -5)
       param3=(csi(i+1,18)/100.)*0.5*(xlenl+xlenr)
       end if

c      Interpolate new vent init
c      Left side
       do j=1,npo
       xpoly(j)=ufa(i,j,9)
       ypoly(j)=vfa(i,j,9)
       end do
       call interpoly2d(xpoly,ypoly,x_poly,y_poly,xlenlr,1,npo,npolyl,
     + distrel)
       x_poly1=x_poly
       y_poly1=y_poly
       distrel1=distrel
c      Right side
       do j=1,npo
       xpoly(j)=ufa(i,j,10)
       ypoly(j)=vfa(i,j,10)
       end do
       call interpoly2d(xpoly,ypoly,x_poly,y_poly,xlenrr,1,npo,npolyr,
     + distrel)
       x_poly2=x_poly
       y_poly2=y_poly
       distrel2=distrel

c      Points 14-15
       alpha=dabs(datan((y_poly2-y_poly1)/(x_poly2-x_poly1)))
       ufa(i,1,14)=x_poly1-csi(i,12)*0.1*dsin(alpha)
       vfa(i,1,14)=y_poly1-csi(i,12)*0.1*dcos(alpha)
       ufa(i,1,15)=x_poly2-csi(i,12)*0.1*dsin(alpha)
       vfa(i,1,15)=y_poly2-csi(i,12)*0.1*dcos(alpha)

       npoly=npolyl
       if (npolyl.eq.1) then
       npoly=2
       end if       

c      Point 24'
       xru(1)=ufa(i,npolyl+1,11)
       xrv(1)=vfa(i,npolyl+1,11)
       xru(2)=ufa(i,npolyl,11)
       xrv(2)=vfa(i,npolyl,11)
       xsu(1)=ufa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(1)=vfa(i,1,14)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,24)=xtu
       vfa(i,1,24)=xtv

c      Point 11'
       x_poly11=ufa(i,npolyl,11)+(ufa(i,npolyl+1,11)-ufa(i,npolyl,11))*
     + distrel1
       y_poly11=vfa(i,npolyl,11)+(vfa(i,npolyl+1,11)-vfa(i,npolyl,11))*
     + distrel1

c      Point 12'
       x_poly12=ufa(i,npolyr,12)+(ufa(i,npolyr+1,12)-ufa(i,npolyr,12))*
     + distrel2
       y_poly12=vfa(i,npolyr,12)+(vfa(i,npolyr+1,12)-vfa(i,npolyr,12))*
     + distrel2

       npoly=npolyr
       if (nployr.eq.1) then
       npoly=2
       end if  

c      Point 25'
       xru(1)=ufa(i,npolyr+1,12)
       xrv(1)=vfa(i,npolyr+1,12)
       xru(2)=ufa(i,npolyr,12)
       xrv(2)=vfa(i,npolyr,12)
       xsu(1)=ufa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(1)=vfa(i,1,14)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,25)=xtu
       vfa(i,1,25)=xtv

c      Subcase ic1=1 (Print)
       if (ic1.eq.1) then

c      Points vent
c      Point left
       xu=x_poly1
       xv=y_poly1
       alp=abs(datan((vfa(i,npolyl+1,9)-vfa(i,npolyl,9)/
     + (ufa(i,npolyl+1,9)-ufa(i,npolyl,9)))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call pointg(psep+xu,-xv+psey,xcir,4)
c      Point right
       xu=x_poly2
       xv=y_poly2
       alp=abs(datan((vfa(i,npolyr+1,10)-vfa(i,npolyr,10)/
     + (ufa(i,npolyr+1,10)-ufa(i,npolyr,10)))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)   
       call pointg(psep+xu,-xv+psey,xcir,4)

c      Segments
c      Line 9-10
       call line(psep+ufa(i,npo,9),psey-vfa(i,npo,9),psep+ufa(i,npo,10),
     + psey-vfa(i,npo,10),1)

       if (ic2.eq.-4) then
c      Line 9'-10'
       call line(psep+x_poly1,psey-y_poly1,psep+x_poly2,psey-y_poly2,1)
c      Line 14'-15'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),3)
       end if

       if (ic2.eq.-5) then
c      Line 9'-10'
       call arcfle(psep+x_poly1,psey-y_poly1,psep+x_poly2,psey-y_poly2,
     + param3,1,1)
c      Line 14'-15'
       call arcfle(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),param3,1,3)
       end if
     
c      Corners
c      Line 14'-24' and 15-25'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,24),psey-vfa(i,1,24),3)
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Line 24'-11' and 25'-12'      
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+x_poly11,psey-y_poly11,3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+x_poly12,psey-y_poly12,3)
c      Line 9'-11'
       call line(psep+x_poly1,psey-y_poly1,psep+x_poly11,
     + psey-y_poly11,3)
c      Line 10'-12'
       call line(psep+x_poly2,psey-y_poly2,psep+x_poly12,
     + psey-y_poly12,3)
c      Lines 9'-14' and 10'-15'
       call line(psep+x_poly1,psey-y_poly1,psep+ufa(i,1,14),
     + psey-vfa(i,1,14),3)
       call line(psep+x_poly2,psey-y_poly2,psep+ufa(i,1,15),
     + psey-vfa(i,1,15),3)

c      Laterals right
       call line(psep+ufa(i,npolyr+1,10),psey-vfa(i,npolyr+1,10),
     + psep+x_poly2,psey-y_poly2,1)
       do j=npolyr+1,npo-1
       call line(psep+ufa(i,j,10),psey-vfa(i,j,10),psep+ufa(i,j+1,10),
     + psey-vfa(i,j+1,10),1)
       end do
       call line(psep+ufa(i,npolyr+1,12),psey-vfa(i,npolyr+1,12),
     + psep+x_poly12,psey-y_poly12,3)
       do j=npolyr+1,npo-1
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Laterals left
       call line(psep+ufa(i,npolyl+1,9),psey-vfa(i,npolyl+1,9),
     + psep+x_poly1,psey-y_poly1,1)
       do j=npolyl+1,npo-1
       call line(psep+ufa(i,j,9),psey-vfa(i,j,9),psep+ufa(i,j+1,9),
     + psey-vfa(i,j+1,9),1)
       end do
       call line(psep+ufa(i,npolyl+1,11),psey-vfa(i,npolyl+1,11),
     + psep+x_poly11,psey-y_poly11,3)
       do j=npolyl+1,npo-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       end do

       end if ! ic1=1

c      Subcase ic1=2 (Laser)
       if (ic1.eq.2) then

c      Points vent
c      Point left
       xu=x_poly1
       xv=y_poly1
       alp=abs(datan((vfa(i,npolyl+1,9)-vfa(i,npolyl,9)/
     + (ufa(i,npolyl+1,9)-ufa(i,npolyl,9)))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)
c      Point right
       xu=x_poly2
       xv=y_poly2
       alp=abs(datan((vfa(i,npolyr+1,10)-vfa(i,npolyr,10)/
     + (ufa(i,npolyr+1,10)-ufa(i,npolyr,10)))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)

c      Segments

       if (ic2.eq.-4) then
c      Line 14'-15'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),3)
       end if

       if (ic2.eq.-5) then
c      Line 14'-15'
       call arcfle(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),param3,1,3)
       end if

c      Corners
c      Line 14'-24' and 15-25'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,24),psey-vfa(i,1,24),3)
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Line 24'-11' and 25'-12'      
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+x_poly11,psey-y_poly11,3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+x_poly12,psey-y_poly12,3)

c      Laterals right
       call line(psep+ufa(i,npolyr+1,12),psey-vfa(i,npolyr+1,12),
     + psep+x_poly12,psey-y_poly12,3)
       do j=npolyr+1,npo-1
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Laterals left
       call line(psep+ufa(i,npolyl+1,11),psey-vfa(i,npolyl+1,11),
     + psep+x_poly11,psey-y_poly11,3)
       do j=npolyl+1,npo-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       end do


       end if ! ic1=2


       end if ! ic2=-4,-5

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw complete vent case ic2=4,5 (extrados)
c      Advanced generic vent...
c      Use vector csi(i,k) for transport additional interpolation data
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic2.eq.4.or.ic2.eq.5) then

c       write(*,*) "CCCCCCCC ",xupplenew


       if (ic2.eq.4) then
c      Length vent left
       xlenl=0.0d0
       do j=1,npo-1
       xlenl=xlenl+dsqrt((ufa(i,j,9)-ufa(i,j+1,9))**2.+
     + (vfa(i,j,9)-vfa(i,j+1,9))**2.)
       end do
       xlenlr=xlenl*(1.-csi(i+1,19)/100.)

c      Length vent rigth
       xlenr=0.0d0
       do j=1,npo-1
       xlenr=xlenr+dsqrt((ufa(i,j,10)-ufa(i,j+1,10))**2.+
     + (vfa(i,j,10)-vfa(i,j+1,10))**2.)
       end do
       xlenrr=xlenr*(1.-csi(i+1,20)/100.)
       end if

       if (ic2.eq.5) then
c      Length vent left
       xlenl=0.0d0
       do j=1,npo-1
       xlenl=xlenl+dsqrt((ufa(i,j,9)-ufa(i,j+1,9))**2.+
     + (vfa(i,j,9)-vfa(i,j+1,9))**2.)
       end do
       xlenlr=xlenl*(1.-csi(i+1,19)/100.)

c      Length vent rigth
       xlenr=0.0d0
       do j=1,npo-1
       xlenr=xlenr+dsqrt((ufa(i,j,10)-ufa(i,j+1,10))**2.+
     + (vfa(i,j,10)-vfa(i,j+1,10))**2.)
       end do
       xlenrr=xlenr*(1.-csi(i+1,20)/100.)

c      Deflection parameter (vent type 5)
       param3=(csi(i+1,18)/100.)*0.5*(xlenl+xlenr)
       end if

c      Interpolate new vent init
c      Left side
       do j=1,npo
       xpoly(j)=ufa(i,j,9)
       ypoly(j)=vfa(i,j,9)
       end do
       call interpoly2d(xpoly,ypoly,x_poly,y_poly,xlenlr,1,npo,npolyl,
     + distrel)
       x_poly1=x_poly
       y_poly1=y_poly
       distrel1=distrel
c      Right side
       do j=1,npo
       xpoly(j)=ufa(i,j,10)
       ypoly(j)=vfa(i,j,10)
       end do
       call interpoly2d(xpoly,ypoly,x_poly,y_poly,xlenrr,1,npo,npolyr,
     + distrel)
       x_poly2=x_poly
       y_poly2=y_poly
       distrel2=distrel

c      USE BRUTE FORCE!!!!!!!!!!!!!!
c       csi(i,13)=xupple

c      Points 14-15
       alpha=dabs(datan((y_poly2-y_poly1)/(x_poly2-x_poly1)))
       ufa(i,1,14)=x_poly1+xupple*0.1*dsin(alpha)
       vfa(i,1,14)=y_poly1+xupple*0.1*dcos(alpha)
       ufa(i,1,15)=x_poly2+xupple*0.1*dsin(alpha)
       vfa(i,1,15)=y_poly2+xupple*0.1*dcos(alpha)

       npoly=npolyl
       if (npolyl.eq.1) then
       npoly=2
       end if       

c      Point 24'
       xru(1)=ufa(i,npolyl+1,11)
       xrv(1)=vfa(i,npolyl+1,11)
       xru(2)=ufa(i,npolyl,11)
       xrv(2)=vfa(i,npolyl,11)
       xsu(1)=ufa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(1)=vfa(i,1,14)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,24)=xtu
       vfa(i,1,24)=xtv

c      Point 11'
       x_poly11=ufa(i,npolyl,11)+(ufa(i,npolyl+1,11)-ufa(i,npolyl,11))*
     + distrel1
       y_poly11=vfa(i,npolyl,11)+(vfa(i,npolyl+1,11)-vfa(i,npolyl,11))*
     + distrel1

c      Point 12'
       x_poly12=ufa(i,npolyr,12)+(ufa(i,npolyr+1,12)-ufa(i,npolyr,12))*
     + distrel2
       y_poly12=vfa(i,npolyr,12)+(vfa(i,npolyr+1,12)-vfa(i,npolyr,12))*
     + distrel2

       npoly=npolyr
       if (nployr.eq.1) then
       npoly=2
       end if  

c      Point 25'
       xru(1)=ufa(i,npolyr+1,12)
       xrv(1)=vfa(i,npolyr+1,12)
       xru(2)=ufa(i,npolyr,12)
       xrv(2)=vfa(i,npolyr,12)
       xsu(1)=ufa(i,1,14)
       xsu(2)=ufa(i,1,15)
       xsv(1)=vfa(i,1,14)
       xsv(2)=vfa(i,1,15)
       call xrxs(xru,xrv,xsu,xsv,xtu,xtv)
       ufa(i,1,25)=xtu
       vfa(i,1,25)=xtv

c      Subcase ic1=1 (Print)
       if (ic1.eq.1) then

c      Points vent
c      Point left
       xu=x_poly1
       xv=y_poly1
       alp=abs(datan((vfa(i,npolyl+1,9)-vfa(i,npolyl,9)/
     + (ufa(i,npolyl+1,9)-ufa(i,npolyl,9)))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call pointg(psep+xu,-xv+psey,xcir,4)
c      Point right
       xu=x_poly2
       xv=y_poly2
       alp=abs(datan((vfa(i,npolyr+1,10)-vfa(i,npolyr,10)/
     + (ufa(i,npolyr+1,10)-ufa(i,npolyr,10)))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)   
       call pointg(psep+xu,-xv+psey,xcir,4)

c      Segments
c      Line 9-10
       call line(psep+ufa(i,1,9),psey-vfa(i,1,9),psep+ufa(i,1,10),
     + psey-vfa(i,1,10),1)

       if (ic2.eq.4) then
c      Line 9'-10'
       call line(psep+x_poly1,psey-y_poly1,psep+x_poly2,psey-y_poly2,1)
c      Line 14'-15'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),3)
       end if

       if (ic2.eq.5) then
c      Line 9'-10'
       call arcfle(psep+x_poly1,psey-y_poly1,psep+x_poly2,psey-y_poly2,
     + param3,-1,1)
c      Line 14'-15'
       call arcfle(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),param3,-1,3)
       end if
     
c      Corners
c      Line 14'-24' and 15-25'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,24),psey-vfa(i,1,24),3)
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Line 24'-11' and 25'-12'      
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+x_poly11,psey-y_poly11,3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+x_poly12,psey-y_poly12,3)
c      Line 9'-11'
       call line(psep+x_poly1,psey-y_poly1,psep+x_poly11,
     + psey-y_poly11,3)
c      Line 10'-12'
       call line(psep+x_poly2,psey-y_poly2,psep+x_poly12,
     + psey-y_poly12,3)
c      Lines 9'-14' and 10'-15'
       call line(psep+x_poly1,psey-y_poly1,psep+ufa(i,1,14),
     + psey-vfa(i,1,14),3)
       call line(psep+x_poly2,psey-y_poly2,psep+ufa(i,1,15),
     + psey-vfa(i,1,15),3)

c      Laterals right
       call line(psep+ufa(i,npolyr,10),psey-vfa(i,npolyr,10),
     + psep+x_poly2,psey-y_poly2,2)
       do j=1,npolyr-1
       call line(psep+ufa(i,j,10),psey-vfa(i,j,10),psep+ufa(i,j+1,10),
     + psey-vfa(i,j+1,10),1)
       end do
       call line(psep+ufa(i,npolyr,12),psey-vfa(i,npolyr,12),
     + psep+x_poly12,psey-y_poly12,2)
       do j=1,npolyr-1
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Laterals left
       call line(psep+ufa(i,npolyl,9),psey-vfa(i,npolyl,9),
     + psep+x_poly1,psey-y_poly1,2)
       do j=1,npolyl-1
       call line(psep+ufa(i,j,9),psey-vfa(i,j,9),psep+ufa(i,j+1,9),
     + psey-vfa(i,j+1,9),1)
       end do
       call line(psep+ufa(i,npolyl,11),psey-vfa(i,npolyl,11),
     + psep+x_poly11,psey-y_poly11,2)
       do j=1,npolyl-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       end do

       end if ! ic1=1

c      Subcase ic1=2 (Laser)
       if (ic1.eq.2) then

c      Points vent
c      Point left
       xu=x_poly1
       xv=y_poly1
       alp=abs(datan((vfa(i,npolyl+1,9)-vfa(i,npolyl,9)/
     + (ufa(i,npolyl+1,9)-ufa(i,npolyl,9)))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)
c      Point right
       xu=x_poly2
       xv=y_poly2
       alp=abs(datan((vfa(i,npolyr+1,10)-vfa(i,npolyr,10)/
     + (ufa(i,npolyr+1,10)-ufa(i,npolyr,10)))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)

c      Segments
       if (ic2.eq.4) then
c      Line 14'-15'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),3)
       end if
       if (ic2.eq.5) then
c      Line 14'-15'
       call arcfle(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,15),psey-vfa(i,1,15),param3,-1,3)
       end if
     
c      Corners
c      Line 14'-24' and 15-25'
       call line(psep+ufa(i,1,14),psey-vfa(i,1,14),
     + psep+ufa(i,1,24),psey-vfa(i,1,24),3)
       call line(psep+ufa(i,1,15),psey-vfa(i,1,15),
     + psep+ufa(i,1,25),psey-vfa(i,1,25),3)
c      Line 24'-11' and 25'-12'      
       call line(psep+ufa(i,1,24),psey-vfa(i,1,24),
     + psep+x_poly11,psey-y_poly11,3)
       call line(psep+ufa(i,1,25),psey-vfa(i,1,25),
     + psep+x_poly12,psey-y_poly12,3)

c      Laterals right
       call line(psep+ufa(i,npolyr,12),psey-vfa(i,npolyr,12),
     + psep+x_poly12,psey-y_poly12,3)
       do j=1,npolyr-1
       call line(psep+ufa(i,j,12),psey-vfa(i,j,12),psep+ufa(i,j+1,12),
     + psey-vfa(i,j+1,12),3)
       end do
c      Laterals left
       call line(psep+ufa(i,npolyl,11),psey-vfa(i,npolyl,11),
     + psep+x_poly11,psey-y_poly11,3)
       do j=1,npolyl-1
       call line(psep+ufa(i,j,11),psey-vfa(i,j,11),psep+ufa(i,j+1,11),
     + psey-vfa(i,j+1,11),3)
       end do

       end if ! ic1=2

       end if ! ic2=4,5

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL WITHOUT FIRST LIMIT
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelc1(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1
c      Sobreamples esquerra

       call line(psep+uf(i,j,9),psey-vf(i,j,9),psep+uf(i,j+1,9),
     + psey-vf(i,j+1,9),1)

c      Sobreamples dreta

       call line(psep+uf(i,j,10),psey-vf(i,j,10),psep+uf(i,j+1,10),
     + psey-vf(i,j+1,10),1)

c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      Two horizontal segments 11-9, 10-12

       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,9),psey-vf(i,npo,9),3)

       call line(psep+uf(i,npo,10),psey-vf(i,npo,10),
     + psep+uf(i,npo,12),psey-vf(i,npo,12),3)

c      Two vertical segments 10-15, 9-14

       call line(psep+uf(i,npo,10),psey-vf(i,npo,10),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)
       
       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),
     + psep+uf(i,npo,14),psey-vf(i,npo,14),3)

c      Two horizontal lines 14-15

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)

c      Draw four corner segments

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,15),psey-vf(i,npo,15),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
     
       call line(psep+uf(i,npo,12),psey-vf(i,npo,12),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
       
c      Init extrados
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,10),psey-vf(i,1,10),1)

       call line(psep+uf(i,npo,9),psey-vf(i,npo,9),
     + psep+uf(i,npo,10),psey-vf(i,npo,10),1)
      
       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL WITHOUT LAST BORDER
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelc2(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1
c      Sobreamples esquerra

       call line(psep+uf(i,j,9),psey-vf(i,j,9),psep+uf(i,j+1,9),
     + psey-vf(i,j+1,9),1)

c      Sobreamples dreta

       call line(psep+uf(i,j,10),psey-vf(i,j,10),psep+uf(i,j+1,10),
     + psey-vf(i,j+1,10),1)

c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      Two horizontal segments 11-9, 10-12

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,9),psey-vf(i,1,9),3)

       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,12),psey-vf(i,1,12),3)

c      Two vertical segments 10-15, 9-14

       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)
       
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,14),psey-vf(i,1,14),3)

c      One horizontal lines 14-15

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)

c      Draw four corner segments

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,15),psey-vf(i,1,15),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
     
       call line(psep+uf(i,1,12),psey-vf(i,1,12),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)

c      Trailing edge extrados
       call line(psep+uf(i,1,9),psey-vf(i,1,9),
     + psep+uf(i,1,10),psey-vf(i,1,10),1)
                   
       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL TYPE -2  WITHOUT LAST BORDER
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelcm2(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1
c      Sobreamples esquerra

c       call line(psep+uf(i,j,9),psey-vf(i,j,9),psep+uf(i,j+1,9),
c     + psey-vf(i,j+1,9),1)

c      Sobreamples dreta

       call line(psep+uf(i,j,10),psey-vf(i,j,10),psep+uf(i,j+1,10),
     + psey-vf(i,j+1,10),1)

c      Vores de costura esquerra

c       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
c     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      Two horizontal segments 11-9, 10-12

c       call line(psep+uf(i,1,11),psey-vf(i,1,11),
c     + psep+uf(i,1,9),psey-vf(i,1,9),3)

       call line(psep+uf(i,1,10),psey-vf(i,1,10),
     + psep+uf(i,1,12),psey-vf(i,1,12),3)

c      Two vertical segments 10-15, 9-14

c       call line(psep+uf(i,1,10),psey-vf(i,1,10),
c     + psep+uf(i,1,15),psey-vf(i,1,15),3)
       
c       call line(psep+uf(i,1,9),psey-vf(i,1,9),
c     + psep+uf(i,1,14),psey-vf(i,1,14),3)

c      One horizontal lines 14-15

c       call line(psep+uf(i,1,14),psey-vf(i,1,14),
c     + psep+uf(i,1,15),psey-vf(i,1,15),3)

c      Draw four corner segments

c       call line(psep+uf(i,1,14),psey-vf(i,1,14),
c     + psep+uf(i,1,24),psey-vf(i,1,24),3)

c       call line(psep+uf(i,1,11),psey-vf(i,1,11),
c     + psep+uf(i,1,24),psey-vf(i,1,24),3)

c       call line(psep+uf(i,1,15),psey-vf(i,1,15),
c     + psep+uf(i,1,25),psey-vf(i,1,25),3)
     
c       call line(psep+uf(i,1,12),psey-vf(i,1,12),
c     + psep+uf(i,1,25),psey-vf(i,1,25),3)

c      Trailing edge extrados
c       call line(psep+uf(i,1,9),psey-vf(i,1,9),
c     + psep+uf(i,1,10),psey-vf(i,1,10),1)
                   
       return
       end





ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL TYPE -3  WITHOUT LAST BORDER
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelcm3(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1
c      Sobreamples esquerra

       call line(psep+uf(i,j,9),psey-vf(i,j,9),psep+uf(i,j+1,9),
     + psey-vf(i,j+1,9),1)

c      Sobreamples dreta

c       call line(psep+uf(i,j,10),psey-vf(i,j,10),psep+uf(i,j+1,10),
c     + psey-vf(i,j+1,10),1)

c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

c       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
c     + psey-vf(i,j+1,12),3)

       end do

c      Two horizontal segments 11-9, 10-12

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,9),psey-vf(i,1,9),3)

c       call line(psep+uf(i,1,10),psey-vf(i,1,10),
c     + psep+uf(i,1,12),psey-vf(i,1,12),3)

c      Two vertical segments 10-15, 9-14

c       call line(psep+uf(i,1,10),psey-vf(i,1,10),
c     + psep+uf(i,1,15),psey-vf(i,1,15),3)
       
c       call line(psep+uf(i,1,9),psey-vf(i,1,9),
c     + psep+uf(i,1,14),psey-vf(i,1,14),3)

c      One horizontal lines 14-15

c       call line(psep+uf(i,1,14),psey-vf(i,1,14),
c     + psep+uf(i,1,15),psey-vf(i,1,15),3)

c      Draw four corner segments

c       call line(psep+uf(i,1,14),psey-vf(i,1,14),
c     + psep+uf(i,1,24),psey-vf(i,1,24),3)

c       call line(psep+uf(i,1,11),psey-vf(i,1,11),
c     + psep+uf(i,1,24),psey-vf(i,1,24),3)

c       call line(psep+uf(i,1,15),psey-vf(i,1,15),
c     + psep+uf(i,1,25),psey-vf(i,1,25),3)
     
c       call line(psep+uf(i,1,12),psey-vf(i,1,12),
c     + psep+uf(i,1,25),psey-vf(i,1,25),3)

c      Trailing edge extrados
c       call line(psep+uf(i,1,9),psey-vf(i,1,9),
c     + psep+uf(i,1,10),psey-vf(i,1,10),1)
                   
       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL ONLY BORDERS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelb(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1

c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      Draw eight corner segments

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,15),psey-vf(i,1,15),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
     
       call line(psep+uf(i,1,12),psey-vf(i,1,12),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,15),psey-vf(i,npo,15),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
     
       call line(psep+uf(i,npo,12),psey-vf(i,npo,12),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)

c      Trailing edge extrados
       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)
       
c      Init extrados
       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)
    
       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL WITHOUT FIRST LIMIT (LASER)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelb1(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1
  
c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      Two horizontal lines 14-15

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,15),psey-vf(i,npo,15),3)

c      Draw four corner segments

       call line(psep+uf(i,npo,14),psey-vf(i,npo,14),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,11),psey-vf(i,npo,11),
     + psep+uf(i,npo,24),psey-vf(i,npo,24),3)

       call line(psep+uf(i,npo,15),psey-vf(i,npo,15),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
     
       call line(psep+uf(i,npo,12),psey-vf(i,npo,12),
     + psep+uf(i,npo,25),psey-vf(i,npo,25),3)
             
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE DRAW PANEL WITHOUT LAST BORDER (LASER)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE dpanelb2(i,uf,vf,npo,psep,psey)

       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey

       do j=1,npo-1

c      Vores de costura esquerra

       call line(psep+uf(i,j,11),psey-vf(i,j,11),psep+uf(i,j+1,11),
     + psey-vf(i,j+1,11),3)

c      Vores de costura dreta

       call line(psep+uf(i,j,12),psey-vf(i,j,12),psep+uf(i,j+1,12),
     + psey-vf(i,j+1,12),3)

       end do

c      One horizontal lines 14-15

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,15),psey-vf(i,1,15),3)

c      Draw four corner segments

       call line(psep+uf(i,1,14),psey-vf(i,1,14),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,11),psey-vf(i,1,11),
     + psep+uf(i,1,24),psey-vf(i,1,24),3)

       call line(psep+uf(i,1,15),psey-vf(i,1,15),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
     
       call line(psep+uf(i,1,12),psey-vf(i,1,12),
     + psep+uf(i,1,25),psey-vf(i,1,25),3)
                   
       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE JONCS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE joncs(i,u,v,rib,xintra,xextra,xjonc,npo,atp,np)

       real*8 u(0:100,500,99),v(0:100,500,99)
       real*8 xextra(0:100,10),xintra(0:100,10)
       real*8 xjonc(0:100,500,10),k1,k2
       real*8 x1i,x1f,x2i,x2f
       real*8 x1pi,x1pf,x2pi,x2pf
       real*8 x1,x2,x3,x4,y1,y2,y3,y4
       real*8 rib(0:100,500)
       integer np(0:100,9)
       character*2 atp

       ng=int(rib(i,166))

       if (ng.ne.0) then ! Only if rod is defined

c      Read airfoil i and detect transition segments

c      Set provisional virtual point 3 "ss"
       if (atp.eq."ss".and.xintra(ng,2).gt.rib(i,12)) then 
       
       j=np(i,2)+np(i,3)-1

       x4=u(i,j+1,3) ! safe vector
       y4=v(i,j+1,3) ! safe vector

       x1=u(i,j-1,3)
       y1=v(i,j-1,3)
       x2=u(i,j,3)
       y2=v(i,j,3)
       x3=xintra(ng,2)*rib(i,5)/100.0d0
      
       call interpola(x1,y1,x2,y2,x3,y3)
  
       u(i,j+1,3)=x3 ! modification
       v(i,j+1,3)=y3 ! modification      
       end if

c      Set initial and final points
       x1f=xextra(ng,2)*rib(i,5)/100.0d0
       x1i=xextra(ng,1)*rib(i,5)/100.0d0
       x2f=xintra(ng,2)*rib(i,5)/100.0d0
       x2i=xintra(ng,1)*rib(i,5)/100.0d0

c      Set points to explore
       if (atp.eq."ss") then 
       npunts=np(i,2)+np(i,3)-1
       end if
       if (atp.ne."ss") then 
       npunts=np(i,1)-1
       end if

       do j=1,npunts! Explore airfoil

c       do j=1,np(i,2)+np(i,3)-1

c      Final point extrados
       if (u(i,j,3).ge.x1f.and.u(i,j+1,3).lt.x1f.and.v(i,j,3).ge.0) 
     + then 
       j1f=j
       x1=u(i,j+1,3)
       y1=v(i,j+1,3)
       x2=u(i,j,3)
       y2=v(i,j,3)
       x3=x1f
       call interpola(x1,y1,x2,y2,x3,y3)
       x1pf=x3
       y1pf=y3
       end if

c      Initial point extrados
       if (u(i,j,3).ge.x1i.and.u(i,j+1,3).lt.x1i.and.v(i,j,3).ge.0) 
     + then 
       j1i=j
       x1=u(i,j+1,3)
       y1=v(i,j+1,3)
       x2=u(i,j,3)
       y2=v(i,j,3)
       x3=x1i
       call interpola(x1,y1,x2,y2,x3,y3)
       x1pi=x3
       y1pi=y3
       end if

       np1=j1i-j1f+2

c      Initial point intrados
       if (u(i,j,3).le.x2i.and.u(i,j+1,3).gt.x2i.and.v(i,j,3).lt.0) 
     + then 
       j2i=j
       x1=u(i,j,3)
       y1=v(i,j,3)
       x2=u(i,j+1,3)
       y2=v(i,j+1,3)
       x3=x2i
       call interpola(x1,y1,x2,y2,x3,y3)
       x2pi=x3
       y2pi=y3
       end if

c      Final point intrados
c      Warning amb el ge.x2f 
       if (u(i,j,3).le.x2f.and.u(i,j+1,3).ge.x2f.and.v(i,j,3).lt.0) 
     + then 
       j2f=j
       x1=u(i,j,3)
       y1=v(i,j,3)
       x2=u(i,j+1,3)
       y2=v(i,j+1,3)
       x3=x2f
       call interpola(x1,y1,x2,y2,x3,y3)
       x2pf=x3
       y2pf=y3
       end if

       np2=j1f-j1i+2

       end do   ! j in airfoil  

c      Define jonc line 0 (without deflection)
       
c      Extrados segment
       xjonc(i,j1f,1)=x1pf
       xjonc(i,j1f,2)=y1pf
       do j=j1f+1,j1i
       xjonc(i,j,1)=u(i,j,3)
       xjonc(i,j,2)=v(i,j,3)
       end do

c      Nose segment
       xjonc(i,j1i+1,1)=x1pi
       xjonc(i,j1i+1,2)=y1pi
       do j=j1i+1,j2i
       xjonc(i,j+1,1)=u(i,j,3)
       xjonc(i,j+1,2)=v(i,j,3)
       end do

c      Intrados segment
       xjonc(i,j2i+2,1)=x2pi
       xjonc(i,j2i+2,2)=y2pi
       do j=j2i+1,j2f
       xjonc(i,j+2,1)=u(i,j,3)
       xjonc(i,j+2,2)=v(i,j,3)
       end do
       xjonc(i,j2f+3,1)=x2pf
       xjonc(i,j2f+3,2)=y2pf

       npo=j2f-j1f+4

c      Add jonc deflections
       k1=(xextra(ng,3)*rib(i,5)/100.0d0)/((x1f-x1i)**xextra(ng,4))
       k2=(xintra(ng,3)*rib(i,5)/100.0d0)/((x2f-x2i)**xintra(ng,4))

       do j=j1i+1,j1f,-1
       xjonc(i,j,2)=xjonc(i,j,2)-k1*((xjonc(i,j,1))-x1i)**xextra(ng,4)
       end do

       do j=j2i+2,j2f+3
       xjonc(i,j,2)=xjonc(i,j,2)+k2*((xjonc(i,j,1))-x2i)**xintra(ng,4)
       end do

c      Reformat jonc
       do j=1,npo
       xjonc(i,j,3)=xjonc(i,j+j1f-1,1)
       xjonc(i,j,4)=xjonc(i,j+j1f-1,2)
       end do

c      Reformat jonc again (change name)
       do j=1,npo
       xjonc(i,j,1)=xjonc(i,j,3)
       xjonc(i,j,2)=xjonc(i,j,4)
       end do

c      Restitution of virtual point 3
       if (atp.eq."ss".and.xintra(ng,2).gt.rib(i,12)) then 
       j=np(i,2)+np(i,3)-1
       u(i,j+1,3)=x4
       v(i,j+1,3)=y4
       end if
  
       end if ! ng.ne.0

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE JONCS2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE joncs2(i,u,v,rib,x21,xjonc,nparc,atp,np,m,ng)

       real*8 u(0:100,500,99),v(0:100,500,99)
       real*8 x21(20,100,20)
       real*8 xjonc(0:100,500,10),k1,k2
       real*8 x1i,x1f,x2i,x2f
       real*8 x1pi,x1pf,x2pi,x2pf
       real*8 x0,y0,x1,x2,x3,x4,y1,y2,y3,y4
       real*8 b,c,d,f,g,xp231,xp221,xp012,xp013
       real*8 dx,dy,alpha,radi,pi,xsign,xsign2
       real*8 rib(0:100,500)
       integer np(0:100,9)
       character*2 atp

       dx=(x21(m,ng,3)-x21(m,ng,1))/dfloat(nparc-1)
       dy=(x21(m,ng,4)-x21(m,ng,2))/dfloat(nparc-1)
       pi=4.0d0*datan(1.0d0)
       
c      Define straight rod
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (dabs(x21(m,ng,5)).lt.0.01) then
       do j=1,nparc
       xjonc(i,j,1)=(x21(m,ng,1)+dx*dfloat(j-1))*rib(i,5)/100.0d0
       xjonc(i,j,2)=(x21(m,ng,2)+dy*dfloat(j-1))*rib(i,5)/100.0d0
       end do
       rib(i,167)=(rib(i,5)/100.0)*dsqrt((x21(m,ng,3)-x21(m,ng,1))**2.+
     + (x21(m,ng,4)-x21(m,ng,2))**2.)
       end if

c      Define an arc jonc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (dabs(x21(m,ng,5)).ge.0.01) then

c      Control signs
       if (x21(m,ng,5).gt.0.01) then
       xsign=1.0d0
       end if
       if (x21(m,ng,5).le.-0.01) then
       xsign=-1.0d0
       end if
       if (x21(m,ng,2).gt.x21(m,ng,4)) then
       xsign2=1.0d0
       end if
       if (x21(m,ng,2).lt.x21(m,ng,4)) then
       xsign2=-1.0d0
       end if
       if (x21(m,ng,2).gt.x21(m,ng,4).and.x21(m,ng,3).gt.x21(m,ng,1)) 
     + then
       xsign3=-1.0d0
       end if
       if (x21(m,ng,2).gt.x21(m,ng,4).and.x21(m,ng,3).lt.x21(m,ng,1))
     + then
       xsign3=1.0d0
       end if

c      Segment 1-4-2
       x1=x21(m,ng,1)
       y1=x21(m,ng,2)
       x2=x21(m,ng,3)
       y2=x21(m,ng,4)
       x4=(x1+x2)*0.5
       y4=(y1+y2)*0.5

c      Point 3 
c       x3=x4-dabs(x21(m,ng,5))*dsin(alpha)
c       y3=y4+dabs(x21(m,ng,5))*dcos(alpha)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case segmentation in y axis
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (dabs(y2-y1).gt.dabs(x2-x1)) then

       alpha=datan((y2-y1)/(x2-x1))

       if (x1.eq.x2.and.y2.gt.y1) then
       alpha=-pi/2.0d0
       end if

       if (x1.eq.x2.and.y2.lt.y1) then
       alpha=pi/2.0d0
       end if

c      Circle by tree points, geometric method
       d=0.5d0*dsqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
       f=dabs(x21(m,ng,5))
       radi=(f*f+d*d)/(2.0d0*f)
       g=radi-f
       x0=x4+xsign*g*dsin(alpha)
       y0=y4-xsign*g*dcos(alpha)

       do j=1,nparc
       xjonc(i,j,2)=(x21(m,ng,2)+dy*dfloat(j-1))
       b=-2.*x0
       c=x0*x0+xjonc(i,j,2)*xjonc(i,j,2)-2*xjonc(i,j,2)*y0+y0*y0-
     + radi*radi
       xjonc(i,j,1)=(-b-xsign*xsign2*xsign3*dsqrt(b*b-4.*c))/2.0d0
       end do

       end if ! case y-axis

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case segmentation in x axis
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (dabs(y2-y1).le.dabs(x2-x1)) then

       alpha=datan((y2-y1)/(x2-x1))

c      Circle by tree points, geometric method
       d=0.5d0*dsqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
       f=dabs(x21(m,ng,5))
       radi=(f*f+d*d)/(2.0d0*f)
       g=radi-f
       x0=x4+xsign*g*dsin(alpha)
       y0=y4-xsign*g*dcos(alpha)

       do j=1,nparc
       xjonc(i,j,1)=(x21(m,ng,1)+dx*dfloat(j-1))
       b=-2.*y0
       c=x0*x0+xjonc(i,j,1)*xjonc(i,j,1)-2*xjonc(i,j,1)*x0+y0*y0-
     + radi*radi
       xjonc(i,j,2)=(-b+xsign*dsqrt(b*b-4.*c))/2.0d0
       end do

       end if ! case x-axis

c      Set to scale
       do j=1,nparc
       xjonc(i,j,1)=xjonc(i,j,1)*rib(i,5)/100.0d0
       xjonc(i,j,2)=xjonc(i,j,2)*rib(i,5)/100.0d0
       end do

       end if ! case circle

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINEAL INTERPOLATION
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE interpola(x1,y1,x2,y2,x3,y3)

       real*8 x1,y1,x2,y2,x3,y3,xm,xb

       xm=(y2-y1)/(x2-x1)
       xb=y2-xm*x2
       y3=xm*x3+xb

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINEAL INTERPOLATION AT DISTANCE D
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE interpd(x1,y1,x2,y2,x3,y3,xd)

       real*8 x1,y1,x2,y2,x3,y3
       real*8 xd,xdx,xdy,xd13,yd13,xdi

       xdx=x2-x1
       xdy=y2-y1
       xdi=dsqrt((x2-x1)**2.0d0+(y2-y1)**2.0d0)

       if (xdi.ne.0.0d0) then
       xd13=xdx*xd/xdi
       yd13=xdy*xd/xdi
       x3=x1+xd13
       y3=y1+yd13
       else
       x3=x1
       y3=y1
       end if

c       write (*,*) i,xd,xdi,x3,y3

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE PRINT JONCS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE pjoncs(i,xjonc,npo,sjo,sepx,sepy,rib,xkf)

       real*8 xjonc(0:100,500,10),sjo(0:100,10),sepx,sepy
       real*8 rib(0:100,500),joini(0:100,10),jofin(0:100,10)
       real*8 uo(500,2),vo(500,2)
       real*8 xo,x1,x2,x3,x4,y1,y2,y3,y4,xkf,xad4,xad7

       integer typm1(50),typm4(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50),xcir,alpha
       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

       xcir=0.1d0*typm2(1)
       xad4=2530.0d0*xkf
       xad7=1260.0d0*5.0d0*xkf

       ng=rib(i,166)

c      Jonc length
       rib(i,167)=0.0d0
       do j=1,npo-1
       rib(i,167)=rib(i,167)+sqrt(((xjonc(i,j+1,1)-xjonc(i,j,1))**2)+
     + ((xjonc(i,j+1,2)-xjonc(i,j,2))**2))
       end do
       
c      Load jonc base line
       do j=1,npo+1
       uo(j,1)=xjonc(i,j,1)
       vo(j,1)=xjonc(i,j,2)
       end do

c      Print line 1 (jonc)
       xo=-sjo(ng,1)
       call loffset(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),
     + sepx+uo(j+1,2),sepy-vo(j+1,2),150)
       end do

c      Print init and final point
       call point(sepx+uo(1,2),sepy-vo(1,2),160)
       call point(sepx+uo(j,2),sepy-vo(j,2),160)
       call point(2530.*xkf+sepx+uo(1,2),sepy-vo(1,2),160)
       call point(2530.*xkf+sepx+uo(j,2),sepy-vo(j,2),160)


       x1=uo(1,2)
       y1=vo(1,2)
       x4=uo(npo,2)
       y4=vo(npo,2)

c      Print line 2 (jonc)
       xo=-(sjo(ng,1)+sjo(ng,3))
       call loffset(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),
     + sepx+uo(j+1,2),sepy-vo(j+1,2),150)
       end do

c      Print init and final point
       call point(sepx+uo(1,2),sepy-vo(1,2),160)
       call point(sepx+uo(j,2),sepy-vo(j,2),160)
       call point(2530.*xkf+sepx+uo(1,2),sepy-vo(1,2),160)
       call point(2530.*xkf+sepx+uo(j,2),sepy-vo(j,2),160)

       x2=uo(1,2)
       y2=vo(1,2)
       x3=uo(npo,2)
       y3=vo(npo,2)

c      Joncs points ini and fin
       joini(i,1)=0.5d0*(x1+x2)
       joini(i,2)=0.5d0*(y1+y2)
       jofin(i,1)=0.5d0*(x3+x4)
       jofin(i,2)=0.5d0*(y3+y4)

c      Print line 3
       xo=sjo(ng,2)-sjo(ng,1)
       call loffset(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),      ! BOX(1,2)
     + sepx+uo(j+1,2),sepy-vo(j+1,2),30)
       call line(sepx+uo(j,2)+xad7,sepy-vo(j,2), ! BOX(1,7)
     + sepx+uo(j+1,2)+xad7,sepy-vo(j+1,2),30)
       end do

       x1=uo(1,2)
       y1=vo(1,2)
       x4=uo(npo,2)
       y4=vo(npo,2)

c      Print line 4
       xo=-(sjo(ng,1)+sjo(ng,3)+sjo(ng,4))
       call loffset(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),      ! BOX(1,2)
     + sepx+uo(j+1,2),sepy-vo(j+1,2),30)
       call line(sepx+uo(j,2)+xad7,sepy-vo(j,2), ! BOX(1,7)
     + sepx+uo(j+1,2)+xad7,sepy-vo(j+1,2),30)

       end do

       x2=uo(1,2)
       y2=vo(1,2)
       x3=uo(npo,2)
       y3=vo(npo,2)

c      BOX(1,2)
       call line(sepx+x1,sepy-y1,sepx+x2,sepy-y2,30)
       call line(sepx+x3,sepy-y3,sepx+x4,sepy-y4,30)

c      Print points jonc ini and fin BOX(1,2)
c       call pointg(sepx+joini(i,1),sepy-joini(i,2),xcir,150)
c       call pointg(sepx+jofin(i,1),sepy-jofin(i,2),xcir,150)

c      Laser cuting BOX(1,4)
c       call point(sepx+joini(i,1)+xad4,sepy-joini(i,2),150)
c       call point(sepx+jofin(i,1)+xad4,sepy-jofin(i,2),150)

c      BOX(1,7)
       call line(sepx+x1+xad7,sepy-y1,sepx+x2+xad7,sepy-y2,30)
       call line(sepx+x3+xad7,sepy-y3,sepx+x4+xad7,sepy-y4,30)


c      Romano number in jonc BOX(1,7)
       if (typm5(9).gt.0.01d0) then
       ijo=dint(dfloat(npo)*0.25d0)
       alpha=datan((xjonc(i,ijo,2)-xjonc(i,ijo-1,2))/
     + (xjonc(i,ijo,1)-xjonc(i,ijo-1,1)))
       call romano(i,sepx+xad7+xjonc(i,ijo,1),sepy-xjonc(i,ijo,2),
     + alpha,typm5(9)*0.1,30)
       end if

       return
       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE PRINT JONCS2
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE pjoncs2(i,xjonc,nparc,sjo,sepx,sepy,rib,xkf)

       real*8 xjonc(0:100,500,10),sjo(0:100,10),sepx,sepy
       real*8 rib(0:100,500),joini(0:100,10),jofin(0:100,10)
       real*8 uo(500,2),vo(500,2)
       real*8 xo,x1,x2,x3,x4,y1,y2,y3,y4,xkf,xad4,xad7,alpha

       integer typm1(50),typm4(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50),xcir
       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

       xcir=0.1d0*typm2(1)
       xad4=2530.0d0*xkf
       xad7=1260.0d0*5.0d0*xkf

       ng=rib(i,166)
       npo=nparc

c      Jonc length
       rib(i,167)=0.0d0
       do j=1,npo-1
       rib(i,167)=rib(i,167)+sqrt(((xjonc(i,j+1,1)-xjonc(i,j,1))**2)+
     + ((xjonc(i,j+1,2)-xjonc(i,j,2))**2))
       end do
       
c      Load jonc base line
       do j=1,npo+1
       uo(j,1)=xjonc(i,j,1)
       vo(j,1)=xjonc(i,j,2)
       end do
c      Print line 1
       xo=-sjo(ng,3)/2.0d0
       call loffset2(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),
     + sepx+uo(j+1,2),sepy-vo(j+1,2),150)
       end do

c      Print init and final point
       call point(sepx+uo(1,2),sepy-vo(1,2),160)
       call point(sepx+uo(j,2),sepy-vo(j,2),160)
       call point(2530.*xkf+sepx+uo(1,2),sepy-vo(1,2),160)
       call point(2530.*xkf+sepx+uo(j,2),sepy-vo(j,2),160)

c      Load jonc base line
       do j=1,npo+1
       uo(j,1)=xjonc(i,j,1)
       vo(j,1)=xjonc(i,j,2)
       end do
c      Print line 2
       xo=sjo(ng,3)/2.0d0
       call loffset2(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),   ! BOX(1,2)
     + sepx+uo(j+1,2),sepy-vo(j+1,2),150)
       end do

c      Print init and final point
       call point(sepx+uo(1,2),sepy-vo(1,2),160)
       call point(sepx+uo(j,2),sepy-vo(j,2),160)
       call point(2530.*xkf+sepx+uo(1,2),sepy-vo(1,2),160)
       call point(2530.*xkf+sepx+uo(j,2),sepy-vo(j,2),160)

c      Load jonc base line
       do j=1,npo+1
       uo(j,1)=xjonc(i,j,1)
       vo(j,1)=xjonc(i,j,2)
       end do
c      Print line 3
       xo=-sjo(ng,3)/2.0d0-sjo(ng,2)
       call loffset2(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),      ! BOX(1,2)
     + sepx+uo(j+1,2),sepy-vo(j+1,2),30)
       call line(sepx+uo(j,2)+xad7,sepy-vo(j,2), ! BOX(1,7)
     + sepx+uo(j+1,2)+xad7,sepy-vo(j+1,2),10)
       end do

       x1=uo(1,2)
       y1=vo(1,2)
       x4=uo(npo,2)
       y4=vo(npo,2)

c      Load jonc base line
       do j=1,npo+1
       uo(j,1)=xjonc(i,j,1)
       vo(j,1)=xjonc(i,j,2)
       end do
c      Print line 4
       xo=sjo(ng,3)/2.0d0+sjo(ng,4)
       call loffset2(uo,vo,npo,xo)
       do j=1,npo-1
       call line(sepx+uo(j,2),sepy-vo(j,2),      ! BOX(1,2)
     + sepx+uo(j+1,2),sepy-vo(j+1,2),30)
       call line(sepx+uo(j,2)+xad7,sepy-vo(j,2), ! BOX(1,7)
     + sepx+uo(j+1,2)+xad7,sepy-vo(j+1,2),10)
       end do

       x2=uo(1,2)
       y2=vo(1,2)
       x3=uo(npo,2)
       y3=vo(npo,2)

c      Print end and final segments
       call line(sepx+x1,sepy-y1,      ! BOX(1,2)
     + sepx+x2,sepy-y2,30)
       call line(sepx+x1+xad7,sepy-y1, ! BOX(1,7)
     + sepx+x2+xad7,sepy-y2,10)
       call line(sepx+x3,sepy-y3,      ! BOX(1,2)
     + sepx+x4,sepy-y4,30)
       call line(sepx+x3+xad7,sepy-y3, ! BOX(1,7)
     + sepx+x4+xad7,sepy-y4,10)

c      Joncs points ini and fin
       joini(i,1)=0.5d0*(x1+x2)
       joini(i,2)=0.5d0*(y1+y2)
       jofin(i,1)=0.5d0*(x3+x4)
       jofin(i,2)=0.5d0*(y3+y4)

c      Print points jonc ini and fin BOX(1,2)
c       call pointg(sepx+joini(i,1),sepy-joini(i,2),xcir,150)
c       call pointg(sepx+jofin(i,1),sepy-jofin(i,2),xcir,150)

c      Laser cuting BOX(1,4)
c       call point(sepx+joini(i,1)+xad4,sepy-joini(i,2),150)
c       call point(sepx+jofin(i,1)+xad4,sepy-jofin(i,2),150)

c      Print romano points BOX(1,7) -exp-
c       call romanop(i,1,sepx+uo(1,1)+xad7,sepy-vo(1,1), ! BOX(1,7)
c     + sepx+uo(npo,1)+xad7,sepy-vo(npo,1),0,0,0,xkf)


c      Romano number in jonc BOX(1,7)
       if (typm5(9).gt.0.01d0) then
       ijo=dint(dfloat(npo)*0.25d0)
       alpha=datan((xjonc(i,ijo,2)-xjonc(i,ijo-1,2))/
     + (xjonc(i,ijo,1)-xjonc(i,ijo-1,1)))
       call romano(i,sepx+xad7+xjonc(i,ijo,1),sepy-xjonc(i,ijo,2),
     + alpha,typm5(9)*0.1,10)
       end if

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINE OFFSET
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE loffset(uo,vo,npo,xo)

       real*8 uo(500,2),vo(500,2)
       real*8 xo,alpha1,alpha2,alpha

       do j=1,npo

c      Angle alpha
       if (j.eq.1) then
       alpha=(datan((vo(j+1,1)-vo(j,1))/
     + (uo(j+1,1)-uo(j,1))))
       end if
       if (j.ge.2.and.j.lt.npo) then
       alpha1=(datan((vo(j+1,1)-vo(j,1))/
     + (uo(j+1,1)-uo(j,1))))
       alpha2=(datan((vo(j,1)-vo(j-1,1))/
     + (uo(j,1)-uo(j-1,1))))
       alpha=0.5*(alpha1+alpha2)
       end if
       if (j.eq.npo) then
       alpha=(datan((vo(j,1)-vo(j-2,1))/
     + (uo(j,1)-uo(j-2,1))))
       end if

c      OFFSET OTION 1 IS OK
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Offset points

       if(vo(j,1).ge.0.0d0) then
       uo(j,2)=uo(j,1)-xo*0.1d0*dsin(alpha)
       vo(j,2)=vo(j,1)+xo*0.1d0*dcos(alpha)
       end if

       if(vo(j,1).ge.0.0d0.and.uo(j,1).gt.uo(j-1,1).and.j.gt.1) then
       uo(j,2)=uo(j,1)+xo*0.1d0*dsin(alpha)
       vo(j,2)=vo(j,1)-xo*0.1d0*dcos(alpha)
       end if

       if(vo(j,1).lt.0.0d0) then
       uo(j,2)=uo(j,1)+xo*0.1d0*dsin(alpha)
       vo(j,2)=vo(j,1)-xo*0.1d0*dcos(alpha)
       end if

       if(uo(j,1).eq.0.0d0) then
       uo(j,2)=uo(j,1)-xo*0.1d0
       vo(j,2)=vo(j,1)
       end if
c       OPTION 1

c      OFFSET  OTION 2 IS IN TEST
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c       if(uo(j,1).gt.uo(j+1,1).or.uo(j,1).eq.0.0d0) then
c       uo(j,2)=uo(j,1)+xo*0.1d0*dsin(alpha)
c       vo(j,2)=vo(j,1)-xo*0.1d0*dcos(alpha)
c       end if

c       if(uo(j,1).lt.uo(j+1,1)) then
c       uo(j,2)=uo(j,1)-xo*0.1d0*dsin(alpha)
c       vo(j,2)=vo(j,1)+xo*0.1d0*dcos(alpha)
c       end if

c       if(uo(j,npo).lt.uo(npo-1,1)) then
c       uo(npo,2)=uo(npo,1)-xo*0.1d0*dsin(alpha)
c       vo(npo,2)=vo(npo,1)+xo*0.1d0*dcos(alpha)
c       end if
c      OPTION 2 TEST

c       if (j.eq.24) then
c       write (*,*) "SUP", j,uo(j,2),uo(j,1),vo(j,2),vo(j,1),alpha
c       end if

       end do ! j

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE LINE OFFSET2
c      Another version
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE loffset2(uo,vo,npo,xo)

       real*8 uo(500,2),vo(500,2)
       real*8 xo,alpha1,alpha2,alpha,alphaa,xsign
      
       xsign=-1.0d0
       pi=4.0d0*datan(1.0d0)

       do j=1,npo

c      Angle alpha definition and corrections
       if (j.eq.1) then
       alpha=(datan((vo(j+1,1)-vo(j,1))/
     + (uo(j+1,1)-uo(j,1))))
       end if
       if (j.ge.2.and.j.lt.npo) then
       alpha=(datan((vo(j+1,1)-vo(j,1))/
     + (uo(j+1,1)-uo(j,1))))
       end if
       if (j.eq.npo) then
       alpha=(datan((vo(j,1)-vo(j-1,1))/
     + (uo(j,1)-uo(j-1,1))))
       end if
c      Correction when x increasing       
       if (uo(j+1,1).ge.uo(j,1).and.j.lt.npo) then
       alpha=alpha-pi
       end if
       if (uo(j,1).ge.uo(j-1,1).and.j.eq.npo) then
       alpha=alpha-pi
       end if

c      Definition of displaced points
       uo(j,2)=uo(j,1)+xo*xsign*0.1d0*dsin(alpha)
       vo(j,2)=vo(j,1)-xo*xsign*0.1d0*dcos(alpha)
       
c       write (*,*) j," fi ",alpha,(uo(j+1,1)-uo(j,1))*1000.,
c     + uo(j,2),vo(j,2)

       end do

       return

       end




ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE PUNTS LATERALS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE puntslat(i,pulat1x,pulat1y,pulat2x,pulat2y,npulati,
     + npulatf,latu,latv,xupp,latsgn)

       real*8 pulat1x(0:100,500),pulat1y(0:100,500),pulat2x(0:100,500),
     + pulat2y(0:100,500)
       real*8 latu(0:100,500,99),latv(0:100,500,99),xdu,xdv
       real*8 siu(0:500),siv(0:500),alplat,xupp
       integer npulati,npulatf,npulatflatsgn

c      Calcula punts esquerra (-1)

       if (latsgn.eq.-1) then

       do j=npulati,npulatf

       xdv=(pulat2y(i,j)-pulat1y(i,j))
       xdu=(pulat2x(i,j)-pulat1x(i,j))

       if (xdv.ne.0.) then
       alplat=abs(datan((pulat2y(i,j)-pulat1y(i,j))/(pulat2x(i,j)-
     + pulat1x(i,j))))
       else
       alplat=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 2-I
       siu(j)=-1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 2-II
       siu(j)=-1.
       siv(j)=-1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 2-III
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 2-IV
       siu(j)=1.
       siv(j)=-1.
       end if

       latu(i,j+1,9)=pulat2x(i,j)+siu(j)*latv(i,j+1,7)*dsin(alplat)
       latv(i,j+1,9)=pulat2y(i,j)+siv(j)*latv(i,j+1,7)*dcos(alplat)

       latu(i,j+1,11)=latu(i,j+1,9)+siu(j)*xupp*0.1*dsin(alplat)
       latv(i,j+1,11)=latv(i,j+1,9)+siv(j)*xupp*0.1*dcos(alplat)

c      Set central panel
       if (i.eq.1) then
      


       end if

c      Impresió de control
c       if (j.eq.10) then
c       write (*,*) "BBB ",i,latu(i,j+1,9),latv(i,j+1,9)
c       end if

       end do ! j

c      Punt inicial

       j=npulati
       
       alplat=abs(datan((pulat2y(i,j)-pulat1y(i,j))/
     + (pulat2x(i,j)-pulat1x(i,j))))

c      Potser hauria de ser pl1x i pl1y???? Yes
       latu(i,j,9)=pulat1x(i,j)+siu(j)*latv(i,j,7)*dsin(alplat)
       latv(i,j,9)=pulat1y(i,j)+siv(j)*latv(i,j,7)*dcos(alplat)

       latu(i,j,11)=latu(i,j,9)+siu(j)*xupp*0.1*dsin(alplat)
       latv(i,j,11)=latv(i,j,9)+siv(j)*xupp*0.1*dcos(alplat)

       end if ! Punts esquerra (-1)


c      Calcula punts dreta (1)

       if (latsgn.eq.1) then

       do j=npulati,npulatf

       xdv=(pulat2y(i,j)-pulat1y(i,j))
       xdu=(pulat2x(i,j)-pulat1x(i,j))

       if (xdv.ne.0.) then
       alplat=abs(datan((pulat2y(i,j)-pulat1y(i,j))/(pulat2x(i,j)-
     + pulat1x(i,j))))
       else
       alplat=2.*datan(1.0d0)
       end if

       if (xdu.ge.0.and.xdv.ge.0) then ! case 3-I
       siu(j)=1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.ge.0) then ! case 3-II
       siu(j)=1.
       siv(j)=1.
       end if
       if (xdu.ge.0.and.xdv.le.0) then ! case 3-III
       siu(j)=-1.
       siv(j)=-1.
       end if
       if (xdu.le.0.and.xdv.le.0) then ! case 3-IV
       siu(j)=-1.
       siv(j)=1.
       end if

       latu(i,j+1,10)=pulat2x(i,j)+siu(j)*latv(i,j+1,8)*dsin(alplat)
       latv(i,j+1,10)=pulat2y(i,j)+siv(j)*latv(i,j+1,8)*dcos(alplat)

       latu(i,j+1,12)=latu(i,j+1,10)+siu(j)*xupp*0.1*dsin(alplat)
       latv(i,j+1,12)=latv(i,j+1,10)+siv(j)*xupp*0.1*dcos(alplat)

c      Impresió de control
c       if (j.eq.10) then
c       write (*,*) "BBB ",i,latu(i,j+1,9),latv(i,j+1,9)
c       end if

       end do ! j

c      Punt inicial

       j=npulati
       
       alplat=abs(datan((pulat2y(i,j)-pulat1y(i,j))/(pulat2x(i,j)-
     + pulat1x(i,j))))

       latu(i,j,10)=pulat1x(i,j)+siu(j)*latv(i,j,8)*dsin(alplat)
       latv(i,j,10)=pulat1y(i,j)+siv(j)*latv(i,j,8)*dcos(alplat)

       latu(i,j,12)=latu(i,j,10)+siu(j)*xupp*0.1*dsin(alplat)
       latv(i,j,12)=latv(i,j,10)+siv(j)*xupp*0.1*dcos(alplat)

       end if ! Punts dreta (1)


       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE MYLARS
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE mylars(i,u,v,sepx,sepy,rib,xmy,np,xkf,atp)

       real*8 u(0:100,500,99),v(0:100,500,99),sepx,sepy
       real*8 rib(0:100,500),xmy(0:100,10)
       real*8 mx(20),my(20)
       real*8 x1,x2,x3,y1,y2,y3,xad4,xad7,xkf,alpha,xd
       integer np(0:100,9)
       character*2 atp

       xad7=(1260.*5.+80.)*xkf
       xad4=2530.*xkf
       ng=int(rib(i,168))
       jvi=np(i,2)           ! vent in
       jvo=np(i,2)+np(i,3)-1 ! vent out

       if (ng.ne.0) then ! Only if mylar is defined

c      Read airfoil and detect initial and final points

c      Initial i final points x-ccordinate
       mx(1)=xmy(ng,1)*rib(i,5)/100.
       mx(8)=xmy(ng,4)*rib(i,5)/100.

       do j=1,np(i,1)-1! Explore airfoil

c      Initial point

       if (u(i,j,3).ge.mx(1).and.u(i,j+1,3).lt.mx(1).and.v(i,j,3).ge.0) 
     + then 

       jini=j

       x1=u(i,j+1,3)
       y1=v(i,j+1,3)
       x2=u(i,j,3)
       y2=v(i,j,3)
       x3=mx(1)
       call interpola(x1,y1,x2,y2,x3,y3)
       my(1)=y3
       end if

c      Final point

       if (u(i,j,3).le.mx(8).and.u(i,j+1,3).gt.mx(8).and.j.ge.np(i,2)) 
     + then 

       jfin=j

       x1=u(i,j+1,3)
       y1=v(i,j+1,3)
       x2=u(i,j,3)
       y2=v(i,j,3)
       x3=mx(8)
       call interpola(x1,y1,x2,y2,x3,y3)
       my(8)=y3
       end if

       end do

c      Compute others points

       mx(3)=mx(1)+xmy(ng,2)*rib(i,5)/100.0d0
       my(3)=my(1)
       mx(6)=mx(8)
       my(6)=my(8)+xmy(ng,5)*rib(i,5)/100.0d0

c      Airfoil contour

c      Case not "pc"
       if (atp.ne."pc") then
       call line(sepx+mx(1)+xad7,sepy-my(1),
     + sepx+u(i,jini+1,3)+xad7,sepy-v(i,jini+1,3),10)
       do j=jini+1,jfin-1
       call line(sepx+u(i,j,3)+xad7,sepy-v(i,j,3),
     + sepx+u(i,j+1,3)+xad7,sepy-v(i,j+1,3),10)
       end do  
       call line(sepx+mx(8)+xad7,sepy-my(8),
     + sepx+u(i,jfin,3)+xad7,sepy-v(i,jfin,3),10)
       end if 

c      Case "pc"

       if (atp.eq."pc") then
       call line(sepx+mx(1)+xad7,sepy-my(1),
     + sepx+u(i,jini+1,3)+xad7,sepy-v(i,jini+1,3),10)
       do j=jini+1,jvi-1
       call line(sepx+u(i,j,3)+xad7,sepy-v(i,j,3),
     + sepx+u(i,j+1,3)+xad7,sepy-v(i,j+1,3),10)
       end do  
       call line(sepx+u(i,jvi,3)+xad7,sepy-v(i,jvi,3),
     + sepx+u(i,jvo,3)+xad7,sepy-v(i,jvo,3),3)  
       do j=jvo,jfin-1
       call line(sepx+u(i,j,3)+xad7,sepy-v(i,j,3),
     + sepx+u(i,j+1,3)+xad7,sepy-v(i,j+1,3),10)
       end do 
       call line(sepx+mx(8)+xad7,sepy-my(8),
     + sepx+u(i,jfin,3)+xad7,sepy-v(i,jfin,3),10)
       end if ! "pc"

c      Mylar roman number

       x1=0.5*(mx(3)+mx(6))
       y1=0.5*(my(3)+my(6))

       alpha=datan((my(6)-my(3))/(mx(6)-mx(3)))

       x2=x1+1.0*dsin(alpha)  ! Shift 1 cm
       y2=y1-1.0*dcos(alpha)

       call romano(i,sepx+x2+xad7,sepy-y2,alpha,3.0d0,7)

c      Compute additional points 2-4
c      First use one unit distance xd=1.0

       xd=1.0d0
c      Point 2
       x1=mx(3)
       y1=my(3)
       x2=mx(1)
       y2=my(1)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(2)=x3
       my(2)=y3
c      Point 4
       x1=mx(3)
       y1=my(3)
       x2=mx(6)
       y2=my(6)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(4)=x3
       my(4)=y3

c      Second make proportional triangles

       xdi=dsqrt((mx(2)-mx(4))**2.+(my(2)-my(4))**2.)
       if (xdi.ne.0.) then
       xd=xmy(ng,3)*rib(i,5)/(100.*xdi)
c      Point 2
       x1=mx(3)
       y1=my(3)
       x2=mx(1)
       y2=my(1)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(2)=x3
       my(2)=y3
c      Point 4
       x1=mx(3)
       y1=my(3)
       x2=mx(6)
       y2=my(6)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(4)=x3
       my(4)=y3
       else
       end if

c      Compute additional points 5-6
c      First use one unit distance xd=1.0

       xd=1.0d0
c      Point 5
       x1=mx(6)
       y1=my(6)
       x2=mx(3)
       y2=my(3)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(5)=x3
       my(5)=y3
c      Point 7
       x1=mx(6)
       y1=my(6)
       x2=mx(8)
       y2=my(8)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(7)=x3
       my(7)=y3

c      Second make proportional triangles

       xdi=dsqrt((mx(5)-mx(7))**2.+(my(5)-my(7))**2.)
       if (xdi.ne.0.) then
       xd=xmy(ng,6)*rib(i,5)/(100.*xdi)
c      Point 5
       x1=mx(6)
       y1=my(6)
       x2=mx(3)
       y2=my(3)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(5)=x3
       my(5)=y3
c      Point 7
       x1=mx(6)
       y1=my(6)
       x2=mx(8)
       y2=my(8)
       call interpd(x1,y1,x2,y2,x3,y3,xd)
       mx(7)=x3
       my(7)=y3
       else
       end if

c      Draw basic mylar contour 1-8 in ribs
      
       call line(sepx+mx(1),sepy-my(1),sepx+mx(2),sepy-my(2),10)
       call line(sepx+mx(2),sepy-my(2),sepx+mx(4),sepy-my(4),10)
       call line(sepx+mx(4),sepy-my(4),sepx+mx(5),sepy-my(5),10)
       call line(sepx+mx(5),sepy-my(5),sepx+mx(7),sepy-my(7),10)
       call line(sepx+mx(7),sepy-my(7),sepx+mx(8),sepy-my(8),10)
     
c      Draw basic mylar contour 1-8 in BOX(1,7)

       call line(sepx+mx(1)+xad7,sepy-my(1),
     + sepx+mx(2)+xad7,sepy-my(2),10)
       call line(sepx+mx(2)+xad7,sepy-my(2),
     + sepx+mx(4)+xad7,sepy-my(4),10)
       call line(sepx+mx(4)+xad7,sepy-my(4),
     + sepx+mx(5)+xad7,sepy-my(5),10)
       call line(sepx+mx(5)+xad7,sepy-my(5),
     + sepx+mx(7)+xad7,sepy-my(7),10)
       call line(sepx+mx(7)+xad7,sepy-my(7),
     + sepx+mx(8)+xad7,sepy-my(8),10)

c      Draw marks in BOX(1,4)

       x1=mx(1)
       y1=my(1)
       x2=mx(1)+0.7
       y2=my(1)
       call segment101(sepx+x1+xad4,sepy-y1,sepx+x2+xad4,sepy-y2,2)
       x1=mx(8)
       y1=my(8)
       x2=mx(8)
       y2=my(8)+0.7
       call segment101(sepx+x1+xad4,sepy-y1,sepx+x2+xad4,sepy-y2,2)

       end if

       return
       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE interpolation of polyline - linear
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE interpolyg(n,xpoint,ypoint,xvalue,yvalue)

      real*8 xpoint(50),ypoint(50),xvalue,yvalue,xm,xb
      real*8 funsup(50),funinf(50),funval(50)

      yvalue=0.0d0

      do i=1,n-1

      if (xvalue.ge.xpoint(i).and.xvalue.le.xpoint(i+1)) then
      xm=(ypoint(i+1)-ypoint(i))/(xpoint(i+1)-xpoint(i))
      xb=ypoint(i)-xm*xpoint(i)
      yvalue=xm*xvalue+xb
      end if

      end do

      return

      end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE interpolation of polyline - lagrange
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


      SUBROUTINE lagrangeip(n,xpoint,ypoint,xvalue,yvalue)

      real*8 xpoint(50),ypoint(50),xvalue,yvalue
      real*8 funsup(50),funinf(50),funval(50)

      yvalue=0.0d0

      do i=1,n

      funsup(i)=1.
      do j=1,n
      if (j.ne.i) then
      funsup(i)=funsup(i)*(xvalue-xpoint(j))
      end if
      end do

      funinf(i)=1.
      do j=1,n
      if (j.ne.i) then
      funinf(i)=funinf(i)*(xpoint(i)-xpoint(j))
      end if
      end do
      
      funval(i)=funsup(i)/funinf(i)

      yvalue=yvalue+funval(i)*ypoint(i)

      end do

      return

      end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE FLETXA (arrow or haut)
c      Numerical calculus arrow "haut" of circular segment
c      s = segment of the arc
c      sm =length of the arc
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE fletxa(s,sm,haut)

       real*8 s,g,sm,haut,llarg,radi,pi
       real*8 beta,alpha,alp20
       pi=4.0d0*datan(1.0d0)

       g=0.0d0
       i=1

       llarg=pi*s/2.

       do while (llarg.ge.sm)

       write (*,*) i,g,llarg,pi*s/2.

       x1=llarg
       y1=g

       beta=datan(g/(0.5d0*s))
       alpha=pi-2.*beta
       alp20=alpha/20.0d0        ! Discretize arc in 20 segments
       radi=dsqrt(g*g+0.25d0*s*s)
       llarg=40.*radi*dsin(0.5d0*alp20)
      
       g=g+(s/100.)  ! increment a cent of s
       i=i+1
       
       end do

       x2=llarg
       y2=g

       haut=radi-g-s/100.
       write (*,*) i,g,llarg,pi*s/2.
       write (*,*) "haut=",haut

       write (*,*) x1,y1
       write (*,*) x2,y2

c      Interpolation

       xm=(y2-y1)/(x2-x1)
       xb=y1-xm*x1
       g=xm*sm+xb

       radi=dsqrt(g*g+0.25d0*s*s)
       haut=radi-g

       write (*,*) sm,g,haut

       return

       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE panels3d
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE panels3d(i,rib,np,u,v,w,
     + uppcuts,iupp,kiupp,lowcuts,ilow,kilow,hautok)

       integer k29d,ncuts(200),jcut(0:10),np(0:100,9)
       real*8 u(0:100,500,99),v(0:100,500,99),w(0:100,500,99)
       real*8 rib(0:100,500)
       real*8 cutamp(10),cut29(0:10,200)
       real*8 llargc,llarg(500)
       real*8 s,sm,haut,hautm,tetha,radi,scontrol
       real*8 hautmmax,hautmax,q
       real*8 hautok(0:100,500),anglok(0:100,500)

       integer iupp(10,10,200),ilow(10,10,200)
       real*8 kiupp(10,200),kilow(10,200)
       integer uppcuts(200),lowcuts(200),iflag

       real*8 punt0(3),punt1(3),punt2(3),punt3(3),punt4(3)
       real*8 aplane,bplane,cplane,dplane,xt,dp0
       real*8 aplanei(0:100),bplanei(0:100),cplanei(0:100),
     + dplanei(0:100)

       real*8 lcosd(3),mcosd(3),ncosd(3),xdis

       ng=rib(i,169)

c      1. First step: Set median airfoil between i and i-1

       do j=1,np(i,1)
       u(i,j,48)=0.5d0*(u(i-1,j,47)+u(i,j,47))
       v(i,j,48)=0.5d0*(v(i-1,j,47)+v(i,j,47))
       w(i,j,48)=0.5d0*(w(i-1,j,47)+w(i,j,47))
       end do

c      2. Second steep: Compute hautok(i,j)

       do j=1,np(i,1)

       s=dsqrt((u(i-1,j,47)-u(i,j,47))**2+(v(i-1,j,47)-v(i,j,47))**2+
     + (w(i-1,j,47)-w(i,j,47))**2)
       sm=dsqrt((u(i-1,j,69)-u(i-1,j,70))**2+(v(i-1,j,69)-v(i-1,j,70))
     + **2)

c      Numerical root finding
c      Millorar algorisme per a tensions altes, assegurar que funciona

c      (Avoid sqrt of negative numbers)
       hautmax=0.5d0*dsqrt((dabs(sm*sm-s*s)))
       q=sm*s/((8.0d0*hautmax)+0.00001d0)
       hautmmax=(q-hautmax)

       iflag=0

c      Numerical solution by increments in hautm
       do l=0,300
       hautm=((dfloat(l)+0.00001d0)/300.0d0)*hautmmax*4.0d0  ! value 4.0 experimental (!)
       tetha=datan(0.5d0*s/hautm)
       radi=sm/(2.0d0*tetha)
       haut=radi-hautm
       scontrol=2.0d0*radi*sin(tetha)
       if (scontrol.ge.s.and.iflag.eq.0) then
       hautok(i,j)=haut
       iflag=1
c      Works these if?
       if (dabs(sm-s).le.0.01) then
       hautok(i,j)=0.0d0
       end if
       end if
       end do ! l

       end do ! j

c      3. Compute ovalized airfoil

c      Set the plane of the airfoil
 
       punt1(1)=u(i,1,48)
       punt1(2)=v(i,1,48)
       punt1(3)=w(i,1,48)

       jjj=dint(dfloat((1+np(i,2)))/2.0d0)
       punt2(1)=u(i,jjj,48)
       punt2(2)=v(i,jjj,48)
       punt2(3)=w(i,jjj,48)
       
       punt3(1)=u(i,np(i,2),48)
       punt3(2)=v(i,np(i,2),48)
       punt3(3)=w(i,np(i,2),48)

c      Plane Ax+By+Cz+D=0
       call planeby123(punt1,punt2,punt3,aplane,bplane,cplane,
     + dplane)

       aplanei(i)=aplane
       bplanei(i)=bplane
       cplanei(i)=cplane
       dplanei(i)=dplane

c      Points 55 perpendicular to the airfoil plane
       do j=1,np(i,1)
       dp0=10.0d0
       punt0(1)=u(i,j,48)
       punt0(2)=v(i,j,48)
       punt0(3)=w(i,j,48)
       call pointp3d(punt0,aplane,bplane,cplane,dp0,punt4)
       u(i,j,55)=punt4(1)
       v(i,j,55)=punt4(2)
       w(i,j,55)=punt4(3)
       end do ! j

c      Points 49 of the ovalized airfoil
       do j=1,np(i,1)

       punt1(1)=u(i,j-1,48)
       punt1(2)=v(i,j-1,48)
       punt1(3)=w(i,j-1,48)
       punt2(1)=u(i,j+1,48)
       punt2(2)=v(i,j+1,48)
       punt2(3)=w(i,j+1,48)
       punt3(1)=u(i,j,55)
       punt3(2)=v(i,j,55)
       punt3(3)=w(i,j,55)

       if (j.eq.1) then
       punt1(1)=u(i,j,48)
       punt1(2)=v(i,j,48)
       punt1(3)=w(i,j,48)
       punt2(1)=u(i,j+1,48)
       punt2(2)=v(i,j+1,48)
       punt2(3)=w(i,j+1,48)
       punt3(1)=u(i,j,55)
       punt3(2)=v(i,j,55)
       punt3(3)=w(i,j,55)
       end if

       if (j.eq.np(i,1)) then
       punt1(1)=u(i,j-1,48)
       punt1(2)=v(i,j-1,48)
       punt1(3)=w(i,j-1,48)
       punt2(1)=u(i,j,48)
       punt2(2)=v(i,j,48)
       punt2(3)=w(i,j,48)
       punt3(1)=u(i,j-1,55)
       punt3(2)=v(i,j-1,55)
       punt3(3)=w(i,j-1,55)
       end if

c      Plane 1-2-3 perpendicular to the airfoil in point j
       call planeby123(punt1,punt2,punt3,aplane,bplane,cplane,
     + dplane)

c      Point perpendicular to the plane 1-2-3 in line passing by punt0 at dp0
       dp0=hautok(i,j)
       punt0(1)=u(i,j,48)
       punt0(2)=v(i,j,48)
       punt0(3)=w(i,j,48)
       call pointp3d(punt0,aplane,bplane,cplane,dp0,punt4)

       u(i,j,49)=punt4(1)
       v(i,j,49)=punt4(2)
       w(i,j,49)=punt4(3)

       end do ! j

c      4. Compute median airfoil in local coordinates

c      Local axes in airfoil i: 0-1,0-2,0-3

c      punt0 = nose point coordinates median airfoil
       punt0(1)=u(i,np(i,6),48)
       punt0(2)=v(i,np(i,6),48)
       punt0(3)=w(i,np(i,6),48)

c      Point1 in line perpendicular to plane 48, by point 0
       call  pointp3d(punt0,aplanei(i),bplanei(i),cplanei(i),50.0d0,
     + punt1)

c       call line3d(punt0(1),punt0(2),punt0(3),
c     + punt1(1),punt1(2),punt1(3),4)

c      Point 2 in the leading edge of median airfoil (48)
       punt2(1)=u(i,np(i,1),48)
       punt2(2)=v(i,np(i,1),48)
       punt2(3)=w(i,np(i,1),48)

c      Define plane 0-1-2
       call planeby123(punt0,punt1,punt2,aplane,bplane,cplane,
     + dplane)
       
c      Point3 in line perpendicular to plane 0-1-2, by point 0
       call pointp3d(punt0,aplane,bplane,cplane,50.0d0,punt3)

c      Now we have tree the local axys in airfoil (48) 0-1,0-2,0-3

c       call line3d(punt0(1),punt0(2),punt0(3),
c     + punt3(1),punt3(2),punt3(3),1)

c      Director cosine 0-1,0-2,0-3

       lcosd(1)=(punt1(1)-punt0(1))/50.0d0
       mcosd(1)=(punt1(2)-punt0(2))/50.0d0
       ncosd(1)=(punt1(3)-punt0(3))/50.0d0

       xdis=dsqrt((punt2(1)-punt0(1))**2+(punt2(2)-punt0(2))**2+
     + (punt2(3)-punt0(3))**2)
       lcosd(2)=(punt2(1)-punt0(1))/xdis
       mcosd(2)=(punt2(2)-punt0(2))/xdis
       ncosd(2)=(punt2(3)-punt0(3))/xdis

       lcosd(3)=(punt3(1)-punt0(1))/50.0d0
       mcosd(3)=(punt3(2)-punt0(2))/50.0d0
       ncosd(3)=(punt3(3)-punt0(3))/50.0d0

c      Compute local coordinates of the median airfoil
       call glo2loc(i,punt0,lcosd,mcosd,ncosd,u,v,w,np)
c      Return vectors u(i,j,53) > median local
c      Return vectors u(,j,54) > median ovalized


c      Define cut points

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE czinf compute zones of influence of cutts
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      REMOVE write (*,*)
c      REMOVE not used variables
c      print in lep-out.txt

       SUBROUTINE czinf(i,rib,np,u,v,w,
     + uppcuts,iupp,kiupp,lowcuts,ilow,kilow,hautok,zinf)

       integer k29d,ncuts(200),jcut(0:10),np(0:100,9)
       real*8 u(0:100,500,99),v(0:100,500,99),w(0:100,500,99)
       real*8 rib(0:100,500)
       real*8 cutamp(10),cut29(0:10,200)
       real*8 llargc,llarg(500)
       real*8 s,sm,haut,hautm,tetha,radi,scontrol
       real*8 hautmmax,hautmax,q
       real*8 hautok(0:100,500),anglok(0:100,500)

       integer iupp(10,10,200),ilow(10,10,200)
       real*8 kiupp(10,200),kilow(10,200)
       integer uppcuts(200),lowcuts(200),iflag

       real*8 punt0(3),punt1(3),punt2(3),punt3(3),punt4(3)
       real*8 aplane,bplane,cplane,dplane,xt,dp0
       real*8 aplanei(0:100),bplanei(0:100),cplanei(0:100),
     + dplanei(0:100)

       real*8 lcosd(3),mcosd(3),ncosd(3),xdis

       real*8 zinf(0:100,10,10)

       ng=rib(i,169)

c      Cases
       if (uppcuts(ng).eq.0) then
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 1 cut extrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (uppcuts(ng).eq.1) then

c      Zone 1
       d1=0.0d0
       d2=0.0d0
       do j=iupp(1,2,ng),iupp(1,3,ng)-1
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=iupp(1,2,ng),iupp(1,3,ng)-1
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,1)=d1
       zinf(i,2,1)=d2
       zinf(i,3,1)=0.0d0
       zinf(i,4,1)=d2-d1
       zinf(i,5,1)=zinf(i,4,1)

c      Zone 2 (not considered, beacuse j2=j3)
       zinf(i,1,2)=0.0d0
       zinf(i,2,2)=0.0d0
       zinf(i,3,2)=0.0d0
       zinf(i,4,2)=0.0d0

c      Zone 3
       d1=0.0d0
       d2=0.0d0
       do j=iupp(1,3,ng),np(i,2)-1
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=iupp(1,3,ng),np(i,2)-1
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,3)=d1
       zinf(i,2,3)=d2
       zinf(i,3,3)=d2-d1
       zinf(i,4,3)=0.0d0
       zinf(i,5,3)=zinf(i,3,3)

c      Compatibility vaule in first cut
       zinf(i,6,1)=0.5d0*(zinf(i,5,3)+zinf(i,5,1))*kiupp(1,ng)

       end if ! Case 1 cut extrados

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 2 cuts extrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (uppcuts(ng).eq.2) then

c      Zone 1
       d1=0.0d0
       d2=0.0d0
       do j=iupp(1,2,ng),iupp(1,3,ng)-1
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=iupp(1,2,ng),iupp(1,3,ng)-1
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,1)=d1
       zinf(i,2,1)=d2
       zinf(i,3,1)=0.0d0
       zinf(i,4,1)=d2-d1
       zinf(i,5,1)=zinf(i,4,1)
       
c      Zone 2
       d1=0.0d0
       d2=0.0d0
       do j=iupp(2,2,ng),iupp(2,3,ng)-1
       d1=d1+dsqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=iupp(2,2,ng),iupp(2,3,ng)-1
       d2=d2+dsqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,2)=d1
       zinf(i,2,2)=d2
       zinf(i,3,2)=0.5d0*(d2-d1)
       zinf(i,4,2)=0.5d0*(d2-d1)
       zinf(i,5,2)=zinf(i,3,2)*2.0d0

c      Compatibility value first cut
       zinf(i,6,1)=0.5d0*(zinf(i,5,2)*0.5d0+zinf(i,5,1))*kiupp(1,ng)

c      Zone 3
       d1=0.0d0
       d2=0.0d0
       do j=iupp(2,3,ng),np(i,2)-1
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=iupp(2,3,ng),np(i,2)-1
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,3)=d1
       zinf(i,2,3)=d2
       zinf(i,3,3)=d2-d1
       zinf(i,4,3)=0.0d0
       zinf(i,5,3)=zinf(i,3,3)

c      Compatibility value second cut
       zinf(i,6,2)=0.5d0*(zinf(i,5,3)+zinf(i,5,2)*0.5d0)*kiupp(2,ng)

       end if ! Case 2 cut extrados

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case vents
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Zone 4
       d1=0.0d0
       d2=0.0d0
       do j=np(i,2),np(i,2)+np(i,3)-2
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=np(i,2),np(i,2)+np(i,3)-2
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,4)=d1
       zinf(i,2,4)=d2
       zinf(i,3,4)=0.5d0*(d2-d1)
       zinf(i,4,4)=0.5d0*(d2-d1)
       zinf(i,5,4)=2.0d0*zinf(i,4,4)
 
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case 1 cut intrados
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (lowcuts(ng).eq.1) then

c      Zone 5
       d1=0.0d0
       d2=0.0d0
       do j=np(i,2)+np(i,3)-1,ilow(1,2,ng)-1
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=np(i,2)+np(i,3)-1,ilow(1,2,ng)-1
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,5)=d1
       zinf(i,2,5)=d2
       zinf(i,3,5)=0.0d0
       zinf(i,4,5)=d2-d1
       zinf(i,5,5)=zinf(i,4,5)
 
c      Zone 6
       d1=0.0d0
       d2=0.0d0
       do j=ilow(1,2,ng),ilow(1,3,ng)-1
       d1=d1+sqrt((v(i,j,53)-v(i,j+1,53))**2.0d0+
     + (w(i,j,53)-w(i,j+1,53))**2.0d0)
       end do
       do j=ilow(1,2,ng),ilow(1,3,ng)-1
       d2=d2+sqrt((v(i,j,54)-v(i,j+1,54))**2.0d0+
     + (w(i,j,54)-w(i,j+1,54))**2.0d0)
       end do
       zinf(i,1,6)=d1
       zinf(i,2,6)=d2
       zinf(i,3,6)=d2-d1
       zinf(i,4,6)=0.0d0
       zinf(i,5,6)=zinf(i,3,6)

c      Compatibility value first cut intrados
       zinf(i,6,4)=0.5d0*(zinf(i,5,6)+zinf(i,5,5))*kilow(1,ng)

       end if ! Case 1 cut intrados

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE planeby123
c     Plane Ax+By+Cz+D=0 defined by points 1,2,3
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE planeby123(punt1,punt2,punt3,aplane,bplane,cplane,
     + dplane)

       real*8 punt1(3),punt2(3),punt3(3)
       real*8 aplane,bplane,cplane,dplane
       real*8 ag,bg,cg,dg
       real*8 x1,y1,z1,x2,y2,z2,x3,y3,z3

       x1=punt1(1)
       y1=punt1(2)
       z1=punt1(3)
       x2=punt2(1)
       y2=punt2(2)
       z2=punt2(3)
       x3=punt3(1)
       y3=punt3(2)
       z3=punt3(3)

       ag=(y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
       bg=(z2-z1)*(x3-x1)-(x2-x1)*(z3-z1)
       cg=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)

       aplane=ag
       bplane=bg
       cplane=cg
       dplane=-ag*x1-bg*y1-cg*z1

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE pointp3d
c     Point by 0 perpendicular to plane Ax+By+Cz+D=0 at distance d
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


       SUBROUTINE pointp3d(punt0,aplane,bplane,cplane,dp0,punt4)

       real*8 punt0(3),punt1(3),punt2(3),punt3(3),punt4(3)
       real*8 aplane,bplane,cplane,xt,dp0

       xt=dp0/dsqrt(aplane*aplane+bplane*bplane+cplane*cplane)

       punt4(1)=punt0(1)+aplane*xt
       punt4(2)=punt0(2)+bplane*xt
       punt4(3)=punt0(3)+cplane*xt

       return

       end

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE glo2loc
c     Transform global 3d coordinates to local coordinates
c     Specifically applied to middle airfoil index 53 and 54
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      (x0,y0,z0) center of local axes
c      Index 48 = 3D median airfoil
c      Index 49 = 3D ovalized median airfoil
c      Index 53 = 2D median airfoil
c      Index 54 = 2D ovalized median airfoil

       SUBROUTINE glo2loc(i,punt0,lcosd,mcosd,ncosd,u,v,w,np)

       real*8 lcosd(3),mcosd(3),ncosd(3)
       real*8 punt0(3)
       real*8 u(0:100,500,99),v(0:100,500,99),w(0:100,500,99)
       integer np(0:100,9)

       x0=punt0(1)
       y0=punt0(2)
       z0=punt0(3)

       do j=1,np(i,1)
       u(i,j,53)=lcosd(1)*(u(i,j,48)-punt0(1))+
     + mcosd(1)*(v(i,j,48)-punt0(2))+ncosd(1)*(w(i,j,48)-punt0(3))
       v(i,j,53)=lcosd(2)*(u(i,j,48)-punt0(1))+
     + mcosd(2)*(v(i,j,48)-punt0(2))+ncosd(2)*(w(i,j,48)-punt0(3))
       w(i,j,53)=lcosd(3)*(u(i,j,48)-punt0(1))+
     + mcosd(3)*(v(i,j,48)-punt0(2))+ncosd(3)*(w(i,j,48)-punt0(3))

       u(i,j,54)=lcosd(1)*(u(i,j,49)-punt0(1))+
     + mcosd(1)*(v(i,j,49)-punt0(2))+ncosd(1)*(w(i,j,49)-punt0(3))
       v(i,j,54)=lcosd(2)*(u(i,j,49)-punt0(1))+
     + mcosd(2)*(v(i,j,49)-punt0(2))+ncosd(2)*(w(i,j,49)-punt0(3))
       w(i,j,54)=lcosd(3)*(u(i,j,49)-punt0(1))+
     + mcosd(3)*(v(i,j,49)-punt0(2))+ncosd(3)*(w(i,j,49)-punt0(3))
       end do
  
       return

       end


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c     SUBROUTINE print01
c     Print TE extrados
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE print01(i,psep,psey,u,v,icase)

       real*8 u(0:100,500,99),v(0:100,500,99),w(0:100,500,99)
       real*8 psep,psey
       integer j,icase,np(0:100,9)

c      Incorpore subroutine extpoints
      
c      Segments

       j=1

c       write (*,*) i

       if (icase.eq.1) then ! case print
       call line(psep+u(i,j,9),psey-v(i,j,9),
     + psep+u(i,j,10),psey-v(i,j,10),1)
       end if

       return

       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print initial i final points
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE prinifp(i,npi,npf,u,v,psep,psey,xcir,xdes,xkf)
       
       real*8 u(0:100,500,99),v(0:100,500,99),psep,psey,xcir
       real*8 xu,xv,xdes,xkf
       real*8 alp
       integer i,j,npi,npf

       j=npi
       xu=u(i,j,9)
       xv=v(i,j,9)
       alp=abs(datan((v(i,j+1,9)-v(i,j,9))/(u(i,j+1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)     
       call point(psep+xu+2520.*xkf,-xv+psey,7)

       j=npf
       xu=u(i,j,9)
       xv=v(i,j,9)
       alp=abs(datan((v(i,j-1,9)-v(i,j,9))/(u(i,j-1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)     
       call point(psep+xu+2520.*xkf,-xv+psey,7)

       j=npi
       xu=u(i,j,10)
       xv=v(i,j,10)
       alp=abs(datan((v(i,j+1,10)-v(i,j,10))/(u(i,j+1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)
       call point(psep+xu+2520.*xkf,-xv+psey,7)

       j=npf
       xu=u(i,j,10)
       xv=v(i,j,10)
       alp=abs(datan((v(i,j-1,10)-v(i,j,10))/(u(i,j-1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)
       call point(psep+xu+2520.*xkf,-xv+psey,7)

       return

       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE prinfpv - Print final points vents
c      Case print, case laser (ic1)
c      Case type vent (ic2)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE prinfpv(i,j9,j10,ufr,vfr,psep,psey,xcir,xdes,xkf,
     + ic1,ic2)
       
       real*8 ufr(0:100,500,50),vfr(0:100,500,50),psep,psey,xcir
       real*8 xu,xv,xdes,xkf
       real*8 alp
       integer i,ic1,ic2,j9,j10

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case print, vent +1 +6
c      ic1=1 ic2=1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (ic1.eq.1) then
       if (ic2.eq.1.or.ic2.eq.6) then
c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j,9)-vfr(i,j-1,9))/
     + (ufr(i,j,9)-ufr(i,j-1,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)     
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j,10)-vfr(i,j-1,10))/
     + (ufr(i,j,10)-ufr(i,j-1,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)
       end if
       end if
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case laser, vent +1 +6
c      ic1=2 ic2=1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (ic1.eq.2) then
       if (ic2.eq.1.or.ic2.eq.6) then
c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j,9)-vfr(i,j-1,9))/
     + (ufr(i,j,9)-ufr(i,j-1,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j,10)-vfr(i,j-1,10))/
     + (ufr(i,j,10)-ufr(i,j-1,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call point(psep+xu,-xv+psey,7)
       end if
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case print, vent -1 -6
c      ic1=1 ic2=-1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic1.eq.1) then
       if (ic2.eq.-1.or.ic2.eq.-6) then
c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j+1,9)-vfr(i,j,9))/
     + (ufr(i,j+1,9)-ufr(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)     
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j+1,10)-vfr(i,j,10))/
     + (ufr(i,j+1,10)-ufr(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)
       end if
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case laser, vent -1 -6
c      ic1=2 ic2=-1
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (ic1.eq.2) then
       if (ic2.eq.-1.or.ic2.eq.-6) then
c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j+1,9)-vfr(i,j,9))/
     + (ufr(i,j+1,9)-ufr(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j+1,10)-vfr(i,j,10))/
     + (ufr(i,j+1,10)-ufr(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call point(psep+xu,-xv+psey,7)
       end if
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case print, vent -2
c      ic1=1 ic2=-2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic1.eq.1.and.ic2.eq.-2) then

c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j+1,9)-vfr(i,j,9))/
     + (ufr(i,j+1,9)-ufr(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
c       call pointg(psep+xu,psey-xv,xcir,4)     
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j+1,10)-vfr(i,j,10))/
     + (ufr(i,j+1,10)-ufr(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case laser, vent -2
c      ic1=2 ic2=-2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (ic1.eq.2.and.ic2.eq.-2) then
c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j+1,9)-vfr(i,j,9))/
     + (ufr(i,j+1,9)-ufr(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
c       call point(psep+xu,-xv+psey,7)
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j+1,10)-vfr(i,j,10))/
     + (ufr(i,j+1,10)-ufr(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
       call point(psep+xu,-xv+psey,7)
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case print, vent -3
c      ic1=1 ic2=-3
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       if (ic1.eq.1.and.ic2.eq.-3) then

c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j+1,9)-vfr(i,j,9))/
     + (ufr(i,j+1,9)-ufr(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       call pointg(psep+xu,psey-xv,xcir,4)     
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j+1,10)-vfr(i,j,10))/
     + (ufr(i,j+1,10)-ufr(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
c       call pointg(psep+xu,psey-xv,xcir,4)
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Print final points vents, case laser, vent -3
c      ic1=2 ic2=-3
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       if (ic1.eq.2.and.ic2.eq.-3) then
c      Point left
       j=j9
       xu=ufr(i,j,9)
       xv=vfr(i,j,9)
       alp=abs(datan((vfr(i,j+1,9)-vfr(i,j,9))/
     + (ufr(i,j+1,9)-ufr(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)   
       call point(psep+xu,-xv+psey,7)
c      Point right
       j=j10
       xu=ufr(i,j,10)
       xv=vfr(i,j,10)
       alp=abs(datan((vfr(i,j+1,10)-vfr(i,j,10))/
     + (ufr(i,j+1,10)-ufr(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
c       call point(psep+xu,-xv+psey,7)
       end if


       return

       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE llarlr
c      Computes length at left and right of the partial rectagular
c      panel i formed by npo points
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE llarlr(i,i12,i22,npo,ufr,vfr,llarl,llarr)

       real*8 ufr(0:100,500,50),vfr(0:100,500,50)
       real*8 llarl(0:100,3,100),llarr(0:100,3,100)
       integer i,j,i12,i22,npo

c      Set panel side lengths 
       llarl(i,i12,i22)=0.0d0
       llarr(i,i12,i22)=0.0d0      
       do j=1,npo-1
       llarl(i,i12,i22)=llarl(i,i12,i22)+dsqrt((ufr(i,j+1,9)-
     + ufr(i,j,9))**2.+(vfr(i,j+1,9)-vfr(i,j,9))**2.)
       llarr(i,i12,i22)=llarr(i,i12,i22)+dsqrt((ufr(i,j+1,10)-
     + ufr(i,j,10))**2.+(vfr(i,j+1,10)-vfr(i,j,10))**2.)
       end do

c       write (*,*) i,i12,i22,npo,llarl(i,i12,i22),llarr(i,i12,i22)

       return

       end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE xmarksi
c      Makes internal marks in a rectangular panel
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE xmarksi(i,i1,i2,npo,u,v,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf)

       real*8 u(0:100,500,50),v(0:100,500,50),rib(0:100,500)
       real*8 llarl(0:100,3,100),llarr(0:100,3,100)
       real*8 xmk,xmk0,xmark,xmklast,xprev,xpost,xacu(0:100)
       real*8 dist,dist1,dist2,alp,xu,xv,psep,psey,xcir,xdes,xkf
       real*8 xinil,xinir
       real*8 xfinl(0:100,3,100),xfinr(0:100,3,100)
       integer i,j,k,i1,i2,npo

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      STILL RECOMMENDED APPLY AMPLIFICATION COEFFICIENTS 
c      set in 11. rib(i,194) rib(i,195) extra
c      and        rib(i,200) rib(i,201) intra
c      Separate left and right calculus using proper coefficient
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      For extrados panels (i1=1)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc  

c      SEPARAR L i R !!!!!!!!!!!!!!!
            
       if (i1.eq.1) then
       
c      Set successive distance marks
c      WARNING!!!! Compute proper amplification coefficient!!!!!!!
c      Use amplification coefficient (panel border/rib)
c      Use different coeeficients for left and right
c      xmk=xmk*rib(i,36) ! amplificacio de segment

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw at left 
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
c      Iterate in marks
       do k=1,60

       xacu(i)=0.0d0

c       write (*,*) "xinil ",i,xinil

c      Set successive distance marks
       if (k.eq.1) then
       xmk=xinil
       end if
       if (k.gt.1) then
       xmk=xmark*float(k-1)*1.0d0+xinil
       end if
      
       do j=1,npo-1
       xprev=xacu(i)
       xacu(i)=xacu(i)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))
       xpost=xacu(i)

c      Detect segment where is mark
       if(xmk.le.xpost.and.xmk.ge.xprev.and.xmk.le.llarl(i,i1,i2)) then

c      dibuixa marca

       dist=dsqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       dist1=xmk-xprev

       xu=u(i,j,9)+(u(i,j+1,9)-u(i,j,9))*(dist1/dist)
       xv=v(i,j,9)+(v(i,j+1,9)-v(i,j,9))*(dist1/dist)

c      REVISSAR SIGNES DESPLAÇAMENT!!!!!!!
c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j+1,9)-v(i,j,9))/(u(i,j+1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       
       if (xinil.ge.0.01d0.or.k.gt.1) then
c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if
       
       xmklast=xmk

       end if
       end do ! j left
      
       end do ! k

       xfinl(i,i1,i2)=xmark*1.0d0-(llarl(i,i1,i2)-xmklast)

c       write (*,*) "L ",i,i1,i2,xmklast,llarl(i,i1,i2),xfinl(i,i1,i2)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw at right
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xacu(i)=xinir  

c      Iterate in marks
       do k=1,60

       xacu(i)=0.0d0

c      Set successive distance marks
       if (k.eq.1) then
       xmk=xinir
       end if
       if (k.gt.1) then
       xmk=xmark*float(k-1)*1.0d0+xinir
       end if
  
       do j=1,npo-1
       xprev=xacu(i)
       xacu(i)=xacu(i)+sqrt((u(i,j,10)-u(i,j+1,10))**2.+((v(i,j,10)
     + -v(i,j+1,10))**2.))
       xpost=xacu(i)

c      Detect segment where is mark
       if(xmk.le.xpost.and.xmk.ge.xprev.and.xmk.le.llarr(i,i1,i2)) then

c      dibuixa marca

       dist=dsqrt((u(i,j,10)-u(i,j+1,10))**2.+((v(i,j,10)
     + -v(i,j+1,10))**2.))

       dist1=xmk-xprev

       xu=u(i,j,10)+(u(i,j+1,10)-u(i,j,10))*(dist1/dist)
       xv=v(i,j,10)+(v(i,j+1,10)-v(i,j,10))*(dist1/dist)

c      REVISSAR SIGNES DESPLAÇAMENT!!!!!!!
c      I COHERENCIA AMB ALTRES MARQUES LATERALS
c      Despla a vores punts de control de costures
c      Segons verificació, aquí està be!!!!!!!!
c      Veure vents i altres zones!!!!!!!!!!
       alp=abs(datan((v(i,j+1,10)-v(i,j,10))/(u(i,j+1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
c      SIGNE CREC QUE CORREGIT!!!! :)

       if (xinir.ge.0.01d0.or.k.gt.1) then
c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if
       
       xmklast=xmk

       end if ! mark xmk
       end do ! j right

       end do ! k iteration

       xfinr(i,i1,i2)=xmark*1.0d0-(llarr(i,i1,i2)-xmklast)
c       write (*,*) "R ",i,i1,i2,xmklast,llarr(i,i1,i2),xfinr(i,i1,i2)

       end if ! i1=1 Extrados panels


ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      For intrados panels (i1=2)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc              
       if (i1.eq.2) then
 

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw at left 
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
c      write (*,*) i,"2 ",u(i,npo-4,9),v(i,npo-4,9)


c      Iterate in marks
       do k=1,60

       xacu(i)=0.0d0

c      Set successive distance marks
       if (k.eq.1) then
       xmk=xinil
       end if
       if (k.gt.1) then
       xmk=xmark*float(k-1)*1.0d0+xinil
       end if
      
       do j=npo-1,1,-1
       xprev=xacu(i)
       xacu(i)=xacu(i)+sqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))
       xpost=xacu(i)

c      Detect segment where is mark
       if(xmk.le.xpost.and.xmk.ge.xprev.and.xmk.le.llarl(i,i1,i2)) then

c      dibuixa marca

       dist=dsqrt((u(i,j,9)-u(i,j+1,9))**2.+((v(i,j,9)
     + -v(i,j+1,9))**2.))

       dist1=xmk-xprev
       dist2=dist-dist1

       xu=u(i,j,9)+(u(i,j+1,9)-u(i,j,9))*(dist2/dist)
       xv=v(i,j,9)+(v(i,j+1,9)-v(i,j,9))*(dist2/dist)

c      REVISSAR SIGNES DESPLAÇAMENT!!!!!!!
c      Despla a vores punts de control de costures
       alp=abs(datan((v(i,j+1,9)-v(i,j,9))/(u(i,j+1,9)-u(i,j,9))))
       xu=xu-xdes*dsin(alp)
       xv=xv+xdes*dcos(alp)
       
       if (xinil.ge.0.01d0.or.k.gt.1) then
c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if
       
       xmklast=xmk

       end if
       end do ! j left
      
       end do ! k

       xfinl(i,i1,i2)=xmark*1.0d0-(llarl(i,i1,i2)-xmklast)

c       write (*,*) "L ",i,i1,i2,xmklast,llarl(i,i1,i2),xfinl(i,i1,i2)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Draw at right
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xacu(i)=xinir  

c      Iterate in marks
       do k=1,60

       xacu(i)=0.0d0

c      Set successive distance marks
       if (k.eq.1) then
       xmk=xinir
       end if
       if (k.gt.1) then
       xmk=xmark*float(k-1)*1.0d0+xinir
       end if
  
       do j=npo-1,1,-1
       xprev=xacu(i)
       xacu(i)=xacu(i)+sqrt((u(i,j,10)-u(i,j+1,10))**2.+((v(i,j,10)
     + -v(i,j+1,10))**2.))
       xpost=xacu(i)

c      Detect segment where is mark
       if(xmk.le.xpost.and.xmk.ge.xprev.and.xmk.le.llarr(i,i1,i2)) then

c      dibuixa marca

       dist=dsqrt((u(i,j,10)-u(i,j+1,10))**2.+((v(i,j,10)
     + -v(i,j+1,10))**2.))

       dist1=xmk-xprev
       dist2=dist-dist1

       xu=u(i,j,10)+(u(i,j+1,10)-u(i,j,10))*(dist2/dist)
       xv=v(i,j,10)+(v(i,j+1,10)-v(i,j,10))*(dist2/dist)

c      REVISSAR SIGNES DESPLAÇAMENT!!!!!!!
c      I COHERENCIA AMB ALTRES MARQUES LATERALS
c      Despla a vores punts de control de costures
c      Segons verificació, aquí està be!!!!!!!!
c      Veure vents i altres zones!!!!!!!!!!
       alp=abs(datan((v(i,j+1,10)-v(i,j,10))/(u(i,j+1,10)-u(i,j,10))))
       xu=xu+xdes*dsin(alp)
       xv=xv-xdes*dcos(alp)
c      SIGNE CORREGIT!!!!!!!! :)

       if (xinir.ge.0.01d0.or.k.gt.1) then
c      Point imp
       call pointg(psep+xu,psey-xv,xcir,3)
c      Point laser
       call point(psep+xu+2520.*xkf,-xv+psey,7)
       end if
       
       xmklast=xmk

       end if ! mark xmk
       end do ! j right

       end do ! k iteration

       xfinr(i,i1,i2)=xmark*1.0d0-(llarr(i,i1,i2)-xmklast)
c       write (*,*) "R ",i,i1,i2,xmklast,llarr(i,i1,i2),xfinr(i,i1,i2)

       end if ! i1=2 Intrados panels

       return
       end



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE iam
c      intrados anchor marks
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE iam(i,i1,i2,np,npo,u,v,rib,xinil,xinir,
     + xfinl,xfinr,xmark,llarl,llarr,psep,psey,xcir,xdes,xkf,
     + typm1,typm2,typm3,typm4,typm5,typm6,xrib)

       real*8 u(0:100,500,50),v(0:100,500,50),rib(0:100,500)
       real*8 llarl(0:100,3,100),llarr(0:100,3,100)
       integer np(0:100,9)
       real*8 xmk,xmk0,xmark,xmklast,xprev,xpost,xacu(0:100)
       real*8 dist,dist1,dist2,alp,xu,xv,psep,psey,xcir,xdes,xkf
       real*8 xinil,xinir
       real*8 xfinl(0:100,3,100),xfinr(0:100,3,100)
       integer i,j,k,i1,i2,npo

       integer klz
       real*8 xlen,xlenp,xequis,yequis,xdu,xdv,alpha,pi
       real*8 xanchor(100,6),yanchor(100,6)
       real*8 xanchoril(100,6),yanchoril(100,6)
       real*8 xanchorir(100,6),yanchorir(100,6)
c       real*8 xpeq,ypeq,xdesp,xdesp1x,xdesp1y,xdesp2x,xdesp2y

       integer typm1(50),typm4(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50)
       real*8 xrib


       pi=4.*atan(1.)


c       write (*,*) i, "Ep..."

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Left side
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,int(rib(i,15)) ! rib(i,15)=anchors number

       xlen=xinil
       j=npo
       xlenp=xlen+dsqrt((v(i,j,9)-v(i,j-1,9))**2.+
     + (u(i,j,9)-u(i,j-1,9))**2.)

       do j=npo,2,-1

c      Detect and draw anchor point
       if (rib(i,130+klz).ge.xlen.and.rib(i,130+klz).le.xlenp) then

       rib(i,107)=rib(i,130+klz)-xlen
       rib(i,108)=dsqrt((v(i,j,9)-v(i,j-1,9))**2.+(u(i,j,9)-u(i,j-1,9))
     + **2.)

c      Interpolate
       xequis=u(i,j,9)-(rib(i,107)*(u(i,j,9)-u(i,j-1,9)))/
     + rib(i,108)
       yequis=v(i,j,9)-(rib(i,107)*(v(i,j,9)-v(i,j-1,9)))/
     + rib(i,108)

c      SOLUCIÓ PROVISIONAL translació a base vent:
       if (i2.eq.4) then
       xequis=xequis-(u(i,npo,9)-u(i,1,9))
       yequis=yequis-(v(i,npo,9)-v(i,1,9))
       end if

c      Define anchor points in planar panel
       xanchoril(i,klz)=xequis
       yanchoril(i,klz)=yequis

c      Draw
       xdu=u(i,j,9)-u(i,j-1,9)
       xdv=v(i,j,9)-v(i,j-1,9)

       if (xdu.ne.0) then
       alpha=-(datan(xdv/xdu))
       end if
       if (xdu.eq.0.) then
       alpha=pi/2.
       end if
       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case imp
c      Line 4*xrib in plotting panels
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Case all
       call line(psep+xequis,psey-yequis,psep+xequis-0.4*xrib*
     + dsin(-alpha),psey-yequis-0.4*xrib*dcos(-alpha),30)
       
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case laser
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xpeq=xequis+1.*xdes*dsin(-alpha)
       ypeq=yequis-1.*xdes*dcos(-alpha)

       xdesp=1.0*(0.5*(xrib-20.*xdes))/10.
c       xdesp=typm6(5)
c      REVISAR

       xdesp1x=xdesp*dsin(-alpha)
       xdesp1y=-xdesp*dcos(-alpha)
       xdesp2x=2.*xdesp*dsin(-alpha)
       xdesp2y=-2.*xdesp*dcos(-alpha)

c      Case 1: classic 3 orange points
       if (typm4(5).eq.1) then
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq+xdesp1x+2520*xkf,psey-ypeq-xdesp1y,30)
       call point (psep+xpeq+xdesp2x+2520*xkf,psey-ypeq-xdesp2y,30)
       end if

c      Case 2: Controled 3 orange points
       if (typm4(5).eq.2) then
       xpeq=xequis+1.*typm6(5)*dsin(-alpha)
       ypeq=yequis-1.*typm6(5)*dcos(-alpha)
       xdesp1x=typm5(5)*dsin(-alpha)
       xdesp1y=-typm5(5)*dcos(-alpha)
       xdesp2x=2.*typm5(5)*dsin(-alpha)
       xdesp2y=-2.*typm5(5)*dcos(-alpha)
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq+xdesp1x+2520*xkf,psey-ypeq-xdesp1y,30)
       call point (psep+xpeq+xdesp2x+2520*xkf,psey-ypeq-xdesp2y,30)
       end if

c      Case 3: triangle h mm
       if (typm4(5).eq.3) then
       xpeq=xequis-typm6(5)*dsin(alpha)
       ypeq=yequis+typm6(5)*dcos(alpha)
       call mtriangle(psep+xpeq+2520*xkf,psey-ypeq,typm5(5),-alpha,1)
       end if

       end if

       xlen=xlen+sqrt((v(i,j,9)-v(i,j-1,9))**2.+(u(i,j,9)-u(i,j-1,9))
     + **2.)
       xlenp=xlen+sqrt((v(i,j-1,9)-v(i,j-2,9))**2.+
     + (u(i,j-1,9)-u(i,j-2,9))**2.)

       end do ! j

       end do ! klz

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Right side
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       do klz=1,rib(i+1,15)

       xlen=xinir
       j=npo
       xlenp=xlen+dsqrt((v(i,j,10)-v(i,j-1,10))**2.+
     + (u(i,j,10)-u(i,j-1,10))**2.)

       do j=npo,2,-1

c      Detect and draw anchor point
       if (rib(i+1,130+klz).ge.xlen.and.rib(i+1,130+klz).le.xlenp) then

       rib(i+1,107)=rib(i+1,130+klz)-xlen
       rib(i+1,108)=dsqrt((v(i,j,10)-v(i,j-1,10))**2.+(u(i,j,10)-
     + u(i,j-1,10))**2.)

c      Interpolate
       xequis=u(i,j,10)-(rib(i+1,107)*(u(i,j,10)-u(i,j-1,10)))/
     + rib(i+1,108)
       yequis=v(i,j,10)-(rib(i+1,107)*(v(i,j,10)-v(i,j-1,10)))/
     + rib(i+1,108)

c      SOLUCIÓ PROVISIONAL translació a base vent:
       if (i2.eq.4) then
       xequis=xequis-(u(i,npo,10)-u(i,1,10))
       yequis=yequis-(v(i,npo,10)-v(i,1,10))
       end if

c      Define anchor points in planar panel
       xanchorir(i+1,klz)=xequis
       yanchorir(i+1,klz)=yequis

c      Draw
       alpha=-(datan((v(i,j,10)-v(i,j-1,10))/(u(i,j,10)-u(i,j-1,10))))

       if (alpha.lt.0.) then
       alpha=alpha+pi
       end if

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case imp
c      Line 4*xrib in plotting panels
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       call line(psep+xequis,psey-yequis,psep+xequis+0.4*xrib*
     + dsin(-alpha),psey-yequis+0.4*xrib*dcos(-alpha),30)

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Case laser
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       xpeq=xequis-1.*xdes*dsin(-alpha)
       ypeq=yequis+1.*xdes*dcos(-alpha)

       xdesp=1.0*(0.5*(xrib-20.*xdes))/10.
c      REVISAR
c       xdesp=typm6(5)

       xdesp1x=xdesp*dsin(-alpha)
       xdesp1y=-xdesp*dcos(-alpha)
       xdesp2x=2.*xdesp*dsin(-alpha)
       xdesp2y=-2.*xdesp*dcos(-alpha)

c      Case 1: classic 3 orange points
       if (typm4(5).eq.1) then
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq-xdesp1x+2520*xkf,psey-ypeq+xdesp1y,30)
       call point (psep+xpeq-xdesp2x+2520*xkf,psey-ypeq+xdesp2y,30)
       end if

c      Case 2: controled 3 orange points
       if (typm4(5).eq.2) then
       xpeq=xequis+1.*typm6(5)*dsin(-alpha)
       ypeq=yequis-1.*typm6(5)*dcos(-alpha)
       xdesp1x=typm5(5)*dsin(-alpha)
       xdesp1y=-typm5(5)*dcos(-alpha)
       xdesp2x=2.*typm5(5)*dsin(-alpha)
       xdesp2y=-2.*typm5(5)*dcos(-alpha)
       call point (psep+xpeq+2520*xkf,psey-ypeq,30)
       call point (psep+xpeq-xdesp1x+2520*xkf,psey-ypeq+xdesp1y,30)
       call point (psep+xpeq-xdesp2x+2520*xkf,psey-ypeq+xdesp2y,30)
       end if

c      Case 3: triangle 2 mm
       if (typm4(5).eq.3) then
       xpeq=xequis-typm6(5)*dsin(-alpha)
       ypeq=yequis+typm6(5)*dcos(-alpha)
       call mtriangle(psep+xpeq+2520*xkf,psey-ypeq,typm5(5),-alpha+pi,1)
       end if

       end if

       xlen=xlen+dsqrt((v(i,j,10)-v(i,j-1,10))**2.+(u(i,j,10)-
     + u(i,j-1,10))**2.)
       xlenp=xlen+dsqrt((v(i,j-1,10)-v(i,j-2,10))**2.+
     + (u(i,j-1,10)-u(i,j-2,10))**2.)

       end do ! j

       end do ! klz right side

       return
       end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUROUTINE ROMANO POINT I LINE 1-2
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE romanop(i,is,x1,y1,x2,y2,y3,psep,psey,xkf)

       real*8 x1,x2,x3,x4,y1,y2,y3,y4,xkf,psep,psey
       integer typm1(50),typm4(50),is
       real*8 typm2(50),typm3(50),typm5(50),typm6(50)
       real*8 alpha1,alpha2
       real*8 xu,xv,horz,vert,hipo
       real*8 u1,v1,u2,v2
       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

c      is=1    Extrados
c      is=-1   Intrados
       if (is.eq.1) then
       alpha1=-datan((y2-y1)/(x2-x1))
       end if
       if (is.eq.-1) then
       alpha1=-datan((y2-y1)/(x2-x1))+4.*atan(1.)
       end if
       horz=typm2(8)*dsqrt((x2-x1)**2.+(y2-y1)**2.)
       vert=typm3(8)*0.10d0
       hipo=dsqrt(horz*horz+vert*vert)
       alpha2=2.*datan(1.0d0)+alpha1

       u1=hipo*dcos(alpha1)
       v1=-hipo*dsin(alpha1)
       u2=u1-vert*dcos(alpha2)
       v2=v1+vert*dsin(alpha2)

       call romano(i+1,psep+x1+u2,y1+v2+psey,alpha1,typm6(8)*0.1,7)
       call romano(i+1,psep+x1+u2+2520.*xkf,y1+v2+psey,alpha1,
     + typm6(8)*0.1,7)

       return
       end





cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUROUTINE ROMANO POINT IN ARC using points 1-2
c      call subroutine arc3parc
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE romanoparc(i,iq,npunt,uf,vf,dfle,is,psep,psey,ic,xkf)

c      SUBROUTINE romanoparc(i,uu1,vv1,uu2,vv2,y3,psep,psey,xkf)


       real*8 uf(0:100,500,50),vf(0:100,500,50)
       real*8 psep,psey,dfle,sfle,tetha,omega,puntu(0:10),puntv(0:10)
       real*8 a,b,c,d,e,f,ep,eps,ep1,ep3,radi,epinc,bv,cv,xupp
       real*8 g,mu,xi,parcu(0:21),parcv(0:21),parcul(0:21),parcvl(0:21)
       real*8 parcve(0:21),parcue(0:21)
       real*8 xru(2),xrv(2),xsu(2),xsv(2)
       real*8 uu1,vv1,uu2,vv2,xlen1,xlen2,xlenco
       integer npunt,j,iq,ic,is,isn,kini,kfin,ii

       real*8 xkf
       integer typm1(50),typm4(50)
       real*8 typm2(50),typm3(50),typm5(50),typm6(50)
       real*8 alpha1,alpha2
       real*8 vert,hipo
       real*8 u1,v1,u2,v2
       common /markstypes/ typm1,typm2,typm3,typm4,typm5,typm6

c      Parameters interpretation:
c      iq=1  extrados
c      iq=-1 intrados
c      is=1  fletxa +
c      is=-1 fletxa -
c      ic=1  case print
c      ic=2  case laser


c      Sign control (negative 3D)
       isn=is
       ii=1
       if (dfle.lt.0.) then
       ii=-1
       end if
       isn=isn*ii

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      1. Selection points in the arc (based in subroutine arc3p)
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
       
       xlenco=typm2(8)  ! fraction of arc
       xupp=1.0d0 ! (no cal aquí)
       j=npunt

c      Evita radi infinit
       if (dabs(dfle).lt.0.000001d0) then
       dfle=0.00001d0 ! :)
       end if

c      ic=1 draw complete borders
c      ic=2 draw only external borders

c      Set basic points 1-2-3-4

       puntu(1)=uf(i,j,9)
       puntv(1)=vf(i,j,9)
       puntu(3)=uf(i,j,10)
       puntv(3)=vf(i,j,10)
       puntu(4)=0.5d0*(puntu(1)+puntu(3))
       puntv(4)=0.5d0*(puntv(1)+puntv(3))
       puntu(9)=puntu(3)
       puntv(9)=puntv(3)

       sfle=0.5d0*dsqrt((puntu(1)-puntu(3))**2.+(puntv(1)-puntv(3))**2.)
       tetha=datan(dfle/sfle)
       omega=datan((puntv(1)-puntv(3))/(puntu(3)-puntu(1)))
       if (isn.eq.1) then
       puntu(2)=puntu(4)+dfle*dsin(omega)
       puntv(2)=puntv(4)+dfle*dcos(omega)
       end if
       if (isn.eq.-1) then
       puntu(2)=puntu(4)-dfle*dsin(omega)
       puntv(2)=puntv(4)-dfle*dcos(omega)
       end if

c      Circle by 1-2-3 analytical solution
       a=2.0d0*(puntu(2)-puntu(1))
       b=2.0d0*(puntv(2)-puntv(1))
       c=puntu(1)*puntu(1)-puntu(2)*puntu(2)+
     + puntv(1)*puntv(1)-puntv(2)*puntv(2)
       d=2.0d0*(puntu(3)-puntu(2))
       e=2.0d0*(puntv(3)-puntv(2))
       f=puntu(2)*puntu(2)-puntu(3)*puntu(3)+
     + puntv(2)*puntv(2)-puntv(3)*puntv(3)
       puntv(0)=((c*d/a)-f)/(e-(b*d/a))
       puntu(0)=-(puntv(0)*b+c)/a
       radi=dsqrt((puntu(1)-puntu(0))**2.+(puntv(1)-puntv(0))**2.)

c      Consider points in an horizontal segment 1-3
       if (dabs(puntu(3)-puntu(1)).ge.0.01d0) then
       xi=datan((puntv(1)-puntv(3))/(puntu(1)-puntu(3)))
       end if

       g=dsqrt(radi*radi-sfle*sfle)
       mu=datan(sfle/g)

       puntu(3)=puntu(1)+2.0d0*sfle
       puntv(3)=puntv(1)
       puntu(0)=puntu(1)+sfle
       puntv(0)=puntv(1)-g

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      Arc internal
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

c      Arc global coordinates (u,v) using 21 points
       if (iq.eq.1) then ! extrados orientation
       do k=1,21
       ep=mu-(2.0d0*mu/20.0d0)*dfloat(k-1)
       parcu(k-1)=puntu(0)-radi*dsin(ep)
       parcv(k-1)=puntv(0)+radi*dcos(ep)
       end do
       end if
       if (iq.eq.-1) then ! intrados orientation
       do k=1,21
       ep=mu-(2.0d0*mu/20.0d0)*dfloat(k-1)
       parcu(21-k)=puntu(0)-radi*dsin(ep)
       parcv(21-k)=puntv(0)+radi*dcos(ep)
       end do
       end if

c      Arc local coordinates (u',v')
       do k=0,20
       parcul(k)=parcu(k)-puntu(1)
       parcvl(k)=dfloat(isn)*(parcv(k)-puntv(1))
       end do

c      Rotate local coordinates around punt 1
       do k=0,20
       parcu(k)=parcul(k)*dcos(xi)-parcvl(k)*dsin(xi)+puntu(1)
       parcv(k)=parcul(k)*dsin(xi)+parcvl(k)*dcos(xi)+puntv(1)
       end do

c      Draw rotated arc
       do k=1,20
c       call line(psep+parcu(k-1),psey-parcv(k-1)-5.,
c     + psep+parcu(k),psey-parcv(k)-5.,2)
       end do

c      Arc length
       xlen1=0.0d0
       do k=0,20-1
       xlen1=xlen1+dsqrt((parcu(k+1)-parcu(k))**2.+
     + (parcv(k+1)-parcv(k))**2.)
       end do

c      Detect kini and kfin
       xlen2=0.0d0
       do k=0,20-1
       xlen2=xlen2+dsqrt((parcu(k+1)-parcu(k))**2.+
     + (parcv(k+1)-parcv(k))**2.)
       if (xlen2.le.xlen1*xlenco) then
       kini=k
       kfin=k+2
       end if
       end do

c       write (*,*) i,kini,kfin,xlen1,xlen1*xlenco

c      Some arrangements...
       if (kini.ge.19) then
       kfin=20
       end if
       if (kfin.eq.20) then
       kini=18
       end if

c      Define especial points in the arc
       uu1=parcu(kini)
       vv1=parcv(kini)
       uu2=parcu(kfin)
       vv2=parcv(kfin)

ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      2. Romano calculus
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       alpha1=datan((vv2-vv1)/(uu2-uu1))
       vert=typm3(8)*0.10d0
       alpha2=2.*datan(1.0d0)+alpha1

       if (iq.eq.1) then
       u1=uu1
       v1=vv1
       u2=u1-vert*dcos(alpha2)
       v2=v1-vert*dsin(alpha2)
       end if

       if (iq.eq.-1) then
       u1=uu1
       v1=vv1
       u2=u1+vert*dcos(alpha2)
       v2=v1+vert*dsin(alpha2)
       alpha1=alpha1+4.*atan(1.)
       end if
       
       call romano(i+1,psep+u2,psey-v2,alpha1,typm6(8)*0.1,7)
       call romano(i+1,psep+u2+2520.*xkf,psey-v2,alpha1,typm6(8)*0.1,7)

       return
       end





cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUROUTINE REFORMAT DAT AIRFOILS
c      call subroutine datair
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE datair(i,rib,np,u,v)

      integer np(0:100,9),kini(0:100),kfin(0:100),npini,npfin
      integer jkini,jkfin
      real*8 u(0:100,500,99),v(0:100,500,99)
      real*8 rib(0:100,500),xini,xfin,yini,yfin,d0,d1,d2,d3,dm
      real*8 ucont(500),vcont(500)

c     Read and count airfoil points

      rewind (24)

      read (24,*)

c      Read up to 1000 points and exit if end of file

       k=1

       do 100 j=1,1000

       read (24,*,IOSTAT=io) u(i,j,1),v(i,j,1)

       write (*,*) i,k,u(i,j,1),v(i,j,1)

       k=k+1

c      Exit if end of file
       if (io.lt.0) goto 200

 100   continue

 200   continue

       np(i,1)=k-2
      
       write (*,*) "Num punts initial",np(i,1)

c      Set inlet points

       xini=rib(i,11)/100.
       xfin=rib(i,12)/100.
       kini(i)=0
       kfin(i)=0

       do j=1,np(i,1)

c      Detect xini and reasign if necesary

       if (u(i,j,1).le.xini.and.u(i,j+1,1).gt.xini.and.v(i,j,1).
     + le.0.0d0.and.rib(i,11).ge.0.0d0) then
       jkini=j
       write (*,*) "jkini= ",j

       d0=dsqrt((u(i,j,1)-u(i,j-1,1))**2.+(v(i,j,1)-v(i,j-1,1))**2.)
       xm=(v(i,j+1,1)-v(i,j,1))/(u(i,j+1,1)-u(i,j,1))
       xb=v(i,j,1)-xm*u(i,j,1)
       yini=xm*xini+xb
       d1=dsqrt((xini-u(i,j,1))**2.+(yini-v(i,j,1))**2.)
       d2=dsqrt((xini-u(i,j+1,1))**2.+(yini-v(i,j+1,1))**2.)
       d3=dsqrt((u(i,j+2,1)-u(i,j+1,1))**2.+(v(i,j+2,1)-v(i,j+1,1))**2.)
       dm=(d0+d1+d2+d3)/3.0d0

       write (*,*) "Ep ini"
       write (*,*) u(i,j,1),xini
       write (*,*) v(i,j,1),yini
       write (*,*) d0,d1,d2,d3,dm

       if (d1.lt.(dm/5.0)) then ! move point j to xini
       u(i,j,1)=xini
       v(i,j,1)=yini
       endif

       if (d2.lt.(dm/5.0)) then ! move point j+1 to xini
       u(i,j+1,1)=xini
       v(i,j+1,1)=yini
       endif

       if (d1.ge.(dm/5.0).and.d2.ge.(dm/5)) then ! add point
       kini=1
       endif

       end if ! xini

c      A verificar gràficament (!!!!) cas inici extrados
c      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       if (u(i,j,1).ge.xini.and.u(i,j+1,1).lt.xini.and.v(i,j,1).
     + gt.0.0d0.and.rib(i,11).lt.0.0d0) then
       jkini=j
       write (*,*) "jkini= ",j
       end if

c      Detect xfin and reasign if necesary

       if (u(i,j,1).le.xfin.and.u(i,j+1,1).gt.xfin.and.v(i,j,1).
     + le.0.0d0) then
       jkfin=j
       write (*,*) "jkfin= ",j

       d0=dsqrt((u(i,j,1)-u(i,j-1,1))**2.+(v(i,j,1)-v(i,j-1,1))**2.)
       xm=(v(i,j+1,1)-v(i,j,1))/(u(i,j+1,1)-u(i,j,1))
       xb=v(i,j,1)-xm*u(i,j,1)
       yfin=xm*xfin+xb
       d1=dsqrt((xfin-u(i,j,1))**2.+(yfin-v(i,j,1))**2.)
       d2=dsqrt((xfin-u(i,j+1,1))**2.+(yfin-v(i,j+1,1))**2.)
       d3=dsqrt((u(i,j+2,1)-u(i,j+1,1))**2.+(v(i,j+2,1)-v(i,j+1,1))**2.)
       dm=(d0+d1+d2+d3)/3.0d0

       write (*,*) "Ep fin"
       write (*,*) u(i,j,1),xfin
       write (*,*) v(i,j,1),yfin
       write (*,*) d0,d1,d2,d3,dm

       if (d1.lt.(dm/5.0)) then ! move point j to xini
       u(i,j,1)=xfin
       v(i,j,1)=yfin
       endif

       if (d2.lt.(dm/5.0)) then ! move point j+1 to xini
       u(i,j+1,1)=xfin
       v(i,j+1,1)=yfin
       endif

       if (d1.ge.(dm/5.0).and.d2.ge.(dm/5)) then ! add point
       kfin(i)=1
       endif

       end if ! xfin

       end do ! j

c      Points counting
       np(i,1)=np(i,1)+kini(i)+kfin(i)
       np(i,2)=jkini+kini(i)
       np(i,3)=jkfin-jkini+1
       np(i,4)=np(i,1)-jkfin+1+kfin(i)

       write (*,*) "np(i,1)= ",np(i,1)
       write (*,*) "np(i,2)= ",np(i,2)
       write (*,*) "np(i,3)= ",np(i,3)
       write (*,*) "np(i,4)= ",np(i,4)

c      Reasign airfoil points

    
c      Remap airfoils using predefined points

       npini=1
       npfin=np(i,2)
       npobj=66

       do j=npini,npfin
       ucont(j)=u(i,j,1)
       vcont(j)=v(i,j,1)
       end do

       call remapcont(npini,npfin,npobj,ucont,vcont)

       return
       end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE REMAP CONTOUR
c      call subroutine remapcont
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE remapcont (npini,npfin,npobj,ucont,vcont)

       integer npini,npfin,npobj
       real*8 ucont(500),vcont(500),dx(500),dy(500),da(0:500),ds(500)
       real*8 dxn(500),dyn(500),dsn(500),dan(0:500)
       real*8 xl,dm,dmn,dyy,xln


c      Remap airfoils using predefined points

c      Law of points distribution

       xl=0.0d0
       da(npini-1)=0.0d0

c      Contour length
       do j=npini,npfin-1
       xl=xl+dsqrt((ucont(j)-ucont(j+1))**2.0+(vcont(j)
     + -vcont(j+1))**2.0)
       end do

       dm=xl/dfloat(npfin-npini)

       write (*,*) "Ep reformat"
       write (*,*) npini,npfin

c      Law of points distribution
       do j=npini,npfin-1
       dy(j)=dsqrt((ucont(j)-ucont(j+1))**2.+(vcont(j)-vcont(j+1))**2.)
     + /dm
       ds(j)=dsqrt((ucont(j)-ucont(j+1))**2.0+(vcont(j)
     + -vcont(j+1))**2.0)
       da(j)=da(j-1)+ds(j)
       dx(j)=da(j-1)/xl
       write (*,*) j,ds(j)*100.,da(j)*100.,dx(j)
       end do
       dx(npfin)=1.0d0
       dy(npfin)=dy(npfin-1)
       write (*,*) xl*100.

       write (*,*) "Law of points distribution"
       do j=npini,npfin
       write (*,*) j,dx(j),dy(j)
       end do

c      Reformat unitari segment

       dmn=1.0d0/dfloat(npobj-1)
       dan(0)=0.0d0
       dsn(0)=0.0d0
       xln=0.0d0

       do k=1,npobj-1

       dsn(k)=dmn*dyy

       dxn(k)=dmn*dfloat(k-1)

c       write (*,*) k,dxn(k)

c      Detect point
       do j=npini,npfin
       if (dxn(k).ge.dx(j).and.dxn(k).lt.dx(j+1)) then
       dyn(k)=dy(j)
       end if
       end do 

       dsn(k)=dmn*dyn(k)
       dan(k)=dan(k-1)+dsn(k-1)

       xln=xln+dsn(k-1)

       write (*,*) k,dsn(k)*100.,dan(k)*100.

       

       end do ! k

       write (*,*) "XLN= ",xln*100.

c      Scale contour

c      Old contour (xl)
c      New contor  (xln)
c      Scale factor xl/xln

c      Reformat contour

       do k=1,npobj-1

c      Detect point
       do j=npini,npfin-1
       if (dan(k).ge.da(j).and.dan(k).lt.da(j+1)) then
       dyn(k)=dy(j)
       end if

      
       end do


       end do ! k


       return
       end



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE xyzt
c      Rotates points in airfoils in tree axes and moves
c      to absolute ccordinates
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE xyzt(i,j,u,v,w,rib,np,u_aux,v_aux,w_aux)

       real*8 u(0:100,500,99),v(0:100,500,99),w(0:100,500,99) ! airfoil 3D
       real*8 rib(0:100,500)
       real*8 u_aux(0:100,500,10),v_aux(0:100,500,10),
     + w_aux(0:100,500,10)
       real*8 pi,tetha,rot_z,pos
       integer np(0:100,9)

       pi=4.0d0*datan(1.0d0)
       tetha=rib(i,8)*pi/180.0d0
       rot_z=rib(i,250)*pi/180.0d0
       pos=rib(i,5)*rib(i,251)/100.0d0

c      Starts with scaled and Z DISPLACED coordinates (i,j,3)

c      Washin rotation around X-axis
       u_aux(i,j,2)=(u_aux(i,j,1)-(rib(i,10)/100.)*rib(i,5))*
     + dcos(tetha)+(v_aux(i,j,1))*dsin(tetha)+(rib(i,10)/100.)*rib(i,5)
       v_aux(i,j,2)=(-u_aux(i,j,1)+(rib(i,10)/100.)*rib(i,5))*
     + dsin(tetha)+(v_aux(i,j,1))*dcos(tetha)
       w_aux(i,j,2)=0.0d0

c      Rotation around Z-axis
       w_aux(i,j,3)=-u_aux(i,j,2)*dsin(rot_z)+pos*dsin(rot_z)
       u_aux(i,j,3)=u_aux(i,j,2)*dcos(rot_z)+pos*(1-dcos(rot_z))
       v_aux(i,j,3)=v_aux(i,j,2)

c      Rotation around Y-axis
       w_aux(i,j,4)=-w_aux(i,j,3)*dcos(rib(i,9)*pi/180.)-
     + v_aux(i,j,3)*dsin(rib(i,9)*pi/180.)
       u_aux(i,j,4)=u_aux(i,j,3)
       v_aux(i,j,4)=-w_aux(i,j,3)*dsin(rib(i,9)*pi/180.)+
     + v_aux(i,j,3)*dcos(rib(i,9)*pi/180.)

c      Move to absolute coordinates
       w_aux(i,j,5)=rib(i,6)-w_aux(i,j,4)
       u_aux(i,j,5)=rib(i,3)+u_aux(i,j,4)
       v_aux(i,j,5)=rib(i,7)-v_aux(i,j,4)

       return
       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE elliquad
c      Draw ellipses inside quadrilaters
c      Use in vents type 6 and -6
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE elliquad(pgx,pgy,param1,param2)

       real*8 pgx(100),pgy(100) ! generic point
       real*8 param1,param2
       real*8 pi,tetha,angle1,angleinc
       real*8 xp1,yp1,x1,y1,xp2,yp2,x2,y2
       real*8 a,b,distance,distance1,distance2

       pi=4.0d0*datan(1.0d0)

c      Auxiliar points in the quadrilater P1-P2-P3-P4
       pgx(5)=0.5*(pgx(1)+pgx(4))
       pgy(5)=0.5*(pgy(1)+pgy(4))
       pgx(6)=0.5*(pgx(2)+pgx(3))
       pgy(6)=0.5*(pgy(2)+pgy(3))
       pgx(9)=0.5*(pgx(5)+pgx(6))
       pgy(9)=0.5*(pgy(5)+pgy(6))

c      Ellipse angle
       tetha=datan((pgy(6)-pgy(5))/(pgx(6)-pgx(5)))

c      Distance P9-P8
       call distpr(pgx(1),pgy(1),pgx(2),pgy(2),pgx(9),pgy(9),distance)
       distance1=distance
c      Distance P9-P7
       call distpr(pgx(4),pgy(4),pgx(3),pgy(3),pgx(9),pgy(9),distance)
       distance2=distance

c      Definition of ellipse semiaxis
       a=(param1/200.)*dsqrt((pgx(5)-pgx(6))*(pgx(5)-pgx(6))+
     + (pgy(5)-pgy(6))*(pgy(5)-pgy(6)))
       b=(param2/200.)*(distance1+distance2)

c      Draw ellipses in 50 points
       angleinc=2.0d0*pi/dfloat(50)
       do i=1,50
       angle1=angleinc*dfloat(i-1)
       xp1=a*dcos(angle1)
       yp1=b*dsin(angle1)
       x1=xp1*dcos(tetha)-yp1*dsin(tetha)
       y1=xp1*dsin(tetha)+yp1*dcos(tetha)
       xp2=a*dcos(angle1+angleinc)
       yp2=b*dsin(angle1+angleinc)
       x2=xp2*dcos(tetha)-yp2*dsin(tetha)
       y2=xp2*dsin(tetha)+yp2*dcos(tetha)
       call line(pgx(9)+x1,pgy(9)+y1,pgx(9)+x2,pgy(9)+y2,3)
       end do

       return
       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE distpr
c      Distance between point P3 and line r (P1-P2)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE distpr(p1x,p1y,p2x,p2y,p3x,p3y,distance)

       real*8 p1x,p1y,p2x,p2y,p3x,p3y,distance
       real*8 A,B,C

c      Line Ax+By+C=0 by points P1,P2
       A=(p2y-p1y)/(p2x-p1x)
       B=-1.0d0
       C=(p2x*p1y-p1x*p2y)/(p2x-p1x)

c      Manage case A*A+B*B=0 !!!!!!!

c      Distance point P3 to line P1-P2
       distance=dabs((A*p3x+B*p3y+C)/dsqrt(A*A+B*B))

c      Manage special cases
c      Case p2x=p1x
       if (dabs(p2x-p1x).lt.0.001d0) then
       distance=dabs(p3x-p1x)
       end if

       return
       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE arcfle
c      Draw arc known the segment 1-2 and the arrow flet
c      Arc between points P1-P2, arrow flet, sign, and color
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE arcfle(p1x,p1y,p2x,p2y,flet,iflet,isvet)

       real*8 p1x,p1y,p2x,p2y,p3x,p3y,p4x,p4y,p5x,p5y,flet
       real*8 p6x,p6y,p7x,p7y
       real*8 R,h,s,tethaa
       real*8 tetha,omega,angle,angle0,incangle,pi,sgn
       integer iflet,isvet

       pi=4.0d0*datan(1.0d0)

c      Anticipate the case fle=0.0
       if (flet.le.0.01d0) then
       flet=0.01d0
       end if

c      Solve the circle x^2+y^2=R^2
       s=dsqrt((p2y-p1y)*(p2y-p1y)+(p2x-p1x)*(p2x-p1x))
       h=((s*s/4.)-flet*flet)/(2.*flet)
       R=flet+h

c      Draw arc
       sgn=dfloat(iflet)
       tethaa=datan((p2y-p1y)/(p2x-p1x))
       p3x=0.5*(p1x+p2x)
       p3y=0.5*(p1y+p2y)
       p4x=p3x+sgn*flet*dsin(tethaa)
       p4y=p3y-sgn*flet*dcos(tethaa)
       p5x=p3x-sgn*h*dsin(tethaa)
       p5y=p3y+sgn*h*dcos(tethaa)
       omega=datan(0.5d0*s/h)

       incangle=2.*omega/20.0d0
       angle0=0.5*pi-(tethaa+omega)

c       call line(p1x,p1y,p2x,p2y,3)
c       call line(p3x,p3y,p4x,p4y,2)
c       call line(p3x,p3y,p5x,p5y,1)

       do k=1,20
       angle=angle0+incangle*dfloat(k-1)
       p6x=p5x+sgn*R*dcos(angle)
       p6y=p5y-sgn*R*dsin(angle)
       p7x=p5x+sgn*R*dcos(angle+incangle)
       p7y=p5y-sgn*R*dsin(angle+incangle)
       call line(p6x,p6y,p7x,p7y,isvet)
       end do

       return
       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE interpoly2D
c      Interpolate a point in a 2D polyline
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE interpoly2d(xpoly,ypoly,x_poly,y_poly
     + ,xpolylen,npoly1,npoly2,npoly3,distrel)

       real*8 xpoly(500),ypoly(500),x_poly,y_poly,xpolylen
       real*8 xacum1,xacum2,angle,pi,dist,distrel
       integer npoly1,npoly2,npoly3

       pi=4.0d0*datan(1.0d0)

       xacum1=0.0d0
       xacum2=0.0d0

       do j=npoly1,npoly2-1

       xacum2=xacum2+dsqrt((xpoly(j+1)-xpoly(j))*(xpoly(j+1)-xpoly(j))+
     + (ypoly(j+1)-ypoly(j))*(ypoly(j+1)-ypoly(j)))

c      Detect segment and interpolate easy (without angles!)
       if (xpolylen.ge.xacum1.and.xpolylen.le.xacum2) then

       dist=xpolylen-xacum1
       distrel=dist/(xacum2-xacum1) ! Relative distance in interpolation segment
       x_poly=xpoly(j)+distrel*(xpoly(j+1)-xpoly(j))
       y_poly=ypoly(j)+distrel*(ypoly(j+1)-ypoly(j))

       npoly3=j

       end if

       xacum1=xacum2
  
       end do

       return
       end

cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      SUBROUTINE interpoly3D
c      Interpolate a point in a 2D polyline
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

       SUBROUTINE interpoly3d(xpoly,ypoly,zpoly,x_poly,y_poly,z_poly,
     + xpolylen,npoly1,npoly2,npoly3,distrel)

       real*8 xpoly(500),ypoly(500),zpoly(500),x_poly,y_poly,z_poly
       real*8 xpolylen,xacum1,xacum2,angle,pi,dist,distrel
       integer npoly1,npoly2,npoly3

       pi=4.0d0*datan(1.0d0)

       xacum1=0.0d0
       xacum2=0.0d0

       do j=npoly1,npoly2-1

       xacum2=xacum2+dsqrt((xpoly(j+1)-xpoly(j))*(xpoly(j+1)-xpoly(j))+
     + (ypoly(j+1)-ypoly(j))*(ypoly(j+1)-ypoly(j))+
     + (zpoly(j+1)-zpoly(j))*(zpoly(j+1)-zpoly(j)))

c      Detect segment and interpolate easy (without angles!)
       if (xpolylen.ge.xacum1.and.xpolylen.le.xacum2) then

       dist=xpolylen-xacum1
       distrel=dist/(xacum2-xacum1) ! Relative distance in interpolation segment
       x_poly=xpoly(j)+distrel*(xpoly(j+1)-xpoly(j))
       y_poly=ypoly(j)+distrel*(ypoly(j+1)-ypoly(j))
       z_poly=zpoly(j)+distrel*(zpoly(j+1)-zpoly(j))

       npoly3=j

       end if

       xacum1=xacum2

       end do

       return
       end

