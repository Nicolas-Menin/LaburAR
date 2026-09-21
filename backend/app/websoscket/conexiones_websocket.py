class ConexionWebSocket:
    """Conexiones de WebSocket"""
    def __init__(self):
        self.conexiones = {} # DICCIONARIO DONDE GUARDAMOS LAS CONEXIONES

    def conectar(self, conversacion_id: int, websocket,usuario_id: int):
        """Registra una conexion WebSocket en una conversacion"""
        # SI EL ID DE LA CONVERSACION NO SE ENCUENTRA
        # SE LE CREA UNA LISTA A LA CONVERSACION EN DONDE VAN A ESTAR LAS CONEXIONES WEBSOCKET DE LOS USUARIOS
        if conversacion_id not in self.conexiones:

            self.conexiones[conversacion_id] = []

        # SE LE AGREGA LA CONEXION WEBSOCKET Y EL ID DEL USUARIO A LA CONVERSACION
        self.conexiones[conversacion_id].append((usuario_id,websocket))

    def desconectar(self, conversacion_id: int, websocket):
        """Elimina una conexion WebSocket de una conversacionn"""

        # SI LA CONVERSACION SE ENCUENTRA EN EL DICCIONARIO
        if conversacion_id in self.conexiones:

            # OBTIENE LOS DATOS DENTRO DE LA LISTA DE CONVERSACION
            conexiones = self.conexiones[conversacion_id]

            # ITERAMOS LAS CONEXIONES DEE LA CONVERSACION
            for conexion in conexiones:

                # DONDE SI LA CONEXION WEBSOCKET ALMACENADA ES IGUAL A LA CONEXION RECIBIDA
                # ENTONCES LA ELIMINA DEL DICCIONARIO
                if conexion[1] == websocket:
                    conexiones.remove(conexion)
                    break

            # SI  NO HAY NINGUNA CONEXION ENTONCES ELIMINA LA CONVERSACION CON CONEXIONES VACIAS
            if not conexiones:
                del self.conexiones[conversacion_id]


    def obtener_conexiones(self, conversacion_id: int):
        """Obtiene las conexiones WebSocket activas de una conversación."""

        # RETORNA LAS CONEXIONES DE LA CONVERSACIONN
        return self.conexiones.get(conversacion_id, [])

conexion_websocket = ConexionWebSocket()