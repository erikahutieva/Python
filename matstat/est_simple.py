from scipy.optimize import minimize
from scipy import stats
import scipy.special as sc
from numpy import linalg
from more_itertools import distinct_permutations as dp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter
from pandas.core.common import flatten
from time import time
import math


##############################################################################################
def distr(Distr_Name,Distr_Type,a=0,s=1,x=0,p=0.5,df=3,df1=3,df2=3,nc=0):
    rez=0
    match Distr_Name.split():
        case ["Norm"]:
            if Distr_Type=="cdf": rez=stats.norm.cdf(x,a,s) #Cumulative distribution function
            if Distr_Type=="ppf": rez=stats.norm.ppf(p) #Percent point function (inverse of cdf — percentiles)
            if Distr_Type=="pdf": rez=stats.norm.pdf(x,a,s) #Probability density function
        case ["T"]:
            if Distr_Type=="cdf": rez=stats.t.cdf(x,df)
            if Distr_Type=="ppf": rez=stats.t.ppf(p,df)
            if Distr_Type=="pdf": rez=stats.t.pdf(x,df)
        case ["Chi2"]:
            if Distr_Type=="cdf": rez=stats.chi2.cdf(x,df)
            if Distr_Type=="ppf": rez=stats.chi2.ppf(p,df)
            if Distr_Type=="pdf": rez=stats.chi2.pdf(x,df)
        case ["F"]:
            if Distr_Type=="cdf": rez=stats.f.cdf(x,df1,df2)
            if Distr_Type=="ppf": rez=stats.f.ppf(p,df1,df2)
            if Distr_Type=="pdf": rez=stats.f.pdf(x,df1,df2)
        case ["NonCT"]:
            if Distr_Type=="cdf": rez=stats.nct.cdf(x,df,nc)
            if Distr_Type=="ppf": rez=stats.nct.ppf(p,df,nc)
            if Distr_Type=="pdf": rez=stats.nct.pdf(x,df,nc)
        case ["Beta"]:
            if Distr_Type=="cdf": rez=stats.beta.cdf(x,df)
            if Distr_Type=="ppf": rez=stats.beta.ppf(p,df)
            if Distr_Type=="pdf": rez=stats.beta.pdf(x,df)
        case ["Gamma"]:
            if Distr_Type=="cdf": rez=stats.gamma.cdf(x,df)
            if Distr_Type=="ppf": rez=stats.gamma.ppf(p,df)
            if Distr_Type=="pdf": rez=stats.gamma.pdf(x,df)

    return(rez)
#########################################
def prints(txt,x,f):
    kr=len(x)
    print(txt,file=f)
    for i in range(kr):
         if(i<(kr-1)):print(x[i],end=" ",file=f)
         if(i==(kr-1)):print(x[i],file=f)
#######################################

def MLE_Normal():
    finp=open("Inp\MLE_Normal.inp")
    finp.readline()
    n=int(finp.readline())
    ss=finp.readline()
    beta=float(finp.readline())
    ss=finp.readline()
    y=tuple(map(float,finp.readline().split(" ")))
    ss=finp.readline()
    kp=int(finp.readline())
    ss=finp.readline()
    p=tuple(map(float,finp.readline().split(" ")))
    finp.close()

    fout=open('Out\MLE_Normal.out','w')
    n=len(y)

    print("MO and Std by observed values",file=fout)
 
    a=np.average(y)
    s=np.sqrt(n/(n-1))*np.std(y)
    print("a=",a,file=fout)
    print("s=",s,file=fout)
    print("Sample size n=",n,file=fout)
    prints("Sample:",y,fout)

    w=cum(n)
    print("Observed values sample size n=",len(w),file=fout)
    prints("Empirical probability:",w,fout)
    w=stats.norm.ppf(w)
    zp=stats.norm.ppf(p)
    delta=zp*np.sqrt(n)
    print("Tolerance probability=",beta,file=fout)
    f=n-1

    tlow,tup=nctlimit_exact(f,beta,delta)

    prints("Probability range:",p,fout)
    prints("Normal quantiles:",w,fout)
    prints("Upper non central t quantile",tup,fout)
    prints("Low non central t quantile",tlow,fout)
    xp=a+s*zp
    xpup=a+s*tup/np.sqrt(n)
    xplow=a+s*tlow/np.sqrt(n)
    prints("Upper tolerance limit",xpup,fout)
    prints("Quantile estimations",xp,fout)
    prints("Low tolerance limit",xplow,fout)
    fout.close()

    show_distr("Normal",True,True,y,w,xp,zp,xplow,zp,xpup,zp,grid_size=n,distr_name=r'$N({a=}$'+str(round(a,4))+",${s=}$"+str(round(s,4))+")")

