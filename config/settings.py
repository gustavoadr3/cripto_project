import os
from dotenv import load_dotenv


load_dotenv()

# Configurações do Banco de Dados MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Configuração da API
API_BASE_URL = os.getenv("API_BASE_URL")

