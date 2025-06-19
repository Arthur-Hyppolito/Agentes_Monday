import os
from config import Config
import logging
from agentes.agente_pre import AgentePre
from agentes.agente_analista import AgenteAnalista
from agentes.agente_validador import AgenteValidador
from agentes.agente_mapeamap import AgenteMapeaMap
from agentes.agente_executor import AgenteExecutor
from agentes.agente_boss import AgenteBoss

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

class SistemaMultiagentes:
    def __init__(self):
        """Inicializa o sistema multiagentes com todos os agentes"""
        logger.info("Inicializando Sistema Multiagentes...")
        
        # Inicializar todos os agentes
        self.agentes = {
            'pre': AgentePre(),
            'analista': AgenteAnalista(),
            'validador': AgenteValidador(),
            'mapeamap': AgenteMapeaMap(),
            'executor': AgenteExecutor(),
            'boss': AgenteBoss()
        }
        
        logger.info("Todos os agentes inicializados com sucesso!")

    def processar_transcricao(self, texto: str) -> dict:
        """
        Processa uma transcrição completa através de todos os agentes.
        
        Args:
            texto (str): Texto da transcrição ou comando
            
        Returns:
            dict: Resultado do processamento completo
        """
        logger.info("Iniciando processamento de transcrição...")
        
        # 1. Pré-processamento com AgentePre
        logger.info("Processando texto com AgentePre...")
        resultado_pre = self.agentes['pre'].processar_texto(texto)
        
        # 2. Análise semântica com AgenteAnalista
        logger.info("Analisando texto com AgenteAnalista...")
        intencoes = self.agentes['analista'].analisar_intencoes(
            resultado_pre['texto_processado'],
            resultado_pre['metadados']
        )
        
        # 3. Validação com AgenteValidador
        logger.info("Validando dados com AgenteValidador...")
        validacao = self.agentes['validador'].validar_entidades(
            intencoes['entidades']
        )
        
        # Se houver erros de validação, retornar
        if validacao['status'] == 'falha':
            return {
                'status': 'falha',
                'erros': validacao['erros'],
                'mensagem': 'Validação falhou'
            }
        
        # 4. Mapeamento para Monday.com com AgenteMapeaMap
        logger.info("Mapeando dados para Monday.com...")
        payload = self.agentes['mapeamap'].criar_payload_mutation(intencoes)
        
        # 5. Execução na API com AgenteExecutor
        logger.info("Executando operação na API do Monday.com...")
        resultado = self.agentes['executor'].executar_mutation(payload)
        
        # 6. Registrar operação no AgenteBoss
        logger.info("Registrando operação no AgenteBoss...")
        self.agentes['boss'].registrar_operacao(
            'executor',
            'executar_mutation',
            resultado
        )
        
        # 7. Gerar relatório final
        relatorio = {
            'status': resultado['status'],
            'texto_original': texto,
            'texto_processado': resultado_pre['texto_processado'],
            'intencoes': intencoes,
            'resultado_monday': resultado,
            'tempo_execucao': resultado.get('tempo_execucao', 0),
            'erros': resultado.get('erros', [])
        }
        
        logger.info("Processamento concluído!")
        return relatorio

    def analisar_desempenho(self) -> dict:
        """Analisa o desempenho geral do sistema"""
        return self.agentes['boss'].analisar_desempenho()

    def obter_sugestoes_otimizacao(self) -> dict:
        """Obtém sugestões de otimização"""
        return self.agentes['boss'].gerar_sugestoes_otimizacao()

def initialize_system():
    """Inicializa o sistema multiagentes"""
    logger.info("Iniciando sistema multiagentes...")
    
    # Verificar configurações
    if not Config.MONDAY_API_TOKEN:
        logger.error("Token do Monday.com não configurado!")
        return None
    
    try:
        # Criar sistema
        sistema = SistemaMultiagentes()
        logger.info("Sistema inicializado com sucesso!")
        return sistema
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema: {str(e)}")
        return None

def main():
    """Função principal do sistema"""
    sistema = initialize_system()
    if not sistema:
        return
    
    # Exemplo de uso
    texto = "João precisa criar uma tarefa para o projeto Marketing até sexta-feira"
    
    logger.info("Processando exemplo de texto...")
    resultado = sistema.processar_transcricao(texto)
    
    # Mostrar resultado
    print("\nResultado do processamento:")
    print(f"Status: {resultado['status']}")
    print(f"Tempo de execução: {resultado['tempo_execucao']}s")
    
    if resultado['erros']:
        print("\nErros encontrados:")
        for erro in resultado['erros']:
            print(f"- {erro}")
    
    # Analisar desempenho
    logger.info("Analisando desempenho do sistema...")
    metricas = sistema.analisar_desempenho()
    print("\nMétricas do sistema:")
    for agente, precisao in metricas['precisao'].items():
        print(f"Precisão {agente}: {precisao:.2%}")

if __name__ == "__main__":
    main()
