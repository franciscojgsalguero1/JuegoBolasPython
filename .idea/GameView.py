import pygame

# Clase encargada de mostrar la interfaz gráfica de una pantalla
class GameView:
    def __init__(self, screen_id, screen_width, screen_height):
        # Inicialización de parámetros
        self.screen_id = screen_id  # Identificador único de la pantalla (0 o 1)
        self.screen_width = screen_width  # Ancho de la pantalla
        self.screen_height = screen_height  # Alto de la pantalla

        # Inicialización de la ventana de Pygame
        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Ball Game - Screen {screen_id}")

        # Fuente para mostrar texto en pantalla
        self.font = pygame.font.SysFont(None, 24)

    # Método para dibujar todas las bolas en pantalla
    def draw(self, balls):
        print(f"[Pantalla {self.screen_id}] Dibujando {len(balls)} bolas")
        self.window.fill((0, 0, 0))  # Limpiar pantalla con color negro

        # Dibujar cada bola como un círculo
        for ball in balls:
            pygame.draw.circle(self.window, ball.color, (int(ball.x), int(ball.y)), ball.radius)

        # Mostrar el número de bolas activas en pantalla
        text = self.font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
        self.window.blit(text, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()

    # Método para cerrar correctamente la ventana
    def close(self):
        pygame.quit()
