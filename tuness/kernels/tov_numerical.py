F77_TOV_DERIVS = r"""
      Subroutine derivs(r,y,dydr)
      Implicit None
      Integer flag
      Real*8 r,y(3),dydr(3)
      Real*8 p,e,m,dpdr,dmdr,dadr,baryon,pi
      Real*8 ms,gms
      Data ms,gms/5660.57d0,1.47556d0/
      Data pi/3.1415926535897d0/

      If(r.eq.0.d0)Then
            dydr(1)=0.d0
            dydr(2)=0.d0
            dydr(3)=0.d0
      Else
            p=y(1)
            Call sfe(p,e,flag)
            m=y(2)
            Call sfb(e,baryon,flag)
            baryon=baryon*939.d0/197.33d0
            dpdr=-(e+p)*(m+4.d0*pi*r**3*p/ms)/(r**2/gms-2.d0*r*m)
            dmdr=4.d0*pi*r**2*e/ms
            dadr=4.d0*pi*(1.d0-2.d0*m/(r/gms))**(-0.5d0)*r*r*baryon/ms
            dydr(1)=dpdr
            dydr(2)=dmdr
            dydr(3)=dadr
      End If

      Return
      End
"""

F77_TOV_SFB = r"""
      Subroutine sfb(ex,fb,flag)
      Implicit None
      Integer dime
      Parameter (dime=9000)
      Integer ndat,flag
      Real*8 e(dime),p(dime),e2(dime),p2(dime)
      Real*8 rho(dime),b2(dime)
      Real*8 ex,fb
      Common/Cf/e,p,rho,e2,p2,b2,ndat
      flag=0
      If(ex.lt.e(1).or.ex.gt.e(ndat))Then
            flag=1
      Else
            Call splint(e,rho,b2,ndat,ex,fb)
      End If

      Return
      End
"""

F77_TOV_SFP = r"""
      Subroutine sfp(ex,fp,flag)
      Implicit None
      Integer dime
      Parameter (dime=9000)
      Integer ndat,flag
      Real*8 e(dime),p(dime),e2(dime),p2(dime)
      Real*8 rho(dime),b2(dime)
      Real*8 ex,fp
      Common/Cf/e,p,rho,e2,p2,b2,ndat

      flag=0
      If(ex.lt.e(1).or.ex.gt.e(ndat))Then
            flag=1
      Else
            Call splint(e,p,p2,ndat,ex,fp)
      End If

      Return
      End
"""

F77_TOV_SFE = r"""
      Subroutine sfe(px,fe,flag)
      Implicit None
      Integer dime
      Parameter (dime=9000)
      Real*8 e(dime),p(dime),e2(dime),p2(dime)
      Real*8 rho(dime),b2(dime)
      Integer ndat,flag
      Real*8 px,fe
      Common/Cf/e,p,rho,e2,p2,b2,ndat

      flag=0
      If(px.lt.p(1))Then
            fe=0.d0
            Write(6,*)'Warning: attemp to use a pressure less than
     ^Pmin in tov.inp!'
            Write(6,*)'P=',px,'Pmin=',p(1)
            flag=1
      Else
            Call splint(p,e,e2,ndat,px,fe)
      End If

      Return
      End
"""

F77_TOV_SPLINE = r""""
      SUBROUTINE spline(x,y,n,yp1,ypn,y2)
      INTEGER n,NMAX
      REAL*8 yp1,ypn,x(n),y(n),y2(n)
      PARAMETER (NMAX=9000)
      INTEGER i,k
      REAL*8 p,qn,sig,un,u(NMAX)
      if (yp1.gt..99d30) then
        y2(1)=0.d0
        u(1)=0.d0
      else
        y2(1)=-0.5d0
        u(1)=(3.d0/(x(2)-x(1)))*((y(2)-y(1))/(x(2)-x(1))-yp1)
      endif
      do 11 i=2,n-1
        sig=(x(i)-x(i-1))/(x(i+1)-x(i-1))
        p=sig*y2(i-1)+2.d0
        y2(i)=(sig-1.d0)/p
        u(i)=(6.d0*((y(i+1)-y(i))/(x(i+
     *1)-x(i))-(y(i)-y(i-1))/(x(i)-x(i-1)))/(x(i+1)-x(i-1))-sig*
     *u(i-1))/p
11    continue
      if (ypn.gt..99d30) then
        qn=0.d0
        un=0.d0
      else
        qn=0.5d0
        un=(3.d0/(x(n)-x(n-1)))*(ypn-(y(n)-y(n-1))/(x(n)-x(n-1)))
      endif
      y2(n)=(un-qn*u(n-1))/(qn*y2(n-1)+1.d0)
      do 12 k=n-1,1,-1
        y2(k)=y2(k)*y2(k+1)+u(k)
12    continue
      return
      END
"""

