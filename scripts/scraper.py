import requests
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import re

options = Options() #Instanciando um objeto options
options.add_argument("window-size=800,800") #Padronizando o tamanho da janela (Quando não utilizado o headless)
options.add_argument("--headless") #Para executar os métodos sem abrir uma janela do browser

print("Acessando site...") #Mostrando no terminal que o site está sendo acessado
browser = webdriver.Chrome(options=options) #Passando o objeto como parâmetro para inserir as configurações alteradas
browser.get("https://www.google.com.br/travel/") #Link inicial de onde o algoritmo irá entrar

wait = WebDriverWait(browser, 10)

sleep(2) #Esperando dois segundos para a página renderizar e conseguir pegar informações do código fonte

city = input("Qual local deseja visitar?: ") #Pega a cidade onde a busca será feita
print("Buscando...") #Mostrando no terminal que a cidade está sendo procurada

#Fazendo as rotinas para entrar na aba de hoteis
sleep(2)
input_place = browser.find_element(By.TAG_NAME,"input") #Pega a região onde insere o lugar para onde quer ir
input_place.send_keys("hotel em " + city) #Coloca um prefixo para filtrar a busca do google para os hoteis (sem isso, irá para o search convencional do google)
sleep(1)
input_place.send_keys(Keys.RETURN) #Sai da caixa de texto
sleep(1)
input_enter = browser.find_element(By.TAG_NAME,"li") #Procura a primeira recomendação de pesquisa
input_enter.click() #Clica na primeira recomendação de pesquisa
sleep(2)

content = browser.page_source #Atributo que contém o código fonte da página
site = BeautifulSoup(content, "html.parser") #Transformando o código fonte em um objeto do bs4
page = 1

#Linha de código para pegar o conteúdo HTML do site para análises mais fáceis
'''
with open("arquivo.txt", "w", encoding="utf-8") as arquivo: #Escrevendo o site em um arquivo txt
    arquivo.write(site.prettify())
'''

hotels = site.find_all("div", attrs={"class": "uaTTDe BcKagd bLc2Te Xr6b1e"}) #Pega onde está as informações sobre cada hotell
hotel_amout = site.find("div", attrs={"class": "GDEAO"}) #Pega a quantidade de hoteis encontrados
print(hotel_amout.text + " encontrados") #Printa a quantidade de hoteis encontrados
number_hotels = int(''.join(c for c in hotel_amout.text if c.isdigit())) #Transforma a string de hoteis encontrados em um inteiro contendo o valor

#Iterando até encerrar o loop
while(True):
    search_amout = int(input("Quantos hotéis deseja procurar?: ")) #Pergunta quantos hoteis deseja procurar
    if(search_amout <= number_hotels): #Se o número que deseja encontrar estiver dentro do possível, quebra o loop
        break #Sai do loop
    print("Número superior ao de hotéis encontrados!") #Alerta o erro de um valor inválido e o loop continua
rest = search_amout #Atribui o resto como o valor desejado a ser procurado
count = 0 #Contador de hotéis começa zerado
print("Buscando...") #Mostrando no terminal que a cidade está sendo procurada

lista_hoteis = [] #Lista de hoteis começa vazia
hotel_conveniences = [] #Lista de conveniências dos hoteis começa vazzia

