from src.Map import Map

class Player:
    def __init__(self, connection, mapSize, encode):
        self.connection = connection
        self.map = Map(mapSize)
        self.score = 0
        self.encode = encode

    def sendMessage(self, message):
        self.connection.sendall(bytes(message, self.encode))

    def receiveMessage(self):
        return self.connection.recv(64).decode(self.encode)

    def place(self, lin, col):
        return self.map.place(lin, col)

    def getMap(self):
        return self.map

    def updateScore(self, score):
        self.score += score

    def getScore(self):
        return self.score

    def closeConnection(self):
        self.connection.close()