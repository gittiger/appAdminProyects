import wx
import os
from ovi.xml import reader

#Tiene la informacion para ejecutar los comandos(remota o localmente) y dar la informacion sobre el proyecto
class Izquierdo(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self, parent, id, size=(250,300), style=wx.BORDER_SUNKEN)

	#Se declaran los botones y se les pasan algunos parametros
	botonRun = wx.Button(self, -1, "EJECUTAR", (0,0), wx.Size(150,80));
	botonRun.SetFont(wx.Font(12,wx.DEFAULT,wx.NORMAL, wx.BOLD));
	botonRun.SetOwnBackgroundColour(wx.Colour(120,1,0)); 

	botonInfo = wx.Button(self, -1, "Ver Info", (0,0), wx.Size(100, 60));

	#se agregan los eventos para cada uno de los botones
	self.Bind(wx.EVT_BUTTON, self.OnEjecutar, id=botonRun.GetId());
	self.Bind(wx.EVT_BUTTON, self.OnInfo, id=botonInfo.GetId());

	#Organizador principal del panel izquierdo
	mainSizer = wx.BoxSizer(wx.VERTICAL);

	#Organizador de botones
	botonSizer = wx.BoxSizer(wx.HORIZONTAL);
	botonSizer.Add(botonRun, 0, wx.SHAPED);
	botonSizer.Add(botonInfo, 0, wx.SHAPED);


	mainSizer.Add(botonSizer, 0, wx.SHAPED);
	self.SetSizer(mainSizer);

	self.host="132.248.124.90"

        #El lanzador de aplicaciones es una lista que contiene 2 elementos(la aplicacion, y argumentos)
        self.lanzadorAplicaciones = "";
        
    def OnEjecutar(self, event):
        comandoFinal = self.lanzadorAplicaciones.getLanzador() + self.lanzadorAplicaciones.getArgumentos();
	print(os.getcwd());
        os.system("source /home/ixtli/.bashrc")
        print("comandoFinal"+comandoFinal);
 	os.system(comandoFinal+" &");
    
    
    def OnInfo(self, event):
        dlgInfo = wx.Dialog(self, -1, "Informacion Proyectos")
        dlgInfo.ShowModal()

    #Establece el lanzador de aplicaciones
    def setLanzador(self, lanz):
        self.lanzadorAplicaciones = lanz;

