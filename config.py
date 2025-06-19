class Config:
    # Configurações do Monday.com
    MONDAY_API_URL = "https://api.monday.com/v2"
    MONDAY_API_TOKEN = None  # Será carregado do .env
    
    # Configurações do MCP
    MCP_URL = "https://mcp.zapier.com/api/mcp/s/M2RlOTAzNmMtNmJkYS00ZDkwLTlhMGUtMTYxOTRmYmRiYzVjOjNmYWIyZTMxLWMyY2YtNDIyOS1hMDdiLWU1ZGU0NmUzMzFmZQ==/mcp"
    
    # Configurações do NLP
    NLP_MODEL = "pt_core_news_lg"  # Modelo do spaCy para português
    
    # Configurações de validação
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # segundos
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "agentes.log"
