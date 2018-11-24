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
import traceback
import os.path
from os import path

ENCODE = 'UTF-8'
DEFAULT_PORT = 8080

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False  

    print("Type 'exit' or empty message to exit")
    print("Available commands:")
    print("\tconnect <hostname> <port> - Use only connect for default values")
    print("\tGET <archive name> - to get an archive from server")
    print("\tPUT <archive name> - to send an archive to server\n")
    data = input("Type a message: ")
    
    while data.lower() != 'exit' and data != '':
        if not connected:
            inputText = data.split()
            if inputText[0].lower() == 'connect':
                if connected:
                    print("You've already connected")
                else:
                    try:
                        if len(inputText) > 2:
                            print("Connecting to '%s' port %i" % (inputText[1], int(inputText[2])))
                            s.connect((inputText[1], int(inputText[2])))
                        else:
                            print("Connecting to 'localhost' port %i\n" % DEFAULT_PORT)
                            s.connect(('localhost', DEFAULT_PORT))
                        connected = True
                    except:
                        print("\nConnection denied: ", sys.exc_info()[0])
                        traceback.print_exc()
                        print("\tCheck if server is waiting for connections")
                        print("\tCheck connect arguments\n")
            elif connected:
                if inputText[0].lower() == 'get':
                    if len(inputText) == 2:
                        getFunction(s, inputText[0], inputText[1])
                    else:
                        print("\nError in GET format\n")
                elif inputText[0].lower() == 'put':
                    if len(inputText) == 2:
                        putFunction(s, inputText[0], inputText[1])
                    else:
                        print("\nError in PUT format\n")
                else:
                    s.sendall(bytes(data, ENCODE))
                    print("Received data: %s\n" % s.recv(50).decode(ENCODE))
            else:
                print("You must first get connected\n")
                data = input("Type a message: ")
        else:
            battleshipFunction(s)

        # data = input("Type a message: ")

    print("Closing socket")
    s.close()
    connected = False

def battleshipFunction(s):
    waitPhase(s)
    print(s.recv(256).decode(ENCODE))
    placePhase(s)

def waitPhase(s):
    message = s.recv(256).decode(ENCODE)
    print(message)
    while(message != "Ready to play"):
        message = s.recv(256).decode(ENCODE)
        print(message)

def placePhase(s):
    message = s.recv(256).decode(ENCODE)
    while(message != "end"):
        if message == "turn":
            while (message == "turn"):
                print(s.recv(256).decode(ENCODE), end='') # print da frase
                s.sendall(bytes(input(), ENCODE))
                message = s.recv(256).decode(ENCODE) # recebe ok quando der certo, turn quando for errado
                if (message == 'ok'):
                    print(s.recv(256).decode(ENCODE)) # print do mapa
        elif message == "wait":
            print(s.recv(256).decode(ENCODE))

        message = s.recv(256).decode(ENCODE)


def getFunction(s, comando, nomeArquivo):
    s.sendall(bytes(comando + ' ' + nomeArquivo, ENCODE))
    dataResp = s.recv(64).decode(ENCODE).split()
    if dataResp[0] == 'ERROR1':
        print('ERROR1: File not found\n')
    else:
        fileReceived = s.recv(int(dataResp[1]))
        nomeArquivoSplit = nomeArquivo.split('.')
        saveName = nomeArquivoSplit[0] + '(' + time.strftime('%d-%m-%Y %Hh%Mm%Ss') + ')' + ('.' + nomeArquivoSplit[1] if len(nomeArquivoSplit) > 1 else '')
        file = open(saveName, 'w')
        file.write(fileReceived.decode(ENCODE))
        file.close()
        print("File '%s' received successfully\n" %saveName)

def putFunction(s, comando, nomeArquivo):
    if path.exists(nomeArquivo):
        file = open(nomeArquivo, 'r')
        fileInfo = os.stat(nomeArquivo)
        s.sendall(bytes(comando + ' ' + nomeArquivo + ' ' + str(fileInfo.st_size), ENCODE))       
        s.sendall(bytes(file.read(fileInfo.st_size), ENCODE))
        print ('File sent successfully\n')
    else:
        print ("File not found\n")

main()

    
