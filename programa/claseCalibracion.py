import numpy as np
from PIL import Image
import SimpleITK as sitk
from scipy.optimize import curve_fit
from scipy.optimize import root_scalar,minimize
from imagenMatplotlibLibre import *
from scipy.stats.distributions import chi2
import dill
from numba import jit


def funcionRacionalLineal(x,p0,p1,p2):
    return -np.log10((p0+p1*x)/(x+p2))
@jit    
def funcionInversaRacionalLineal(y,p0,p1,p2):
    r=10**-y
    return (p0-p2*(r))/((r-p1))
@jit
def derivadaInversaRacionalLineal(y,p0,p1,p2):
    r=10**-y
    l=np.log(10)
    return -l*r*((p2*p1-p0))/((r-p1)**2)
@jit    
def derivada2InversaRacionalLineal(y,p0,p1,p2):
    r=10**-y
    l=np.log(10)
    return (l**2)*r*(((p2*p1-p0)/(r-p1)**2)-((2*(p2*p1-p0)*(r-p1))/(r-p1)**4))
    
def funcionCubica(x,p0,p1,p2,p3):
    return p0+p1*x+p2*x*x+p2*x*x*x
    
def funcionExponencialPolinomica(x,p0,p1,p2):
    return  p0+p1*(x**p2)
    
def funcionLineal(x,p0,p1):
    return  p0+p1*(x)   
    

def guardar_calibracion(tipoCanal,tipoCurva,parametros,covarianzas,dosis,transmitancias,ceros,incertidumbres,funcionesRGB,funcionCalDel,funcionTaD,nombreArchivo):
    f=open(nombreArchivo,'a')
    dis={"Nombre":nombreArchivo,"TipoCanal":tipoCanal,"TipoCurva":tipoCurva,"Parametros":parametros,"Covarianzas":covarianzas,"Dosis":dosis,"Dopticas":transmitancias,"Ceros":ceros,"Incertidumbres":incertidumbres,"funcionesRGB":funcionesRGB,"funcionCalDel":funcionCalDel,"funcionTaD":funcionTaD}
    dill.settings['recurse'] = True
    dill.dump(dis, open(nombreArchivo, 'wb'))
    
def leer_Calibracion(nombreArchivo):
    f=open(nombreArchivo,'rb')
    return dill.load(f)
    
