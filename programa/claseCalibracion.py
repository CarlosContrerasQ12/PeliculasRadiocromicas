import numpy as np
from PIL import Image
import SimpleITK as sitk
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from imagenMatplotlibLibre import *
import dill


def funcionRacionalLineal(x,p0,p1,p2):
    return -np.log10((p0+p1*x)/(x+p2))
    
def funcionInversaRacionalLineal(y,p0,p1,p2):
    r=10**-y
    return (p0-p2*(r))/((r-p1))

def funcionCubica(x,p0,p1,p2,p3):
    return p0+p1*x+p2*x*x+p2*x*x*x
    
def funcionExponencialPolinomica(x,p0,p1,p2):
    return  p0+p1*(x**p2)
    
def funcionLineal(x,p0,p1):
    return  p0+p1*(x)   
    

def guardar_calibracion(tipoCanal,tipoCurva,parametros,covarianzas,dosis,transmitancias,ceros,funcionCalDel,funcionTaD,nombreArchivo):
    f=open(nombreArchivo,'a')
    dis={"Nombre":nombreArchivo,"TipoCanal":tipoCanal,"TipoCurva":tipoCurva,"Parametros":parametros,"Covarianzas":covarianzas,"Dosis":dosis,"Trans":transmitancias,"Ceros":ceros,"funcionCalDel":funcionCalDel,"funcionTaD":funcionTaD}
    dill.settings['recurse'] = True
    dill.dump(dis, open(nombreArchivo, 'wb'))
    
def leer_Calibracion(nombreArchivo):
    f=open(nombreArchivo,'rb')
    return dill.load(f)
    
class CalibracionImagen:
    def __init__(self,promsR,promsG,promsB,dosis,tipoCanal,tipoCurva):
        self.T=[]
        self.TCeros=[]
        self.promsR=promsR[0]
        if promsR[1][0]<1e-5:
            self.promsRCero=[self.promsR[0]]*len(promsR[1])
        else:   
            self.promsRCero=promsR[1]
        
        self.promsG=promsG[0]
        if promsG[1][0]<1e-5:
            self.promsGCero=[self.promsG[0]]*len(promsG[1])
        else:   
            self.promsGCero=promsG[1]
        self.promsB=promsB[0]
        if promsB[1][0]<1e-5:
            self.promsBCero=[self.promsB[0]]*len(promsB[1])
        else:   
            self.promsBCero=promsB[1]
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
            
        netODR=np.log10(np.array(self.promsRCero)/np.array(self.promsR))
        netODG=np.log10(np.array(self.promsGCero)/np.array(self.promsG))
        netODB=np.log10(np.array(self.promsBCero)/np.array(self.promsB))        
            
        if self.tipoCurva=="Racional lineal":
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionRacionalLineal, self.dosis, netODR)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionRacionalLineal, self.dosis, netODG)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionRacionalLineal, self.dosis, netODB)
            def fRa(oD):
                return funcionInversaRacionalLineal(oD,*self.parametrosOptimosR)
            def fGa(oD):
                return funcionInversaRacionalLineal(oD,*self.parametrosOptimosG)
            def fBa(oD):
                return funcionInversaRacionalLineal(oD,*self.parametrosOptimosB)
            fR=fRa
            fG=fGa
            fB=fBa
            
        if self.tipoCurva=="Cubica":
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionCubica, netODR, self.dosis)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionCubica, netODG, self.dosis)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionCubica, netODB, self.dosis)
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
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionExponencialPolinomica, netODR, self.dosis)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionExponencialPolinomica, netODG, self.dosis)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionExponencialPolinomica, netODB, self.dosis)
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
            self.parametrosOptimosR,self.pCovarianzaR=curve_fit(funcionLineal, netODR, self.dosis)
            self.parametrosOptimosG,self.pCovarianzaG=curve_fit(funcionLineal, netODG, self.dosis)
            self.parametrosOptimosB,self.pCovarianzaB=curve_fit(funcionLineal, netODB, self.dosis)
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
                    return (fR(oDr)+fG(oDG)+fB(oDB))/3
                self.funcionTaD=fac
        else:
            def fMickDiferencia(DeltaD,oDR,oDG,oDB):
                a=fR(oDR*DeltaD)
                b=fG(oDG*DeltaD)
                c=fB(oDB*DeltaD)
                return (a-b)**2+(a-c)**2+(b-c)**2
               
            def deltaOptimo(oDR,oDG,oDB):
                delResp=np.zeros(oDR.shape)
                for i in range(delResp.shape[0]):
                    for j in range(delResp.shape[1]):
                        delResp[i,j]=minimize(fMickDiferencia,1.0,args=(oDR[i,j],oDG[i,j],oDB[i,j])).x
                        print(i,j)
                return delResp
            def fux(DeltaD,oDR,oDG,oDB):
                return (fR(oDR*DeltaD)+fG(oDG*DeltaD)+fB(oDB*DeltaD))/3
            self.funcionCalculaDelta=deltaOptimo
            self.funcionTaD=fux
            
        pOptimos=[self.parametrosOptimosR,self.parametrosOptimosG,self.parametrosOptimosB]
        pCova=[self.pCovarianzaR,self.pCovarianzaG,self.pCovarianzaB]
        trasmi=[self.promsR,self.promsG,self.promsB]
        ceros=[self.promsRCero,self.promsGCero,self.promsBCero]
        guardar_calibracion(self.tipoCanal,
                            self.tipoCurva,
                            pOptimos,
                            pCova,
                            self.dosis,
                            trasmi,
                            ceros,
                            self.funcionCalculaDelta,
                            self.funcionTaD,
                            nombreArchivo)  
                            
        grafica=ImagenMatplotlibLibre(None)
        grafica.ax.scatter(self.dosis,netODR,color='r')
        grafica.ax.scatter(self.dosis,netODG,color='g')
        grafica.ax.scatter(self.dosis,netODB,color='b')
        xasR=np.linspace(netODR[0],netODR[-1]+0.05,100)
        xasG=np.linspace(netODG[0],netODG[-1]+0.05,100)
        xasB=np.linspace(netODB[0],netODB[-1]+0.05,100)
        yasR=fR(xasR)
        yasG=fG(xasG)
        yasB=fB(xasB)
        grafica.ax.plot(yasR,xasR,'r--')
        grafica.ax.plot(yasG,xasG,'g--')
        grafica.ax.plot(yasB,xasB,'b--')
        grafica.Show() 
                            
                
                
                
                    

            

        
        


