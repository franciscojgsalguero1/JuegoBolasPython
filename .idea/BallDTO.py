class BallDTO(dict):
    def __init__(self, id, x, y, dx, dy, color):
        super().__init__(id=id, x=x, y=y, dx=dx, dy=dy, color=color)