#########################################################################################
def MLE_Weibull():

    finp=open("Inp\MLE_Weibull.inp")
    finp.readline()
    n=int(finp.readline())
    ss=finp.readline()
    beta=float(finp.readline())
    ss=finp.readline()
    y=tuple(map(float,finp.readline().split(" ")))
    ss=finp.readline()
    kp=int(finp.readline())
    ss=finp.readline()
    p=tuple(map(float,finp.readline().split(" ")))
    finp.close()

    fout=open('Out\MLE_Weibull.out','w')
    n=len(y)
    b=0.5
    c=1.5
    bnds = ((0, None), (0, None))

    res=minimize(WeibullMinFunction,(b,c),args=(y,n), method='Nelder-Mead',bounds=bnds, tol=1e-12,options={'disp': True})

    b=res.x[0]
    c=(sum(y**b))/n
    a=(np.log(c))/b
    s=1/b 
    print("b and c by MLE",file=fout)
    print("a=",a,"s=",s,file=fout)
    print("FunMin="+str(WeibullMinFunction(res.x,y,n)),file=fout)
    print("Sample size n=",n,file=fout)
    prints("Sample:",y,fout)
  
    y=np.log(y)
    wcum=cum(n)
    zwcum=np.log(np.log(1/(1-np.array(wcum))))
    zw=np.log(np.log(1/(1-np.array(p))))
    v=CovMatrixMleW(n,(y-a)/s)
    t1=v[0][0];t2=v[1][1];t12=v[0][1] 

    print("Observed values sample size n=",n,file=fout)
    prints("Empiricalr probability:",wcum,fout)
    print("Tolerance probability=",beta,file=fout)
    
    tlow,tup=nctlimit_app(n,beta,zw,t1,t2,t12)

    prints("Probability range:",p,fout)
    prints("Weibull quantiles:",zw,fout)
    prints("Upper non central t quantile",tup,fout)
    prints("Low non central t quantile",tlow,fout)
    xp=a+zw*s
    xpup=a+s*tup/np.sqrt(n)
    xplow=a+s*tlow/np.sqrt(n)
    prints("Upper tolerance limit",xpup,fout)
    prints("Quantile estimations",xp,fout)
    prints("Low tolerance limit",xplow,fout)
    fout.close()
  
    show_distr("Weibull",True,True,y,zwcum,xp,zw,xplow,zw,xpup,zw,grid_size=n, distr_name=r'$N({a=}$'+str(round(a,4))+",${s=}$"+str(round(s,4))+")")

######################################################

def MLS_Normal():
    finp=open("Inp\MLS_Normal.inp")
    finp.readline()
    n=int(finp.readline())
    ss=finp.readline()
    beta=float(finp.readline())
    ss=finp.readline()
    y=tuple(map(float,finp.readline().split(" ")))
    ss=finp.readline()
    kp=int(finp.readline())
    ss=finp.readline()
    p=tuple(map(float,finp.readline().split(" ")))
    finp.close()

    fout=open('Out\MLS_Normal.out','w')
    n=len(y)
    print("MO and Std by observed values",file=fout)
 
    b,db=mlsordern(n,y)          
    a=b[0]
    s=b[1]

    print("a=",a,file=fout)
    print("s=",s,file=fout)
    print("Sample size n=",n,file=fout)
    prints("Sample:",y,fout)

    w=cum(n)
    print("Observed values sample size n=",len(w),file=fout)
    prints("Empirical probability:",w,fout)
    w=stats.norm.ppf(w)
    zp=stats.norm.ppf(p)
    delta=zp*np.sqrt(n)
    print("Tolerance probability=",beta,file=fout)
    f=n-1

    db=db*n
    print("D{b}=",db,file=fout)
    t1=db[0][0];t2=db[1][1];t12=db[0][1] 
 
    print("Tolerance probability=",beta,file=fout)
    tlow,tup=nctlimit_app(n,beta,zp,t1,t2,t12)   

    #tlow,tup=nctlimit_exact(f,beta,delta)

    prints("Probability range:",p,fout)
    prints("Normal quantiles:",w,fout)
    prints("Upper non central t quantile",tup,fout)
    prints("Low non central t quantile",tlow,fout)
    xp=a+s*zp
    xpup=a+s*tup/np.sqrt(n)
    xplow=a+s*tlow/np.sqrt(n)
    prints("Upper tolerance limit",xpup,fout)
    prints("Quantile estimations",xp,fout)
    prints("Low tolerance limit",xplow,fout)
    fout.close()

    show_distr("Normal",True,True,y,w,xp,zp,xplow,zp,xpup,zp,grid_size=n,distr_name=r'$N({a=}$'+str(round(a,4))+",${s=}$"+str(round(s,4))+")")

