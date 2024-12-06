import pandas as pd
import random as rd
import os
import csv
from pesquisa import organizar_tudo

def questao_aleatoria():
    dados = pd.read_csv(r'questoes\bd\questoes.csv', encoding='utf', sep=';')
    questao = {}
    linha = dados.loc[rd.randrange(len(dados.index))]

    for coluna in dados.columns:
        questao[coluna] = str(linha[coluna])

    return questao

def confirmar():
    print('\nTentar Novamente? [1 - SIM] [2 - NÃO]')
    resp = int(input())
    if (resp == 1):
        return True
    else:
        return False

def mostrar_questao(titulo):
    while True:
        os.system('cls')
        print('--------------- ' + str(titulo) + ' ---------------')
        
        questao = questao_aleatoria()

        for chave in questao.keys():
            if (chave != 'GABARITO'):
                print(chave + ': ' + questao[chave])
    
        print('[1] - Certo')
        print('[2] - Errado')
        print('[3] - Tipo C')
        print('[4] - Problema com a questao')
        print('[5] - Voltar')
        resposta = int(input('Escolha uma opção: '))

        match resposta:
            case 1:
                if (questao['GABARITO'] == 'C'):
                    print('Parabéns! Você acertou.')
                else:
                    print('Que pena! Você errou.')
                    print('A resposta correta é: ' + questao['GABARITO'])
                
                if (not confirmar()):
                    break
            case 2:
                if (questao['GABARITO'] == 'E'):
                    print('Parabéns! Você acertou!')
                else:
                    print('Que pena! Você errou.')
                    print('A resposta correta é: ' + questao['GABARITO'])
                
                if (not confirmar()):
                    break
            case 3:
                resp = str(input('Digite a alternativa correta [A, B, C ou D]: '))
                if (questao['GABARITO'] == resp.upper()):
                    print('Parabéns! Você acertou!')
                else:
                    print('Que pena! Você errou.')
                    print('A resposta correta é: ' + questao['GABARITO'])
                
                if (not confirmar()):
                    break
            case 4:
                with open(r'questoes\bd\erros.csv', 'w', encoding='utf-8') as arq:
                    escritor = csv.writer(arq, delimiter=';')
                    escritor.writerow([questao['ID']])
                    
                print('Desculpe o incoveniente. Erro registrado.')
                if (not confirmar()):
                    break
            case 5:
                break
            case _:
                print('Opção não encontrada. Tente novamente.')

def tela_apresentacao():
    organizar_tudo()
    while True:
        os.system('cls')
        print('--------------- BANCO DE QUESTÕES ---------------')
        print('[1] - Questão aleatória')
        print('[2] - Bateria de questões - (EM DESENVOLVIMENTO)')
        print('[3] - Criar/Recriar banco de dados ')
        print('[4] - Sair')
        resposta = int(input('Escolha uma opção: '))

        match resposta:
            case 1:
                mostrar_questao('QUESTÃO ALEATÓRIA') 
            case 2:
                break
            case 3:
                 break
            case 4:
                break
            case _:
                print('Opção não encontrada. Tente novamente.')
                
tela_apresentacao()