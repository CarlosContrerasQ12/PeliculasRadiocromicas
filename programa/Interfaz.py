#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Sun Sep 13 13:11:50 2020
#

import numpy as np
import wx
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit
from PIL import Image
from scipy.misc import face
from scipy.signal.signaltools import wiener

from dialogoCalibracionAlternativo import DialogoCalibracion
from claseCalibracion import *
from claseDialogoBackground import *

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

import tifffile as tiff

def leerDosis(nombre_archivo):
    arch=open(nombre_archivo)
    dosis=[]
    for line in arch.readlines():
        dosis.append(float(line))
    arch.close()
    return dosis

class ImagenWx(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.sbm=wx.StaticBitmap(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.sbm, 1, wx.EXPAND | wx.GROW)
        self.SetSizer(sizer)
        self.Fit()
        
class ImagenCuadernoMatplotlib(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi)
        #self.figure.gca().axis('off')
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        #sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1164, 626))
        self.notebookImagenes = aui.AuiNotebook(self, wx.ID_ANY)
        self.paginas=[]
        self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))
        #self.paginas.append(ImageFrame(self.notebookImagenes,size=(1024,576),mode='rgb'))
        #self.paginas.append(ImagenWx(self.notebookImagenes))
        self.PanelOpcionesImagen = wx.Panel(self, wx.ID_ANY)
        self.notebookControl = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1_pane_2 = wx.Panel(self.notebookControl, wx.ID_ANY)
        self.tree_ctrl_1 = wx.TreeCtrl(self.notebook_1_pane_2, wx.ID_ANY)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        
        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Guardar...", "")
        self.Bind(wx.EVT_MENU, self.funcionGuardar, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Abrir...", "")
        self.Bind(wx.EVT_MENU, self.funcionAbrir, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Cerrar", "")
        self.Bind(wx.EVT_MENU, self.funcionCerrar, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Archivo")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu_sub = wx.Menu()
        item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, "Calibracion Manual", "")
        self.Bind(wx.EVT_MENU, self.calibracionManual, id=item.GetId())
        item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, u"CalibracionAutomática", "")
        self.Bind(wx.EVT_MENU, self.calibracionAutomatica, id=item.GetId())
        wxglade_tmp_menu.Append(wx.ID_ANY, "Generar Calibracion", wxglade_tmp_menu_sub, "")
        self.frame_menubar.Append(wxglade_tmp_menu, "Calibracion")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Nuevo mapa de dosis", "")
        self.Bind(wx.EVT_MENU, self.generarMapaDosis, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Mapa de dosis")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Nueva comparacion", "")
        self.Bind(wx.EVT_MENU, self.generarComparacion, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Comparacion plan")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_5.Add(self.notebookImagenes, 5, wx.EXPAND, 0)
        sizer_5.Add(self.PanelOpcionesImagen, 1, wx.ALL | wx.EXPAND, 1)
        sizer_4.Add(sizer_5, 3, wx.EXPAND, 0)
        sizer_7.Add(self.tree_ctrl_1, 1, wx.EXPAND, 0)
        
        self.notebookImagenes.AddPage(self.paginas[0], "Bienvenido")
        figInicial=self.paginas[0].figure
        a1=figInicial.gca()
        im = Image.open('54fb8810327dd.jpg')
        araar=np.array(im)
        #self.paginas[0].sbm.SetBitmap(wx.Bitmap('54fb8810327dd.jpg'))
        a1.imshow(araar,aspect='auto',interpolation='spline36')
        
        self.notebook_1_pane_2.SetSizer(sizer_7)
        self.notebookControl.AddPage(self.notebook_1_pane_2, "notebook_1_pane_1")
        sizer_6.Add(self.notebookControl, 1, wx.EXPAND, 0)
        sizer_6.Add(self.panel_2, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_3)
        self.Layout()
        # end wxGlade

    def funcionGuardar(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'funcionGuardar' not implemented!")
        event.Skip()

    def funcionAbrir(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'funcionAbrir' not implemented!")
        event.Skip()

    def funcionCerrar(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'funcionCerrar' not implemented!")
        event.Skip()

    def calibracionManual(self, event):  # wxGlade: MyFrame.<event_handler>
        dialogoCalibracion=DialogoCalibracion(self)
        dialogoCalibracion.ShowModal()
        if dialogoCalibracion.resultado[0]!='cancelar':
            print(dialogoCalibracion.resultado)
            self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))
            self.notebookImagenes.AddPage(self.paginas[-1], "Calibracion")
            nuem=self.notebookImagenes.GetPageCount()-1
            self.notebookImagenes.SetSelection(nuem)
            figActual=self.paginas[-1].figure
            a1=figActual.gca()
            aray=tiff.imread(dialogoCalibracion.resultado[0])
            escalado=(aray/65535.0)*255
            dosisReal=leerDosis(dialogoCalibracion.resultado[1])
            araySinIrra=0*aray
            araySinLuz=0*aray
            a1.imshow(escalado.astype(int)) 

            if(dialogoCalibracion.resultado[6]):
                dialogoBackground=DialogoBackground(self)
                dialogoBackground.ShowModal()
                if dialogoBackground.resultado[0]!='cancelar' and dialogoBackground.resultado[0]!='':
                    araySinIrra=tiff.imread(dialogoBackground.resultado[0])
                    if(dialogoBackground.resultado[1]!=''):
                        araySinLuz=tiff.imread(dialogoBackground.resultado[1])
                
            if(dialogoCalibracion.resultado[4]):
                aray=wiener(aray,(40, 40))
                araySinIrra=wiener(araySinIrra,(40, 40))
                araySinLuz=wiener(araySinLuz,(40, 40))
                    
            
            
            #dosisReal.sort()
            n=len(dosisReal)
            print(n)
            dosisReal=np.array(dosisReal)
            k=figActual.ginput(n=2*n)
            print(k)
            print(dosisReal)
            x=[]
            y=[]
            
            promedioRojo=[]
            promedioVerde=[]
            promedioAzul=[]
            
            promedioRojoSinIrra=[]
            promedioVerdeSinIrra=[]
            promedioAzulSinIrra=[]
            
            promedioRojoSinLuz=[]
            promedioVerdeSinLuz=[]
            promedioAzulSinLuz=[]
            
            for i in range(2*n):
                x.append(k[i][0])
                y.append(k[i][1])
            for i in range(1,2*n,2):
                prom=65535-np.mean(aray[min(int(y[i-1]),int(y[i])):max(int(y[i-1]),int(y[i])),min(int(x[i-1]),int(x[i])):max(int(x[i-1]),int(x[i])),:],axis=(0,1))
                promSinIrra=65535-np.mean(araySinIrra[min(int(y[i-1]),int(y[i])):max(int(y[i-1]),int(y[i])),min(int(x[i-1]),int(x[i])):max(int(x[i-1]),int(x[i])),:],axis=(0,1))
                promSinLuz=65535-np.mean(araySinLuz[min(int(y[i-1]),int(y[i])):max(int(y[i-1]),int(y[i])),min(int(x[i-1]),int(x[i])):max(int(x[i-1]),int(x[i])),:],axis=(0,1))
                
                promedioRojo.append(prom[0])
                promedioVerde.append(prom[1])
                promedioAzul.append(prom[2])
                
                promedioRojoSinIrra.append(promSinIrra[0])
                promedioVerdeSinIrra.append(promSinIrra[1])
                promedioAzulSinIrra.append(promSinIrra[2])
                
                promedioRojoSinLuz.append(promSinLuz[0])
                promedioVerdeSinLuz.append(promSinLuz[1])
                promedioAzulSinLuz.append(promSinLuz[2])
                
            promedioRojo=np.array(promedioRojo)
            promedioVerde=np.array(promedioVerde)
            promedioAzul=np.array(promedioAzul)
            
            promedioRojoSinIrra=np.array(promedioRojoSinIrra)
            promedioVerdeSinIrra=np.array(promedioVerdeSinIrra)
            promedioAzulSinIrra=np.array(promedioAzulSinIrra)
            
            promedioRojoSinLuz=np.array(promedioRojoSinLuz)
            promedioVerdeSinLuz=np.array(promedioVerdeSinLuz)
            promedioAzulSinLuz=np.array(promedioAzulSinLuz)
            
            fdlg = wx.FileDialog(self, "Guardar calibracion",wildcard="calibraciones (*.txt)|*.txt", style=wx.FD_SAVE)
            fdlg.SetFilename("calibracion-")
            nombreArchivo=''
            
            promedioRojo=promedioRojo-promedioRojoSinIrra
            promedioAzul=promedioAzul-promedioAzulSinIrra
            promedioVerde=promedioVerde-promedioVerdeSinIrra
            

            if fdlg.ShowModal() == wx.ID_OK:
                nombreArchivo = fdlg.GetPath() + ".txt"
            print(dialogoCalibracion.resultado[2])
            print(dialogoCalibracion.resultado[3])
            
            calibr=CalibracionImagen(promedioRojo,promedioVerde,promedioAzul,dosisReal,dialogoCalibracion.resultado[2],dialogoCalibracion.resultado[3],dialogoCalibracion.resultado[5])  
            calibr.generar_calibracion(nombreArchivo)
            
            self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))    
            self.notebookImagenes.AddPage(self.paginas[-1], "Curva Calibracion")    
            nuem=self.notebookImagenes.GetPageCount()-1
            self.notebookImagenes.SetSelection(nuem)
            figActual=self.paginas[-1].figure
            a1=figActual.gca()
            
            a1.scatter(dosisReal,promedioRojo,marker='x',color='r')
            a1.scatter(dosisReal,promedioVerde,marker='x',color='g')
            a1.scatter(dosisReal,promedioAzul,marker='x',color='b')
            
            xGra=np.linspace(dosisReal[0],dosisReal[-1],100)
            yGra=calibr.funcionCali(xGra)
            
            a1.plot(xGra,yGra,'--')
        

    def calibracionAutomatica(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'calibracionAutomatica' not implemented!")
        event.Skip()

    def generarMapaDosis(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'generarMapaDosis' not implemented!")
        event.Skip()

    def generarComparacion(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'generarComparacion' not implemented!")
        event.Skip()

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    FilmQADog = MyApp(0)
    FilmQADog.MainLoop()
