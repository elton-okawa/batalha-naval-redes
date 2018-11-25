#############################################
#                                           #
# PCS3614 - Redes de Computadores I         #
# Nome: Helio Jin Wu Kim   NUSP 9833106     #
# Nome: Elton Yoshio Okawa NUSP 9836579     #
#                                           #
#############################################

import socket
import sys
import time
import os
import traceback
from _thread import *
import threading
import os.path
from os import path

from src.Player import Player

ENCODE = 'UTF-8'
MAP_SIZE = 8
TURN = 'turn'
WAIT = 'wait'
OK = 'ok'

# print_lock = threading.Lock() 

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    s.bind(server_address)

    s.listen()

    connected = 0
    try:
        while True:
            print('Waiting for connection')
            player1, player1Address = s.accept()
            # print_lock.acquire()
            player1.sendall(bytes('Waiting for another player\n', ENCODE))

            player2, player2Address = s.accept()
            player1.sendall(bytes('Ready to play', ENCODE))
            player2.sendall(bytes('Ready to play', ENCODE))
            start_new_thread(battleshipFunction, (player1, player2))

            # connection, client_address = s.accept()
            # start_new_thread(handleRequest, (connection, client_address))
        # try:
        #     print('Connection from %s' %str(client_address))

        #     while True:
        #         print('Waiting for client...\n')
        #         data = connection.recv(64).decode(ENCODE)
        #         request = data.split()
        #         print('Received data: %s' %data)
        #         if len(request) == 0:
        #             break
        #         elif request[0].lower() == 'get':
        #             getFunction (connection, request[1])
        #         elif request[0].lower() == 'put':
        #             putFunction (connection, request[1], request[2])
        #         elif request[0].lower() == 'exit':
        #             print('End of transmission %s' %str(client_address))
        #             break
        #         else:
        #             print('Sending the same data to client\n')
        #             connection.sendall(bytes(data, ENCODE))
        # except:
        #     print("\nServer error: ", sys.exc_info()[0])
        #     connection.close()
        #     traceback.print_exc()
        # finally:
        #     print("Closing connection")
        #     connection.close()
        #     break
    except:
        print("\nServer error: ", sys.exc_info()[0])
        print("Closing socket")
        s.close()
    finally:
        print("Closing socket")
        s.close()

def handleRequest(connection, client_address):
    try:
        print('Connection from %s' %str(client_address))
        while True:
            print('Waiting for client...\n')
            data = connection.recv(64).decode(ENCODE)
            request = data.split()
            print('Received data from %s: %s' %(str(client_address), data))
            if len(request) == 0:
                break
            elif request[0].lower() == 'get':
                getFunction (connection, request[1], client_address)
            elif request[0].lower() == 'put':
                putFunction (connection, request[1], request[2], client_address)
            elif request[0].lower() == 'exit':
                print('End of transmission %s' %str(client_address))
                break
            else:
                print('Sending the same data to client %s\n' %str(client_address))
                connection.sendall(bytes(data, ENCODE))
    except:
        print("\nServer error: ", sys.exc_info()[0])
        connection.close()
        traceback.print_exc()
    finally:
        print("Closing connection for " + str(client_address))
        connection.close()
        
def getFunction (connection, archiveName, client_address):
    if path.exists(archiveName):
         print('%s file requested\n' %archiveName)
         file = open(archiveName, 'r')
         fileInfo = os.stat(archiveName)
         connection.sendall(bytes('LENGTH ' + str(fileInfo.st_size), ENCODE))
         connection.sendall(bytes(file.read(fileInfo.st_size), ENCODE))
         print('Finished sending file for %s\n' %str(client_address))
    else:
        print('ERROR1: File not found - %s\n' %str(client_address))
        connection.sendall(bytes('ERROR1', ENCODE))

def putFunction (connection, archiveName, length, client_address):
    fileReceived = connection.recv(int(length))
    requestSplit = archiveName.split('.')
    saveName = requestSplit[0] + '(' + time.strftime('%d-%m-%Y %Hh%Mm%Ss') + ')' + ('.' + requestSplit[1] if len(requestSplit) > 1 else '')
    print('Receiving %s file - %s\n' %(saveName, str(client_address)))
    file = open(saveName, 'w')
    file.write(fileReceived.decode(ENCODE))
    file.close()
    print('File received successfully from %s\n' %str(client_address))

