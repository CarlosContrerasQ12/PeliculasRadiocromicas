#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Wed Nov 18 15:02:51 2020
#

import wx
from imagenMatplotlibLibre import *
from scipy import interpolate as interp
import matplotlib
from matplotlib.widgets import Slider
from dialogoNormalizacion import *
import numpy as np
import pydicom 
import tempfile
import datetime
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset


#matplotlib.interactive(True)
#matplotlib.use('WXAgg')
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class Perfil():
    def __init__(self,parent,mapIntesidadR,mapIntesidadG,mapIntesidadB,figura,ax):
        self.fig=figura
        self.ax=ax
        self.mapeoR=mapIntesidadR
        self.mapeoG=mapIntesidadG
        self.mapeoB=mapIntesidadB
        k=self.fig.ginput(2)
        self.x1=k[0][0]
        self.y1=k[0][1]
        self.x2=k[1][0]
        self.y2=k[1][1]
        self.longes=np.sqrt((self.x2-self.x1)**2+(self.y2-self.y1)**2)
        self.xa=0
        self.ya=0
        
        self.ventanaAparte=ImagenMatplotlibLibre(None)
        self.fig2=self.ventanaAparte.figure
        self.ax2 =self.ventanaAparte.ax
        self.ax2.set_xlabel("Longitud(px)")
        self.ax2.set_ylabel("Dosis(Gy)")
        self.ax2.grid()
        
        
        
        #self.fig2,self.ax2=plt.subplots()
        self.line,=self.ax.plot([self.x1,self.x2],[self.y1,self.y2])
        
        
        self.pintarPerfil()
        
        self.cidPress=self.fig.canvas.mpl_connect('button_press_event', self.click)
        self.cidSoltar=''
        self.cidMover=''
        self.ventanaAparte.Show()
    def click(self,event):
        self.xa=event.xdata
        self.ya=event.ydata
        self.cidMover=self.fig.canvas.mpl_connect('motion_notify_event', self.mover)
        self.cidSoltar=self.fig.canvas.mpl_connect('button_release_event', self.soltar)
    def mover(self,event):
        despx=event.xdata-self.xa
        despy=event.ydata-self.ya   
        self.xa=event.xdata
        self.ya=event.ydata
        self.x1=self.x1+despx
        self.x2=self.x2+despx
        self.y1=self.y1+despy
        self.y2=self.y2+despy
        self.pintarPerfil()
    def soltar(self,event): 
        self.fig.canvas.mpl_disconnect(self.cidSoltar)
        self.fig.canvas.mpl_disconnect(self.cidMover)
    def pintarPerfil(self):
        m=(self.y2-self.y1)/(self.x2-self.x1)
        b=self.y1-m*self.x1
        x=np.linspace(self.x1,self.x2,300)
        y=m*x+b
        self.line.set_data([x[0],x[-1]],[y[0],y[-1]])
        ysr=np.zeros(x.shape[0])
        ysg=np.zeros(x.shape[0])
        ysb=np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            ysr[i]=self.mapeoR(x[i],y[i])
            ysg[i]=self.mapeoG(x[i],y[i])
            ysb[i]=self.mapeoB(x[i],y[i])
        xs=np.linspace(0,self.longes,ysr.shape[0])
        self.ax2.clear()
        self.ax2.set_xlabel("Longitud(px)")
        self.ax2.set_ylabel("Dosis(Gy)")
        self.ax2.grid()
        
        self.ax2.plot(xs,ysr,color='r')
        self.ax2.plot(xs,ysg,color='g')
        self.ax2.plot(xs,ysb,color='b')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.fig2.canvas.draw()
        self.fig2.canvas.flush_events()


