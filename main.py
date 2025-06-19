import os
from config import Config
import logging

# Configurar logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def initialize_system():
    """Inicializa o sistema multiagentes"""
    logger.info("Iniciando sistema multiagentes...")
    
    # Verificar configurações
    if not Config.MONDAY_API_TOKEN:
        logger.error("Token do Monday.com não configurado!")
        return False
    
    logger.info("Sistema inicializado com sucesso!")
    return True

def main():
    """Função principal do sistema"""
    if not initialize_system():
        return
    
    # Aqui você pode implementar a lógica principal do sistema
    # que orquestrará a comunicação entre os agentes
    
    logger.info("Sistema pronto para processar transcrições")

if __name__ == "__main__":
    main()
