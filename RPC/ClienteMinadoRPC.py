import rpyc
import sys
from rpyc.utils.server import ThreadedServer
import re


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
    
def inicio(proxy):
    menu()
    comando = input(': ')
    
    if (comando == '1'):
        jogo = proxy.root.novo_Jogo()
        print(jogo)
    elif (comando == '2'):
        jogo = proxy.root.restaurar_Jogo()
    elif (comando == '9'):
        sys.exit(0)
    else:
        print('Comando inválido.')
    
    if jogo[0] == JOGO_CRIADO or jogo[0]==JOGO_REINICIADO:
        qtdLinhas = int(jogo[1])
        qtd_Minas_Vizinhas = eval(jogo[2])
        jogadas_Restantes = int(jogo[3])
        imprimir_Tabuleiro(qtdLinhas,qtd_Minas_Vizinhas)
        print('Restam ',jogadas_Restantes,' jogadas.')
        print()
        iniciar_Jogo(proxy)

    
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
    
def iniciar_Jogo(proxy):
    while (True):
        a = input('Informe a linha e coluna: ')
        
        if a == "quit": 
            sys.exit(0)
        elif a == "quitSave":
            proxy.salvar_Jogo()
            sys.exit(0)
        
        padrao = re.match("[0-9],[0-9]",a)
        if (padrao == None):
            print('Jogada inválida')
            print()
            continue
        
        jogo = proxy.root.iniciar_Jogo(a)
        
                
        if jogo[0] == JOGADA_ERRADA:
            print("Jogada inválida")
            print()
            continue
        elif jogo[0] == JOGADA_REALIZADA:
            qtdLinhas = jogo[1]
            qtd_Minas_Vizinhas = jogo[2]
            jogadas_Restantes = jogo[3]
        elif jogo[0] == ACERTOU_MINA:
            print("YYYYEEEEE, Você Morreeeuuu Abestadoo!\n")
            inicio(proxy)
        elif jogo[0] == ENCERROU:
            print('*** Valeu Abestado, ganhou!!!!! Oh Cabra arretado!!! ***')
            inicio(proxy)
            
        imprimir_Tabuleiro(qtdLinhas,qtd_Minas_Vizinhas)
        print('Faltam ',jogadas_Restantes,' jogadas.')
        print()

if __name__ == "__main__":
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    inicio(proxy)