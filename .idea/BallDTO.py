# Clase BallDTO: objeto de transferencia de datos para una bola

class BallDTO:
    def __init__(self, id, x, y, dx, dy, color):
        self.id = id      # Identificador único de la bola
        self.x = x        # Posición X de la bola
        self.y = y        # Posición Y de la bola
        self.dx = dx      # Velocidad horizontal
        self.dy = dy      # Velocidad vertical
        self.color = color  # Color de la bola (en texto, por ejemplo: "red")

    # Metodo que convierte un objeto BallDTO en diccionario (útil para serialización)
    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'color': self.color
        }

    # Metodo estático que crea un BallDTO desde un diccionario
    @staticmethod
    def from_dict(data):
        return BallDTO(
            id=data['id'],
            x=data['x'],
            y=data['y'],
            dx=data['dx'],
            dy=data['dy'],
            color=data['color']
        )