def battleshipFunction(player1Connection, player2Connection):
    player1 = Player(player1Connection, MAP_SIZE, ENCODE)
    player2 = Player(player2Connection, MAP_SIZE, ENCODE)
    placePhase(player1, player2)

def placePhase(player1, player2):
    messageAll(player1, player2,
               "=========================================\n"
               "\n"
               "Fase de escolha da posição dos navios\n"
               "\n"
               "=========================================\n")
    for i in range(3):
        communicationMessage(player1, player2)
        placeForPlayer(player1, player2, i)
        communicationMessage(player2, player1)
        placeForPlayer(player2, player1, i)
	
	messageAll("end")
	gamePhase(player1, player2)

def messageAll(player1, player2, message):
    player1.sendMessage(message)
    player2.sendMessage(message)

def communicationMessage(playerTurn, playerWaiting):
    playerTurn.sendMessage(TURN)
    playerWaiting.sendMessage(WAIT)

def placeForPlayer(playerPlacing, playerWaiting, number):
    playerWaiting.sendMessage("Esperando o outro jogador.")
    playerPlacing.sendMessage("%dº navio: " % (number + 1))
    message = playerPlacing.receiveMessage()
    lin, col = message.split()
    result = playerPlacing.place(lin, col)
    while (not result):
        playerPlacing.sendMessage(TURN)
        playerPlacing.sendMessage("\nInválido, digite novamente o %dº navio: " % (number + 1))
        lin, col = message.split()
        result = playerPlacing.place(lin, col)
    playerPlacing.sendMessage(OK)
    playerPlacing.sendMessage(str(playerPlacing.getMap()) + "\n")

def gamePhase (player1, player2):
	messageAll(player1, player2,
               "=========================================\n"
               "\n"
               "Inicio do jogo\n"
               "\n"
               "=========================================\n")
	while (True)
		communicationMessage(player1, player2)
		firePlayer(player1, player2)
		printMaps (player1, player2)
		communicationMessage(player2, player1)
		firePlayer(player2, player1)
		printMaps (player1, player2)
		
		messageAll("end")

def firePlayer(playerFiring, playerWaiting)
	playerWaiting.sendMessage("Esperando o outro jogador.")
	playerFiring.sendMessage("Realize sua jogada.")
	while (True)
		message = playerFiring.receiveMessage()
		lin, col = message.split()
		result = playerWaiting.fire(lin, col)
		outcome = "Resultado da jogada: "
		if result == 'X':
			outcome += "Acerto\n"
			playerFiring.updateEnemyMap(lin, col, result)
			playerFiring.updateScore()
			break
		elif result == 'A'
			playerFiring.updateEnemyMap(lin, col, result)
			outcome += "Agua\n"
			break
		elif result == 'E'
			outcome += "Erro. Jogue novamente.\n"
			playerWaiting.sendMessage(outcome)
			playerFiring.sendMessage(TURN)
	playerFiring.sendMessage(OK)
	messageAll(playerFiring, playerWaiting, outcome)
	if playerFiring.getScore() == 3
		win(playerFiring, playerWaiting)
	else
		messageAll("Vez do inimigo")

#encerrar o jogo
def win(playerFiring, playerWaiting)
	playerFiring.sendMessage("Vitoria!")
	playerWaiting.sendMessage("-22PDL")
	s.close()
	
#imprime para cada jogador o mapa aliado e o inimigo
def printMaps (player1, player2)
	player1.sendMessage("Mapa aliado:\n" + player1.getMap.__srt__ + "\n" + "Mapa inimigo:\n" + player1.getEnemyMap.__str__ + "\n")
	player2.sendMessage("Mapa aliado:\n" + player2.getMap.__srt__ + "\n" + "Mapa inimigo:\n" + player2.getEnemyMap.__str__ + "\n")

	
main()