F77_TOV_SPLINT = r"""
      SUBROUTINE splint(xa,ya,y2a,n,x,y)
      INTEGER n
      REAL*8 x,y,xa(n),y2a(n),ya(n)
      INTEGER k,khi,klo
      REAL*8 a,b,h
      klo=1
      khi=n
1     if (khi-klo.gt.1) then
        k=(khi+klo)/2
        if(xa(k).gt.x)then
          khi=k
        else
          klo=k
        endif
      goto 1
      endif
      h=xa(khi)-xa(klo)
      if (h.eq.0.d0) stop ! 'bad xa input in splint'
      a=(xa(khi)-x)/h
      b=(x-xa(klo))/h
      y=a*ya(klo)+b*ya(khi)+((a**3-a)*y2a(klo)+(b**3-b)*y2a(khi))*(h**
     *2)/6.d0
      return
      END
"""

F77_TOV_ODEINT = r"""
      SUBROUTINE odeint(ystart,nvar,x1,x2,eps,h1,hmin,nok,nbad,derivs,
     *rkqs)
      INTEGER nbad,nok,nvar,KMAXX,MAXSTP,NMAX
      REAL*8 eps,h1,hmin,x1,x2,ystart(nvar),TINY
      EXTERNAL derivs,rkqs
      PARAMETER (MAXSTP=90000,NMAX=3,KMAXX=3000,TINY=1.d-30)
      INTEGER i,kmax,kount,nstp
      REAL*8 dxsav,h,hdid,hnext,x,xsav,dydx(NMAX),xp(KMAXX),y(NMAX),
     *yp(NMAX,KMAXX),yscal(NMAX)
      Real*8 Pmin,Pnew                      !MC 10/96
      Common/CPmin/Pmin                     !MC 10/96
      COMMON /path/ kmax,kount,dxsav,xp,yp
      x=x1
      h=sign(h1,x2-x1)
      nok=0
      nbad=0
      kount=0
      do 11 i=1,nvar
        y(i)=ystart(i)
11    continue
      if (kmax.gt.0) xsav=x-2.d0*dxsav
      do 16 nstp=1,MAXSTP
        call derivs(x,y,dydx)
        do 12 i=1,nvar
          yscal(i)=abs(y(i))+abs(h*dydx(i))+TINY
12      continue
        if(kmax.gt.0)then
          if(abs(x-xsav).gt.abs(dxsav)) then
            if(kount.lt.kmax-1)then
              kount=kount+1
              xp(kount)=x
              do 13 i=1,nvar
                yp(i,kount)=y(i)
13            continue
              xsav=x
            endif
          endif
        endif
        if((x+h-x2)*(x+h-x1).gt.0.d0) h=x2-x
        Pnew=y(1)+h*dydx(1)                 !MC 10/96
        If(Pnew.le.Pmin)Return              !MC 10/96
        call rkqs(y,dydx,nvar,x,h,eps,yscal,hdid,hnext,derivs)
        if(hdid.eq.h)then
          nok=nok+1
        else
          nbad=nbad+1
        endif
        if((x-x2)*(x2-x1).ge.0.d0)then
          do 14 i=1,nvar
            ystart(i)=y(i)
14        continue
          if(kmax.ne.0)then
            kount=kount+1
            xp(kount)=x
            do 15 i=1,nvar
              yp(i,kount)=y(i)
15          continue
          endif
          return
        endif
        if(abs(hnext).lt.hmin) pause
     *'stepsize smaller than minimum in odeint'
        h=hnext
16    continue
      stop ! 'too many steps in odeint'
      return
      END
"""

