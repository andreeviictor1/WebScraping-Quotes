import requests
from bs4 import BeautifulSoup
import csv 
from tqdm import tqdm

# Função para extrair citações de uma página específica com base em tags filtradas
def extrair_citacoes(url, tag_filtrada=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    citacoes = []
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        
        # Filtra citações com base na tag desejada
        if tag_filtrada is None or tag_filtrada in tags and author_filtrado is None or author_filtrado in author:
            citacoes.append({'Citação': text, 'Autor': author, 'Tags': ', '.join(tags)})
    return citacoes

# URL base
url = "https://quotes.toscrape.com/page/{}/"

# Defina a tag filtrada (por exemplo, 'life')
tag_filtrada = 'life'
author_filtrado = 'Albert Einstein'
# Armazena todas as citações em uma lista
todas_citacoes = []

# Usa tqdm para mostrar a barra de progresso
for page in tqdm(range(1, 11), desc="Processando páginas"):
    citacoes = extrair_citacoes(url.format(page), tag_filtrada)
    todas_citacoes.extend(citacoes)

# Abre um arquivo CSV para escrita
with open('citacoes_filtradas.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Citação', 'Autor', 'Tags']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for citacao in todas_citacoes:
        writer.writerow(citacao)
