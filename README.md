# Sistema Multiagentes para Monday.com

Este sistema é composto por 6 agentes especializados que trabalham em conjunto para processar transcrições de texto e automatizar a gestão de tarefas no Monday.com.

## Agentes do Sistema

1. **AgentePre (Transcritor & Limpador)**
   - Limpeza e pré-processamento de texto
   - Correção de erros ortográficos
   - Padronização do formato

2. **AgenteAnalista (Interpretador de Intenções)**
   - Análise semântica
   - Extração de entidades
   - Identificação de ações
   - Estruturação de dados

3. **AgenteValidador (Verificador de Integridade)**
   - Validação cruzada de dados
   - Resolução de ambiguidades
   - Detecção de conflitos
   - Sinalização para intervenção humana

4. **AgenteMapeaMonday (Tradutor de API)**
   - Mapeamento de entidades para o Monday.com
   - Construção de payloads GraphQL
   - Aplicação de regras de negócio

5. **AgenteExecutor (Executor de API)**
   - Integração com a API do Monday.com
   - Gerenciamento de autenticação
   - Tratamento de erros e limites
   - Logging de operações

6. **AgenteBoss (Otimizador de Aprendizagem)**
   - Supervisão do sistema
   - Coleta de feedback
   - Análise de desempenho
   - Otimização contínua

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
