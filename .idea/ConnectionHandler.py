# ConnectionHandler.py
import socket
import threading
import pickle

class ConnectionHandler:
    def __init__(self, port, peer_port, on_receive_callback):
        self.port = port
        self.peer_port = peer_port
        self.on_receive_callback = on_receive_callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', self.port))
        self.socket.listen(1)
        self.connection = None
        self.running = True
        threading.Thread(target=self._connect_loop, daemon=True).start()

    def _connect_loop(self):
        while self.running and self.connection is None:
            try:
                self.socket.settimeout(1.0)
                self.connection, _ = self.socket.accept()
            except socket.timeout:
                try:
                    self.connection = socket.create_connection(('localhost', self.peer_port), timeout=1.0)
                except (ConnectionRefusedError, socket.timeout):
                    continue
        if self.connection:
            threading.Thread(target=self._receive_loop, daemon=True).start()

    def _receive_loop(self):
        try:
            while self.running:
                header = self._recv_exact(4)
                if not header:
                    break
                length = int.from_bytes(header, 'big')
                data = self._recv_exact(length)
                if data:
                    message = pickle.loads(data)
                    self.on_receive_callback(message)
        except Exception as e:
            print(f"[ConnectionHandler] Error de recepción: {e}")

    def _recv_exact(self, n):
        data = b''
        while len(data) < n:
            try:
                packet = self.connection.recv(n - len(data))
                if not packet:
                    return None
                data += packet
            except:
                return None
        return data

    def send(self, obj):
        if not self.connection:
            return
        try:
            data = pickle.dumps(obj)
            length = len(data).to_bytes(4, 'big')
            self.connection.sendall(length + data)
        except Exception as e:
            print(f"[ConnectionHandler] Error de envío: {e}")

    def close(self):
        self.running = False
        if self.connection:
            self.connection.close()
        self.socket.close()
