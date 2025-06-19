from main import SistemaMultiagentes

# Inicializar sistema
sistema = SistemaMultiagentes()

# Texto de exemplo
texto = """
João Silva precisa criar uma tarefa para o projeto XPTO até 30/06/2025.
A tarefa é de alta prioridade e deve ser concluída até 30/06/2025.
"""

# Processar texto
resultado = sistema.processar_transcricao(texto)

# Mostrar resultados
print(f"\nResultados:")
print(f"Entidades válidas: {resultado['entidades_validas']}")
print(f"Ação: {resultado['acao']}")
print(f"Prioridade: {resultado['prioridade']}")
print(f"Métricas: {resultado['metricas']}")
