import pickle
import socket
import threading
from BallDTO import BallDTO

class BallTransferManager:
    """
    Clase que gestiona la lógica de transferencia de bolas entre pantallas usando sockets en una arquitectura peer-to-peer.
    """

    def __init__(self, screen_id, on_receive_callback):
        """
        Inicializa el gestor de transferencia de bolas.

        :param screen_id: ID de la pantalla actual (0 o 1)
        :param on_receive_callback: Función que se ejecuta cuando se recibe una bola del socket
        """
        self.screen_id = screen_id
        self.on_receive_callback = on_receive_callback  # Callback para procesar bolas recibidas

        self.port = 1000  # Puerto compartido
        self.host = 'localhost'

        self.conn = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1.0)  # Evita bloquearse indefinidamente

        # Intenta conectar al puerto compartido. Si falla, se pone en modo servidor.
        try:
            self.socket.connect((self.host, self.port))
            self.conn = self.socket
            print(f"[TransferManager] Pantalla {screen_id} conectada como cliente")
        except:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"[TransferManager] Pantalla {screen_id} esperando conexión como servidor")
            self.conn, _ = self.socket.accept()
            print(f"[TransferManager] Pantalla {screen_id} aceptó conexión")

        # Hilo de escucha de recepción de bolas
        self.listen_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.listen_thread.start()

        self.lock = threading.Lock()

    def send_ball(self, ball):
        """
        Envía una bola a la otra pantalla a través del socket.

        :param ball: Instancia de la clase Ball
        """
        try:
            ball_dto = BallDTO.from_ball(ball)
            data = pickle.dumps(ball_dto)
            with self.lock:
                self.conn.sendall(len(data).to_bytes(4, byteorder='big') + data)
        except Exception as e:
            print(f"[TransferManager] Error al enviar bola: {e}")

    def receive_loop(self):
        """
        Hilo dedicado a recibir bolas constantemente del socket.
        """
        while True:
            try:
                # Recibir primero los 4 bytes que indican el tamaño del mensaje
                size_data = self.conn.recv(4)
                if not size_data:
                    continue
                size = int.from_bytes(size_data, byteorder='big')
                data = b''
                while len(data) < size:
                    packet = self.conn.recv(size - len(data))
                    if not packet:
                        break
                    data += packet
                if data:
                    ball_dto = pickle.loads(data)
                    self.on_receive_callback(ball_dto)
            except Exception as e:
                pass  # Se puede imprimir si se quiere debuggear