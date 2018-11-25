class Map:
    def __init__(self, size):
        self.map = self.__createMap(size)
        self.size = size

    # imprime mapa aliado
    def __str__(self):
        mapStr = ""
        mapStr += "\n "
        for col in range(self.size):
            mapStr += " " + str(col + 1)
        for lin in range(self.size):
            mapStr += ("\n%s " % (chr(ord('A') + lin)))
            for col in range(8):
                mapStr += ("%c " % self.map[lin][col])
        return mapStr

    # coloca uma embarcacao na posicao especificada
    def place(self, lin, col):
        linInt, colInt = self.__convertCoord(lin, col)
        if (linInt >= 0 and linInt < 8 and colInt >= 0 and colInt < 8):
            self.map[linInt][colInt] = 'N'
            return True
        else:
            return False

    # atualiza o mapa inimigo com o char especificado
    def updateMap(self, lin, col, char):
        linInt, colInt = self.__convertCoord(lin, col)
        self.map[linInt][colInt] = char

    # processa uma jogada na posicao especificada
    def fire(self, lin, col):
        linInt, colInt = self.__convertCoord(lin, col)
        if (linInt >= 0 and linInt < 8 and colInt >= 0 and colInt < 8):
            if self.map[linInt][colInt] == 'N':  # Navio aliado vira acerto
                self.map[linInt][colInt] = 'X'
                return 'X'
            elif self.map[linInt][colInt] == '~':  # Água não acertada vira A
                self.map[linInt][colInt] = 'A'
                return 'A'
            else:
                return 'E'
        else:
            return 'E'

    def __createMap(self, size):
        map = []
        for i in range(size):
            map.append(['~'] * size)
        return map

    def __convertCoord(self, lin, col):
        return ord(lin) - ord('A'), int(col) - 1


def main():
    aliado = Map(8)
    for i in range(4):
        aliado.place(chr(i + ord('A')), i)
        print(aliado)
    print(aliado.fire('A', 1))
    print(aliado.fire('B', 1))
    print(aliado)

# main()
