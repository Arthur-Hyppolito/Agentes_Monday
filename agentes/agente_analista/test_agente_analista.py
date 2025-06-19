import pytest
from agente_analista import AgenteAnalista

def test_extrair_entidades():
    """Testa a extração de entidades"""
    agente = AgenteAnalista()
    texto = "João precisa criar uma tarefa para o projeto Marketing até sexta-feira"
    
    entidades = agente.extrair_entidades(texto)
    
    assert isinstance(entidades, dict)
    assert 'pessoas' in entidades
    assert 'datas' in entidades
    assert 'projetos' in entidades
    assert 'João' in entidades['pessoas']
    assert any('sexta' in data for data in entidades['datas'])

def test_identificar_acoes():
    """Testa a identificação de ações"""
    agente = AgenteAnalista()
    texto = "Criar uma nova tarefa para o projeto Marketing"
    
    acoes = agente.identificar_acoes(texto)
    
    assert isinstance(acoes, list)
    assert len(acoes) > 0
    assert 'confianca' in acoes[0]

def test_analisar_intencoes():
    """Testa a análise de intenções"""
    agente = AgenteAnalista()
    texto = "João precisa criar uma tarefa para o projeto Marketing até sexta-feira"
    entidades = agente.extrair_entidades(texto)
    
    intencoes = agente.analisar_intencoes(texto, entidades)
    
    assert isinstance(intencoes, dict)
    assert 'objetivo' in intencoes
    assert 'prioridade' in intencoes
    assert 'entidades' in intencoes
