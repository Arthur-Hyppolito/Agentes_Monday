import logging
import requests
import time
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class AgenteExecutor:
    def __init__(self):
        """Inicializa o AgenteExecutor"""
        logger.info("Inicializando AgenteExecutor...")
        
        # Configurar headers para a API do Monday.com
        self.headers = {
            'Authorization': Config.MONDAY_API_TOKEN,
            'Content-Type': 'application/json'
        }
        
        # Configurações de retry
        self.max_retries = Config.MAX_RETRIES
        self.retry_delay = Config.RETRY_DELAY
        
        # Limites da API
        self.limits = {
            'complexidade': 1000,
            'minutos': 1000,
            'concorrencia': 10
        }
        
        # Métricas
        self.metrics = {
            'sucessos': 0,
            'falhas': 0,
            'retries': 0,
            'ultima_execucao': None
        }
        
        logger.info("AgenteExecutor inicializado com sucesso!")

    def executar_mutation(self, payload: dict) -> dict:
        """
        Executa uma mutation na API do Monday.com com retry automático.
        
        Args:
            payload (dict): Payload com query e variáveis
            
        Returns:
            dict: Resultado da execução
        """
        logger.info("Executando mutation...")
        
        for attempt in range(self.max_retries + 1):
            try:
                # Verificar limites antes de executar
                if not self.verificar_limites():
                    logger.warning("Limite atingido, aguardando janela de 1 minuto...")
                    time.sleep(60)
                    continue
                    
                response = requests.post(
                    Config.MONDAY_API_URL,
                    json=payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Verificar erros na resposta
                    if 'errors' in data:
                        raise Exception(f"Erro na API: {data['errors']}")
                        
                    self.metrics['sucessos'] += 1
                    self.metrics['ultima_execucao'] = datetime.now()
                    
                    logger.info("Mutation executada com sucesso!")
                    return data
                    
                raise Exception(f"Status code: {response.status_code}")
                
            except Exception as e:
                if attempt < self.max_retries:
                    logger.warning(f"Erro na tentativa {attempt + 1}: {str(e)}")
                    logger.info(f"Aguardando {self.retry_delay}s antes de tentar novamente...")
                    time.sleep(self.retry_delay)
                    self.metrics['retries'] += 1
                    continue
                    
                logger.error(f"Falha após {self.max_retries} tentativas: {str(e)}")
                self.metrics['falhas'] += 1
                raise

    def verificar_limites(self) -> bool:
        """Verifica se os limites da API foram atingidos"""
        try:
            # Consultar limites atuais
            query = '''
            query {
                limits {
                    complexity
                    minutes
                    concurrency
                }
            }
            '''
            
            response = requests.post(
                Config.MONDAY_API_URL,
                json={'query': query},
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verificar cada limite
                for key, value in data['data']['limits'].items():
                    if value >= self.limits[key]:
                        logger.warning(f"Limite atingido: {key} = {value}")
                        return False
                
                return True
                
        except Exception as e:
            logger.error(f"Erro ao verificar limites: {str(e)}")
            return False

    def obter_status_execucao(self) -> dict:
        """Retorna as métricas de execução"""
        return {
            'sucessos': self.metrics['sucessos'],
            'falhas': self.metrics['falhas'],
            'retries': self.metrics['retries'],
            'ultima_execucao': str(self.metrics['ultima_execucao'])
        }

    def tratar_erro_api(self, error: dict) -> str:
        """
        Trata erros específicos da API do Monday.com.
        
        Args:
            error (dict): Erro retornado pela API
            
        Returns:
            str: Mensagem de erro formatada
        """
        if not isinstance(error, dict):
            return str(error)
            
        # Tratar erros conhecidos
        if 'message' in error:
            if 'ComplexityException' in error['message']:
                return "A operação é muito complexa para ser executada"
            elif 'DAILY_LIMIT_EXCEEDED' in error['message']:
                return "Limite diário da API atingido"
            elif 'RATE_LIMIT_EXCEEDED' in error['message']:
                return "Limite de taxa da API atingido"
                
        return error.get('message', str(error))
