class GameController:
    def __init__(self, model, transfer_manager):
        self.model = model
        self.transfer_manager = transfer_manager
        self.running = True
        self.paused = False
        self.model.add_ball()  # Start with one ball

    def update(self):
        if self.paused:
            return

        self.model.update_balls()

        # Handle outgoing transfers
        balls_to_transfer = self.model.get_balls_to_transfer()
        if balls_to_transfer:
            target_screen = self.model.screen_index ^ 1  # Flip between 0 and 1
            self.transfer_manager.send_balls(target_screen, balls_to_transfer)

        # Handle incoming transfers
        received_dto = self.transfer_manager.receive_balls()
        if received_dto:
            self.handle_received_balls(received_dto)

    def add_ball(self):
        self.model.add_ball()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False

    def handle_received_balls(self, balls_dto):
        if balls_dto:  # Only process if we actually got data
            for dto in balls_dto:
                self.model.add_received_ball(dto)