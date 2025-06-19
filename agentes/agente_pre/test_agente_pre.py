import pytest
from agente_pre import AgentePre

def test_processar_texto():
    """Testa o processamento básico de texto"""
    agente = AgentePre()
    texto = "Olá, preciso que você crie uma tarefa para o João."
    
    resultado = agente.processar_texto(texto)
    
    assert isinstance(resultado, dict)
    assert 'texto_processado' in resultado
    assert 'metadados' in resultado
    assert 'status' in resultado
    assert resultado['status'] == 'sucesso'

def test_validar_texto_valido():
    """Testa validação de texto válido"""
    agente = AgentePre()
    texto = "Criar uma nova tarefa para o projeto X"
    
    assert agente.validar_texto(texto) is True

def test_validar_texto_invalido():
    """Testa validação de texto inválido"""
    agente = AgentePre()
    
    # Testar string vazia
    assert agente.validar_texto("") is False
    
    # Testar string muito curta
    assert agente.validar_texto("oi") is False
    
    # Testar não string
    assert agente.validar_texto(123) is False
