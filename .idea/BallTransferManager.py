import pickle
import threading
from ConnectionHandler import ConnectionHandler

class BallTransferManager:
    def __init__(self, screen_index, port, receive_callback):
        self.screen_index = screen_index                          # Índice de la pantalla actual (0 o 1)
        self.port = port                                          # Puerto local para escuchar
        self.peer_port = port                                     # Puerto del peer (el mismo inicialmente)
        self.receive_callback = receive_callback                  # Función a llamar al recibir bolas

        self.connection_handler = ConnectionHandler(port, self._handle_received_data)
        threading.Thread(target=self.connection_handler.start, daemon=True).start()

    def _handle_received_data(self, data_bytes):
        """Callback interno para deserializar y procesar bolas recibidas."""
        try:
            balls_dto = pickle.loads(data_bytes)                 # Deserializa lista de DTOs
            self.receive_callback(balls_dto)                     # Llama al callback del controlador
        except Exception as e:
            print(f"[Pantalla {self.screen_index}] Error al procesar datos recibidos: {e}")

    def send_balls(self, target_screen_index, balls):
        """Serializa y envía bolas al otro extremo."""
        try:
            data = [ball.to_dto() for ball in balls]
            data_bytes = pickle.dumps(data)
            self.connection_handler.send(data_bytes)
        except Exception as e:
            print(f"[Pantalla {self.screen_index}] Error en transferencia: {e}")

    def close(self):
        """Cierra correctamente la conexión."""
        self.connection_handler.close()
