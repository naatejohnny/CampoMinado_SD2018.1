import rpyc
import sys
import re
from rpyc.utils.server import ThreadedServer
from random import randint


u"""Este módulo possui a implementação de UDP Server"""


class CampMinado(rpyc.Service):
   
    qtdLinhas = 0
    qtd_Minas_Vizinhas = []
    coordenadas_Minas = []
    jogadas_Restantes = 0
    
    JOGO_CRIADO = "Jogo_Criado"
    JOGO_REINICIADO = "Jogo_Reiniciado"
    JOGADA_REALIZADA = "Jogada_Realizada"
    JOGADA_ERRADA = "Jogada_Errada"
    ACERTOU_MINA = "Acertou_Mina"
    ENCERROU = "Encerrou"

    def exposed_novo_Jogo(self):
        self.coordenadas_Minas = self.distribuir_Minas(self.qtdLinhas)
        self.qtd_Minas_Vizinhas = []
        self.jogadas_Restantes = self.qtdLinhas*self.qtdLinhas-len(self.coordenadas_Minas)
        print('Jogo criado',self.qtdLinhas,self.coordenadas_Minas,self.jogadas_Restantes)
        return [self.JOGO_CRIADO, str(self.qtdLinhas), str(self.qtd_Minas_Vizinhas), str(self.jogadas_Restantes)]
        
    def distribuir_Minas(self,qtdLinhas):
        minas = []
        qtdMinas = randint(int((qtdLinhas*qtdLinhas)/5),int((qtdLinhas*qtdLinhas)/3))
        for i in range(qtdMinas):
            linha = randint(0,qtdLinhas-1)
            coluna = randint(0,qtdLinhas-1)
            if ([linha,coluna] in minas):
                qtdMinas += 1
            else:
                minas.append([linha,coluna])
        return minas
    
    def validar_Coordenadas(self,tupla):
        if (tupla[0] < 0 or tupla[1] < 0) or (tupla[0] > self.qtdLinhas or tupla[1] > self.qtdLinhas):
            print("Coordenada inválida",tupla[0],tupla[1],self.qtdLinhas)
            return False, "Coordenada inválida"
        for qtd in self.qtd_Minas_Vizinhas:
            if tupla == qtd[0]:
                print("Coordenada repetida.")
                return False,"Coordenada repetida."
        return True, "ok"
    
    def exposed_iniciar_Jogo(self,tuplaStr):
        tupla = eval(tuplaStr)
        print(self.coordenadas_Minas)
        if tupla in self.coordenadas_Minas:
            print("YYYYEEEEE, Você Morreeeuuu Abestadoo! Acertou uma mina!!!!\n"))
            return([self.ACERTOU_MINA])
        qtdMinas = 0
        a = int(tupla[0])
        b = int(tupla[1])
        for y in [-1,0,1]:
            for x in [-1,0,1]:
                if self.verifica_Bombas([a+y,b+x], self.coordenadas_Minas):
                    qtdMinas += 1
        self.qtd_Minas_Vizinhas.append([[a,b],qtdMinas])
        self.jogadas_Restantes -= 1
        if self.jogadas_Restantes == 0:
            return [self.ENCERROU]
        return [self.JOGADA_REALIZADA,self.qtdLinhas,self.qtd_Minas_Vizinhas,self.jogadas_Restantes]
        
    def verifica_Bombas(self,posicao,minas):
        if (posicao[0]>=0 and posicao[1]>=0) and (posicao[0]<self.qtdLinhas and posicao[1]<self.qtdLinhas):
            if (posicao in minas):
                return True
            else:
                return False
    
    def exposed_salvar_Jogo(self):
        arq = open("game.txt",'w')
        arq.write(str(self.qtdLinhas)+"\n")
        arq.write(str(self.qtd_Minas_Vizinhas)+"\n")
        arq.write(str(self.coordenadas_Minas)+"\n")
        arq.write(str(self.jogadas_Restantes))
        arq.close()

    def exposed_restaurar_Jogo(self):
        arquivo = open('game.txt', 'r')
        self.qtdLinhas = int(arquivo.readline())
        self.qtd_Minas_Vizinhas  = eval(arquivo.readline())
        self.coordenadas_Minas = eval(arquivo.readline())
        self.jogadas_Restantes = int(arquivo.readline())
        arquivo.close()
        return [self.JOGO_REINICIADO, str(self.qtdLinhas), str(self.qtd_Minas_Vizinhas), str(self.jogadas_Restantes)]
    
    def server(self, socket, data):
        text = data.decode(self.ENCODE)
        print("Chegou",text)
        
        if (text == '1'):
            self.novo_Jogo()
            print("Jogo criado")
            retorno = self.JOGO_CRIADO + "$" + str(self.qtdLinhas) + "$" + str(self.qtd_Minas_Vizinhas) + "$" + str(self.jogadas_Restantes)
            data = retorno.encode(self.ENCODE)
            socket.send(data)
            
        elif (text == '2'):
            self.restaurar_Jogo()
            print("Jogo reiniciado")
            retorno = self.JOGO_REINICIADO + "$" + str(self.qtdLinhas) + "$" + str(self.qtd_Minas_Vizinhas) + "$" + str(self.jogadas_Restantes)
            data = retorno.encode(self.ENCODE)
            socket.send(data)
            
        else:
            padrao = re.match("[0-9],[0-9]",text)
            
            if (padrao == None):
                if (text == "quit"):
                    print('Jogo encerrado')
                    retorno = ""
                    data = text.encode(self.ENCODE)
                    socket.send(data)
                elif (text == "quitSave"):
                    self.salvar_Jogo()
                    print('Jogo encerrado e salvo')
                    retorno = ""
                    data = text.encode(self.ENCODE)
                    socket.send(data)
                print('Comando inválido')
            else:
                tupla = text.split(",")
                tupla[0] = int(tupla[0])
                tupla[1] = int(tupla[1])
                jogadaValida, msg = self.validar_Coordenadas(tupla)
                
                if (jogadaValida):
                    print('tupla valida',tupla)
                    jogo = self.iniciar_Jogo(tupla)
                    retorno = jogo + "$" + str(self.qtdLinhas) + "$" + str(self.qtd_Minas_Vizinhas) + "$" + str(self.jogadas_Restantes)
                    data = retorno.encode(self.ENCODE)
                    socket.send(data)
                else:
                    print('tupla invalida')
                    retorno = self.JOGADA_ERRADA + "$" + str(self.qtdLinhas) + "$" + str(self.qtd_Minas_Vizinhas) + "$" + str(self.jogadas_Restantes)
                    data = retorno.encode(self.ENCODE)
                    socket.send(data)
    

if __name__ == "__main__":
    CampMinado.qtdLinhas = 5
    try:
        thread = ThreadedServer(CampMinado, port=18861)
        thread.start()
    except:
        for val in sys.exc_info():
            print(val)