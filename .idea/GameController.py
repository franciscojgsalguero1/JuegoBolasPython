import pygame
import time

class GameController:
    def __init__(self, model, transfer_manager):
        self.model = model
        self.transfer_manager = transfer_manager
        self.running = True
        self.paused = False

        # ✅ Crear una bola al inicio del juego
        self.model.add_ball()

    def update(self):
        if self.paused:
            return

        # Actualizar posición de las bolas
        self.model.update_balls()

        # Verificar si alguna bola debe ser transferida
        balls_to_transfer = self.model.get_balls_to_transfer()
        if balls_to_transfer:
            print(f"[TransferManager] Enviando {len(balls_to_transfer)} bolas a pantalla {self.model.screen_index ^ 1}")
            self.transfer_manager.send_balls(self.model.screen_index ^ 1, balls_to_transfer)

    def add_ball(self):
        # Método público para agregar una bola manualmente (por tecla, etc.)
        self.model.add_ball()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False

    def handle_received_balls(self, balls_dto):
        # Manejar bolas recibidas desde otra pantalla
        for dto in balls_dto:
            self.model.add_received_ball(dto)
