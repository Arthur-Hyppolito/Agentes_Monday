import pytest
from agente_mapeamap import AgenteMapeaMap

def test_mapear_entidades_para_column_values():
    """Testa o mapeamento de entidades para column_values"""
    agente = AgenteMapeaMap()
    
    entidades = {
        'pessoas': ['João'],
        'datas': ['2025-06-20'],
        'prioridade': ['alta']
    }
    
    column_values = agente.mapear_entidades_para_column_values(entidades, 'Marketing')
    
    assert isinstance(column_values, dict)
    assert 'person' in column_values
    assert 'date' in column_values
    assert 'priority' in column_values

def test_mapear_pessoas():
    """Testa o mapeamento de pessoas"""
    agente = AgenteMapeaMap()
    
    pessoas = ['João', 'Maria']
    resultado = agente.mapear_pessoas(pessoas)
    
    assert isinstance(resultado, dict)
    assert 'personsAndTeams' in resultado

def test_mapear_data():
    """Testa o mapeamento de data"""
    agente = AgenteMapeaMap()
    
    texto_data = '2025-06-20'
    resultado = agente.mapear_data(texto_data)
    
    assert isinstance(resultado, dict)
    assert 'date' in resultado
    assert 'time' in resultado
