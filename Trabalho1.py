import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx

# leitura do arquivo csv
# df = dataFrame

# Abertura do arquivo para o grafico de contagem de postos pos estado
with open(r'combustiveis\Preços semestrais - AUTOMOTIVOS_2023.02.csv', 'r', encoding='utf-8', errors='ignore') as file:

    df = pd.read_csv(file, header=0, index_col=0, parse_dates=True,sep=';', encoding='utf-8',date_format='%Y-%m-%d')

# Filtrando os dados
df.drop_duplicates(subset='Revenda', inplace=True)

# Contagem de postos por estado
contagem_por_estado= df['Estado - Sigla'].value_counts()

# Agrupamento dos estados
grupo_por_estado = df.groupby(['Estado - Sigla'])
# Convertendo a virgula por ponto pra realizar a conversao
df['Valor de Venda'] = df['Valor de Venda'].str.replace(',','.')
# Convertendo os valores da coluna Valor de venda em numeros
df['Valor de Venda'] = pd.to_numeric(df['Valor de Venda'], errors='coerce')

# Calculo da média dos preços por estado
media_por_estado = grupo_por_estado['Valor de Venda'].mean()

# # Filtrando apenas o estado de MG
df_mg = df[(df['Estado - Sigla'] == 'MG') & (df['Produto'] == 'GASOLINA')]

mg_grupo = df_mg.groupby(['Data da Coleta'])

# Calculando a média dos preços de venda por município e produto
media_por_municipio_produto = mg_grupo['Valor de Venda'].mean()

# Transformando o resultado em um novo DataFrame
df_media_municipio_produto = media_por_municipio_produto.reset_index()

# Convertendo a coluna "Data da Coleta" em datetime
df_media_municipio_produto['Data da Coleta'] = pd.to_datetime(df_media_municipio_produto['Data da Coleta'],format='%d/%m/%Y')

# Criando uma nova coluna para o mes
df_media_municipio_produto['Mes'] = df_media_municipio_produto['Data da Coleta'].dt.month

# Calculando a media por mes
media_por_mes = df_media_municipio_produto.groupby('Mes')['Valor de Venda'].mean()



# --------- Plotagem dos Graficos ----------------- #

# # Grafico de contagem por estado
plt.figure(figsize=(10,6))

plt.bar(contagem_por_estado.index, contagem_por_estado.values)
plt.title("Postos de combustiveis por estado")
plt.ylabel('Quantidade de postos')
plt.xlabel('Estados')
plt.show()


# Grafico temporal da média de venda da gasolina no estado de minas Gerais
plt.plot(media_por_mes.index, media_por_mes.values, marker = 0)
plt.title('Valor médio de Venda da Gasilina no estado de Minas Gerais')
plt.xlabel('Mês')
plt.ylabel('Valor médio de venda')
plt.show()

# Grafico de rede
G = nx.Graph()

# definição dos dados que serão apresentados(regiao e estado)
regioes = df['Regiao - Siglas'].unique()
estados = df['Estado - Sigla'].unique()

# definição dos nós(pontos de ligação do grafico)
G.add_node('Brasil')
G.add_nodes_from(regioes)
G.add_nodes_from(estados)

# Realizando as conexões
for _, row in df.iterrows():
    G.add_edge(row['Estado - Sigla'], row['Regiao - Siglas'])
    G.add_edge(row['Regiao - Siglas'], 'Brasil')

# impressao do grafico
nx.draw(G, with_labels=True, node_color="skyblue", font_size=10)
plt.show()

