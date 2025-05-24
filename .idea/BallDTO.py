class BallDTO:
    def __init__(self, data):
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.dx = data['dx']
        self.dy = data['dy']
        self.color = data['color']