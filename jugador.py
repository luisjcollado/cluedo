"""Documentació de módulo
Este módulo se utiliza para dar toda la funcionalidad de los jugadores de cluedo, tanto locales como remotos
La clase Jugador contiente la información para conectar al jugador con el servidor de juego, así como la situación 
del jugador durante el desarrollo de la partida"""

__author__='Luis José Pérez Sánchez del Collado'
__copyright__ = ''
__licencia__= 'GPL'
__version__="1.0.1"
__email__="luisjcollado@malvecinos.com"
__status__="Desarrollo"


class Jugador(object):
    def __init__(self,alias:str,codigo:str,conn) -> None:
        super().__init__()
        self.alias = alias      #nombre que se usará para identificar al jugador en el juego
        self.codigo = codigo    #código de verificación para posibles reconoxiones que se asigna en su primera conexión.
        self.personaje = None   #Personaje tradicional del cluedo que el jugador elige para el juego  
        self.conn = conn
