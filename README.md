## PIPELINE DE ANÁLISE DE CRIPTOMOEDAS ## 

## DESCRIÇÃO DO PROJETO 

Esse é um pipeline que tem como objetivo extrair os dados de uma API de criptomoedas, tratar os dados com pandas, subir para o banco de dados MySQL e realizar a criação de um DataViz para a retirada de insights.

    # ESTRUTURA DO PROJETO:
        - config/settings.py - Contém as configurações do banco de dados e da API
        - data_viz/criptos.pbix - Dashboard desenvolvimento para métricas e insights das criptomoedas
        - scripts/banco_dados.py - Script responsavel por ações do banco de dados. (Conectar, criar tabelas, inserir dados, criação de views)
        - scripts/requisições.py - Script responsavel para realizar as chamadas de APIs e coletar os dados
        - scripts/tratamentos.py - Script responsavel por realizar a limpeza e transformação dos dados antes de envia-los para o banco
        - .env - Arquivo onde contém as variaveis de ambiente
        - app.py - Arquivo principal conectando todas as etapas do ETL
        
    # ESTRUTURA DO BANCO DE DADOS:
        - dim_criptos -  Informações básicas sobre as moedas (nome, simbolo, ranking)
        - cripto_atual - Dados recentes das moedas (preço, market cap, volume, etc)
        - cripto_historico - Dados historicos das moedas (preço)

    # ESTRUTURA DO DATA VIZ: 
        # Tela 'Geral'
            - Market Cap Total: Mostra a soma total do market cap de todas as criptos;
            - Total de Moedas: Quantidade total de moedas coletadas no banco;
            - Volume total de negociações: Soma do volume de negociações das moedas nas últimas 24h;
            - Gráfico de barras 'Moedas com Melhor Capitalização': Mostra um comparativo da capitaliazção das moedas;
            - Gráfico 'Evolução do Preço Médio': Mostra a variação do preço médio das moedas;
            - Árvore Hierárquico: Da liberdade ao usuario de poder analisar de diversas formas diferentes.
        
        # Tela 'Cripto'
            - Nessa tela filtramos a moeda que queremos ver;
            - Indicadores Principais: Os principais indicadores das moedas, preço atual, maior e menor dos últimos 12 meses;
            - Evolução de Variação Percentual: Representa a variação percentual da moeda ao longo do tempo;
            - Evolução de Preço: Exibe o histórico de preços da moeda;
            - Maiores e Menores Valores Mensais: Mostra para cada mes, o maior, menor e o preço médio;
            - Market Share da Moeda: Mostra a participação da moeda no total do Market Cap.

## EXECUÇÃO DO PIPELINE

1° Clonar o repositorio
    git clone <url>
    cd CRIPTO_DATA_PROJECT

2° Instalar Dependencias 
    pip install -r requirements.txt

3° Configurar variaveis de ambiente
    Configue as variaveis no arquivo '.env' lá voce deve colocar os dados do seu banco de dados. 

4° Execução do programa
    Execute o pipeline principal pelo terminal
    python app.py

5° DataViz 
    Abra o arquivo cripto.pbxi na pasta 'DataViz' e configue a conexão do banco de dados MySQL. Logo após, atualize os dados para carregar as informações mais recentes

