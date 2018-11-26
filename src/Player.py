from Map import Map
import time

class Player:
    def __init__(self, connection, mapSize, encode):
        self.connection = connection
        self.map = Map(mapSize)
        self.enemyMap = Map(mapSize)
        self.score = 0
        self.encode = encode

    def __str__(self):
        string = ""
        string += "Seu status:\n"
        string += "Score: %d\n" %(self.score)
        string += "Seu mapa:\t\t\t\t\tMapa adversário:"
        ownMap = str(self.map).split('\n')
        enemyMap = str(self.enemyMap).split('\n')
        for i in range(len(ownMap)):
            string += ownMap[i] + "\t\t\t\t" + enemyMap[i] + "\n"
        return string

    def sendMessage(self, message):
        time.sleep(0.05)
        self.connection.sendall(bytes(message, self.encode))

    def receiveMessage(self):
        return self.connection.recv(64).decode(self.encode)

    def place(self, lin, col):
        return self.map.place(lin, col)

    def fire(self, lin, col):
        return self.map.fire(lin, col)

    def updateEnemyMap(self, lin, col, char):
        self.enemyMap.updateMap(lin, col, char)

    def printMap(self):
        return self.map.__str__()

    def getMap(self):
        return self.map

    def getEnemyMap(self):
        return self.enemyMap

    def updateScore(self):
        self.score += 1

    def getScore(self):
        return self.score

    def closeConnection(self):
        self.connection.close()
