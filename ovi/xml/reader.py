import xml.sax.handler

class Version():
    def __init__(self):
        self.id ="";
        self.name="";
        self.script="";
        self.description="";
        
class VersionEquipo():
    def __init__(self):
        self.eqp_computer = "";
        self.eqp_os = "";
        self.path = "";
        self.listVersions = [];
    def setComputer(self, comp):
        self.eqp_computer = comp;
    def setOS(self, os):
        self.eqp_os = os;
    def setPath(self, path):
        self.path = path;
    def getComputer(self):
        return self.eqp_computer;
    def getOS(self):
        return self.eqp_os;
    def getPath(self):
        return self.path;

class ProyectoOVI():
    def __init__(self):
        self.pro_thumnail="";
        self.pro_id="";
        self.pro_nombre="";
        self.pro_area="";
        self.pro_listEquipos=[];
        
    def setNombre(self, nombre):
        self.pro_nombre=nombre;
    def getNombre(self):
        return self.pro_nombre;
    def setThumbnail(self, thumb):
        self.pro_thumbnail=thumb;
    def getThumbnail(self):
        return self.pro_thumbnail;
    def setID(self, sID):
        self.id=sID;
    def getID(self):
        return self.id;
    def setArea(self, areaConoc):
        self.area = areaConoc;
    def getArea(self):
        return self.area;

class ContenidosReader(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.listaElementos = [];
        self.numProyectos = 0;
        self.bProyecto = False;
        self.bPath = False;#indica si se encontro la ruta
        self.bProyectPath = False;#indica que se encontro o no la etiqueta proyectPath
        self.bListaConts = False;#indica que se encontro la etiqueta ListaContenidos
        self.thumbnail = "";
        self.pathProyecto = "";
        self.idVer = "";
        self.nickname = "";
        self.comandoEje = "";
        self.descripcion = "";

    
    def startElement(self, name, attrs):
        if name == 'content':
          numProyectos = int(attrs.get('total',""));
          fechaAct = attrs.get('date',"");
          self.bListaConts = True;
        if self.bListaConts == True:   
            if name == 'proyect':
                self.proyectoTemp = ProyectoOVI();
                self.proyectoTemp.setID(attrs.get('id',""));
                self.proyectoTemp.setNombre(attrs.get('name',""));
                self.proyectoTemp.setArea(attrs.get('area',""));
                self.bProyecto = True;
        if self.bProyecto == True:
            if name == 'img':
                self.proyectoTemp.setThumbnail(attrs.get('src',""));
            elif name == 'tags':
                pass
            elif name == 'proyect_path':  
                self.verEquipo_path = VersionEquipo();
                self.verEquipo_path.setComputer(attrs.get('computer', ""));
                self.verEquipo_path.setOS(attrs.get('os', ""));
                self.bProyectPath = True;
        if self.bProyectPath == True:
            if name == 'path':
                self.bPath = True;
		self.verEquipo_path.setPath(attrs.get('value',""));
            if name == 'version':
                self.version1 = Version();
                self.version1.id = attrs.get('id',"");
                self.version1.name = attrs.get('name',"");
                self.version1.script = attrs.get('script',"");
                self.version1.description =  attrs.get('description',"")
                
                   
          
    def endElement(self, name):
        if name == 'proyect':
            self.numProyectos = self.numProyectos+1;
            self.listaElementos.append(self.proyectoTemp);
            self.bProyecto = False;
        elif name == 'content':
            self.bListaConts = False;
        elif name == 'proyect_path':
            self.proyectoTemp.pro_listEquipos.append(self.verEquipo_path);
            self.bProyectPath = False;
        elif name == 'version':
            self.verEquipo_path.listVersions.append(self.version1)
        elif name == 'path':
            self.bPath = False;

    def characters(self, ch):
        if self.bPath == True:
            self.pathProyecto = ch;
            self.bPath = False;
            

class EquiposOVI(xml.sax.handler.ContentHandler):
    def __init__(self):
        pass

    def startElement(self, name, attrs):
        if name == 'ListaContenidos':
            numContenidos = int(attrs.get('numContenidos',""));
            fechaActualizacionCont = attrs.get('fechaActualizacion', "");
        elif name == 'Equipo':
            nombreEq = attrs.get('nombre',"");
            nombreEq = attrs.get('modelo',"");
            nombreEq = attrs.get('IP',"");
        elif name == 'RefProyecto':
            ListContenidos = [];
            ListContenidos.append(attrs.get('nickname',""));
        elif name == 'ListaSoftware':
            numAplicaciones = int(attrs.get('numAplicaciones',""));
            fechaActualizacionApp = attrs.get('fechaActualizacion', "");
        elif name == 'Software':
            pass;
        elif name == 'UsuarioConexionRemota':
            self.ListUsr = [];
            self.ListUsr.append([attrs.get('nombre',""),attrs.get('password',""),attrs.get('puerto',"")]);

    def characters(self, ch):
        pass;
            
        
