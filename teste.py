from main import SistemaMultiagentes

# Criar instância do sistema
sistema = SistemaMultiagentes()

# Texto de exemplo
texto = """
Precisamos criar uma tarefa para o projeto Marketing.
A tarefa é desenvolver um novo design para o site.
Responsável: João Silva.
Data de entrega: sexta-feira.
Prioridade: alta.
"""

# Processar o texto
resultado = sistema.processar_transcricao(texto)

# Mostrar resultados
print("\nResultados:")
print(f"Entidades extraídas: {resultado['entidades']}")
print(f"Ações identificadas: {resultado['acoes']}")
print(f"Métricas: {resultado['metricas']}")
