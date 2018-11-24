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

ENCODE = 'UTF-8'

# print_lock = threading.Lock() 

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    s.bind(server_address)

    s.listen()


    try:
        while True:
            print('Waiting for connection')
            connection, client_address = s.accept()
            # print_lock.acquire() 
            start_new_thread(handleRequest, (connection, client_address)) 
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

main()
