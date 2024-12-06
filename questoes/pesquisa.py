from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import shutil
import requests
import os 
import pymupdf
from multi_column import column_boxes
import re
import csv

dir = r'questoes\pdfs'

def baixar_pdfs():
    driver = webdriver.Edge()
    driver.get('https://passeandounb.com/provas-anteriores-do-pas-3/')
    elementos = driver.find_elements(By.CLASS_NAME, 'elementor-widget-container')
    
    ano = ''
    
    print('Baixando as provas...')
    for elemento in elementos:
        if (elemento.text.split(' ')[0] == 'PROVA'):
            links = elemento.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                response = requests.get(href, stream=True)
                if ( href.split('/')[-1][:3] != 'pas'):
                    nome = os.path.join(dir, href.split('/')[-1][:-4] + ('_' + ano + '.pdf'))
                    with open(nome, 'wb') as arq:
                        shutil.copyfileobj(response.raw, arq)
                del response
        else:
            if (elemento.text != ''):
                if(elemento.text[0] == '2'):
                    ano = elemento.text
    
    print('Concluído') 
    driver.close()
    
def renomear_pdfs():
    for file in os.listdir(dir):
        if (os.path.isfile(os.path.join(dir, file))):
            if (file[-8:-4] in ['2008','2009','2010','2011','2012','2013','2014','2015', '2016', '2017', '2020', '2021']):
                os.remove(os.path.join(dir, file))
            else:
                if (file[:3] != 'pas'):
                    antigo = os.path.join(dir, file)
                    if (file[:3].lower() == 'gab'):
                        if (file[-8:-4] == '2020' or file[-8:-4] == '2021'):
                            if (file.split('_')[-3][-1] == '2'):
                                novo = os.path.join(dir, 'pas3-gabarito-2-' + file.split('_')[-1])  
                            else:
                                novo = os.path.join(dir, 'pas3-gabarito-1-' + file.split('_')[-1])
                        else:
                            novo = os.path.join(dir, 'pas3-gabarito-' + file.split('_')[-1])
                    else: 
                        if (file[-8:-4] == '2020' or file[-8:-4] == '2021'):
                            if (file.split('_')[-3][-1] == '2'):
                                novo = os.path.join(dir, 'pas3-prova-2-' + file.split('_')[-1])
                            else:
                                novo = os.path.join(dir, 'pas3-prova-1-' + file.split('_')[-1])
                        else:
                            novo = os.path.join(dir, 'pas3-prova-' + file.split('_')[-1])
                    os.rename(antigo, novo)
                    
def extrair_gabarito(ano):
    if (ano in ['2018', '2019', '2022', '2023']):
        #Lendo o arquivo
        
        elementos= []
        
        paginas = pymupdf.open(dir + r'\pas3-gabarito-'+ str(ano)+'.pdf')
        
        for pagina in paginas:
            elementos.append(pagina.get_text(sort=True))
    
        #Filtrando as respostas
        
        with open(r'questoes\ignorar\generico.txt', 'w', encoding='utf-8') as arq:
            for elemento in elementos:
                arq.write(elemento)
        
        linhas =  ''
        
        with open(r'questoes\ignorar\generico.txt', 'r', encoding='utf-8') as arq:
             linhas =  arq.readlines()
        
        res = ''
        
        for linha in linhas:
            if (len(linha.split(' ')) > 1):
                if (linha.split(' ')[1].lower() == 'gabarito'):
                    res += str(linha.upper().split('GABARITO')[1])
        
        respostas = []
        alternativas = ['A','B','C','D','E', 'X', '_']
        
        res = re.sub(r'TIPO D', '_', res)
        res = re.sub(r'TIPOD', '_', res)
        numeros = re.findall( r'[0-9][0-9][0-9]', res)
        numeros.extend(re.findall(r'[ ][0-9][0-9][ ]', res))
        numeros.extend(re.findall(r'[ ][0-9][0-9]$', res))
        numeros.extend(re.findall(r'[ ][0-9][ ]', res))
        numeros.extend(re.findall(r'[ ][0-9]$', res))
        
        nums = []
        
        for num in range(len(numeros)):
            nums.append(str(num))
        
        alternativas.extend(nums)
        
        for num in range(len(numeros)):
            res = re.sub(str(numeros[num]), str(num), res)
        
        for letra in res:
            if (letra in alternativas):
                resp = letra
                if (letra in nums):
                    resp = numeros[int(letra)]
                respostas.append(resp)
        
        gabarito = {}
        
        for num in range(len(respostas[30:])):
            gabarito[str(num+11)] = respostas[30:][num]
    
        return gabarito
    else:
        print('Esse ano não está incluso no banco de dados')
        return None
    
