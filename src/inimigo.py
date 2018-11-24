def main():
	size = 8
	inimigo = [['~' for x in range(size)] for y in range (size)]

def imprimir_inimigo(inimigo): #imprime mapa inimigo
	print ("\n   Campo inimigo")
	print ("\n  A B C D E F G H")
	for x in range(7):
		print ("\n%i " %(x + 1))
		for indice in range(7):
			print ("%c " %inimigo[x][indice])

def jogada(linha, coluna, inimigo, resultado): #processa o resultado de uma jogada
	if resultado == 'X' #Registra acerto no mapa
		inimigo[linha][coluna] = 'X'
	if resultado == 'A' #Registra água no mapa
		inimigo[linha][coluna] = 'A'
	if resultado == 'E' #Nada ocorre caso Erro