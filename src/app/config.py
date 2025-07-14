import os
import logging


class Config:

    # Configuração de diretórios
    #BASE_DIR = os.path.dirname(__file__)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

    is_data_reception_active = False

    # Configuracao do logging
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    @staticmethod
    def setup_logging():
        logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)

    # Configuracoes de dados
    VALID_DISTANCES = [10, 20, 30]

    DADOS_RECEBIDOS_PATH = os.path.join(DATA_DIR, "raw-launch-data.json")
    DADOS_BRUTOS_PATH = os.path.join(DATA_DIR, "dados_brutos.csv")

    # Nome de arquivos
    DADOS_RECEBIDOS_FILE = "raw-launch-data.json"
    #DADOS_BRUTOS_FILE = "dados_brutos.csv"
    VELOCIDADE_MEDIA_FILE = "velocidade_media.txt"
