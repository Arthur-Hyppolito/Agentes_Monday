import pytest
from agente_validador import AgenteValidador

def test_validar_entidades():
    """Testa a validação de entidades"""
    agente = AgenteValidador()
    
    entidades = {
        'pessoas': ['João', 'Maria'],
        'datas': ['2025-06-20', '2024-01-01'],
        'projetos': ['Marketing', 'Desenvolvimento']
    }
    
    resultado = agente.validar_entidades(entidades)
    
    assert isinstance(resultado, dict)
    assert 'status' in resultado
    assert 'entidades_validas' in resultado
    assert 'erros' in resultado

def test_validar_usuario():
    """Testa a validação de usuário"""
    agente = AgenteValidador()
    
    # Testar usuário válido (simulação)
    assert agente.validar_usuario('João') is True
    
    # Testar usuário inválido
    assert agente.validar_usuario('Usuário Inexistente') is False

def test_converter_data():
    """Testa a conversão de datas"""
    agente = AgenteValidador()
    
    # Testar formatos válidos
    assert isinstance(agente.converter_data('20/06/2025'), datetime)
    assert isinstance(agente.converter_data('2025-06-20'), datetime)
    
    # Testar formato inválido
    with pytest.raises(ValueError):
        agente.converter_data('data inválida')
