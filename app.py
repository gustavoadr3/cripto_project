from scripts.requisicoes import cripto_atual, cripto_historico
from scripts.tratamentos import tratar_cripto_atual, lista_criptos, tratar_cripto_historico, relacionar_ids_atual, relacionar_ids_historicos
from scripts.banco_dados import conexao_banco, tabela_valores_atuais, tabela_valores_historicos, dim_criptos, dados_dim_criptos, inserir_dados_atuais, inserir_dados_historicos, criar_views

# Fluxo principal para obtenção dos dados das criptos
def main():
    try:
        # Passo 1: Buscar os valores atuais das criptos
        endpoint = "assets"
        data = cripto_atual(endpoint)
        df_atuais = tratar_cripto_atual(data)
        
        # Passo 2: Obter a lista de IDs das criptos
        criptos = lista_criptos(df_atuais)
        
        # Passo 3: Buscar os dados históricos com base nos IDs
        df_historicos = cripto_historico(criptos, interval="d1")
        df_historicos = tratar_cripto_historico(df_historicos)
        
        # Passo 4: Conectar ao banco de dados 
        connection = conexao_banco()
        
        # Passo 5: Criar as tabelas no banco de dados
        dim_criptos(connection)
        tabela_valores_atuais(connection)
        tabela_valores_historicos(connection)
        
        # Passo 6: Adicionar os dados nas tabelas 
        dict_moedas = dados_dim_criptos(connection, df_atuais)
        df_atuais = relacionar_ids_atual(df_atuais, dict_moedas)
        inserir_dados_atuais(connection, df_atuais)
        df_historicos_final = relacionar_ids_historicos(df_historicos, dict_moedas)
        inserir_dados_historicos(connection, df_historicos_final)
        
        # Passo 7: Adicionar views no banco de dados
        criar_views(connection)
        connection.close()

        print('Fluxo finalizado!')
    except Exception as e:
        print(f"Erro no fluxo principal: {e}")

if __name__ == "__main__":
    main()
