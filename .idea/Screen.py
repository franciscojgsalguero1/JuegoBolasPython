import tkinter as tk
from GameModel import GameModel
from BallDTO import BallDTO
from Ball import Ball

class Screen:
    def __init__(self, game_id, transfer_manager):
        self.game_id = game_id
        self.transfer_manager = transfer_manager
        self.model = GameModel(game_id, transfer_manager)
        self.view = None

    def create_view(self):
        self.view = tk.Tk()
        self.view.title(f"Pantalla {self.game_id}")
        self.view.geometry(f"500x400+{100 + self.game_id * 600}+100")
        self.view.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(self.view, width=500, height=400, bg="white")
        self.canvas.pack()

        tk.Button(self.view, text="Crear Bola", command=self.model.create_ball).pack(side=tk.LEFT)
        tk.Button(self.view, text="Destruir Bolas", command=self.model.destroy_balls).pack(side=tk.LEFT)

        self.running = True
        self.update_view()
        self.view.mainloop()

    def update_view(self):
        if not self.running:
            return
        self.model.receive_transferred_balls()
        self.canvas.delete("all")
        for ball in self.model.balls:
            self.canvas.create_oval(
                ball.dto.x, ball.dto.y,
                ball.dto.x + 20, ball.dto.y + 20,
                fill=ball.dto.color
            )
        self.view.after(50, self.update_view)

    def on_close(self):
        self.running = False
        self.model.active = False
        self.transfer_manager.set_active(self.game_id, False)
        self.view.destroy()

def start_screen(game_id, transfer_manager):
    app = Screen(game_id, transfer_manager)
    app.create_view()