###############################################

def MLS_Weibull():
    finp=open("Inp\MLS_Weibull.inp")
    finp.readline()
    n=int(finp.readline())
    ss=finp.readline()
    beta=float(finp.readline())
    ss=finp.readline()
    y=tuple(map(float,finp.readline().split(" ")))
    ss=finp.readline()
    kp=int(finp.readline())
    ss=finp.readline()
    p=tuple(map(float,finp.readline().split(" ")))
    finp.close()

    fout=open('Out\MLS_Weibull.out','w')
    n=len(y)
   
    logy=np.log(y)
    bw,db=mlsorderw(n,logy)         
    db=db*n
    print("D{b}=",db,file=fout)

    wcum=cum(n)
    zwcum=np.log(np.log(1/(1-np.array(wcum))))
    zw=np.log(np.log(1/(1-np.array(p))))
    t1=db[0][0];t2=db[1][1];t12=db[0][1]     

    # ln(Xp)=a+zw*s - quantile
    a=bw[0]  #shift
    s=bw[1]  #scale

    # F(x)=1-exp[-(x/c)^b] #cdf
    # f(x)=dF(x)/dx=(b/c)*(x/c)^(b-1)*exp[-(x/c)^b]  #pdf

    b=1/s
    c=np.exp(a)
   
    print("a and s by MLS",file=fout)
    print("a=",a,"s=",s,file=fout)

    print("b and c by MLS",file=fout) 
    print("c=",c,"b=",b,file=fout)

    print("Sample size n=",n,file=fout)
    prints("Sample:",y,fout)
    prints("Sample log:",logy,fout)

    print("Observed values sample size n=",n,file=fout)
    prints("Empiricalr probability:",wcum,fout)
    print("Tolerance probability=",beta,file=fout)
    
    tlow,tup=nctlimit_app(n,beta,zw,t1,t2,t12)

    prints("Probability range:",p,fout)
    prints("Weibull quantiles:",zw,fout)
    prints("Upper non central t quantile",tup,fout)
    prints("Low non central t quantile",tlow,fout)
    xp=a+zw*s
    xpup=a+s*tup/np.sqrt(n)
    xplow=a+s*tlow/np.sqrt(n)
    prints("Upper tolerance limit",xpup,fout)
    prints("Quantile estimations",xp,fout)
    prints("Low tolerance limit",xplow,fout)
    fout.close()
  
    show_distr("Weibull",True,True,logy,zwcum,xp,zw,xplow,zw,xpup,zw,grid_size=n, distr_name=r'$N({a=}$'+str(round(a,4))+",${s=}$"+str(round(s,4))+")")


#################MLE Weibull Minimized Function#######################

def WeibullMinFunction(x,y,n):
    b=x[0]
    z=y**b
    c=sum(z)/n
    s2=sum(z*np.log(z))
    s1=sum(np.log(z))     
    c1=n+s1-s2/c
    return(c1**2)

##################### ММП Ковариационная матрица распределения Вейбулла ##################

def CovMatrixMleW(n,z):
    v=np.zeros((2,2))
    v[0][0]=1.
    v[0][1]=1.+sum(z)/n
    v[1][0]=v[0][1]
    v[1][1]=1.+sum(z**2*np.exp(z))/n
    v=linalg.inv(v)
    return(v)

#######################################################################################

#Empirical distribution function

