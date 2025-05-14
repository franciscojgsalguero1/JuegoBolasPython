import multiprocessing.connection

class BallTransferManager:
    def __init__(self, screen_index, connections):
        self.screen_index = screen_index
        self.connections = connections

    def send_balls(self, target_index, balls):
        try:
            conn = self.connections[target_index]
            if conn and conn.writable:
                # Mark these balls as coming from this screen
                for ball in balls:
                    ball.screen_index = self.screen_index
                data = [ball.to_dto() for ball in balls]
                conn.send(data)
                print(f"[Transfer] Sent {len(balls)} balls to screen {target_index}")
        except Exception as e:
            print(f"[Transfer Error] {e}")

    def receive_balls(self):
        try:
            conn = self.connections[self.screen_index]
            if conn and conn.poll():
                data = conn.recv()
                print(f"[Transfer] Received {len(data)} balls on screen {self.screen_index}")
                return data
        except Exception as e:
            print(f"[Receive Error] {e}")
        return None