def extrair_questoes(ano):
    if (ano in ['2018', '2019', '2022', '2023']):
        elementos = []
        
        paginas = pymupdf.open(dir + r'\pas3-prova-'+ str(ano) + '.pdf')
        for pagina in paginas:
            bboxes = column_boxes(pagina, footer_margin=0, no_image_text=True)
            for rect in bboxes:
                elementos.append('\n' + ('-'*80) + '\n')
                elementos.append(pagina.get_text(clip=rect, sort=True))
            elementos.append('\n' + ('='*80))
        
        with open(r'questoes\ignorar\generico.txt', 'w', encoding='utf-8') as arq:
            for elemento in elementos:
                arq.write(elemento)
        
        linhas = ''
        
        with open(r'questoes\ignorar\generico.txt', 'r', encoding='utf-8') as arq:
            linhas = arq.readlines()
        
        itens = []
        posicoes = []
        
        for linha in linhas:
            itens.append(re.findall('^[1-9][0-9 ][0-9 ][A-Z ]', linha))
        
        for num in range(len(itens)):
            if (len(itens[num]) > 0):
                posicoes.append(num)
        
        questoes = {}
        
        for num in range(len(posicoes)):
            if (num+1  < len(posicoes)):
                questao = linhas[posicoes[num]:posicoes[num+1]]
                questao[0] = questao[0].replace(' ', '-)', 1)
                questoes[itens[posicoes[num]][0].split(' ')[0]] = questao
        
        for chave in questoes.keys():
            questao = questoes[chave]
            cortar = 0
            for num in range(len(questao)):
                questao[num] = re.sub(r'   FIM ITEM\n$', ('-'*80 + '\n'), questao[num])
                if ((questao[num][:5] == '-'*5 or questao[num][:5] == '='*5) and cortar == 0):
                    cortar = num
            if (cortar == 0):
                cortar = len(questao)
            
            questoes[chave] = questao[0:cortar]
        
            while '\n' in questoes[chave]:
                questoes[chave].remove('\n')
    
        for num in range(1, 11):
            del questoes[str(num)]
        
        return questoes
    else:
        print('Esse ano não está incluso no banco de dados')
        return None
    
def organizar_questoes():
    provas = {}
    gabaritos = {}
    
    for file in os.listdir(dir):
        if (os.path.isfile(os.path.join(dir, file))):
            partes = file.split('-')
            ano = partes[2][:4]
            if ( ano in ['2018', '2019', '2022', '2023']):
                partes = file.split('-')
                ano = partes[2][:4]
                if (partes[1] == 'prova'):
                    provas[ano] = extrair_questoes(ano)
                if (partes[1] == 'gabarito'):
                    gabaritos[ano] = extrair_gabarito(ano)
    
    id = 1
    print('Armazenando as questões...')
    with open(r'questoes\bd\questoes.csv', 'w', encoding='utf-8') as arq:
        escritor =  csv.writer(arq, delimiter=';')
        escritor.writerow(['ID', 'PROVA', 'ANO', 'N° QUESTÃO', 'ENUNCIADO', 'GABARITO'])
        for ano in provas.keys():
            for questao in provas[ano].keys():
                texto = ''
                for linha in provas[ano][questao]:
                    texto += linha
                    
                if (int(questao) <= 120):
                    row = [id, 'PAS3', str(ano), questao, texto, gabaritos[ano][questao]]
                    escritor.writerow(row)
                id += 1
    print('Concluído')

def criar_arq_erros():
    with open(r'questoes\bd\erros.csv', 'w', encoding='utf-8') as arq:
        escritor = csv.writer(arq, delimiter=';')
        escritor.writerow(['ID_QUESTÃO'])

def criar_arq_analise():
    print('Ainda em desenvolvimento.')

def organizar_tudo():
    if (os.path.exists(r'questoes\bd') == False):
        os.mkdir(r'questoes\bd')
        
    if (os.path.exists(r'questoes\ignorar') == False):
        os.mkdir(r'questoes\ignorar')
        
    if (os.path.exists(r'questoes\pdfs') == False):
        os.mkdir(r'questoes\pdfs')
        
    if (len(os.listdir(r'questoes\pdfs')) == 0):
        baixar_pdfs()
        renomear_pdfs()
        organizar_questoes()
        criar_arq_erros()

  