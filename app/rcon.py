import socket
import select
import struct
import time


class Rcon:
    def __init__(self, host, password, port, timeout=5):
        self.host = host
        self.password = password
        self.port = port
        self.timeout = timeout
        self.socket = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self._send(3, self.password)

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def _read(self, length):
        deadline = time.time() + self.timeout
        data = b""
        while len(data) < length:
            if time.time() >= deadline:
                raise TimeoutError("Connection timed out")
            remaining_time = deadline - time.time()
            self.socket.settimeout(remaining_time)
            data += self.socket.recv(length - len(data))
        return data

    def _send(self, out_type, out_data):
        if self.socket is None:
            raise ConnectionError("Must connect before sending data")

        ## send a request packet
        out_payload = struct.pack("<ii", 0, out_type) + out_data.encode("utf-8") + b"\x00\x00"
        out_length = struct.pack("<i", len(out_payload))
        self.socket.send(out_length + out_payload)

        ## read response packets
        in_data = ""
        while True:
            ## read a packet
            (in_length,) = struct.unpack("<i", self._read(4))
            in_payload = self._read(in_length)
            in_id, in_type = struct.unpack("<ii", in_payload[:8])
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]

            ## sanity checks
            if in_padding != b"\x00\x00":
                raise ValueError("Incorrect padding")
            if in_id == -1:
                raise PermissionError("Login failed")

            ## record the response
            in_data += in_data_partial.decode("utf-8")

            ## if there's nothing more to receive, return the response
            if not select.select([self.socket], [], [], 0)[0]:
                return in_data

    def command(self, command):
        result = self._send(2, command)
        time.sleep(0.003)  # MC-72390 fix
        return result

