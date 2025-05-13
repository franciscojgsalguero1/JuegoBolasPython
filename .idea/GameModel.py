import threading
from Ball import Ball
from BallDTO import BallDTO

class GameModel:
    def __init__(self, screen_index, screen_width, screen_height):
        """
        Inicializa el modelo del juego para una pantalla específica.

        :param screen_index: índice de la pantalla actual (0 o 1)
        :param screen_width: ancho de la pantalla
        :param screen_height: alto de la pantalla
        """
        self.screen_index = screen_index
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.balls = []  # Lista de bolas activas en esta pantalla
        self.ball_id_counter = 0  # Contador para asignar IDs únicos a las bolas
        self.lock = threading.Lock()  # Para proteger acceso concurrente a la lista de bolas
        self.just_received = {}  # Diccionario para evitar retransmisión inmediata de bolas

        self.add_ball()  # ✅ Crear una bola al iniciar el modelo

    def update(self):
        """
        Actualiza la posición de las bolas.
        """
        with self.lock:
            for ball in self.balls:
                ball.move()
                ball.check_wall_collision(self.screen_width, self.screen_height)

    def get_balls(self):
        """
        Retorna una copia de las bolas actuales (para dibujarlas).
        """
        with self.lock:
            return list(self.balls)

    def add_ball(self):
        """
        Crea una nueva bola y la añade al modelo.
        """
        with self.lock:
            ball = Ball(self.ball_id_counter, self.screen_width, self.screen_height)
            self.balls.append(ball)
            self.ball_id_counter += 1
            print(f"Bola {ball.id} iniciada en pantalla {self.screen_index}")

    def remove_ball(self, ball_id):
        """
        Elimina una bola del modelo por su ID.
        """
        with self.lock:
            self.balls = [ball for ball in self.balls if ball.id != ball_id]

    def balls_to_transfer(self):
        """
        Retorna una lista de bolas que deben ser transferidas a otra pantalla.
        """
        with self.lock:
            to_transfer = []
            remaining = []

            for ball in self.balls:
                if ball.x < 0 or ball.x > self.screen_width:
                    # Bola ha salido por la izquierda o derecha → se transfiere
                    to_transfer.append(ball)
                else:
                    remaining.append(ball)

            self.balls = remaining
            return to_transfer

    def receive_ball(self, ball_dto: BallDTO):
        """
        Recibe una bola desde otra pantalla y la añade al modelo.
        """
        with self.lock:
            new_ball = Ball.from_dto(ball_dto)
            self.balls.append(new_ball)
            print(f"Bola {new_ball.id} iniciada en pantalla {self.screen_index}")