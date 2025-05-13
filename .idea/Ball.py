# Ball.py

class Ball:
    def __init__(self, ball_id, x, y, dx, dy, color):
        """
        Initializes a new ball with position, direction and color.

        :param ball_id: Unique identifier of the ball
        :param x: X coordinate of the ball
        :param y: Y coordinate of the ball
        :param dx: Horizontal velocity
        :param dy: Vertical velocity
        :param color: Color of the ball (string)
        """
        self.id = ball_id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.just_transferred = 0  # Cooldown to prevent immediate re-transfer

    def update_position(self):
        """
        Updates the position of the ball based on its current velocity.
        """
        self.x += self.dx
        self.y += self.dy

    def to_dict(self):
        """
        Converts the ball to a dictionary for socket transfer.

        :return: Dictionary with ball data
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
        Creates a Ball object from a dictionary received via socket.

        :param data: Dictionary containing ball data
        :return: Ball object
        """
        ball = Ball(
            data['id'],
            data['x'],
            data['y'],
            data['dx'],
            data['dy'],
            data['color']
        )
        return ball