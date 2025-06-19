# Sistema Multiagentes para Monday.com

Este sistema é composto por 6 agentes especializados que trabalham em conjunto para processar transcrições de texto e automatizar a gestão de tarefas no Monday.com.

## Funcionalidades Principais

- **Criação automática de projetos e pessoas no Monday.com**: O sistema detecta nomes de projetos e usuários inexistentes e os cria automaticamente via API, tornando o fluxo totalmente automatizado a partir de comandos ou transcrições.
- **Processamento de transcrições e comandos em linguagem natural**: Extração de tarefas, responsáveis, datas, prioridades e projetos a partir de texto livre.
- **Validação, resolução de ambiguidades e aplicação de regras de negócio**: Garante integridade dos dados antes de executar ações.
- **Integração multiagente modular**: Cada etapa (pré-processamento, análise, validação, mapeamento, execução e monitoramento) é realizada por um agente especializado, facilitando manutenção e evolução.
- **Fluxo end-to-end**: Desde a entrada de texto/transcrição até a criação de itens, projetos e usuários no Monday.com, sem intervenção manual.
- **Logging detalhado e métricas de desempenho**: Todas as operações são registradas e analisadas para melhoria contínua.

## Exemplo de Uso

1. Usuário fornece um texto/transcrição, como:
   > "João Silva precisa criar uma tarefa para o projeto XPTO até 30/06/2025."
2. O sistema identifica entidades, valida, cria projetos/pessoas se necessário e executa a ação no Monday.com.
3. Resultado e métricas são exibidos ao final do processamento.

## Arquitetura dos Agentes

1. **AgentePre (Transcritor & Limpador)**
   - Limpeza e pré-processamento de texto
2. **AgenteAnalista (Interpretador de Intenções)**
   - Extração de entidades e ações
3. **AgenteValidador (Verificador de Integridade)**
   - Validação cruzada e sinalização de entidades a criar
4. **AgenteMapeaMonday (Tradutor de API)**
   - Mapeamento para payloads GraphQL
5. **AgenteExecutor (Executor de API)**
   - Criação automática de projetos/pessoas e execução de mutations
6. **AgenteBoss (Otimizador de Aprendizagem)**
   - Supervisão e análise de desempenho

## Requisitos

- Python 3.8+
- Bibliotecas listadas em requirements.txt
- Token de API do Monday.com
- Servidor MCP configurado

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente no arquivo .env
4. Execute o sistema:
   ```bash
   python main.py
   ```

## Estrutura do Projeto

```
agentes_monday/
├── agentes/
│   ├── agente_pre/
│   ├── agente_analista/
│   ├── agente_validador/
│   ├── agente_mapeamap/
│   ├── agente_executor/
│   └── agente_boss/
├── config.py
├── requirements.txt
└── README.md
```
