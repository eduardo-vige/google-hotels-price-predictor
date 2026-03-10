import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

#Carrega o dataset dos hotéis
df = pd.read_csv('../dataset/df_modelo.csv')

#Cria os hotéis base do cliente 
avaliacao_mediana = df['Avaliação'].median()

hotel_guarulhos = {
    'Avaliação': avaliacao_mediana,
    'estrelas': 4,
    'wifi': 1,
    'cafe_manha': 1,
    'piscina': 0,
    'estacionamento': 1,
    'academia': 0,
    'spa': 0,
    'ar_condicionado': 0,
    'pet_friendly': 0,
    'regiao_Itaim Bibi': 0,
    'regiao_Pinheiros': 0,
    'regiao_Santo Amaro': 0
}

hotel_itaim = {
    'Avaliação': avaliacao_mediana,
    'estrelas': 5,
    'wifi': 1,
    'cafe_manha': 1,
    'piscina': 1,
    'estacionamento': 1,
    'academia': 1,
    'spa': 1,
    'ar_condicionado': 1,
    'pet_friendly': 1,
    'regiao_Itaim Bibi': 1,
    'regiao_Pinheiros': 0,
    'regiao_Santo Amaro': 0
}

hotel_santo_amaro = {
    'Avaliação': avaliacao_mediana,
    'estrelas': 3,
    'wifi': 1,
    'cafe_manha': 0,
    'piscina': 0,
    'estacionamento': 1,
    'academia': 0,
    'spa': 0,
    'ar_condicionado': 1,
    'pet_friendly': 0,
    'regiao_Itaim Bibi': 0,
    'regiao_Pinheiros': 0,
    'regiao_Santo Amaro': 1
}

hotel_pinheiros = {
    'Avaliação': avaliacao_mediana,
    'estrelas': 4,
    'wifi': 1,
    'cafe_manha': 1,
    'piscina': 0,
    'estacionamento': 1,
    'academia': 1,
    'spa': 0,
    'ar_condicionado': 1,
    'pet_friendly': 1,
    'regiao_Itaim Bibi': 0,
    'regiao_Pinheiros': 1,
    'regiao_Santo Amaro': 0
}

#Define as variáveis explicativas (X) e o valor da diária como variável alvo (y)
X = df.drop('Valor da Diária (R$)', axis=1)
y = df['Valor da Diária (R$)']

#Divide os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Treina um modelo de Regressão Linear para prever o valor da diária
model = LinearRegression()
model.fit(X_train, y_train)

#Avalia o desempenho do modelo usando MAE
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

#Realiza a predição do valor da diária para os hotéis do cliente
df_clientes = pd.DataFrame([
    hotel_guarulhos,
    hotel_itaim,
    hotel_santo_amaro,
    hotel_pinheiros
])

precos_previstos = model.predict(df_clientes)
precos_previstos

#Printa os valores da predição mostrando a taxa de variação
for nome, preco in zip(
    ['Guarulhos', 'Itaim Bibi', 'Santo Amaro', 'Pinheiros'],
    precos_previstos
):
    print(
        f"{nome}: R$ {preco:.2f} "
        f"(intervalo: R$ {preco-mae:.2f} – R$ {preco+mae:.2f})"
    )
