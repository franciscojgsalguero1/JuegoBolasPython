import json

class BallDTO:
    """
    BallDTO (Data Transfer Object) representa una bola que se puede enviar a través del socket.
    Esta clase contiene solo los datos necesarios para la transferencia entre pantallas.
    """

    def __init__(self, ball_id, x, y, dx, dy, color):
        """
        Inicializa el objeto BallDTO con los parámetros necesarios.

        :param ball_id: Identificador único de la bola
        :param x: Posición x de la bola
        :param y: Posición y de la bola
        :param dx: Dirección en x (velocidad horizontal)
        :param dy: Dirección en y (velocidad vertical)
        :param color: Color de la bola
        """
        self.id = ball_id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color

    def to_dict(self):
        """
        Convierte el objeto en un diccionario para facilitar la serialización.

        :return: Diccionario con los atributos de la bola
        """
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'color': self.color
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un BallDTO a partir de un diccionario (proceso inverso a to_dict).

        :param data: Diccionario que representa una bola
        :return: Objeto BallDTO
        """
        return BallDTO(
            data['id'],
            data['x'],
            data['y'],
            data['dx'],
            data['dy'],
            data['color']
        )

    def serialize(self):
        """
        Serializa el objeto en una cadena JSON para enviarlo por socket.

        :return: Cadena JSON que representa el objeto
        """
        return json.dumps(self.to_dict()).encode('utf-8')

    @staticmethod
    def deserialize(data):
        """
        Deserializa una cadena JSON en un objeto BallDTO.

        :param data: Cadena de bytes JSON recibida por socket
        :return: Objeto BallDTO
        """
        return BallDTO.from_dict(json.loads(data.decode('utf-8')))