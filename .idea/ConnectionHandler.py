# Importa los módulos necesarios
import socket           # Para comunicación por red
import threading        # Para ejecución en paralelo (hilos)
import pickle           # Para serializar y deserializar objetos Python

# Clase encargada de manejar la conexión entre pantallas
class ConnectionHandler:
    def __init__(self, port, peer_port, on_receive_callback):
        # Puerto en el que esta instancia escuchará conexiones entrantes
        self.port = port
        # Puerto del otro par (pantalla remota)
        self.peer_port = peer_port
        # Función que se llamará al recibir un mensaje
        self.on_receive_callback = on_receive_callback
        # Crea un socket TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar el puerto sin esperar que el sistema lo libere
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Asocia el socket al puerto local y a localhost
        self.socket.bind(('localhost', self.port))
        # Pone el socket en modo de escucha (máximo 1 conexión)
        self.socket.listen(1)
        # Inicialmente no hay conexión establecida
        self.connection = None
        # Bandera para mantener activo el bucle de conexión
        self.running = True
        # Inicia un hilo en segundo plano que intenta conectar con el otro extremo
        threading.Thread(target=self._connect_loop, daemon=True).start()

    # Metodo interno que intenta conectar con el otro extremo
    def _connect_loop(self):
        while self.running and self.connection is None:
            try:
                # Intenta aceptar una conexión entrante
                self.socket.settimeout(1.0)
                self.connection, _ = self.socket.accept()
            except socket.timeout:
                # Si no hay conexión entrante, intenta conectarse al otro puerto
                try:
                    self.connection = socket.create_connection(('localhost', self.peer_port), timeout=1.0)
                except (ConnectionRefusedError, socket.timeout):
                    continue  # Si falla, lo intenta de nuevo en el siguiente ciclo
        # Una vez establecida la conexión, inicia un hilo de recepción
        if self.connection:
            threading.Thread(target=self._receive_loop, daemon=True).start()

    # Metodo interno que recibe mensajes continuamente
    def _receive_loop(self):
        try:
            while self.running:
                # Lee los primeros 4 bytes para saber el tamaño del mensaje
                header = self._recv_exact(4)
                if not header:
                    break
                # Convierte los 4 bytes del encabezado en un entero (longitud del mensaje)
                length = int.from_bytes(header, 'big')
                # Recibe los bytes exactos del mensaje
                data = self._recv_exact(length)
                if data:
                    # Deserializa el objeto recibido
                    message = pickle.loads(data)
                    # Llama al callback con el mensaje recibido
                    self.on_receive_callback(message)
        except Exception as e:
            print(f"[ConnectionHandler] Error de recepción: {e}")

    # Metodo auxiliar que recibe exactamente n bytes (bloqueante)
    def _recv_exact(self, n):
        data = b''
        while len(data) < n:
            try:
                # Recibe los bytes restantes
                packet = self.connection.recv(n - len(data))
                if not packet:
                    return None  # Conexión cerrada
                data += packet
            except:
                return None  # Error en la conexión
        return data

    # Envía un objeto serializado a través de la conexión
    def send(self, obj):
        if not self.connection:
            return
        try:
            # Serializa el objeto con pickle
            data = pickle.dumps(obj)
            # Calcula la longitud del mensaje y la convierte en 4 bytes
            length = len(data).to_bytes(4, 'big')
            # Envía primero la longitud y luego el contenido
            self.connection.sendall(length + data)
        except Exception as e:
            print(f"[ConnectionHandler] Error de envío: {e}")

    # Cierra la conexión y detiene el manejador
    def close(self):
        self.running = False  # Detiene los bucles
        if self.connection:
            self.connection.close()  # Cierra la conexión establecida
        self.socket.close()  # Cierra el socket que escucha conexiones