F77_TOV_RKQS = r"""
      SUBROUTINE rkqs(y,dydx,n,x,htry,eps,yscal,hdid,hnext,derivs)
      INTEGER n,NMAX
      DOUBLE PRECISION eps,hdid,hnext,htry,x,dydx(n),y(n),yscal(n)
      EXTERNAL derivs
      PARAMETER (NMAX=50)
CU    USES derivs,rkck
      INTEGER i
      DOUBLE PRECISION errmax,h,htemp,xnew,yerr(NMAX),ytemp(NMAX),SAFETY
     *,PGROW,
     *PSHRNK,ERRCON
      PARAMETER (SAFETY=0.9d0,PGROW=-.2d0,PSHRNK=-.25d0,ERRCON=1.89d-4)
      h=htry
1     call rkck(y,dydx,n,x,h,ytemp,yerr,derivs)
      errmax=0.d0
      do 11 i=1,n
        errmax=max(errmax,abs(yerr(i)/yscal(i)))
11    continue
      errmax=errmax/eps
      if(errmax.gt.1.d0)then
        htemp=SAFETY*h*(errmax**PSHRNK)
        h=sign(max(abs(htemp),0.1d0*abs(h)),h)
        xnew=x+h
        if(xnew.eq.x)stop
        goto 1
      else
        if(errmax.gt.ERRCON)then
          hnext=SAFETY*h*(errmax**PGROW)
        else
          hnext=5.d0*h
        endif
        hdid=h
        x=x+h
        do 12 i=1,n
          y(i)=ytemp(i)
12      continue
        return
      endif
      END
"""

F77_TOV_RKCK = r"""
      SUBROUTINE rkck(y,dydx,n,x,h,yout,yerr,derivs)
      INTEGER n,NMAX
      DOUBLE PRECISION h,x,dydx(n),y(n),yerr(n),yout(n)
      EXTERNAL derivs
      PARAMETER (NMAX=50)
CU    USES derivs
      INTEGER i
      DOUBLE PRECISION ak2(NMAX),ak3(NMAX),ak4(NMAX),ak5(NMAX),ak6(NMAX)
     *,
     *ytemp(NMAX),A2,A3,A4,A5,A6,B21,B31,B32,B41,B42,B43,B51,B52,B53,
     *B54,B61,B62,B63,B64,B65,C1,C3,C4,C6,DC1,DC3,DC4,DC5,DC6
      PARAMETER (A2=.2d0,A3=.3d0,A4=.6d0,A5=1.d0,A6=.875d0,B21=.2d0,B31
     *=3.d0/40.d0,
     *B32=9.d0/40.d0,B41=.3d0,B42=-.9d0,B43=1.2d0,B51=-11.d0/54.d0,B52
     *=2.5d0,
     *B53=-70.d0/27.d0,B54=35.d0/27.d0,B61=1631.d0/55296.d0,B62=175.d0
     */512.d0,
     *B63=575.d0/13824.d0,B64=44275.d0/110592.d0,B65=253.d0/4096.d0,C1
     *=37.d0/378.d0,
     *C3=250.d0/621.d0,C4=125.d0/594.d0,C6=512.d0/1771.d0,DC1=C1-2825.d0
     */27648.d0,
     *DC3=C3-18575.d0/48384.d0,DC4=C4-13525.d0/55296.d0,DC5=-277.d0
     */14336.d0,
     *DC6=C6-.25d0)
      do 11 i=1,n
        ytemp(i)=y(i)+B21*h*dydx(i)
11    continue
      call derivs(x+A2*h,ytemp,ak2)
      do 12 i=1,n
        ytemp(i)=y(i)+h*(B31*dydx(i)+B32*ak2(i))
12    continue
      call derivs(x+A3*h,ytemp,ak3)
      do 13 i=1,n
        ytemp(i)=y(i)+h*(B41*dydx(i)+B42*ak2(i)+B43*ak3(i))
13    continue
      call derivs(x+A4*h,ytemp,ak4)
      do 14 i=1,n
        ytemp(i)=y(i)+h*(B51*dydx(i)+B52*ak2(i)+B53*ak3(i)+B54*ak4(i))
14    continue
      call derivs(x+A5*h,ytemp,ak5)
      do 15 i=1,n
        ytemp(i)=y(i)+h*(B61*dydx(i)+B62*ak2(i)+B63*ak3(i)+B64*ak4(i)+
     *B65*ak5(i))
15    continue
      call derivs(x+A6*h,ytemp,ak6)
      do 16 i=1,n
        yout(i)=y(i)+h*(C1*dydx(i)+C3*ak3(i)+C4*ak4(i)+C6*ak6(i))
16    continue
      do 17 i=1,n
        yerr(i)=h*(DC1*dydx(i)+DC3*ak3(i)+DC4*ak4(i)+DC5*ak5(i)+DC6*
     *ak6(i))
17    continue
      return
      END
"""