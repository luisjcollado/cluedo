from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from redes.red import obtener_ip

class Inicial(MDScreen):
    pass

class Modo_Juego(MDScreen):
    pass
class Cliente_conf(MDScreen):
    pass

class Configurar_Servidor(MDScreen):
    ipServidor = StringProperty("")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipServidor = obtener_ip()
        print ("La IP del servidor: {}".format(self.ipServidor))
        self.servidor = False
    
    def on_text(self,txtField, contenido):
        print("El contenido es {}".format(len(contenido)))
        if len(contenido)<3 or len(contenido)>15:
            #self.ids.alias.helper_text_mode='on_error'
            self.ids.alias.helper_text='El alias debe tener al menos 3 letras y menos de 15'
            self.ids.alias.error = True

        else:
            self.ids.alias.helper_text='Tu apodo para la partida'
            self.ids.alias.error = False

    def interruptor_servidor(self):
        # Comprobar que iniciamos correctamente el objeto servidor
        # Obtenemos la dirección ip y el puerto de escucha.
        # Creamos un objeto jugador con el alias proporcionado por el usuario y le asignamos el Servidor
        # Ajustamos el color del widget al estado del servidor
        self.servidor = not (self.servidor)
        if self.servidor:
            self.ids.bt_iniciar.text_color='green'
            self.ids.bt_iniciar.line_color='green'
            self.ids.bt_iniciar.text='Parar Servidor'
        else:
            self.ids.bt_iniciar.text_color='red'
            self.ids.bt_iniciar.line_color='red'
            self.ids.bt_iniciar.text='Iniciar Servidor'

        