def cum(n):
    fcum=[(i+0.5)/n for i in range(n)]
    #fcum=[(i+1.-0.375)/(n + 0.25) for i in range(n)] #Blom
    #fcum=[(i+1.)/(n+1) for i in range(n)] #order statistics theory
    return(fcum)

#####################Точные доверительные граница для квантиля####################

def nctlimit_exact(f,beta,delta):
    tlow=stats.nct.ppf(1-beta,f,delta)
    tup=stats.nct.ppf(beta,f,delta)
    return(tlow,tup)

#####################Приближенные доверительные граница для квантиля####################

def nctlimit_app(n,beta,zp,t1,t2,t12):
    zb=stats.norm.ppf(beta)
    d=zp*np.sqrt(n)
    f1x=t2/(n-1)
    f2x=2*t12/np.sqrt(n)
    f4x=1-f1x/2
    e3x=f4x**2-zb**2*f1x
    e11=f4x*d+zb**2*f2x/2
    e2x=d**2-zb**2*t1
    e44=np.sqrt(abs(e11**2-e2x*e3x))
    tlow=(e11-e44)/e3x
    tup=(e11+e44)/e3x
    return(tlow,tup)


##############################################################################

def show_distr(tdistr,nbegin,nend,x,y,xp,yp,xplow,yplow,xpup,ypup,grid_size, distr_name):
    
    if tdistr=="Weibull":
        p=[0.01,0.025,0.05,0.1,0.2,0.3,0.5,0.7,0.9,0.95,0.995]
        zp=np.log(np.log(1./(1.-np.asarray(p))))
    if tdistr=="Normal":
        p=[0.005,0.01,0.025,0.05,0.1,0.2,0.3,0.5,0.7,0.8,0.9,0.95,0.975,0.99,0.995]
        zp=stats.norm.ppf(np.asarray(p),0,1)
    kp=len(p)
    ymin=zp[0]
    ymax=zp[kp-1]+0.5
    xmin=min(xplow)
    xmax=max(xpup)+0.5
   
    grid = np.linspace(xmin, xmax, grid_size) 
    #if nbegin==True:figure,axes=plt.subplots(figsize=(12, 10))
    if nbegin==True:figure,axes=plt.subplots()
    plt.plot(x,y,'r+',markersize=12,label=u'Выборка') 
    plt.plot(xp,yp,'black',lw=3,label=u'Distribution')
    plt.plot(xplow,yplow,'g-',lw=2,label=u'Xlow')
    plt.plot(xpup,ypup,'g-.',lw=2,label=u'Xup')
    
    for i in range(kp):
        xx=[xmin,xmax]
        yy=[zp[i],zp[i]] 
        plt.text (xmax,zp[i],str(100*p[i])+"%")
        plt.plot(xx,yy,'black',lw=1,label='',linestyle='dashed')
    plt.text(xmax,ymax,"P%")

    plt.grid(ls=':') 
    plt.xlabel(r'${X}$', fontsize=18) 
    plt.ylabel(r'${Zp}$', fontsize=18) 
    plt.xlim((xmin, xmax)) 
    plt.ylim((ymin, ymax)) 
    title = 'Distribution {}'.format(distr_name) 
    plt.title(title, fontsize=20) 
    
    if nbegin==True:axes.legend();
    if nbegin==True and nend==True:plt.show()

################################################################################

def standart(x):
    x.sort()
    n=len(x)
    a=np.mean(x)
    s=np.std(x,ddof=1)
    median=np.median(x)
    var=np.var(x,ddof=1)
    return(n,a,s,median,var)

##################################################################################

def Plan_Disp():
    txt="Inp/Plan_Disp.inp"
    finp=open(txt)
    st=finp.readline()
    beta=list(map(float,finp.readline().split()))
    st=finp.readline()
    kstart=int(finp.readline())
    st=finp.readline()
    kfinish=int(finp.readline())
    finp.close()

    kb=len(beta)
    txt="Out/Plan_Disp.out"
    fout=open(txt,'w')
    print("Sample size to evaluate the variance with beta=",file=fout)
    print(beta,file=fout)
    for i in range(kb):
        print("Beta=",beta[i],file=fout)
        bb1=1.-beta[i]
        bb2=1.+beta[i]
        for j in range(kstart,kfinish+1):
            b1=stats.chi2.ppf(1-0.5*bb1,j)
            b2=stats.chi2.ppf(1-0.5*bb2,j)
            delta =np.sqrt(b1/b2)-1.
            print("f=",j,": delta=",delta,file=fout)
    fout.close()
