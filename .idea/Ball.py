# Importa el módulo random para generar valores aleatorios
import random

# Clase que representa una bola en el juego
class Ball:
    def __init__(self, id, screen_width, screen_height):
        self.id = id  # Identificador único de la bola
        self.radius = 10  # Radio de la bola (tamaño fijo)
        # Posición inicial en el eje X: centrada horizontalmente
        self.x = screen_width // 2
        # Posición inicial en el eje Y: valor aleatorio dentro de los límites verticales de la pantalla
        self.y = random.randint(self.radius, screen_height - self.radius)
        # Velocidad horizontal aleatoria: -2 (izquierda) o 2 (derecha)
        self.dx = random.choice([-2, 2])
        # Velocidad vertical aleatoria: -2 (arriba) o 2 (abajo)
        self.dy = random.choice([-2, 2])
        # Color aleatorio entre una lista de colores
        self.color = random.choice(['red', 'green', 'blue', 'yellow'])
        # Índice de la pantalla donde se encuentra actualmente la bola (0 o 1)
        self.screen_index = 0
        # Bandera para controlar si la bola acaba de ser transferida (para evitar rebote inmediato)
        self.just_transferred = False

    # Metodo que actualiza la posición de la bola según su velocidad
    def move(self):
        self.x += self.dx
        self.y += self.dy

    # Metodo que comprueba colisiones con las paredes y rebota si es necesario
    def check_wall_collision(self, screen_width, screen_height):
        # Rebota verticalmente si toca el borde superior o inferior
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.dy *= -1
        if self.screen_index == 1:
            # En pantalla 1, solo rebota si toca el borde derecho (no rebota por la izquierda para recibir bolas)
            if self.x + self.radius >= screen_width:
                self.dx *= -1
        else:
            # En pantalla 0, rebota solo si toca el borde izquierdo
            if self.x - self.radius <= 0:
                self.dx *= -1

    # Metodo que convierte esta bola en un diccionario (para transferir por red)
    def to_dto(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'color': self.color
        }

    # Metodo estático que reconstruye una bola a partir de un diccionario (DTO)
    @staticmethod
    def from_dto(dto):
        # Crea la bola con ID, pero ignora el tamaño de pantalla ya que se reescriben los atributos
        ball = Ball(dto['id'], 0, 0)
        ball.x = dto['x']
        ball.y = dto['y']
        ball.dx = dto['dx']
        ball.dy = dto['dy']
        ball.color = dto['color']
        return ball