while(True): #Iterando por cada hotel da página
    new_content = browser.page_source #Pega o conteúdo da nova página que entrou
    new_site = BeautifulSoup(new_content, "html.parser") #Transforma ela em um objjeto do BS4
    hotels = new_site.find_all("div", attrs={"class": "uaTTDe BcKagd bLc2Te Xr6b1e"}) #Procura todos os hoteis da página
    for hotel in hotels: #Iterando por cada hotel nos hoteis encontrados na página
        hotel_conveniences[:] = [] #Zera as conveniências encontradas (para renovar a cada hotel)
        hotel_name = hotel.find("a", attrs={"class": "PVOOXe"}) #Encontra o nome do hotel
        hotel_value = hotel.find("span", attrs={"class": "qQOQpe prxS3d"}) #Encontra o valor do hotel
        hotel_rating = hotel.find("span", attrs={"class": "ta47le"}) #Encontra a valiação do hotel
        hotel_link = hotel.find("a", attrs={"class": "PVOOXe"}) #Encontra o link do hotel
        conveniences = hotel.find_all("li", attrs={"class": "XX3dkb bX73z lh4a3"}) #Encontra todas as conveniências do hotel (com excessão da primeira)
        first_convenience = hotel.find("div", attrs={"class": "bX73z lh4a3"}) #Encontra a primeira conveniência do hotel
        #Note que a primeira possui um elemento diferente do que a segunda em diante

        if(first_convenience): #Se houver uma conveniencia, adiciona no inicio da lista de conveniencias
            hotel_conveniences.append(first_convenience.get_text(strip=True))

        #Realiza a mesma coisa, mas com as demais conveniencias
        for convenience in conveniences:
            hotel_conveniences.append(convenience.get_text(strip=True))

        #Série de parâmetros para regularizar dados não encontrados e evitar erros no código
        if not (hotel_name):
            nome = "Nome não informado"
        else:
            nome = hotel_name.get("aria-label", "N/A")

        if not (hotel_value):
            valor = "Valor não informado"
        else:
            valor = hotel_value.text.strip()

        if not (hotel_rating):
            avaliacao = "Sem avaliações"
        else:
            avaliacao = hotel_rating.text.strip()

        if not (hotel_link):
            link = "Link não encontrado"
        else:
            link = "https://google.com.br" + hotel_link.get("href", "") #O href no site não contem o domínio do google no link, então concatenamos as duas strings

        if not (hotel_conveniences):
            conveniences_hotel = ""
        else:
            conveniences_hotel = hotel_conveniences

        if not(hotel_name or hotel_value or hotel_rating or hotel_link or hotel_conveniences): #Se não tiver nada, não contabiliza como um hotel encontrado
            continue
        else:
            count+=1

        #Padronizando a saída das strings da lista de conveniências para
        conveniencias = ', '.join(map(str, hotel_conveniences))
        #Utilizando o regex para formatar a saída de avaliação
        avaliacao_regex = re.sub(r"\s\(\d+,?\d*.*\)", '', avaliacao)
        #Padronizando a lista de hoteis com os atributos
        lista_hoteis.append([nome, valor.replace('R$', '').replace('.','').strip(), avaliacao_regex.replace(',', '.'), link, conveniencias])

        #Linha de códigos para printar no terminal os resultados
        '''
        print("Nome do Hotel:", nome)
        print("Valor da Diária:", valor)
        print("Avaliação do Hotel:", avaliacao)
        print("Link do Hotel:", link, "\n")
        '''

        if(count == search_amout): #Quando a contagem for igual ao número desejado, sai do loop
            break
    rest = rest - 20 #Cada página contém 20 hoteis, aqui está pegando o resto para decidir se irá precisar de mais uma página ou não
    if(count == search_amout): #Novamente, sai do segundo loop quando a contagem for igual ao número desejado
        break
    sleep(1)
    if(rest > 20): #Caso ainda precise de mais uma página, entra na condição
        if page == 1: #Se for a primeira página, isto é, não tem uma página anterior, clica no único botão presente no final da página (o de avançar)
            next = browser.find_element(By.CLASS_NAME, "eGUU7b") #Procura o primeiro botão da classe
            next.click() #Clica no botão
        elif page > 1:
            try:
                # Controla a navegação entre páginas de resultados, aguardando o botão de "Próxima página"
                # ficar clicável para evitar erros de interação e encerrar a busca quando não houver mais páginas
                next_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Próxima página']")
                    )
                )
                browser.execute_script("arguments[0].click();", next_button)
                page += 1
            except:
                print("Não há mais páginas.")
                break

if(count == 0): #Se não encontrar nenhum hotel
    print("Nenhum hotel encontrado.") #Printa que não encontrou nenhum hotel
    sleep(0.5)
    print("Acesso concluído.") #Mostra que o acesso foi concluído
    browser.quit() #Fechando o browser

#Puramente estético:
print(f"Escrevendo em {city}.csv...") #Mostrando no terminal que está escrevendo os resultados no {city}.csv
sleep(0.5)

#Linha de código utilizando o pandas para criar o dataframe com os dados da lista dos hoteis encontrados
dados = pd.DataFrame(lista_hoteis, columns=['Nome do Hotel', 'Valor da Diária (R$)', 'Avaliação', 'Link', 'Conveniências'])
dados['Valor da Diária (R$)'] = pd.to_numeric(dados['Valor da Diária (R$)'], errors='coerce')
dados['Avaliação'] = pd.to_numeric(dados['Avaliação'], errors='coerce')
dados.to_csv(f'dataset/{city}.csv', index=False) #Salvando tudo em um csv

print("Acesso concluído.") #Mostra que o acesso foi concluído

#input("Pressione ENTER para fechar o navegador...") #Input para segurar a página do navegador aberta para avaliar o conteúdo html de forma dinâmica
browser.quit() #Fechando o browser