#Contiene otros controles avanzados como la lista de imagenes de proyectos y el combo box de proyectos a elegir
class Derecho(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self, parent, id, size=(500,300));
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL);
        comboSizer = wx.BoxSizer(wx.VERTICAL);
        self.comboEquipos = wx.ComboBox(self, -1, "HP wx4900", wx.Point(0,0), wx.Size(250,80));
        self.comboEquipos.Insert("HP wx4900",0);
        self.comboEquipos.Insert("SGI Onyx 350",1);
        self.comboEquipos.Insert("Cluster SUN Ultra 40",2);

        #Se une con la funcion para manejar en el cambio del combo box
        self.Bind(wx.EVT_COMBOBOX, self.OnComboElementoClicked, id=self.comboEquipos.GetId())

        #Crea el combo de seleccion por area del conocimiento
	self.comboAreaConoc = wx.ComboBox(self, -1, "Ciencias Fisico Matematicas y de las Ingenierias", wx.Point(0,250), wx.Size(250,50));
        self.comboAreaConoc.Insert("Ciencias Fisico Matematicas y de las Ingenierias",0);
        self.comboAreaConoc.Insert("Ciencias Biologicas Quimicas y de la Salud",1);
        self.comboAreaConoc.Insert("Ciencias Sociales",2);
        self.comboAreaConoc.Insert("Humanidades y Artes",3);
        self.comboAreaConoc.Insert("Otros recursos",4);
        #Se crea la union del evento con el combobox de area del conocimiento
        self.Bind(wx.EVT_COMBOBOX, self.OnComboAreaClicked, id=self.comboAreaConoc.GetId());
      
        
        #Lista que contiene las imagenes de los proyectos
        self.listProyectos = wx.ListCtrl(self,-1,wx.Point(0,0),wx.Size(550,600));
        
        #Se enlaza el evento para saber cuando se ha dado click
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnElementoClicked, id=self.listProyectos.GetId())
        
        self.listaImagenes = wx.ImageList(110, 110);
        self.listProyectos.SetImageList(self.listaImagenes,wx.IMAGE_LIST_NORMAL);

        #Se agregan los comboBox al layout con orientacion vertical
	comboSizer.Add(wx.Size(10,50));
	texto1 = wx.StaticText(self,-1,"EQUIPO IXTLI: ", wx.Point(0,0),wx.Size(150,30));
	texto1.SetFont(wx.Font(10,wx.DEFAULT,wx.NORMAL, wx.BOLD));
	comboSizer.Add(texto1,0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL);
        comboSizer.Add(self.comboEquipos, 0, wx.SHAPED);
	comboSizer.Add(wx.Size(10,80));
	texto2 = wx.StaticText(self,-1,"AREA: ");
	texto2.SetFont(wx.Font(10,wx.DEFAULT,wx.NORMAL, wx.BOLD));
	comboSizer.Add(texto2,0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL);
        comboSizer.Add(self.comboAreaConoc, 0, wx.SHAPED);
	comboSizer.Add(wx.Size(10,50));
	bitIxtli = wx.BitmapFromImage(wx.Image("recursos/ixtli.bmp"));
	butMap = wx.BitmapButton(self, -1, bitIxtli, wx.Point(0,0), wx.Size(150,150));
	comboSizer.Add(butMap, 0, wx.SHAPED|wx.ALIGN_CENTER_HORIZONTAL );

        #Sizer para acomodar todos los controles en un layout
        mainSizer.Add(comboSizer, 0, wx.SHAPED, 1);
        mainSizer.Add(self.listProyectos, 1, wx.EXPAND, 1);
        self.SetSizer(mainSizer);

        #Declaracion del lanzador o aplicacion que se va a ejecutar
        self.lanzadorApps = "";
        self.pathLanzador = ""; #Ruta al lanzador de aplicaciones
        #argumentos para la aplicacion que se va a ejecutar
        self.argsApp = "";
        self.equipoActual = "HP wx4900";
        self.areaActual = "Fisico Matematicas e Ingenierias";


    def recargarThumbs(self):#Actualiza todos los thumbnails que se crear de los proyectos leidos del archivo xml
        self.listaImagenes.RemoveAll();
        self.listProyectos.DeleteAllItems();
        indImgs = 0;
        for ix in range(0,self.infoXML.numProyectos):  
            for iEquipos in range(0,len(self.infoXML.listaElementos[ix].pro_listEquipos)):
                for iVersions in range(0,len(self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].listVersions)):
                    computadora = self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].getComputer();
                    areaC = self.infoXML.listaElementos[ix].getArea();
                    if  (computadora == self.equipoActual) & (areaC == self.areaActual):  
                        item1 = wx.ListItem();
                        imagenTemp = wx.Image(self.infoXML.listaElementos[ix].getThumbnail());
                        imagenTemp = imagenTemp.Scale(110,110);
                        bitElement = wx.BitmapFromImage(imagenTemp);
                        self.listaImagenes.Add(bitElement);
                        item1.SetText( self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].listVersions[iVersions].name);
			print(self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].listVersions[iVersions].name);
                        item1.SetImage(indImgs);
                        self.listProyectos.InsertItem(item1);
                        indImgs = indImgs + 1;
                        
                
    def setInfoXML(self, xmlDatos):
        self.infoXML = xmlDatos;
	self.areaActual = "Ciencias Fisico Matematicas y de las Ingenierias" 
        self.recargarThumbs();

                

    def OnElementoClicked(self,event):#Cada vez que se da click sobre un thumbnail, se buscan los datos sobre este proyecto
        i = event.GetIndex();
        strNomProyecto = self.listProyectos.GetItem(i).GetText();
       
        
        for ix in range(0,len(self.infoXML.listaElementos)):
             for iEquipos in range(0,len(self.infoXML.listaElementos[ix].pro_listEquipos)):
                  for iVersions in range(0,len(self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].listVersions)):
                    proyActual = self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].listVersions[iVersions].name;
                    if proyActual == strNomProyecto:
                        self.pathLanzador = str(self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].getPath());
                        self.lanzadorApps= str(self.infoXML.listaElementos[ix].pro_listEquipos[iEquipos].listVersions[iVersions].script);
			print(self.pathLanzador);
                        

    def OnComboElementoClicked(self, event):
        cadComboBox = self.comboEquipos.GetValue();
        self.equipoActual = cadComboBox;
        self.recargarThumbs();
        
    def OnComboAreaClicked(self, event):
        area = self.comboAreaConoc.GetValue();
        self.areaActual = area;
        self.recargarThumbs();
       
        

#Regresa el lanzador de aplicaciones (es decir la aplicacion que se va a ejecutar
    def getLanzador(self):
        return self.pathLanzador+"/"+self.lanzadorApps;
    
    def getArgumentos(self):
        return self.argsApp;

    def getPathProyecto(self):
        return self.pathLanzador;



        
        
