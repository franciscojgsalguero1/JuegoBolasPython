import multiprocessing
from GameController import GameController

# Function to start the game for a given screen
def run_game(screen_id, port):
    # Create a GameController for the given screen ID and shared port
    controller = GameController(screen_id, port)
    # Start the game loop for this screen
    controller.run()

# Entry point of the application
def main():
    port = 10000  # Port for socket communication between screens
    processes = []  # List to keep track of subprocesses

    # Create and start a separate process for each screen
    for screen_id in [0, 1]:  # You can add more screen IDs if needed
        p = multiprocessing.Process(target=run_game, args=(screen_id, port))
        p.start()
        processes.append(p)

    # Wait for all screen processes to finish
    for p in processes:
        p.join()

# Start the program
if __name__ == "__main__":
    main()