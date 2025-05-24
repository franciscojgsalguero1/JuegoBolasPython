# Clase que actúa como controlador del juego, coordinando el modelo y la transferencia de bolas
class GameController:
    def __init__(self, model, transfer_manager):
        # Guarda una referencia al modelo de juego (GameModel)
        self.model = model
        # Guarda una referencia al gestor de transferencias por socket (BallTransferManager)
        self.transfer_manager = transfer_manager
        # Bandera que indica si el juego sigue en ejecución
        self.running = True
        # Bandera que indica si el juego está pausado
        self.paused = False

        # Se añade una bola inicial al modelo al comenzar
        self.model.add_ball()

    # Metodo llamado en cada iteración del bucle principal del juego
    def update(self):
        # Si el juego está pausado, no se hace nada
        if self.paused:
            return

        # Actualiza la posición de las bolas y gestiona colisiones y lógica
        self.model.update_balls()

        # Obtiene las bolas que deben transferirse a la otra pantalla
        balls_to_transfer = self.model.get_balls_to_transfer()

        # Si hay bolas para transferir, se imprimen y se envían
        if balls_to_transfer:
            # ^1 invierte 0 a 1 o 1 a 0 → determina el índice de la otra pantalla
            print(f"[TransferManager] Enviando {len(balls_to_transfer)} bolas a pantalla {self.model.screen_index ^ 1}")
            self.transfer_manager.send_balls(self.model.screen_index ^ 1, balls_to_transfer)

    # Metodo para añadir manualmente una nueva bola (por ejemplo, al pulsar una tecla)
    def add_ball(self):
        self.model.add_ball()

    # Metodo para pausar el juego
    def pause(self):
        self.paused = True

    # Metodo para reanudar el juego
    def resume(self):
        self.paused = False

    # Metodo para detener completamente el juego
    def stop(self):
        self.running = False

    # Metodo llamado cuando se reciben bolas por socket desde la otra pantalla
    def handle_received_balls(self, balls_dto):
        # Recorre cada bola recibida en forma de DTO (diccionario) y la añade al modelo
        for dto in balls_dto:
            self.model.add_received_ball(dto)