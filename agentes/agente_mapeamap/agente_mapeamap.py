import logging
import requests
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class AgenteMapeaMap:
    def __init__(self):
        """Inicializa o AgenteMapeaMap"""
        logger.info("Inicializando AgenteMapeaMap...")
        
        # Configurar headers para a API do Monday.com
        self.headers = {
            'Authorization': Config.MONDAY_API_TOKEN,
            'Content-Type': 'application/json'
        }
        
        # Mapeamento de tipos de colunas
        self.mapeamento_colunas = {
            'texto': 'text_column',
            'pessoa': 'person_column',
            'data': 'date_column',
            'status': 'status_column',
            'prioridade': 'priority_column',
            'numero': 'numbers_column',
            'checklist': 'check_column'
        }
        
        # Cache de metadados dos quadros
        self.cache_quadros = {}
        
        logger.info("AgenteMapeaMap inicializado com sucesso!")

    def mapear_entidades_para_column_values(self, entidades: dict, projeto: str) -> dict:
        """
        Mapeia as entidades para os valores das colunas do Monday.com.
        
        Args:
            entidades (dict): Entidades validadas pelo AgenteValidador
            projeto (str): Nome do projeto
            
        Returns:
            dict: Column values formatados para a API do Monday.com
        """
        logger.info("Mapeando entidades para column_values...")
        
        column_values = {}
        
        # Obter metadados do quadro
        board_id = self.obter_id_quadro(projeto)
        if not board_id:
            logger.error(f"Quadro não encontrado: {projeto}")
            return {}
            
        # Obter metadados das colunas
        colunas = self.obter_metadados_colunas(board_id)
        
        # Mapear cada tipo de entidade
        for tipo, valores in entidades.items():
            if tipo == 'pessoas':
                column_values['person'] = self.mapear_pessoas(valores)
            elif tipo == 'datas':
                column_values['date'] = self.mapear_data(valores[0]) if valores else None
            elif tipo == 'prioridade':
                column_values['priority'] = self.mapear_prioridade(valores[0]) if valores else None
            
        logger.info("Mapeamento de entidades concluído!")
        return column_values

    def mapear_pessoas(self, pessoas: list) -> dict:
        """Mapeia nomes de pessoas para IDs do Monday.com"""
        usuarios = self.obter_usuarios()
        ids = []
        
        for pessoa in pessoas:
            for usuario in usuarios:
                if usuario['name'].lower() == pessoa.lower():
                    ids.append(usuario['id'])
                    break
        
        return {'personsAndTeams': ids}

    def mapear_data(self, texto_data: str) -> dict:
        """Converte texto de data para formato do Monday.com"""
        try:
            data = datetime.strptime(texto_data, '%Y-%m-%d')
            return {
                'date': data.strftime('%Y-%m-%d'),
                'time': 'all_day'
            }
        except ValueError:
            logger.error(f"Formato de data inválido: {texto_data}")
            return None

    def mapear_prioridade(self, prioridade: str) -> dict:
        """Mapeia prioridade para formato do Monday.com"""
        mapeamento = {
            'alta': 'red',
            'média': 'yellow',
            'baixa': 'green'
        }
        
        return {
            'label': mapeamento.get(prioridade.lower(), 'green')
        }

    def obter_id_quadro(self, nome: str) -> int:
        """Obtém o ID do quadro pelo nome"""
        if nome in self.cache_quadros:
            return self.cache_quadros[nome]
            
        query = '''
        query($nome: String!) {
            boards(
                limit: 1
                page: 1
                ids: []
                name: $nome
            ) {
                id
            }
        }
        '''
        
        variables = {'nome': nome}
        response = requests.post(
            Config.MONDAY_API_URL,
            json={'query': query, 'variables': variables},
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['data']['boards']:
                id_quadro = data['data']['boards'][0]['id']
                self.cache_quadros[nome] = id_quadro
                return id_quadro
        
        return None

    def obter_metadados_colunas(self, board_id: int) -> dict:
        """Obtém os metadados das colunas do quadro"""
        query = '''
        query($boardId: Int!) {
            boards(ids: [$boardId]) {
                columns {
                    id
                    title
                    type
                }
            }
        }
        '''
        
        variables = {'boardId': board_id}
        response = requests.post(
            Config.MONDAY_API_URL,
            json={'query': query, 'variables': variables},
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['data']['boards'][0]['columns']
        
        return {}

    def obter_usuarios(self) -> list:
        """Obtém a lista de usuários do workspace"""
        query = '''
        query {
            users {
                id
                name
                email
            }
        }
        '''
        
        response = requests.post(
            Config.MONDAY_API_URL,
            json={'query': query},
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['data']['users']
        
        return []

    def criar_payload_mutation(self, intencoes: dict) -> dict:
        """
        Cria o payload completo para a mutation do Monday.com.
        
        Args:
            intencoes (dict): Intenções validadas e mapeadas
            
        Returns:
            dict: Payload completo para a API do Monday.com
        """
        logger.info("Criando payload para mutation...")
        
        # Obter ID do quadro
        projeto = intencoes['entidades_validas'].get('projetos', [''])[0]
        board_id = self.obter_id_quadro(projeto)
        
        # Preparar column values
        column_values = self.mapear_entidades_para_column_values(
            intencoes['entidades_validas'],
            projeto
        )
        
        # Construir mutation
        mutation = '''
        mutation($boardId: Int!, $name: String!, $columnValues: JSON!) {
            create_item(
                boardId: $boardId
                item_name: $name
                column_values: $columnValues
            ) {
                id
                name
                column_values {
                    id
                    title
                    text
                }
            }
        }
        '''
        
        # Preparar variáveis
        variables = {
            'boardId': board_id,
            'name': intencoes['objetivo'],
            'columnValues': column_values
        }
        
        logger.info("Payload criado com sucesso!")
        return {
            'query': mutation,
            'variables': variables
        }
