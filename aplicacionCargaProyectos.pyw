#!/usr/bin/python
# Aplicacion para la carga de proyectos
# UNIVERSIDAD NACIONAL AUTONOMA DE MEXICO
# DIRECCION GENERAL DE COMPUTO Y DE TECNOLOGIAS DE INFORMACION Y DE COMUNICACION
# OBSERVATORIO DE VISUALIZACION IXTLI


import wx
import os
import xml.sax.handler
from xml import sax
from ovi import Panel
from ovi.xml import reader
import paramiko


class VentanaPrincipal(wx.Frame):
    def __init__(self,parent,id, title):
        wx.Frame.__init__(self, parent, id, title, size=(900,750))

        #panel principal
        panel = wx.Panel(self, -1);

        self.SetIcon(wx.Icon("recursos/ixtli.bmp", wx.BITMAP_TYPE_BMP));

        #Se crean los paneles de la izquierda y derecha
        panelIzq = Panel.Izquierdo(panel, -1);
        panelDer = Panel.Derecho(panel, -1);

        #Se crea el menu
        menuArchivo = wx.Menu();

        #Los menues de salir y de acerca de son proporcionados por wxWidgets
        menuAbout = menuArchivo.Append(wx.ID_ABOUT, "&Acerca de", "Informacion");
        menuExit = menuArchivo.Append(wx.ID_EXIT, "&Salir", "Sale del programa")


        #Se crea la barra de menues
        menuBar = wx.MenuBar();
        menuBar.Append(menuArchivo, "&File");#Se agrega el menu archivo
        #self.SetMenuBar(menuBar)

        hbox = wx.BoxSizer(wx.VERTICAL);
        hbox.Add(panelDer, 0,  wx.EXPAND);
        hbox.Add(panelIzq, 0,  wx.EXPAND);

        panel.SetSizer(hbox);

        readerHandlerContenidos = reader.ContenidosReader();
        parser = sax.make_parser();
        parser.setContentHandler(readerHandlerContenidos);
        parser.parse(open('contenidosIxtli.xml'));

        readerHandlerEquipos = reader.EquiposOVI();
        parser2 = sax.make_parser();
        parser2.setContentHandler(readerHandlerEquipos);
        parser2.parse(open('equiposIxtli.xml'));

        panelDer.setInfoXML(readerHandlerContenidos);
        
        #Establece el lanzador para el panel izquierdo
        panelIzq.setLanzador(panelDer);
            
        self.Centre()
        self.Show(True)

        # Datos para la conexion SSH
        ssh_servidor = '132.248.83.1'
        ssh_usuario  = 'ixtli'
        ssh_clave    = 'ieghee2Q'
        ssh_puerto   = 22 # O el puerto SSH que use nuestro servidor
        comando      = 'amira -mt /home/ixtli/ixtliCraneo/Demo/BOTONERA.hx &' # el comando que vamos a ejecutar en el servidor

        #ssh_servidor = '132.248.83.4'
        #ssh_usuario  = 'ixtli'
        #ssh_clave    = 's@lm0nix'
        #ssh_puerto   = 22 # O el puerto SSH que use nuestro servidor
        #comando      = 'ls' # el comando que vamos a ejecutar en el servidor
 
        # Conectamos al servidor
        #conexion = paramiko.Transport((ssh_servidor, ssh_puerto))
        #conexion.connect(username = ssh_usuario, password = ssh_clave)
 
        # Abrimos una sesion en el servidor
        #canal = conexion.open_session()
        # Ejecutamos el comando, en este caso un sencillo 'ls' para ver
        # el listado de archivos y directorios
        #canal.exec_command(comando);
 
        # Y vamos a ver la salida
        #salida = canal.makefile('rb', -1).readlines()

        #if salida:
             #Si ha ido todo bien mostramos el listado de directorios
            #print salida
        #else:
            # Si se ha producido algun error lo mostramos
            #print canal.makefile_stderr('rb', -1).readlines()
        #conexion.close()

        
        

if __name__=="__main__":
    app = wx.App()
    VentanaPrincipal(None, -1, 'Administrador Proyectos')
    app.MainLoop()
