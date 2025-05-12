import threading
import time

MARGIN = 1
WIDTH, HEIGHT = 500, 400
BALL_SIZE = 20

class Ball(threading.Thread):
    def __init__(self, dto, model):
        super().__init__(daemon=True)
        self.dto = dto
        self.model = model
        self.alive = True

    def run(self):
        print(f"Bola {self.dto.id} iniciada en pantalla {self.model.game_id}")
        while self.alive and self.model.active:
            self.dto.x += self.dto.dx
            self.dto.y += self.dto.dy

            # Rebote vertical con márgenes
            if self.dto.y <= MARGIN:
                self.dto.y = MARGIN
                self.dto.dy *= -1
            elif self.dto.y >= HEIGHT - BALL_SIZE - MARGIN:
                self.dto.y = HEIGHT - BALL_SIZE - MARGIN
                self.dto.dy *= -1

            # Transferencia si sale completamente por izquierda o derecha
            if self.dto.x < -BALL_SIZE or self.dto.x > WIDTH:
                other_id = 1 - self.model.game_id
                if self.model.transfer_manager.transfer_ball(self.model.game_id, self.dto):
                    print(f"Bola {self.dto.id} transferida de {self.model.game_id} a {other_id}")
                    if self in self.model.balls:
                        self.model.balls.remove(self)
                    break
                else:
                    self.dto.dx *= -1
                    self.dto.x = max(MARGIN, min(self.dto.x, WIDTH - BALL_SIZE - MARGIN))

            time.sleep(0.02)