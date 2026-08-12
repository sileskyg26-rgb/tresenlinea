class InvalidMoveException(Exception):
    def __init__(self, message="Movimiento inválido"):
        super().__init__(message)