class CalibracionImagen:
    def __init__(self,promsR,promsG,promsB,incertidumbres,dosis,tipoCanal,tipoCurva):
        self.netODR=promsR[0]
        self.netODG=promsG[0]
        self.netODB=promsB[0]
        
        self.promsRCero=promsR[1]
        self.promsGCero=promsG[1]
        self.promsBCero=promsB[1]
        
        self.varODR=incertidumbres[0]
        self.varODG=incertidumbres[1]
        self.varODB=incertidumbres[2]


        self.dosis=dosis
        self.tipoCanal=tipoCanal
        self.tipoCurva=tipoCurva
        self.parametrosOptimosR=[]
        self.parametrosOptimosG=[]
        self.parametrosOptimosB=[]
        self.pCovarianzaR=[]
        self.pCovarianzaG=[]
        self.pCovarianzaB=[]
        def f():
            return 1
        self.funcionTaD=f
        self.funcionCalculaDelta=f
        
    def generar_calibracion(self,nombreArchivo):
        def fR(D):
            return 0
        def fG(D):
            return 0
        def fB(D):
            return 0
        def fRder(D):
            return 0
        def fGder(D):
            return 0
        def fBder(D):
            return 0
        def fRder2(D):
            return 0
        def fGder2(D):
            return 0
        def fBder2(D):
            return 0
            
        #netODR=np.log10(np.array(self.promsRCero)/np.array(self.promsR))
        #netODG=np.log10(np.array(self.promsGCero)/np.array(self.promsG))
        #netODB=np.log10(np.array(self.promsBCero)/np.array(self.promsB))        
            
        if self.tipoCurva=="Racional lineal":
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionRacionalLineal, self.dosis, self.netODR,sigma=self.varODR)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionRacionalLineal, self.dosis, self.netODG,sigma=self.varODG)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionRacionalLineal, self.dosis, self.netODB,sigma=self.varODB)
            def fRa(oD):
                return funcionInversaRacionalLineal(oD,*self.parametrosOptimosR)
            def fGa(oD):
                return funcionInversaRacionalLineal(oD,*self.parametrosOptimosG)
            def fBa(oD):
                return funcionInversaRacionalLineal(oD,*self.parametrosOptimosB)
            def fRdera(oD):
                return derivadaInversaRacionalLineal(oD,*self.parametrosOptimosR)
            def fGdera(oD):
                return derivadaInversaRacionalLineal(oD,*self.parametrosOptimosG)
            def fBdera(oD):
                return derivadaInversaRacionalLineal(oD,*self.parametrosOptimosB)
            def fRder2a(oD):
                return derivada2InversaRacionalLineal(oD,*self.parametrosOptimosR)
            def fGder2a(oD):
                return derivada2InversaRacionalLineal(oD,*self.parametrosOptimosG)
            def fBder2a(oD):
                return derivada2InversaRacionalLineal(oD,*self.parametrosOptimosB)
            fR=fRa
            fG=fGa
            fB=fBa
            fRder=fRdera
            fGder=fGdera
            fBder=fBdera
            fRder2=fRder2a
            fGder2=fGder2a
            fBder2=fBder2a
            
        if self.tipoCurva=="Cubica":
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionCubica, self.netODR, self.dosis,sigma=self.varODR)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionCubica, self.netODG, self.dosis,sigma=self.varODG)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionCubica, self.netODB, self.dosis,sigma=self.varODB)
            def fRa(oD):
                return funcionCubica(oD,*self.parametrosOptimosR)
            def fGa(oD):
                return funcionCubica(oD,*self.parametrosOptimosG)
            def fBa(oD):
                return funcionCubica(oD,*self.parametrosOptimosB)
            fR=fRa
            fG=fGa
            fB=fBa
            
        if self.tipoCurva=="Exponencial polinomica":
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionExponencialPolinomica, self.netODR, self.dosis,sigma=self.varODR)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionExponencialPolinomica, self.netODG, self.dosis,sigma=self.varODG)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionExponencialPolinomica, self.netODB, self.dosis,sigma=self.varODB)
            def fRa(oD):
                return funcionExponencialPolinomica(oD,*self.parametrosOptimosR)
            def fGa(oD):
                return funcionExponencialPolinomica(oD,*self.parametrosOptimosG)
            def fBa(oD):
                return funcionExponencialPolinomica(oD,*self.parametrosOptimosB)
            fR=fRa
            fG=fGa
            fB=fBa
            
        if self.tipoCurva=="Lineal":
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionLineal, self.netODR, self.dosis,sigma=self.varODR)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionLineal, self.netODG, self.dosis,sigma=self.varODG)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionLineal, self.netODB, self.dosis,sigma=self.varODB)
            def fRa(oD):
                return funcionLineal(oD,*self.parametrosOptimosR)
            def fGa(oD):
                return funcionLineal(oD,*self.parametrosOptimosG)
            def fBa(oD):
                return funcionLineal(oD,*self.parametrosOptimosB)
            fR=fRa
            fG=fGa
            fB=fBa
                

        if self.tipoCanal!="Multicanal":
            
            if self.tipoCanal=="Canal rojo":
                self.funcionTaD=fR
            elif self.tipoCanal=="Canal verde":
                self.funcionTaD=fG
            elif self.tipoCanal=="Canal azul":
                self.funcionTaD=fB
            elif self.tipoCanal=="Promedio RGB":
                def fac(oDR,oDG,oDB):
                    return (fR(oDR)+fG(oDG)+fB(oDB))/3
                self.funcionTaD=fac
        else:
            def fMickDiferencia(DeltaD,oDR,oDG,oDB):
                a=fR(oDR*DeltaD)
                b=fG(oDG*DeltaD)
                c=fB(oDB*DeltaD)
                return (a-b)**2+(a-c)**2+(b-c)**2
                
            def fMickDiferenciaDerivada(DeltaD,oDR,oDG,oDB):
                a=fR(oDR*DeltaD)
                b=fG(oDG*DeltaD)
                c=fB(oDB*DeltaD)
                ad=oDR*fRder(oDR*DeltaD)
                bd=oDG*fGder(oDG*DeltaD)
                cd=oDB*fBder(oDB*DeltaD)
                return 2*((ad-bd)*(a-b)+(ad-cd)*(a-c)+(bd-cd)*(b-c))
            def fMickDiferenciaDerivada2(DeltaD,oDR,oDG,oDB):
                a=fR(oDR*DeltaD)
                b=fG(oDG*DeltaD)
                c=fB(oDB*DeltaD)
                ad=oDR*fRder(oDR*DeltaD)
                bd=oDG*fGder(oDG*DeltaD)
                cd=oDB*fBder(oDB*DeltaD)
                ad2=(oDR**2)*fRder2(oDR*DeltaD)
                bd2=(oDG**2)*fGder2(oDG*DeltaD)
                cd2=(oDB**2)*fBder2(oDB*DeltaD)
                return 2*((ad2-bd2)*(a-b)+(ad-bd)**2+(ad2-cd2)*(a-c)+(ad-cd)**2+(bd2-cd2)*(b-c)+(bd-cd)**2)
            @jit   
            def deltaOptimo(oDR,oDG,oDB):
                delResp=np.zeros(oDR.shape)
                """
                for i in range(delResp.shape[0]):
                    for j in range(delResp.shape[1]):
                        #delResp[i,j]=root_scalar(fMickDiferenciaDerivada,x0=1.0,args=(oDR[i,j],oDG[i,j],oDB[i,j]),fprime=fMickDiferenciaDerivada2,method='newton').root
                        delResp[i,j]=minimize(fMickDiferencia,jac=fMickDiferenciaDerivada,x0=1.0,args=(oDR[i,j],oDG[i,j],oDB[i,j]),hess=fMickDiferenciaDerivada2,method='Newton-CG').x
                    print(i)
                """
                x0=0*oDR+1.0
                N=2
                for i in range(N):
                    x0=x0-fMickDiferenciaDerivada(x0,oDR,oDG,oDB)/fMickDiferenciaDerivada2(x0,oDR,oDG,oDB)
                    print(i)
                delResp=x0
            
                return delResp
                
            def fux(DeltaD,oDR,oDG,oDB):
                return (fR(oDR*DeltaD)+fG(oDG*DeltaD)+fB(oDB*DeltaD))/3
            self.funcionCalculaDelta=deltaOptimo
            self.funcionTaD=fux
            
        pOptimos=[self.parametrosOptimosR,self.parametrosOptimosG,self.parametrosOptimosB]
        pCova=[self.pCovarianzaR,self.pCovarianzaG,self.pCovarianzaB]
        dopts=[self.netODR,self.netODG,self.netODB]
        ceros=[self.promsRCero,self.promsGCero,self.promsBCero]
        incer=[self.varODR,self.varODG,self.varODB]
        funcionesRGB=[fR,fG,fB]
        guardar_calibracion(self.tipoCanal,
                            self.tipoCurva,
                            pOptimos,
                            pCova,
                            self.dosis,
                            dopts,
                            ceros,
                            incer,
                            funcionesRGB,
                            self.funcionCalculaDelta,
                            self.funcionTaD,
                            nombreArchivo)  
                            
        grafica=ImagenMatplotlibLibre(None)
        grafica.ax.errorbar(self.dosis,self.netODR,yerr=self.varODR,color='r',fmt='o',markersize=2)
        grafica.ax.errorbar(self.dosis,self.netODG,yerr=self.varODG,color='g',fmt='o',markersize=2)
        grafica.ax.errorbar(self.dosis,self.netODB,yerr=self.varODB,color='b',fmt='o',markersize=2)
        
        xasR=np.linspace(self.netODR[0],self.netODR[-1]+0.005,100)
        xasG=np.linspace(self.netODG[0],self.netODG[-1]+0.005,100)
        xasB=np.linspace(self.netODB[0],self.netODB[-1]+0.005,100)
        
        yasR=fR(xasR)
        yasG=fG(xasG)
        yasB=fB(xasB)
        
        grafica.ax.plot(yasR,xasR,'r--')
        grafica.ax.plot(yasG,xasG,'g--')
        grafica.ax.plot(yasB,xasB,'b--')

        SR=np.sum(((self.dosis-fR(self.netODR))/self.varODR)**2)
        SG=np.sum(((self.dosis-fG(self.netODG))/self.varODG)**2)
        SB=np.sum(((self.dosis-fB(self.netODB))/self.varODB)**2)
        
        print(SR)
        print(SG)
        print(SB)
        print("La bondad de ajuste para el canal rojo es de ", chi2.sf(SR,len(self.dosis)-len(pOptimos[0])))
        print("La bondad de ajuste para el canal rojo es de ", chi2.sf(SG,len(self.dosis)-len(pOptimos[1])))
        print("La bondad de ajuste para el canal rojo es de ", chi2.sf(SB,len(self.dosis)-len(pOptimos[2])))
        grafica.Show() 
                            
                
                
                
                    

            

        
        