class PanelMapaDosis2(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        self.parent=args[0]
        self.centro=args[1]
        super(PanelMapaDosis2, self).__init__(self.parent)
        self.button_4 = wx.Button(self, wx.ID_ANY, "Histograma de dosis")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Perfil de dosis")
        self.button_6 = wx.Button(self, wx.ID_ANY, "Curvas de Isodosis")
        self.button_9 = wx.Button(self, wx.ID_ANY, "Punto de normalizacion")
        self.button_8 = wx.Button(self, wx.ID_ANY, "Guardar Mapa")
        
        self.normalizacion=np.max(self.parent.paginaActual.arrayIma[:,:,0])

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.histograma, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.generar_perfil, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.generar_mapa_curvas, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.renormalizar, self.button_9)
        self.Bind(wx.EVT_BUTTON, self.guardar_mapa, self.button_8)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.button_9, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_5, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_6, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_4, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_8, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def histograma(self, event):  # wxGlade: MyDialog.<event_handler>
        ima=ImagenMatplotlibLibre(self.parent)
        ima.ax.hist(self.parent.paginaActual.arrayIma[:,:,0].flatten())
        ima.ax.set_xlabel("Dosis(Gy)")
        ima.ax.set_ylabel("Numero de pixeles")
        ima.Show()
    
        
        
        event.Skip()

    def generar_perfil(self, event):  # wxGlade: MyDialog.<event_handler>
        x=np.linspace(0,self.parent.paginaActual.arrayIma.shape[1],self.parent.paginaActual.arrayIma.shape[1])
        y=np.linspace(0,self.parent.paginaActual.arrayIma.shape[0],self.parent.paginaActual.arrayIma.shape[0])
        fr=interp.interp2d(x,y,self.parent.paginaActual.arrayIma[:,:,0],fill_value=0)
        fg=interp.interp2d(x,y,self.parent.paginaActual.arrayIma[:,:,1],fill_value=0)
        fb=interp.interp2d(x,y,self.parent.paginaActual.arrayIma[:,:,2],fill_value=0)
        self.per=Perfil(self.parent,fr,fg,fb,self.parent.paginaActual.figure,self.parent.paginaActual.figure.gca())
        event.Skip()

    def generar_mapa_curvas(self, event):  # wxGlade: MyDialog.<event_handler>
        x=np.linspace(0,self.parent.paginaActual.arrayIma.shape[1],self.parent.paginaActual.arrayIma.shape[1])
        y=np.linspace(0,self.parent.paginaActual.arrayIma.shape[0],self.parent.paginaActual.arrayIma.shape[0])
        arrnorm=self.parent.paginaActual.arrayIma[:,:,0]/self.normalizacion
        ima=ImagenMatplotlibLibre(self.parent)
        ima.ax.set_position(([0.25, 0.3, 0.5,0.5]))
        self.axR=ima.figure.add_axes([0.25, 0.1, 0.50, 0.02])
        self.axR2=ima.figure.add_axes([0.25, 0.15, 0.50, 0.02])
        self.axR3=ima.figure.add_axes([0.25, 0.2, 0.50, 0.02])
        self.spor = Slider(self.axR, '%', 0, 100.0, valinit=50, valstep=1)
        self.spor2 = Slider(self.axR2, '%', 0, 100.0, valinit=50, valstep=1)
        self.spor3 = Slider(self.axR3, '%', 0, 100.0, valinit=50, valstep=1)
        def update(val):
            iv=self.spor.val
            iv2=self.spor2.val
            iv3=self.spor3.val
            ima.ax.clear()
            ima.ax.contour(x, y, arrnorm - iv/100.0, levels = [0],colors=['red'])
            ima.ax.contour(x, y, arrnorm - iv2/100.0, levels = [0],colors=['blue'])
            ima.ax.contour(x, y, arrnorm - iv3/100.0, levels = [0],colors=['green'])
            
            ima.figure.canvas.draw_idle()
        self.spor.on_changed(update)  
        self.spor2.on_changed(update)  
        self.spor3.on_changed(update)  
        ima.Show()
        event.Skip()

    def renormalizar(self, event):  # wxGlade: MyDialog.<event_handler>
        dial=DialogoNormalizacion(self)
        dial.ShowModal()
        if dial.resultado=='cancelar':
            return 
        elif dial.resultado=='maximo':
            self.normalizacion=np.max(self.parent.paginaActual.arrayIma[:,:,0])
        elif dial.resultado=='valorFijo':
            self.normalizacion=dial.valor
        elif dial.resultado=='select':
            k=self.parent.paginaActual.figure.ginput(1)
            xp=int(k[0][0])
            yp=int(k[0][1])
            self.normalizacion=np.mean(self.parent.paginaActual.arrayIma[yp-2:yp+2,xp-2:xp+2,0])   
        event.Skip()

    def guardar_mapa(self, event):  # wxGlade: MyDialog.<event_handler>
        suffix='.dcm'
        fdlg = wx.FileDialog(self, "Guardar calibracion",wildcard="dicom file (*.dcm)|*.dcm", style=wx.FD_SAVE)
        fdlg.SetFilename("Mapa de dosis-")
        nombreArchivo=''
        if fdlg.ShowModal() == wx.ID_OK:
                nombreArchivo = fdlg.GetPath()+suffix
        else:
            return   
        dosisPl=(self.parent.paginaActual.arrayIma[:,:,0]+self.parent.paginaActual.arrayIma[:,:,1]+self.parent.paginaActual.arrayIma[:,:,2])/3
        fact=np.max(dosisPl)
        arr=((dosisPl/ fact)*((2**16)-1)).astype('uint32')
        """
        ds = pydicom.dcmread('piramide4.dcm')
        """
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.246.352.71.7.593947511628.1265684.20201029130910"
        file_meta.ImplementationClassUID = "1.2.246.352.70.2.1.7"
        ds = FileDataset(nombreArchivo, {},
                 file_meta=file_meta, preamble=b"\0" * 128)
        ds.PatientName = "PeliculasRadicromicas"
        ds.Allergies='A la ensalada roja'
        ds.PatientID = "57"
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        ds.is_little_endian = True
        ds.is_implicit_VR = True
        ds.IsocenterPosition=[self.centro[0],self.centro[1],0]
        ds.NormalizationPoint=self.normalizacion
        ds.SamplesPerPixel=1
        ds.PhotometricInterpretation='MONOCHROME2'
        ds.PixelSpacing=[25.4/(self.parent.configuracion["ppi"]-1),25.4/(self.parent.configuracion["ppi"]-1)]
        ds.BitsAllocated=32
        ds.BitsStored=32
        ds.HighBit=31
        ds.PixelRepresentation=0
        ds.DoseUnits='GY'
        ds.DoseGridScaling="{:.7E}".format(fact/(2**16-1))
        
        ds.PixelData=arr.tobytes()
        ds.Rows,ds.Columns=arr.shape
        
        dt = datetime.datetime.now()
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        ds.ContentTime = timeStr
        
        ds.save_as(nombreArchivo)
        

        
        event.Skip()

# end of class MyDialog

class MyApp(wx.App):
    def OnInit(self):
        self.dialog = MyDialog(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
