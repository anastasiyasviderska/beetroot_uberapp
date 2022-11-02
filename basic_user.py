from uber_server import Server

class BasicUser:

    uber_server = Server('database')

    def __init__(self):
        self.username = None
        self.password = None

    def __repr__(self) -> str:
        return f"name: {self.username}"

    def draw_menu(self) -> dict:
        pass