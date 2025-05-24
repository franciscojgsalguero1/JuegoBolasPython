import random

class Ball:
    def __init__(self, id, screen_width, screen_height):
        self.id = id
        self.radius = 10 # radio de la bola
        self.x = screen_width // 2 # posición iniciar de la bola en el eje x (en medio de la pantalla)
        #self.y = random.randint(self.radius, screen_height - self.radius)
        self.y = screen_width // 2 # # posición iniciar de la bola en el eje y (en medio de la pantalla)
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, 2])
        self.color = random.choice(['red', 'green', 'blue', 'yellow'])
        self.screen_index = 0
        self.just_transferred = False

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def check_wall_collision(self, screen_width, screen_height):
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.dy *= -1
        if self.screen_index == 1:
            if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
                self.dx *= -1
        elif self.screen_index == 0:
            if self.x - self.radius <= 0:
                self.dx *= -1

    def to_dto(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'color': self.color
        }

    @staticmethod
    def from_dto(dto):
        ball = Ball(dto['id'], 0, 0)
        ball.x = dto['x']
        ball.y = dto['y']
        ball.dx = dto['dx']
        ball.dy = dto['dy']
        ball.color = dto['color']
        return ball