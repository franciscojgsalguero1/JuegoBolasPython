import random
import time
from BallDTO import BallDTO

class Ball:
    def __init__(self, id, x, y, dx, dy, color, screen_id, last_transfer_time=None):
        self.id = id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.screen_id = screen_id
        self.last_transfer_time = last_transfer_time or 0

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self, width, height):
        if self.y <= 0 or self.y >= height:
            self.dy *= -1
        if self.x <= 0 or self.x >= width:
            self.dx *= -1

    def should_transfer(self, width):
        if time.time() - self.last_transfer_time < 0.5:
            return False
        return self.x < 0 or self.x > width

    def to_dto(self):
        return BallDTO(
            id=self.id,
            x=self.x,
            y=self.y,
            dx=self.dx,
            dy=self.dy,
            color=self.color
        )

    @staticmethod
    def from_dto(dto, screen_id):
        return Ball(
            id=dto["id"],
            x=dto["x"],
            y=dto["y"],
            dx=dto["dx"],
            dy=dto["dy"],
            color=dto["color"],
            screen_id=screen_id,
            last_transfer_time=time.time()
        )