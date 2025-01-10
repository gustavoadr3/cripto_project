import pandas as pd
import requests 
from config.settings import API_BASE_URL

# Requisição para buscar os valores atuais das criptos
def cripto_atual(endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() 
        else:
            raise Exception(f"Erro na requisição: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"Erro de conexão ou requisição: {e}")

# Requisição para buscar os valores historicos das criptos

def cripto_historico(crypto_ids, interval="d1"):
    df_historicos = pd.DataFrame()
    
    for crypto_id in crypto_ids:
        try:
            url = f"{API_BASE_URL}assets/{crypto_id}/history?interval={interval}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()['data']
                df = pd.DataFrame(data)             
                df['cripto'] = crypto_id
                df_historicos = pd.concat([df_historicos, df], ignore_index=True)
                print(f"Dados históricos de {crypto_id} obtidos com sucesso.")
            else:
                print(f"Erro na requisição para {crypto_id}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Erro ao buscar dados para {crypto_id}: {e}")
    
    return df_historicos















