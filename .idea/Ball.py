import random
import math

class Ball:
    def __init__(self, id, screen_width, screen_height, x=None, y=None, dx=None, dy=None, color=None):
        self.id = id
        self.radius = 20  # Increased size for better visibility
        self.x = x if x is not None else random.randint(50, screen_width-50)
        self.y = y if y is not None else random.randint(50, screen_height-50)
        self.dx = dx if dx is not None else random.choice([-4, -3, 3, 4])
        self.dy = dy if dy is not None else random.choice([-4, -3, 3, 4])
        self.color = color if color is not None else (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.transfer_progress = 0
        self.transferring = False
        self.origin_screen = None
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        if not self.transferring:
            self.x += self.dx
            self.y += self.dy

    def check_wall_collision(self, width, height):
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.dy = -self.dy

    def is_off_screen(self, width):
        return (self.x < -self.radius or self.x > width + self.radius) and not self.transferring

    def start_transfer(self, origin_screen):
        self.transferring = True
        self.origin_screen = origin_screen
        self.transfer_progress = 0

    def update_transfer(self, dt):
        if self.transferring:
            self.transfer_progress = min(1, self.transfer_progress + dt * 5)  # Faster transfer
            if self.transfer_progress >= 1:
                self.transferring = False
                return True
        return False

    def to_dto(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'color': self.color,
            'radius': self.radius,
            'transferring': self.transferring,
            'transfer_progress': self.transfer_progress,
            'origin_screen': self.origin_screen,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height
        }

    @staticmethod
    def from_dto(dto):
        ball = Ball(
            id=dto['id'],
            x=dto['x'],
            y=dto['y'],
            dx=dto['dx'],
            dy=dto['dy'],
            color=dto['color'],
            screen_width=dto['screen_width'],
            screen_height=dto['screen_height']
        )
        ball.radius = dto['radius']
        ball.transferring = dto['transferring']
        ball.transfer_progress = dto['transfer_progress']
        ball.origin_screen = dto['origin_screen']
        return ball