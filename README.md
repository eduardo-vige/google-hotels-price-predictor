# Predição de Preços de Hotéis a partir do Google Hotels

## 📌 Visão Geral

Este projeto coleta dados de preços de hotéis a partir do **Google Hotels** e utiliza técnicas de **Regressão Linear** para realizar **predições de valores para hotéis de um cliente**, com base em dados de mercado.

O objetivo é gerar **insights baseados em dados para estratégias de precificação**, permitindo que hotéis posicionem seus preços de forma competitiva em relação a estabelecimentos similares.

O projeto é dividido em dois componentes principais:

- **Web Scraping:** coleta de dados de hotéis no Google Hotels.
- **Modelo de Predição:** treinamento de um modelo de machine learning para estimar preços com base nos dados coletados.

---

## ⚙️ Funcionalidades

- Scraping de dados de hotéis no Google Hotels
- Extração de atributos relevantes, como:
  - nome do hotel
  - localização
  - avaliação
  - preço
  - outras informações disponíveis na listagem
- Limpeza e pré-processamento de dados
- Treinamento de modelo de machine learning para predição de preços
- Geração de estimativas de preço para apoiar decisões estratégicas de precificação

---

## 🧠 Machine Learning

O projeto utiliza uma abordagem de **aprendizado supervisionado** para estimar preços de hotéis com base nas características disponíveis.

Pipeline do projeto:

1. Coleta de Dados (Scraping)
2. Limpeza e Tratamento de Dados
3. Engenharia de Atributos
4. Treinamento do Modelo
5. Predição de Preços

O modelo treinado pode ser utilizado para **estimar faixas de preço esperadas para hotéis semelhantes no mercado**.

---

## 🛠️ Tecnologias Utilizadas

- Python
- Bibliotecas de Web Scraping (ex: BeautifulSoup / Requests / Selenium)
- Processamento de Dados:
  - Pandas
  - NumPy
- Machine Learning:
  - Scikit-learn
- Desenvolvimento:
  - Visual Studio Code

---

## 📂 Estrutura do Projeto

```
project-root
│
├── dataset/
│ └── data.csv
│
├── scripts/
│ └── scraper.py
│
├── notebooks/
│ ├── tratamento.ipynb
│ └── predicao.ipynb
│
```

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/eduardo-vige/google-hotels-price-predictor.git
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o scraper

```bash
python scripts/scraper.py
```

  - Afim de testes, execute 4 vezes o scraper, copiando exatamente este input em cada execução diferente:
    - 1º input: guarulhos
    - 2º input: pinheiros
    - 3º input: itaim_bibi
    - 4º input: santo_amaro

### 4. Executar o script de predição

```bash
python scripts/predicao.py
```

## 📊 Caso de Uso

Este projeto pode ser utilizado por:

  - Hotéis que desejam analisar preços da concorrência

  - Analistas de dados no setor de hospitalidade

  - Equipes de Revenue Management

  - Profissionais de pesquisa de mercado

## 👨‍💻 Autor

Eduardo Nunes e trainees do núcleo de dados da Síntese Jr.
Estudante de Sistemas de Informação — Universidade de São Paulo (USP)