#######################################################################################

def sample():
    beta=[0.95,0.99]
    p=[0.5,0.7,0.9,0.95,0.99,0.995,0.999]  
    delta=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

    f = open('Out\Direct_Plan.out','w')
    f.write("P="+"           ")
    for i in range(len(p)):
        f.write(str(p[i])+"__")
    f.write("\n")
    for m in range(len(beta)):
         f.write("beta="+str(beta[m])+"\n")
         for k in range(len(delta)):
             f.write("delta=")
             f.write(str(delta[k])+":")
             for i in range(len(p)):
                 for j in range(3,4000):
                     n=j;df=n-1
                     zp=stats.norm.ppf(p[i])
                     nc=zp*np.sqrt(n)
                     t=(delta[k]+zp)*np.sqrt(n)
                     bet=stats.nct.cdf(t,df,nc)
                     if(bet>=beta[m]):break
                 f.write(str(n)+(5-len(str(n)))*"_")
             f.write("\n")

    f.close()

#############################################

def mlsordern(n,y):
    x=np.ones((n,2))
    v=np.ones((n,n))
    for i in range(n):
          x[i][1]=ordern(i+1,n)
          for j in range(i,n):
                v[j][i]=covordern(i+1,j+1,n)
                v[i][j] = v[j][i]
    v=np.linalg.inv(v)
    b,db=mls(x,y,v)
    return(b,db)

##############################################

def mlsorderw(n,y):
    x=np.ones((n,2))
    v=np.ones((n,n))
    for i in range(n):
          x[i][1]=orderw(i+1,n)
          for j in range(i,n):
                v[j][i]=covorderw(i+1,j+1,n)
                v[i][j] = v[j][i]
    v=np.linalg.inv(v)
    b,db=mls(x,y,v)
    return(b,db) 

###########################################

def mls(x,y,v):
    db=np.linalg.inv((np.dot(np.dot(x.transpose(),v),x)))
    b=np.dot(np.dot(np.dot(db,x.transpose()),v),y) 
    return(b,db) 

###########################Mean_Order_Statistics_Norm#####################################

def ordern(r,n):
  
    p = 1
    pr=r/(n+1)
    qr = 1 - pr
    xr =stats.norm.ppf(pr)
    dr = stats.norm.pdf(xr)
    xr1 = p / dr
    xr2 = xr * (p / dr) **2
    xr3 = (2 * xr **2 + 1) * (p / dr) ** 3
    xr4 = (6 * xr **3 + 7 * xr) * (p / dr) ** 4
    xr5 = (24 * xr ** 4 + 46 * xr ** 2 + 7) * (p / dr) ** 5
    xr6 = (120 * xr ** 5 + 326 * xr ** 3 + 127 * xr) * (p / dr) ** 6
    er = xr + pr * qr * xr2 / (2 * (n + 2)) + pr * qr * ((qr - pr) * xr3 / 3 + pr * qr * xr4 / 8) / (n + 2) ** 2 + pr * qr * (-(qr - pr) * xr3 / 3 + ((qr - pr) **2 - pr * qr) * xr4 / 4 + qr * pr * (qr - pr) * xr5 / 6 + (qr * pr) ** 2 * xr6 / 48) / (n + 2) ** 3
    return(er)

##evNormOrdStats(10,method="blom")
##evNormOrdStats(10,method="royston")
##evNormOrdStats(10,method="mc",nmc=5000)

############################Mean_Order_Statistics_Weibull#########################################################

