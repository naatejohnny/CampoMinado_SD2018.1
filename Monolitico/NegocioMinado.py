from random import randint
from os.path import isfile
from os import remove
import json

class CampMinado:

    def novo_Jogo(self, linha, coluna):
        self.__linha = int(linha)
        self.__coluna = int(coluna)
        self.jogadas_Restantes = self.calcular_Total_Jogadas(linha, coluna)
        self.tabuleiro = self.inicializar_tabuleiro(linha, coluna)
        self.coordenadas_bombas = self.distribuir_bombas(linha,coluna)
        self.morreu = "Vivo"

    def imprimir_tabuleiro(self):
        for posicao in self.tabuleiro:
            print(str(posicao))
    
    def jogo_incompleto(self):
        return False

    def inicializar_tabuleiro(self, linha, coluna):
        return [[str('X') for x in range(coluna)] for j in range(linha)]

    def distribuir_bombas(self, linha, coluna):
        coordenadas_bombas = [(randint(0, linha - 1), randint(0, coluna - 1)) for x in range(self.total_bombas())]
        '''print(coordenadas_bombas)'''
        return coordenadas_bombas

    def total_bombas(self):
        return int((self.__linha*self.__coluna)/3)
    
    def calcular_Total_Jogadas(self,linha, coluna):
        return (linha*coluna) - self.total_bombas()

    def validar_Coordenadas(self, linha, coluna):
        if linha not in range(0, self.__linha) and coluna not in range(0, self.__coluna):
            print("COORDENADAS INVALIDAS")
            return False
        else:
            return True
    
    def coordenada_e_bombas(self, coordenada):
        return coordenada in self.coordenadas_bombas

    def conta_bombas_vizinhas(self, linha, coluna):
        return len([(linha + x, coluna + y) for x in (-1,0,1) for y in (-1,0,1) if self.coordenada_e_bombas((linha + x, coluna + y))])

    def getMorrer(self):
        return self.morreu

    def fim_Jogo(self):
        print("__________________________________\n")
        print("YYYYEEEEE, Você Morreeeuuu Abestadoo!\n")
        print("__________________________________\n\n")
        self.morreu = "Morreu"


    def salvar_Jogo(self):
        game = {
            'linha': self.__linha,
            'coluna': self.__coluna,
            'jogadasRestantes': self.jogadas_Restantes,
            'tabuleiro': self.tabuleiro,
            'coordenadasBombas': self.coordenadas_bombas
        }
        file = open("game.json", 'w')

        file.write(json.dumps(game))
        file.close()

    def restorar(self, game):
        self.__linha = game['linha']
        self.__coluna = game['coluna']
        self.jogadas_Restantes = game['jogadasRestantes']
        self.tabuleiro = game['tabuleiro']
        self.coordenadas_bombas = game['coordenadasBombas']
        self.morreu = "Vivo"
    
    def jogada(self, linha, coluna):
        linha = int(linha)
        coluna = int(coluna)

        if not self.validar_Coordenadas(linha, coluna):
            return "COORDENADAS INVALIDAS"
        
        if  (linha, coluna) in self.coordenadas_bombas:
            self.fim_Jogo()
        
        self.tabuleiro[linha][coluna] = str(self.conta_bombas_vizinhas(linha, coluna))
        self.jogadas_Restantes -=1
        self.salvar_Jogo()
        return "ÓTIMA_JOGADA"