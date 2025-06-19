import pytest
from agente_boss import AgenteBoss
import pandas as pd

def test_registrar_operacao():
    """Testa registro de operação"""
    agente = AgenteBoss()
    
    resultado = {
        'status': 'sucesso',
        'tempo_execucao': 2.5
    }
    
    agente.registrar_operacao('AgentePre', 'processar_texto', resultado)
    
    assert len(agente.historico) == 1
    assert agente.historico.iloc[0]['agente'] == 'AgentePre'
    assert agente.historico.iloc[0]['resultado'] == 'sucesso'

def test_analisar_desempenho():
    """Testa análise de desempenho"""
    agente = AgenteBoss()
    
    # Simular operações
    for i in range(10):
        resultado = {
            'status': 'sucesso' if i % 2 == 0 else 'falha',
            'tempo_execucao': 2.5
        }
        agente.registrar_operacao('AgentePre', 'processar_texto', resultado)
    
    metricas = agente.analisar_desempenho()
    
    assert 'precisao' in metricas
    assert 'tempo_medio' in metricas
    assert 'taxa_erro' in metricas

def test_gerar_sugestoes_otimizacao():
    """Testa geração de sugestões de otimização"""
    agente = AgenteBoss()
    
    # Simular operações com erros
    for i in range(20):
        resultado = {
            'status': 'falha',
            'tempo_execucao': 10.0,
            'erro': 'Erro simulado'
        }
        agente.registrar_operacao('AgenteAnalista', 'analisar_intencao', resultado)
    
    sugestoes = agente.gerar_sugestoes_otimizacao()
    
    assert 'agentes' in sugestoes
    assert 'AgenteAnalista' in sugestoes['agentes']
