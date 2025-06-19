import pytest
from agente_executor import AgenteExecutor

def test_executar_mutation_sucesso():
    """Testa execução bem-sucedida de mutation"""
    agente = AgenteExecutor()
    
    payload = {
        'query': '''
        mutation($name: String!) {
            create_item(
                boardId: 123
                item_name: $name
            ) {
                id
                name
            }
        }
        ''',
        'variables': {'name': 'Teste'}
    }
    
    try:
        resultado = agente.executar_mutation(payload)
        assert isinstance(resultado, dict)
        assert 'data' in resultado
    except Exception as e:
        pytest.fail(f"Erro inesperado: {str(e)}")

def test_verificar_limites():
    """Testa verificação de limites"""
    agente = AgenteExecutor()
    
    # Testar com limites não atingidos
    assert agente.verificar_limites() is True
    
    # Testar com limite atingido (simulação)
    agente.limits['complexidade'] = 0
    assert agente.verificar_limites() is False

def test_tratar_erro_api():
    """Testa tratamento de erros da API"""
    agente = AgenteExecutor()
    
    # Testar erro de complexidade
    erro = {'message': 'ComplexityException'}
    mensagem = agente.tratar_erro_api(erro)
    assert "operação é muito complexa" in mensagem.lower()
    
    # Testar erro de limite diário
    erro = {'message': 'DAILY_LIMIT_EXCEEDED'}
    mensagem = agente.tratar_erro_api(erro)
    assert "limite diário" in mensagem.lower()
