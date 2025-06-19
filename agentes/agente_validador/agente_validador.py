import logging
import requests
from datetime import datetime, timedelta
from config import Config

logger = logging.getLogger(__name__)

class AgenteValidador:
    def __init__(self):
        """Inicializa o AgenteValidador"""
        logger.info("Inicializando AgenteValidador...")
        
        # Configurar headers para a API do Monday.com
        self.headers = {
            'Authorization': Config.MONDAY_API_TOKEN,
            'Content-Type': 'application/json'
        }
        
        # Cache de dados do Monday.com
        self.cache = {
            'usuarios': {},
            'projetos': {},
            'quadros': {},
            'colunas': {}
        }
        
        # Regras de negócio
        self.regras_negocio = {
            'datas': {
                'minima': timedelta(days=1),  # Não aceitar datas no passado
                'maxima': timedelta(days=365)  # Não aceitar datas mais de 1 ano no futuro
            },
            'prioridades': ['baixa', 'média', 'alta'],
            'tipos_tarefa': ['tarefa', 'subtarefa', 'milestone']
        }
        
        logger.info("AgenteValidador inicializado com sucesso!")

    def validar_entidades(self, entidades: dict) -> dict:
        """
        Valida as entidades extraídas do texto.
        
        Args:
            entidades (dict): Entidades extraídas pelo AgenteAnalista
            
        Returns:
            dict: Resultado da validação
        """
        logger.info("Validando entidades...")
        
        erros = []
        entidades_validas = {}
        
        # Validar pessoas
        for pessoa in entidades.get('pessoas', []):
            if self.validar_usuario(pessoa):
                entidades_validas.setdefault('pessoas', []).append(pessoa)
            else:
                erros.append(f"Usuário '{pessoa}' não encontrado no Monday.com")
        
        # Validar datas
        for data in entidades.get('datas', []):
            try:
                data_obj = self.converter_data(data)
                if self.validar_data(data_obj):
                    entidades_validas.setdefault('datas', []).append(data)
                else:
                    erros.append(f"Data '{data}' fora do intervalo permitido")
            except ValueError:
                erros.append(f"Formato de data inválido: {data}")
        
        # Validar projetos
        for projeto in entidades.get('projetos', []):
            if self.validar_projeto(projeto):
                entidades_validas.setdefault('projetos', []).append(projeto)
            else:
                erros.append(f"Projeto '{projeto}' não encontrado")
        
        resultado = {
            'status': 'sucesso' if not erros else 'falha',
            'entidades_validas': entidades_validas,
            'erros': erros
        }
        
        logger.info(f"Validação concluída: {resultado['status']}")
        return resultado

    def validar_usuario(self, nome: str) -> bool:
        """Valida se um usuário existe no Monday.com"""
        if nome in self.cache['usuarios']:
            return True
            
        # Consultar API do Monday.com
        query = '''
        query($nome: String!) {
            users(
                limit: 1
                page: 1
                ids: []
                name: $nome
            ) {
                id
                name
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
            if data['data']['users']:
                self.cache['usuarios'][nome] = data['data']['users'][0]
                return True
        
        return False

    def validar_projeto(self, nome: str) -> bool:
        """Valida se um projeto existe no Monday.com"""
        if nome in self.cache['projetos']:
            return True
            
        # Consultar API do Monday.com
        query = '''
        query($nome: String!) {
            boards(
                limit: 1
                page: 1
                ids: []
                name: $nome
            ) {
                id
                name
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
                self.cache['projetos'][nome] = data['data']['boards'][0]
                return True
        
        return False

    def converter_data(self, texto_data: str) -> datetime:
        """Converte texto de data em objeto datetime"""
        # Tenta converter várias formatações comuns
        formatos = [
            '%d/%m/%Y',
            '%d-%m-%Y',
            '%Y-%m-%d',
            '%d/%m/%y',
            '%d-%m-%y'
        ]
        
        for formato in formatos:
            try:
                return datetime.strptime(texto_data, formato)
            except ValueError:
                continue
        
        raise ValueError(f"Formato de data não reconhecido: {texto_data}")

    def validar_data(self, data: datetime) -> bool:
        """Valida se uma data está dentro dos limites permitidos"""
        hoje = datetime.now()
        
        # Não aceitar datas no passado
        if data < hoje:
            return False
            
        # Não aceitar datas mais de 1 ano no futuro
        limite_superior = hoje + self.regras_negocio['datas']['maxima']
        if data > limite_superior:
            return False
            
        return True

    def validar_intencoes(self, intencoes: dict) -> dict:
        """Valida as intenções e entidades extraídas do texto."""
        logger.info("Iniciando validação de intenções...")
        
        # Validar entidades
        entidades = intencoes['entidades_validas']
        
        # Validar pessoas
        pessoas_validas = []
        for pessoa in entidades['pessoas']:
            # Consultar API do Monday.com para verificar se a pessoa existe
            query = '''
                query($name: String!) {
                    users(name: $name) {
                        id
                        name
                        email
                    }
                }
            '''
            response = requests.post(
                Config.MONDAY_API_URL,
                json={'query': query, 'variables': {'name': pessoa}},
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                if data['data']['users']:
                    pessoas_validas.append(data['data']['users'][0]['id'])
                else:
                    logger.warning(f"Pessoa não encontrada: {pessoa}")
            else:
                logger.warning(f"Pessoa não encontrada: {pessoa}")
        
        # Validar projetos
        projetos_validos = []
        for projeto in entidades['projetos']:
            # Consultar API do Monday.com para verificar se o projeto existe
            query = '''
                query($name: String!) {
                    boards(name: $name) {
                        id
                        name
                    }
                }
            '''
            response = requests.post(
                Config.MONDAY_API_URL,
                json={'query': query, 'variables': {'name': projeto}},
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                if data['data']['boards']:
                    projetos_validos.append(data['data']['boards'][0]['id'])
                else:
                    logger.warning(f"Projeto não encontrado: {projeto}")
            else:
                logger.warning(f"Projeto não encontrado: {projeto}")
        
        # Validar datas
        datas_validas = []
        for data in entidades['datas']:
            try:
                # Converter string de data para datetime
                dt = datetime.strptime(data, '%d/%m/%Y')
                datas_validas.append(dt)
            except ValueError:
                logger.warning(f"Data inválida: {data}")
        
        # Verificar regras de negócio
        conflitos = []
        dados_faltando = []
        ambiguidades = []
        
        # Regra 1: Deve haver pelo menos uma pessoa e um projeto
        if not pessoas_validas:
            dados_faltando.append("pessoa responsável")
        if not projetos_validos:
            dados_faltando.append("projeto")
        
        # Regra 2: Data não pode ser anterior à data atual
        if datas_validas and min(datas_validas) < datetime.now():
            conflitos.append("data anterior à data atual")
        
        # Regra 3: Verificar se há ambiguidades nas entidades
        if len(pessoas_validas) > 1:
            ambiguidades.append("múltiplas pessoas responsáveis")
        if len(projetos_validos) > 1:
            ambiguidades.append("múltiplos projetos")
        
        logger.info("Validação de intenções concluída!")
        return {
            'sucesso': True,
            'valido': not (conflitos or dados_faltando or ambiguidades),
            'conflitos': conflitos,
            'dados_faltando': dados_faltando,
            'ambiguidades': ambiguidades,
            'entidades_validas': {
                'pessoas': pessoas_validas,
                'projetos': projetos_validos,
                'datas': datas_validas
            },
            'acao': intencoes['acao'],
            'prioridade': intencoes['prioridade'],
            'texto_processado': intencoes['texto_processado'],
            'metricas': {
                'tempo_validacao': datetime.now() - inicio_validacao,
                'entidades_validadas': len(pessoas_validas) + len(projetos_validos) + len(datas_validas)
            }
        }

    def validar_acoes(self, acoes: list) -> dict:
        """
        Valida as ações identificadas.
        
        Args:
            acoes (list): Lista de ações identificadas pelo AgenteAnalista
            
        Returns:
            dict: Resultado da validação das ações
        """
        logger.info("Validando ações...")
        
        erros = []
        acoes_validas = []
        
        for acao in acoes:
            # Verificar se a ação está nas regras de negócio
            if acao['tipo'] not in self.regras_negocio['tipos_tarefa']:
                erros.append(f"Tipo de ação não suportado: {acao['tipo']}")
                continue
                
            # Verificar confiança mínima
            if acao['confianca'] < 0.7:
                erros.append(f"Ação com confiança baixa: {acao['tipo']}")
                continue
                
            acoes_validas.append(acao)
        
        resultado = {
            'status': 'sucesso' if not erros else 'falha',
            'acoes_validas': acoes_validas,
            'erros': erros
        }
        
        logger.info(f"Validação de ações concluída: {resultado['status']}")
        return resultado
