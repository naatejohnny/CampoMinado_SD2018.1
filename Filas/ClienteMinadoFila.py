from socket import socket, AF_INET, SOCK_DGRAM
import sys
import re
import zmq
import random

ENCODE = "UTF-8"
MAX_BYTES = 65535
PORT = 5559
HOST = '127.0.0.1'

u"""Esse módulo possui a implementação de um cliente UDP. """

JOGO_CRIADO = "Jogo_Criado"
JOGO_REINICIADO = "Jogo_Reiniciado"
JOGADA_REALIZADA = "Jogada_Realizada"
JOGADA_ERRADA = "Jogada_Errada"
ACERTOU_MINA = "Acertou_Mina"
ENCERROU = "Encerrou"

def menu():
    print("****************************************")
    print("*             Campo Minado             *")
    print("****************************************")
    print("   1 - Play                            *")
    print("   2 - Continuar                       *")
    print("   9 - Sair                            *")
    print("****************************************\n")
    
def inicio(sock):
    menu()
    comando = input(': ')
    
    if (comando == '1'):
        sock.send(comando.encode(ENCODE))
    elif (comando == '2'):
        sock.send(comando.encode(ENCODE))
    elif (comando == '9'):
        sys.exit(0)
    else:
        print('Comando inválido.')
        inicio(sock)

    data = sock.recv()
    text = data.decode(ENCODE)
    response = text.split("$")
    
    if response[0] == JOGO_CRIADO or response[0]==JOGO_REINICIADO:
        qtdLinhas = int(response[1])
        qtd_Minas_Vizinhas = eval(response[2])
        jogadas_Restantes = int(response[3])
        imprimir_Tabuleiro(qtdLinhas,qtd_Minas_Vizinhas)
        print('Faltam ',jogadas_Restantes,' jogadas.')
        print()
        iniciar_Jogo(sock)

def imprimir_Tabuleiro(qtdLinhas,qtdBombas):
    print()
    print('   0   1   2   3   4')
    linha = 0
    for y in range(qtdLinhas):
        print(str(linha) + ' ',end='')
        for x in range(qtdLinhas):
            if [y,x] in [a[0] for a in qtdBombas]:
                for a in qtdBombas:
                    if a[0] == [y,x]:
                        print('(' + str(a[1]) + ') ',end='')
                        break
            else:
                print('(X) ',end='')
        print()
        linha += 1            
    
def iniciar_Jogo(sock):
    while (True):
        a = input('Insira a linha e coluna: ')
        
        if a == "quit" or a == "quitSave":
            sock.send(a.encode(ENCODE))
            sock.close()
            sys.exit(0)
        
        padrao = re.match("[0-9],[0-9]",a)
        
        if (padrao == None):
            print('Jogada inválida')
            print()
            continue
        
        sock.send(a.encode(ENCODE))
        data = sock.recv()
        response = data.decode(ENCODE)
        response = response.split("$")
        
        if response[0] == JOGADA_ERRADA:
            print("Jogada inválida")
            print()
            continue
        elif response[0] == JOGADA_REALIZADA:
            qtdLinhas = int(response[1])
            qtd_Minas_Vizinhas = eval(response[2])
            jogadas_Restantes = int(response[3])
        elif response[0] == ACERTOU_MINA:
            print("YYYYEEEEE, Você Morreeeuuu Abestadoo!\n")
            inicio(sock)
        elif response[0] == ENCERROU:
            print('*** Valeu Abestado, ganhou!!!!! Oh Cabra arretado!!! ***')
            inicio(sock)
            
        imprimir_Tabuleiro(qtdLinhas,qtd_Minas_Vizinhas)
        print('Restam ',jogadas_Restantes,' jogadas.')
        print()

if __name__ == "__main__":
    context = zmq.Context()
    print("Conectando com o servidor...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % PORT)
    client_id = random.randrange(1, 10005)
    inicio(socket)