# Importa el módulo threading para manejo de hilos
import threading
# Importa la clase Ball (lógica y propiedades de la bola)
from Ball import Ball
# Importa la clase BallDTO (objeto de transferencia de datos de la bola)
from BallDTO import BallDTO

# Clase que representa el Modelo del juego (lógica y estado de las bolas)
class GameModel:
    # Constructor
    def __init__(self, screen_index, screen_width, screen_height):
        # Índice de la pantalla actual (0 o 1)
        self.screen_index = screen_index
        # Dimensiones de la pantalla
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Lista de bolas activas en esta pantalla
        self.balls = []
        # Contador para asignar ID único a cada bola creada localmente
        self.ball_id_counter = 0
        # Lock para garantizar acceso seguro desde múltiples hilos
        self.lock = threading.Lock()
        # Diccionario para marcar bolas que acaban de ser recibidas (no se usa aquí directamente)
        self.just_received = {}

    # Metodo para actualizar la posición de todas las bolas y verificar colisiones con las paredes
    def update_balls(self):
        with self.lock:
            for ball in self.balls:
                ball.move()  # Actualiza la posición según la velocidad
                ball.check_wall_collision(self.screen_width, self.screen_height)  # Rebotar si toca un borde

    # Metodo que devuelve una copia de la lista actual de bolas
    def get_balls(self):
        with self.lock:
            return list(self.balls)

    # Metodo que crea una nueva bola en esta pantalla
    def add_ball(self):
        with self.lock:
            # Crea una nueva bola con ID único
            ball = Ball(self.ball_id_counter, self.screen_width, self.screen_height)
            # Asigna el índice de pantalla actual
            ball.screen_index = self.screen_index
            # Agrega la bola a la lista
            self.balls.append(ball)
            # Incrementa el contador de IDs para la próxima bola
            self.ball_id_counter += 1
            # Muestra por consola la creación de la bola
            print(f"Bola {ball.id} iniciada en pantalla {self.screen_index}")

    # Metodo que agrega una bola recibida desde otra pantalla (transferida)
    def add_received_ball(self, ball_dto):
        with self.lock:
            # Reconstruye la bola a partir del objeto de transferencia
            ball = Ball.from_dto(ball_dto)
            # Asigna el índice de pantalla actual
            ball.screen_index = self.screen_index
            # Coloca la bola al borde izquierdo para que entre desde la izquierda
            ball.x = 0 + ball.radius
            # Agrega la bola a la lista de bolas activas
            self.balls.append(ball)
            # Muestra en consola la recepción de la bola
            print(f"[Pantalla {self.screen_index}] Recibe bola transferida: {ball_dto}")

    # Metodo que selecciona las bolas que deben ser transferidas a la otra pantalla
    def get_balls_to_transfer(self):
        with self.lock:
            to_transfer = []  # Lista de bolas que se van a transferir
            remaining = []    # Lista de bolas que se quedan en la pantalla
            for ball in self.balls:
                # Solo transfiere si estamos en pantalla 0 y la bola sale por el borde derecho
                if self.screen_index == 0 and ball.x + ball.radius >= self.screen_width:
                    to_transfer.append(ball)
                else:
                    remaining.append(ball)
            # Actualiza la lista de bolas con solo las que se quedan
            self.balls = remaining
            # Devuelve las bolas que deben ser enviadas
            return to_transfer