# Importa pickle para serializar objetos (en este caso, listas de bolas)
import pickle
# Importa threading para ejecutar la conexión en segundo plano
import threading
# Importa el manejador de conexiones por socket
from ConnectionHandler import ConnectionHandler

# Clase encargada de gestionar la transferencia de bolas entre pantallas
class BallTransferManager:
    def __init__(self, screen_index, port, receive_callback):
        self.screen_index = screen_index              # Índice de la pantalla actual (0 o 1)
        self.port = port                              # Puerto local en el que escucha esta instancia
        self.peer_port = port                         # Inicialmente el mismo puerto para ambos
        self.receive_callback = receive_callback      # Callback para manejar las bolas recibidas

        # Crea un manejador de conexión que usará sockets para enviar/recibir datos
        # Se le pasa el puerto y el callback interno que se encargará de procesar los datos recibidos
        self.connection_handler = ConnectionHandler(port, self._handle_received_data)

        # Inicia en segundo plano el hilo que se encarga de establecer la conexión
        threading.Thread(target=self.connection_handler.start, daemon=True).start()

    # Callback interno que se ejecuta cuando llegan datos del otro extremo
    def _handle_received_data(self, data_bytes):
        """Callback interno para deserializar y procesar bolas recibidas."""
        try:
            # Convierte los bytes recibidos de vuelta a una lista de DTOs
            balls_dto = pickle.loads(data_bytes)
            # Llama al callback del controlador para procesar las bolas
            self.receive_callback(balls_dto)
        except Exception as e:
            print(f"[Pantalla {self.screen_index}] Error al procesar datos recibidos: {e}")

    # Metodo público que envía bolas al otro extremo
    def send_balls(self, target_screen_index, balls):
        """Serializa y envía bolas al otro extremo."""
        try:
            # Convierte cada bola a su DTO
            data = [ball.to_dto() for ball in balls]
            # Serializa toda la lista como un único objeto
            data_bytes = pickle.dumps(data)
            # Envía los datos usando el manejador de conexión
            self.connection_handler.send(data_bytes)
        except Exception as e:
            print(f"[Pantalla {self.screen_index}] Error en transferencia: {e}")

    # Metodo para cerrar correctamente la conexión de red
    def close(self):
        """Cierra correctamente la conexión."""
        self.connection_handler.close()
