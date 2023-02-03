'''
clase Servidor
Esta clase se ocupa de gestionar el servidor de conexiones entrantes.
'''
#from kivymd.app import App
import socket
from threading import Thread
import random
from redes.comm import Comm


class Servidor(object):
    def __init__(self,parent,conexiones:int):
        self.parent = parent #Normalmente la instancia de la clase App de kivymd
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = self._obtener_ip()
        self.puerto = None 
        self.max_conexiones = conexiones 
        self.thread = None
        self._activo = False
   

    def iniciar_servidor(self) ->list:
        #generamos un puerto aleatorio a partir del 10000
        bind = False
        while not bind:
            puerto = random.randint(10000,30000) 
            try:
                self.sock.bind((self.host,puerto))
                self.sock.listen(self.max_conexiones)
                self.puerto=puerto
                bind = True
            except socket.error as error:
                pass

        self._activo = True
        self.servidor = Thread(target=self._correr)
        self.servidor.start()
        return [self.host,self.puerto]

    def detener_servidor(self):
        self._activo = False

    def _correr(self):
        '''Thread donde va a correr el servidor aceptando conexiones. Cuando la conexión es validada se pasará al servidor para que la asigne a su usuario.
        
        '''
        while self._activo:
            nuevo_socket,direccion = self.sock.accept()
            nThread = Comm(nuevo_socket,self.parent)
            nThread.start()
        self.sock.close()


    def _obtener_ip(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255',1))
            IP=s.getsockname()[0]
        except:
            IP= None
        finally:
            s.close()

        #return IP
        return IP 
