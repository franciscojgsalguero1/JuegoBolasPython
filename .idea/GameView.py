# Importa la librería pygame para gestionar gráficos y eventos del juego
import pygame

# Clase que representa la Vista del juego (responsable de mostrar gráficos en pantalla)
class GameView:
    # Constructor de la clase
    def __init__(self, screen_id, screen_width, screen_height):
        # Identificador de la pantalla (por si hay varias instancias en ejecución)
        self.screen_id = screen_id
        # Ancho de la pantalla
        self.screen_width = screen_width
        # Alto de la pantalla
        self.screen_height = screen_height
        # Crea una ventana de pygame con el tamaño especificado
        self.window = pygame.display.set_mode((screen_width, screen_height))
        # Establece el título de la ventana
        pygame.display.set_caption(f"Ball Game - Screen {screen_id}")
        # Define la fuente para renderizar texto (por defecto, tamaño 24)
        self.font = pygame.font.SysFont(None, 24)

    # Metodo que dibuja las bolas en pantalla
    def draw(self, balls):
        # Rellena el fondo de la ventana con color negro
        self.window.fill((0, 0, 0))
        # Dibuja cada bola en la ventana
        for ball in balls:
            pygame.draw.circle(self.window, pygame.Color(ball.color), (int(ball.x), int(ball.y)), ball.radius)
        # Renderiza un texto con el número de bolas en pantalla
        text = self.font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
        # Dibuja el texto en la esquina superior izquierda
        self.window.blit(text, (10, 10))
        # Actualiza la pantalla con los cambios
        pygame.display.flip()

    # Metodo para cerrar correctamente la ventana del juego
    def close(self):
        # Finaliza el módulo pygame
        pygame.quit()