def orderw(r,n):
    pr=r/(n+1)
    qr = 1 - pr
    xr =np.log(np.log(1 / (1 - pr)))
    xr1 = 1 / (np.log(1 / (1 - pr)) * (1 - pr))
    xr2 = xr1 * (1 / (1 - pr) - xr1)
    xr3 = xr2 ** 2 / xr1 + xr1 * (1 / (1 - pr) ** 2 - xr2)
    xr4 = (3 * xr1 * xr2 * xr3 - 2 * xr2 ** 3) / xr1 ** 2 + xr1 * (2 / (1 - pr) ** 3 - xr3)
    xr55 = (-12 * xr1 * xr2 ** 2 * xr3 + 3 * xr1 ** 2 * xr3 ** 2 + 4 * xr1 ** 2 * xr2 * xr4 + 6 * xr2 ** 4)
    xr5 = xr55 / xr1 ** 3 + xr1 * (6 / (1 - pr) ** 4 - xr4)
    a1 = -12 * xr2 ** 3 * xr3 - 12 * xr1 * (2 * xr2 * xr3 ** 2 + xr2 ** 2 * xr4)
    b1 = 6 * xr1 * xr2 * xr3 ** 2 + 6 * xr1 ** 2 * xr3 * xr4
    c1 = 8 * xr1 * xr2 ** 2 * xr4 + 4 * xr1 ** 2 * (xr3 * xr4 + xr2 * xr5)
    d1 = 24 * xr2 ** 3 * xr3
    xr6 = (xr1 ** 3 * (a1 + b1 + c1 + d1) - 3 * xr1 ** 2 * xr2 * xr55) / xr1 ** 6 + xr2 * (6 / (1 - pr) ** 4 - xr4) + xr1 * (24 / (1 - pr) ** 5 - xr5)
    er = xr + pr * qr * xr2 / (2 * (n + 2)) + pr * qr * ((qr - pr) * xr3 / 3 + pr * qr * xr4 / 8) / (n + 2) ** 2 + pr * qr * (-(qr - pr) * xr3 / 3 + ((qr - pr) ** 2 - pr * qr) * xr4 / 4 + qr * pr * (qr - pr) * xr5 / 6 + (qr * pr) ** 2 * xr6 / 48) / (n + 2) ** 3
    return(er)

###########################Covariance_Order_Statistics_Norm##################################################################

def covordern(r,s,n):
    p = 1
    pr=r/(n+1)
    qr = 1 - pr
    xr =stats.norm.ppf(pr)
    dr = stats.norm.pdf(xr)
    xr1 = p / dr
    xr2 = xr * (p / dr) ** 2
    xr3 = (2 * xr ** 2 + 1) * (p / dr) ** 3
    xr4 = (6 * xr ** 3 + 7 * xr) * (p / dr) ** 4
    xr5 = (24 * xr ** 4 + 46 * xr ** 2 + 7) * (p / dr) ** 5
    xr6 = (120 * xr ** 5 + 326 * xr ** 3 + 127 * xr) * (p / dr) ** 6
    ps=s/(n+1)
    qs = 1 - ps
    xs =stats.norm.ppf(ps)
    ds = stats.norm.pdf(xs)    
    xs1 = p / ds
    xs2 = xs * (p / ds) ** 2
    xs3 = (2 * xs ** 2 + 1) * (p / ds) ** 3
    xs4 = (6 * xs ** 3 + 7 * xs) * (p / ds) ** 4
    xs5 = (24 * xs ** 4 + 46 * xs ** 2 + 7) * (p / ds) ** 5
    xs6 = (120 * xs ** 5 + 326 * xs ** 3 + 127 * xs) * (p / ds) ** 6
    z1 = (qr - pr) * xr2 * xs1 + (qs - ps) * xr1 * xs2 + pr * qr * xr3 * xs1 / 2 + ps * qs * xr1 * xs3 / 2 + pr * qs * xr2 * xs2 / 2
    z1 = z1 * pr * qs / (n + 2) ** 2
    z2 = -(qr - pr) * xr2 * xs1 - (qs - ps) * xr1 * xs2 + ((qr - pr) ** 2 - pr * qr) * xr3 * xs1
    z3 = ((qs - ps) ** 2 - ps * qs) * xr1 * xs3 + (1.5 * (qr - pr) * (qs - ps) + 0.5 * ps * qr - 2 * pr * qs) * xr2 * xs2
    z4 = (5 / 6) * pr * qr * (qr - pr) * xr4 * xs1 + (5 / 6) * ps * qs * (qs - ps) * xr1 * xs4 + (pr * qs * (qr - pr) + 0.5 * pr * qr * (qs - ps)) * xr3 * xs2
    z5 = (pr * qs * (qs - ps) + 0.5 * ps * qs * (qr - pr)) * xr2 * xs3 + (1 / 8) * (pr * qr) ** 2 * xr5 * xs1 + (1 / 8) * (ps * qs) ** 2 * xr1 * xs5
    z6 = 0.25 * pr ** 2 * qr * qs * xr4 * xs2 + 0.25 * pr * ps * qs ** 2 * xr2 * xs4 + (2 * (pr * qs) ** 2 + 3 * pr * qr * ps * qs) * xr3 * xs3 / 12
    z7 = z2 + z3 + z4 + z5 + z6
    vrs = z1 + pr * qs * z7 / (n + 2) ** 3 + pr * qs * xr1 * xs1 / (n + 2)
    return(vrs)

