import threading

class BallTransferManager:
    def __init__(self, manager):
        self.transfer_queues = manager.dict({0: manager.list(), 1: manager.list()})
        self.active_games = manager.dict({0: True, 1: True})
        self.lock = manager.Lock()

    def transfer_ball(self, from_id, dto):
        to_id = 1 - from_id
        with self.lock:
            if not self.active_games[to_id]:
                return False
            self.transfer_queues[to_id].append(dto.__dict__)
            return True

    def get_transferred_balls(self, to_id):
        with self.lock:
            dtos = list(self.transfer_queues[to_id])
            self.transfer_queues[to_id][:] = []
            print(f"[TransferManager] Enviando {len(dtos)} bolas a pantalla {to_id}")
            from BallDTO import BallDTO
            return [BallDTO(**d) for d in dtos]

    def set_active(self, game_id, active):
        with self.lock:
            self.active_games[game_id] = active