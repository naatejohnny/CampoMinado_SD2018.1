from NegocioMinado import CampMinado
from os.path import isfile
from os import remove
import json
import sys

jogoNovo = CampMinado()

def menu():
    print("****************************************")
    print("*             Campo Minado             *")
    print("****************************************")
    print("   1 - Play                            *")
    print("   2 - Continuar                       *")
    print("   3 - Sair                            *")
    print("****************************************\n")
    option = int(input("Insira uma Opção :"))
    if option == 1:
        play()
    elif option == 2:
        restoreGame()
    else:
        exitGame

def play():
    jogoNovo.novo_Jogo(5, 5)
    startGame()

def startGame():
    count = 0    
    while jogoNovo.getMorrer() != "Morreu":
        if jogoNovo.jogadas_Restantes > 0:
            if count != 0:
                print("ÓTIMA JOGADA")
            jogoNovo.imprimir_tabuleiro()
            linha = int(input("Insira a linha :"))
            coluna = int(input("Insira a coluna :"))
            jogoNovo.jogada(linha, coluna)  
            count += count              
    tryAgain()

def restoreGame():
    if isfile("game.json"):
        file = open("game.json")
        game = json.loads(file.read())
        jogoNovo.restorar(game)
        file.close()
        startGame()
    else:
        print("Não há jogo salvo !\n")

def tryAgain():
    print("   1 - Novo Jogo  ")
    print("   2 - Sair       ")
    option = int(input("Insira uma Opção : "))
    if option == 1:
        menu()
    else:
        exitGame()

def exitGame():
    sys.exit(0)

menu()