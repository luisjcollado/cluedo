import json
from threading import Thread,Lock

from jugador import Jugador
from cluedoApp import EstadoApp

class Comm(Thread):
    
    def __init__(self,nsocket,kivyapp, group: None = ..., target= None, name: str | None = ..., args  = ..., kwargs: None = ..., *, daemon: bool | None = ...) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self.app = kivyapp
        self.comm = nsocket
        self.activo = True

    def run(self):
        while self.activo:
            datos = self.comm.recv(1024).decode

            self.interprete(datos)

            if not datos:
                self.activo = False
                break

        self.comm.close()

    def interprete(self,datos):
        '''Redirigimos las órdenes que se reciben del cliente conectado por el socket
        @param: datos Cadena json empaquetados
        '''
        entrada = json.loads(datos)
        if entrada['comando']=="C_Conexion_Inicial":
            #Bloqueamos la conexión para evitar que otro cliente interfiera y superemos el número de conexiones máximas
            self.app.lock_JugadoresExternos.acquire()
            jugadorAnnadido = False
            if self.app.estado == EstadoApp.ADMITIENDO_CLIENTES:
                codigo = "Obtener_Codigo" #Obtenemos la hora de conexion para utilizarla como código de cliente
                nJugador = Jugador(entrada['alias'],codigo,self)
                respuesta = {'comando':'S_Conexion_Inicial','codigo':codigo,'mensaje':'Conectado'}
                resultado = self.actualizar_remoto(respuesta)
                if resultado:
                    jugadorAnnadido = self.app.actualizar_jugador(nJugador)

                else:
                    self.activo = False     #Si hay problemas con la conexión inicial, reiniciamos el proceso desde cero.
            else:
                respuesta = {'comando':'S_Conexion_Inicial','mensaje':'Conexión rechazada (número máximo de jugadores alcanzado)'}
                self.actualizar_cliente(respuesta)
                self.activo = False     #Cerramos la conexión y finalizamos en thread.
            
            #Desbloqueamos la conexion para permitir a otros jugadores acceder
            self.app.lock_JugadoresExternos.release()
        else:
            print(datos)

    def actualizar_(self,datos:dict):
        '''Enviar instrucciones al cliente que se encuentra conectado
        @param: datos objeto diccionario con las instrucciones para el cliente
        '''
        resultado = False
        try:
            self.sock.sendall(json.dumps(datos).encode(encoding = 'UTF-8'))
            resultado=True
        except:
            pass

        return resultado