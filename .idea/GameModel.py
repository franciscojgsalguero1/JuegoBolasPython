import threading  # Para sincronización entre hilos
import time       # Para gestionar cooldowns de transferencia
from Ball import Ball
from BallDTO import BallDTO

# Clase que representa el Modelo del juego (lógica y estado de las bolas)
class GameModel:
    def __init__(self, screen_index, screen_width, screen_height):
        self.screen_index = screen_index                # Índice de la pantalla (0 o 1)
        self.screen_width = screen_width                # Ancho de pantalla
        self.screen_height = screen_height              # Alto de pantalla
        self.balls = []                                 # Lista de bolas activas
        self.ball_id_counter = 0                        # Contador de ID único por bola
        self.lock = threading.Lock()                    # Lock para acceso seguro entre hilos
        self.just_received = {}                         # (opcional) Diccionario para marcar bolas recibidas

    # Actualiza la posición de todas las bolas y verifica colisiones
    def update_balls(self):
        with self.lock:
            for ball in self.balls:
                ball.move()
                ball.check_wall_collision(self.screen_width, self.screen_height)

    # Devuelve una copia segura de la lista actual de bolas
    def get_balls(self):
        with self.lock:
            return list(self.balls)

    # Crea una nueva bola localmente en esta pantalla
    def add_ball(self):
        with self.lock:
            ball = Ball(self.ball_id_counter, self.screen_width, self.screen_height)
            ball.screen_index = self.screen_index
            self.balls.append(ball)
            self.ball_id_counter += 1
            print(f"Bola {ball.id} iniciada en pantalla {self.screen_index}")

    # Añade una bola recibida por transferencia desde otra pantalla
    def add_received_ball(self, ball_dto):
        with self.lock:
            ball = Ball.from_dto(ball_dto)
            ball.screen_index = self.screen_index
            # Posición de entrada según pantalla
            if self.screen_index == 0:
                ball.x = self.screen_width - ball.radius  # entra por la derecha
            else:
                ball.x = 0 + ball.radius  # entra por la izquierda
            self.balls.append(ball)
            print(f"[Pantalla {self.screen_index}] Recibe bola transferida: {ball_dto}")

    # Devuelve las bolas que deben ser transferidas a la otra pantalla
    def get_balls_to_transfer(self):
        with self.lock:
            to_transfer = []     # Lista de bolas que serán transferidas
            remaining = []       # Lista de bolas que se quedarán
            cooldown = 1.0       # Tiempo de espera para permitir retransferencia

            for ball in self.balls:
                # Si acaba de ser transferida, esperamos a que pase el cooldown
                if ball.just_transferred:
                    if time.time() - ball.transfer_time >= cooldown:
                        ball.just_transferred = False
                    else:
                        remaining.append(ball)
                        continue  # No se transfiere aún

                # Condiciones de transferencia por pantalla
                if self.screen_index == 0 and ball.x + ball.radius >= self.screen_width:
                    # Sale por la derecha en pantalla 0
                    to_transfer.append(ball)
                elif self.screen_index == 1 and ball.x - ball.radius <= 0:
                    # Sale por la izquierda en pantalla 1
                    to_transfer.append(ball)
                else:
                    remaining.append(ball)

            self.balls = remaining
            return to_transfer