########################Mean_Order_Statistics_Weibull################################################

def covorderw(r,s,n):
    pr=r/(n+1)
    qr = 1 - pr
    xr = np.log(np.log(1 / (1 - pr)))
    xr1 = 1 / (np.log(1 / (1 - pr)) * (1 - pr))
    xr2 = xr1 * (1 / (1 - pr) - xr1)
    xr3 = xr2 ** 2 / xr1 + xr1 * (1 / (1 - pr) ** 2 - xr2)
    xr4 = (3 * xr1 * xr2 * xr3 - 2 * xr2 ** 3) / xr1 ** 2 + xr1 * (2 / (1 - pr) ** 3 - xr3)
    xr55 = (-12 * xr1 * xr2 ** 2 * xr3 + 3 * xr1 ** 2 * xr3 ** 2 + 4 * xr1 ** 2 * xr2 * xr4 + 6 * xr2 ** 4)
    xr5 = xr55 / xr1 ** 3 + xr1 * (6 / (1 - pr) ** 4 - xr4)

    ps=s/(n+1)
    qs=1-ps
    xs = np.log(np.log(1 / (1 - ps)))
    xs1 = 1 / (np.log(1 / (1 - ps)) * (1 - ps))
    xs2 = xs1 * (1 / (1 - ps) - xs1)
    xs3 = xs2 ** 2 / xs1 + xs1 * (1 / (1 - ps) ** 2 - xs2)
    xs4 = (3 * xs1 * xs2 * xs3 - 2 * xs2 ** 3) / xs1 ** 2 + xs1 * (2 / (1 - ps) ** 3 - xs3)
    xs5 = (-12 * xs1 * xs2 ** 2 * xs3 + 3 * xs1 ** 2 * xs3 ** 2 + 4 * xs1 ** 2 * xs2 * xs4 + 6 * xs2 ** 4) / xs1 ** 3 + xs1 * (6 / (1 - ps) ** 4 - xs4)
    z1 = (qr - pr) * xr2 * xs1 + (qs - ps) * xr1 * xs2 + pr * qr * xr3 * xs1 / 2 + ps * qs * xr1 * xs3 / 2 + pr * qs * xr2 * xs2 / 2
    z1 = z1 * pr * qs / (n + 2) ** 2
    z2 = -(qr - pr) * xr2 * xs1 - (qs - ps) * xr1 * xs2 + ((qr - pr) ** 2 - pr * qr) * xr3 * xs1
    z3 = ((qs - ps) ** 2 - ps * qs) * xr1 * xs3 + (1.5 * (qr - pr) * (qs - ps) + 0.5 * ps * qr - 2 * pr * qs) * xr2 * xs2
    z4 = (5 / 6) * pr * qr * (qr - pr) * xr4 * xs1 + (5 / 6) * ps * qs * (qs - ps) * xr1 * xs4 + (pr * qs * (qr - pr) + 0.5 * pr * qr * (qs - ps)) * xr3 * xs2
    z5 = (pr * qs * (qs - ps) + 0.5 * ps * qs * (qr - pr)) * xr2 * xs3 + (1 / 8) * (pr * qr) ** 2 * xr5 * xs1 + (1 / 8) * (ps * qs) ** 2 * xr1 * xs5
    z6 = 0.25 * pr ** 2 * qr * qs * xr4 * xs2 + 0.25 * pr * ps * qs ** 2 * xr2 * xs4 + (2 * (pr * qs) ** 2 + 3 * pr * qr * ps * qs) * xr3 * xs3 / 12
    z7 = z2 + z3 + z4 + z5 + z6
    vrs = z1 + pr * qs * z7 / (n + 2) ** 3 + pr * qs * xr1 * xs1 / (n + 2)
    return(vrs)

