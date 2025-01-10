import pandas as pd

# Tratamento da tabela de valores atual
def tratar_cripto_atual(data):
    try:
        df = pd.DataFrame(data['data'])
        colunas_numericas = ['supply', 'marketCapUsd', 'volumeUsd24Hr', 'priceUsd', 'vwap24Hr', 'changePercent24Hr']
        df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric, errors='coerce').round(2)
        df = df.drop(columns=['explorer', 'maxSupply'], errors='ignore')
        return df
    except Exception as e:
        print(f"Erro ao tratar os dados: {e}")
        return pd.DataFrame()  
    
# Lista com os IDs das criptos
def lista_criptos(df):
    criptos = df['id'].to_list()
    return criptos   
    
# Tratamento das criptos historicos
def tratar_cripto_historico(df_historicos):
    
    df_historicos = df_historicos.drop(columns=['time'])
    df_historicos['priceUsd'] = pd.to_numeric(df_historicos['priceUsd'], errors='coerce')
    df_historicos['date'] = pd.to_datetime(df_historicos['date']).dt.tz_localize(None).dt.date
    
    return df_historicos

# Função para reclaionar os nomes da moedas de valores atual com os IDs da DIM
def relacionar_ids_atual(df_atuais, id_moedas):
    df_atuais['id_moeda'] = df_atuais['id'].map(id_moedas)
    if df_atuais['id_moeda'].isnull().any():
        faltantes = df_atuais[df_atuais['id_moeda'].isnull()]['id'].unique()
        print(f"Atenção: Os seguintes IDs não foram encontrados no dicionário: {faltantes}")
    df_atuais = df_atuais.drop(columns=['name', 'symbol', 'rank'])

    return df_atuais

# Função para reclaionar os nomes da moedas de valores historicos com os IDs da DIM
def relacionar_ids_historicos(df_historicos, id_moedas):
    df_historicos['id'] = df_historicos['cripto'].map(id_moedas)
    if df_historicos['cripto'].isnull().any():
        faltantes = df_historicos[df_historicos['cripto'].isnull()]['id'].unique()
        print(f"Atenção: Os seguintes IDs não foram encontrados no dicionário: {faltantes}")
    df_historicos = df_historicos.drop(columns=['cripto'])
    return df_historicos