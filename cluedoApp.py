from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from interfaces.inicial import Inicial,Modo_Juego,Configurar_Servidor
from enum import Enum
from jugador import Jugador
from threading import Lock

class ModoJuego(Enum):
    NO_CONFIGURADO=0
    CLIENTE = 1
    SERVIDOR = 2

class EstadoApp(Enum):
    ADMITIENDO_CLIENTES = 0
    SERVIDOR_COMPLETO=1
    EN_JUEGO=2

class Personajes(Enum):
    PIZARRO = "Sr. Pizarro"
    AMAPOLA = "Srta. Amapola"
    RUBIO = "Prof. Rubio"
    PRADO = "Sra. Prado"
    MARINA = "Marqués de Marina"
    

class CluedoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.modoJuego = ModoJuego.NO_CONFIGURADO  
        self.estado =  EstadoApp.ADMITIENDO_CLIENTES
        self.max_numero_jugadores = None    #int numero máximo de jugadores remotos (depende del número de jugadores seleccionado por el usuario) 
        self.jugadorLocal = None            #Objeto Jugador para gestionar Jugador local
        self.jugadoresExternos = {}         #Diccionario con proxys para gestionar objetos Jugador remotos 
        self.lock_JugadoresExternos = Lock()                  #Objeto lock para bloquear concurrencia en el acceso de los threads a jugadoresExternos

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        return Configurar_Servidor()

    def actualizar_jugador(self,jugador:Jugador):
        resultado = False
        if jugador.alias not in self.jugadoresExternos.keys():
            self.jugadoresExternos[jugador.alias] = jugador
            resultado = True
            if len(self.jugadoresExternos)==self.max_numero_jugadores:
                self.estado = EstadoApp.SERVIDOR_COMPLETO

        return resultado

    



CluedoApp().run()