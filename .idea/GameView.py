import tkinter as tk

class GameView:
    def __init__(self, controller, game_id):
        self.controller = controller
        self.game_id = game_id
        self.root = tk.Tk()
        self.root.title(f"Pantalla {game_id}")
        self.root.geometry(f"500x400+{100 + game_id * 600}+100")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="white")
        self.canvas.pack()

        tk.Button(self.root, text="Crear Bola", command=self.controller.create_ball).pack(side=tk.LEFT)
        tk.Button(self.root, text="Destruir Bolas", command=self.controller.destroy_balls).pack(side=tk.LEFT)

        self.running = True
        self.root.after(50, self.update_loop)
        self.root.mainloop()

    def update_loop(self):
        if not self.running:
            return
        try:
            self.controller.receive_transfers()
        except Exception as e:
            print(f"[Pantalla {self.game_id}] Error en transferencia: {e}")
            self.running = False
            return

        self.canvas.delete("all")
        print(f"[Pantalla {self.game_id}] Dibujando {len(self.controller.model.balls)} bolas")
        for ball in self.controller.model.balls:
            d = ball.dto
            self.canvas.create_oval(d.x, d.y, d.x + 20, d.y + 20, fill=d.color)
            self.canvas.create_text(d.x + 10, d.y + 10, text=str(d.id), fill="black")

        self.root.after(50, self.update_loop)

    def on_close(self):
        self.running = False
        print(f"[Pantalla {self.game_id}] Esperando que las bolas terminen antes de cerrar...")
        import time
        time.sleep(2.0)
        self.controller.shutdown()
        self.root.destroy()