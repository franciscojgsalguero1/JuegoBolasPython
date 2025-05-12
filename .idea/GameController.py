from GameModel import GameModel
from GameView import GameView

class GameController:
    def __init__(self, game_id, transfer_manager):
        self.model = GameModel(game_id, transfer_manager)
        self.view = GameView(self, game_id)

    def create_ball(self):
        self.model.create_ball()

    def destroy_balls(self):
        self.model.destroy_balls()

    def receive_transfers(self):
        self.model.receive_transferred_balls()

    def shutdown(self):
        self.model.active = False
        self.model.transfer_manager.set_active(self.model.game_id, False)

def start_game(game_id, transfer_manager):
    GameController(game_id, transfer_manager)