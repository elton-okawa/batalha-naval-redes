def main():
	size = 8
	aliado = [['~' for x in range(size)] for y in range (size)]

def create(linha, coluna, aliado): #coloca uma embarcacao na posicao especificada
	if (linha >= 0 and linha < 7 and coluna >= 0  and coluna < 7):
		aliado[linha][coluna] = 'N'
		return True
	else:
		return False

def imprimir_aliado(aliado): #imprime mapa aliado
	print ("\n   Campo aliado")
	print ("\n  A B C D E F G H")
	for x in range(7):
		print ("\n%i " %(x + 1))
		for indice in range(7):
			print ("%c " %aliado[x][indice])

def jogada(linha, coluna, aliado): #processa uma jogada na posicao especificada
	if (linha > -1 and linha < 7 and coluna > -1 and coluna < 7):
		if aliado[linha][coluna] == 'N' #Navio aliado vira acerto
			aliado[linha][coluna] = 'X'
			return 'X'
		if aliado[linha][coluna] == 'X' #Acerto continua sendo acerto. Envia mensagem de erro
			aliado[linha][coluna] = 'X'
			return 'E'
		if aliado[linha][coluna] == '~' #Água não acertada vira A
			aliado[linha][coluna] = 'A'
			return 'A'
		if aliado[linha][coluna] == 'A' #Água continua sendo água. Envia mensagem de erro
			aliado[linha][coluna] = 'A'
			return 'E'