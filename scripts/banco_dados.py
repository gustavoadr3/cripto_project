import mysql.connector
from mysql.connector import Error
from config.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from scripts.requisicoes import cripto_atual
from scripts.tratamentos import tratar_cripto_atual, lista_criptos

# Conectar com o banco de dados
def conexao_banco():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        if connection.is_connected():
            print(f"Conexão com o MySQL no banco '{MYSQL_DATABASE}' realizada com sucesso!")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None
    
# Criar tabela no banco com os valores atuais
def tabela_valores_atuais(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS cripto_atual (
            id_cripto INT,
            supply DECIMAL(25,2),
            marketCapUsd DECIMAL(25,2),
            volumeUsd24Hr DECIMAL(25,2),
            priceUsd DECIMAL(25,2),
            changePercent24Hr DECIMAL(25,2),
            vwap24Hr DECIMAL(25,2),
            PRIMARY KEY (id_cripto),
            FOREIGN KEY (id_cripto) REFERENCES dim_criptos(id)
        );
        """
        cursor.execute(create_table_query)
        print("Tabela 'cripto_atual' criada com sucesso!")
        cursor.close()
    except Error as e:
        print(f"Erro ao criar a tabela: {e}")

# Criar tabela no banco com os valores históricos
def tabela_valores_historicos(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS cripto_historico (
            id INT AUTO_INCREMENT PRIMARY KEY,
            priceUsd DECIMAL(20,2),
            date DATE,
            id_criptos INT,
            FOREIGN KEY (id_criptos) REFERENCES dim_criptos(id)
        );
        """
        cursor.execute(create_table_query)
        print("Tabela 'cripto_historico' criada com sucesso!")
        cursor.close()
    except Error as e:
        print(f"Erro ao criar a tabela: {e}")
        
# Criar tabela dimensão 
def dim_criptos(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dim_criptos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            symbol VARCHAR(20),
            ranking INT
        );
        """
        cursor.execute(create_table_query)
        print("Tabela 'dim_criptos' criada com sucesso!")
        cursor.close()
    except Error as e:
        print(f"Erro ao criar a tabela: {e}")
        
# Inserir dados na tabela dimensão
def dados_dim_criptos(connection, df):
    try:
        cursor = connection.cursor()
        
        # Buscar moedas já existentes na tabela
        cursor.execute("SELECT nome FROM dim_criptos")
        existentes = set(row[0] for row in cursor.fetchall())  
        novas_moedas = df[~df['id'].isin(existentes)]

        
        if not novas_moedas.empty:
            insert_query = """
            INSERT INTO dim_criptos (nome, ranking, symbol)
            VALUES (%s, %s, %s)
            """
            values = [
                (row['id'], row['rank'], row['symbol']) 
                for _, row in novas_moedas.iterrows()
            ]
            cursor.executemany(insert_query, values)
            connection.commit()
            print(f"{cursor.rowcount} novas criptos inseridas!")
        else:
            print("Nenhuma nova cripto para inserir.")
        
        # Buscar o ID e nome de todas as criptos na tabela
        cursor.execute("SELECT id, nome FROM dim_criptos")
        resultados = cursor.fetchall()
        resultado_final = {nome: id for id, nome in resultados}
        
        cursor.close()
        return resultado_final

    except Error as e:
        print(f"Erro ao inserir dados na dimensão: {e}")
        return {}
        
# Inserir dados na tabela dados atuais
def inserir_dados_atuais(connection, df_atuais):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO cripto_atual (
            id_cripto, supply, marketCapUsd, 
            volumeUsd24Hr, priceUsd, changePercent24Hr, vwap24Hr
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            supply = VALUES(supply),
            marketCapUsd = VALUES(marketCapUsd),
            volumeUsd24Hr = VALUES(volumeUsd24Hr),
            priceUsd = VALUES(priceUsd),
            changePercent24Hr = VALUES(changePercent24Hr),
            vwap24Hr = VALUES(vwap24Hr)
        """
        valores = [
            (
                row['id_moeda'], row['supply'], 
                row['marketCapUsd'], row['volumeUsd24Hr'], row['priceUsd'], 
                row['changePercent24Hr'], row['vwap24Hr']
            )
            for _, row in df_atuais.iterrows()
        ]


        cursor.executemany(insert_query, valores)
        connection.commit()
        
        print('Dados inseridos na tabela cripto_atual')
        cursor.close()

    except Error as e:
        print(f"Erro ao inserir dados na tabela 'cripto_atual': {e}")

# Inserir dados na tabela dados históricos
def inserir_dados_historicos(connection, df_historicos):
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO cripto_historico (
            id_criptos, priceUsd, date
        ) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            priceUsd = VALUES(priceUsd) 
        """
        valores = [
            (row['id'], row['priceUsd'], row['date'])
            for _, row in df_historicos.iterrows()
        ]
        cursor.executemany(insert_query, valores)
        connection.commit()
        print(f"{cursor.rowcount} dados inseridos na tabela 'cripto_historico'.")
        cursor.close()

    except Error as e:
        print(f"Erro ao inserir dados históricos na tabela 'cripto_historico': {e}")

# Função para criar as views
def criar_views(connection):
    try:
        cursor = connection.cursor()

        # View Rendimento Percentual
        view_rendimento_percentual = """
        CREATE VIEW vw_rendimento_percentual AS
        SELECT 
            h1.id_criptos AS id_cripto,
            d.nome AS nome_cripto,
            d.symbol AS simbolo,
            h1.date AS data_atual,
            h2.date AS data_anterior,
            h1.priceUsd AS preco_atual,
            h2.priceUsd AS preco_anterior,
            ROUND(((h1.priceUsd - h2.priceUsd) / h2.priceUsd) * 100, 2) AS variacao_percentual
        FROM 
            cripto_db.cripto_historico h1
        JOIN 
            cripto_db.cripto_historico h2 
            ON h1.id_criptos = h2.id_criptos AND h1.date = DATE_ADD(h2.date, INTERVAL 1 DAY)
        JOIN 
            cripto_db.dim_criptos d ON h1.id_criptos = d.id;
        """
        cursor.execute(view_rendimento_percentual)
        print("View 'vw_rendimento_percentual' criada com sucesso!")

        # View Top Criptos por Valor de Mercado
        view_top_valor_mercado = """
        CREATE VIEW vw_top_valor_mercado AS
        SELECT 
            d.nome AS nome_cripto,
            d.symbol AS simbolo,
            a.marketCapUsd AS valor_mercado,
            d.ranking
        FROM 
            cripto_db.cripto_atual a
        JOIN 
            cripto_db.dim_criptos d ON a.id_cripto = d.id
        ORDER BY 
            a.marketCapUsd DESC
        LIMIT 10;
        """
        cursor.execute(view_top_valor_mercado)
        print("View 'vw_top_valor_mercado' criada com sucesso!")

        # View Histórico de Preços por Cripto
        view_historico_precos = """
        CREATE VIEW vw_historico_precos AS
        SELECT 
            d.nome AS nome_cripto,
            d.symbol AS simbolo,
            h.date,
            h.priceUsd AS preco_historico
        FROM 
            cripto_db.cripto_historico h
        JOIN 
            cripto_db.dim_criptos d ON h.id_criptos = d.id
        ORDER BY 
            h.date ASC;
        """
        cursor.execute(view_historico_precos)
        print("View 'vw_historico_precos' criada com sucesso!")

        connection.commit()
        cursor.close()

    except Exception as e:
        print(f"Erro ao criar as views: {e}")