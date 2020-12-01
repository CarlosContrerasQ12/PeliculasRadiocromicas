#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Thu Nov 19 18:25:50 2020
#

import wx
from scipy import interpolate as interp
from imagenMatplotlibLibre import *
from matplotlib.widgets import Slider
import numpy as np
import pymedphys
import matplotlib as mpl
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class PerfilDoble():
    def __init__(self,parent,mapIntesidad1,mapIntesidad2,imagen1,imagen2,figura,ax):
        self.fig=figura
        self.ax=ax
        self.aray1=imagen1
        self.aray2=imagen2
        self.mapeo1=mapIntesidad1
        self.mapeo2=mapIntesidad2
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
        ys1=np.zeros(x.shape[0])
        ys2=np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            ys1[i]=self.mapeo1(x[i],y[i])
            ys2[i]=self.mapeo2(x[i],y[i])
            
        xs=np.linspace(0,self.longes,ys1.shape[0])
        self.ax2.clear()
        
        self.ax2.plot(xs,ys1,'r')
        self.ax2.plot(xs,ys2,'g')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.fig2.canvas.draw()
        self.fig2.canvas.flush_events()


class PanelComparacionAPlan(wx.Panel):
    def __init__(self, *args, **kwds):
        self.parent=args[0]
        self.tole=args[1]
        self.dta=args[2]
        self.cutoff=args[3]
        self.escala=args[4]
        super(PanelComparacionAPlan, self).__init__(self.parent)
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "",style=wx.TE_READONLY)
        self.button_1 = wx.Button(self, wx.ID_ANY, "Calcular Gamma")
        self.button_2 = wx.Button(self, wx.ID_ANY, "Estadisticas Gamma")
        self.button_3 = wx.Button(self, wx.ID_ANY, "Perfil de dosis")
        self.button_4 = wx.Button(self, wx.ID_ANY, "Curva de isodosis")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Guardar comparacion")
        self.button_6 = wx.Button(self, wx.ID_ANY, "Seleccionar ROI")
        
        self.normalizacion=np.max(self.parent.paginaActual.arrayIma[0])
        self.gamma=0
        self.yaCalculado=False
        self.validgamma=0
        self.gamma_options = {
        'dose_percent_threshold': self.tole,
        'distance_mm_threshold': self.dta,
        'lower_percent_dose_cutoff': self.cutoff,
        'interp_fraction': 15,  # Should be 10 or more for more accurate results
        'max_gamma': 3,
        'random_subset': None,
        'local_gamma': False,
        'ram_available': 5*(2**29)  # 1/2 GB
        }


        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.calcular_gamma, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.generar_estadisticas, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.nuevo_perfil, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.generar_isodosis, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.guardar_comparacion, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.seleccionarROI, self.button_6)
        # end wxGlade

    def __set_properties(self):
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Pasan Gamma")
        sizer_2.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(self.text_ctrl_1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_6, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_1, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_2, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_3, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_4, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_5, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def calcular_gamma(self, event):  # wxGlade: MyDialog.<event_handler>
        ejsx=np.linspace(0,self.parent.arayActual[0].shape[0]*self.escala,self.parent.arayActual[0].shape[0])
        ejsy=np.linspace(0,self.parent.arayActual[0].shape[1]*self.escala,self.parent.arayActual[0].shape[1])
        ej=(ejsx,ejsy)

        self.gamma = pymedphys.gamma(
        ej, self.parent.arayActual[0],
        ej, self.parent.arayActual[1],
        **self.gamma_options)
        self.valid_gamma = self.gamma[~np.isnan(self.gamma)]
        pass_ratio = np.sum(self.valid_gamma <= 1) / len(self.valid_gamma)
        self.text_ctrl_1.SetValue("{0:.2f} ".format(pass_ratio*100)+'%')
        self.yaCalculado=True
        event.Skip()

    def generar_estadisticas(self, event):  # wxGlade: MyDialog.<event_handler>

        if self.yaCalculado:
            num_bins = (self.gamma_options['interp_fraction'] * self.gamma_options['max_gamma'])
            bins = np.linspace(0, self.gamma_options['max_gamma'], num_bins + 1)
            ima=ImagenMatplotlibLibre(self.parent)
            ima.ax.hist(self.valid_gamma, bins, density=True)
            ima.ax.set_xlim([0, self.gamma_options['max_gamma']])
            ima.ax.set_xlabel(r"Gamma($\Gamma$)")
            ima.ax.set_ylabel("Numero de pixeles")
            ima.Show()
            
            imag2=ImagenMatplotlibLibre(self.parent)
            pos=imag2.ax.imshow(self.gamma,'gist_heat')
            imag2.figure.colorbar(pos, ax=imag2.ax)
            imag2.arr=self.gamma
            imag2.Show()
        event.Skip()

    def nuevo_perfil(self, event):  # wxGlade: MyDialog.<event_handler>
        x=np.linspace(0,self.parent.paginaActual.arrayIma[0].shape[1],self.parent.paginaActual.arrayIma[0].shape[1])
        y=np.linspace(0,self.parent.paginaActual.arrayIma[0].shape[0],self.parent.paginaActual.arrayIma[0].shape[0])
        fplan=interp.interp2d(x,y,self.parent.paginaActual.arrayIma[0],fill_value=0)
        fescan=interp.interp2d(x,y,self.parent.paginaActual.arrayIma[1],fill_value=0)
        self.per=PerfilDoble(self.parent,fplan,fescan,self.parent.paginaActual.arrayIma[0],self.parent.paginaActual.arrayIma[1],self.parent.paginaActual.figure,self.parent.paginaActual.axA)
        event.Skip()

    def generar_isodosis(self, event): 
        x=np.linspace(0,self.parent.paginaActual.arrayIma[0].shape[1],self.parent.paginaActual.arrayIma[0].shape[1])
        y=np.linspace(0,self.parent.paginaActual.arrayIma[0].shape[0],self.parent.paginaActual.arrayIma[0].shape[0])
        arrnorm=self.parent.paginaActual.arrayIma[0]/self.normalizacion
        arrnorm1=self.parent.paginaActual.arrayIma[1]/self.normalizacion
        ima=ImagenMatplotlibLibre(self.parent)
        self.axR=ima.figure.add_axes([0.25, .03, 0.50, 0.02])
        self.spor = Slider(self.axR, '%', 0, 100.0, valinit=50, valstep=1)
        def update(val):
            iv=self.spor.val
            ima.ax.clear()
            ima.ax.contour(x, y, arrnorm - iv/100.0, levels = [0],colors=['red'])
            ima.ax.contour(x, y, arrnorm1 - iv/100.0, levels = [0],colors=['green'])
            ima.figure.canvas.draw_idle()
        self.spor.on_changed(update)  
        ima.Show()
        event.Skip()
        event.Skip()
        
    def seleccionarROI(self, event):
        k=self.parent.paginaActual.figure.ginput(2)
        x1=k[0][0]
        y1=k[0][1]
        x2=k[1][0]
        y2=k[1][1]
        
        self.parent.arayActual[0]=(self.parent.arayActual[0])[min(int(y1),int(y2)):max(int(y1),int(y2)),min(int(x1),int(x2)):max(int(x1),int(x2))]
        self.parent.arayActual[1]=(self.parent.arayActual[1])[min(int(y1),int(y2)):max(int(y1),int(y2)),min(int(x1),int(x2)):max(int(x1),int(x2))]

        
        self.parent.paginaActual.axA.clear()
        self.parent.paginaActual.axA.imshow((1.0-self.parent.alpha)*self.parent.arayActual[0]+self.parent.alpha*self.parent.arayActual[1],cmap=mpl.cm.gray)
        self.parent.paginaActual.figure.canvas.draw()
        self.parent.paginaActual.figure.canvas.flush_events()  

    def guardar_comparacion(self, event):  # wxGlade: MyDialog.<event_handler>
        print("Event handler 'guardar_comparacion' not implemented!")
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
