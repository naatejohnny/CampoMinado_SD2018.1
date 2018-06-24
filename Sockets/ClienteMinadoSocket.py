from socket import socket, AF_INET, SOCK_DGRAM
import sys
import re

ENCODE = "UTF-8"
MAX_BYTES = 65535
PORT = 5000
HOST = '127.0.0.1'

u"""Esse módulo possui a implementação de um cliente UDP. """

JOGO_CRIADO = "Jogo_Criado"
JOGO_REINICIADO = "Jogo_Reiniciado"
JOGADA_REALIZADA = "Jogada_Realizada"
JOGADA_ERRADA = "Jogada_Errada"
ACERTOU_MINA = "Acertou_Mina"

def menu():
    print("****************************************")
    print("*             Campo Minado             *")
    print("****************************************")
    print("   1 - Play                            *")
    print("   2 - Continuar                       *")
    print("   9 - Sair                            *")
    print("****************************************\n")

    
def inicio(sock,dest):
    menu()
    comando = input(': ')
    
    if (comando == '1'):
        sock.sendto(comando.encode(ENCODE),dest)
    elif (comando == '2'):
        sock.sendto(comando.encode(ENCODE),dest)
    elif (comando == '9'):
        sys.exit(0)
    else:
        print('Comando inválido.')
        inicio(sock, dest)

    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode(ENCODE)
    response = text.split("$")
    
    if response[0] == JOGO_CRIADO or response[0]== JOGO_REINICIADO:
        qtdLinhas = int(response[1])
        qtd_Minas_Vizinhas = eval(response[2])
        jogadas_Restantes = int(response[3])
        imprimir_Tabuleiro(qtdLinhas,qtd_Minas_Vizinhas)
        print('Restam ',jogadas_Restantes,' jogadas.')
        print()
        iniciar_Jogo(sock,dest)

    
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
    
def iniciar_Jogo(sock,dest):
    while (True):
        a = input('Insira a linha e coluna: ')
        
        if a == "quit" or a == "quitSave":
            sock.sendto(a.encode(ENCODE),dest)
            sock.close()
            sys.exit(0)
        
        padrao = re.match("[0-9],[0-9]",a)
        
        if (padrao == None):
            print('Jogada inválida')
            print()
            continue
        
        sock.sendto(a.encode(ENCODE),dest)
        data, address = sock.recvfrom(MAX_BYTES)
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
            inicio(sock,dest)
            
        imprimir_Tabuleiro(qtdLinhas,qtd_Minas_Vizinhas)
        print('Faltam ',jogadas_Restantes,' jogadas.')
        print()

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_DGRAM)
    dest = (HOST, PORT)
    inicio(sock, dest)