import logging
import spacy
from transformers import pipeline
from config import Config

logger = logging.getLogger(__name__)

class AgenteAnalista:
    def __init__(self):
        """Inicializa o AgenteAnalista com os modelos necessários"""
        logger.info("Inicializando AgenteAnalista...")
        
        # Carregar modelo do spaCy para português
        try:
            self.nlp = spacy.load(Config.NLP_MODEL)
        except OSError:
            logger.error(f"Modelo do spaCy não encontrado: {Config.NLP_MODEL}")
            raise
        
        # Carregar modelo de classificação de intenções
        self.classificador = pipeline(
            'text-classification',
            model='neuralmind/bert-base-portuguese-cased',
            tokenizer='neuralmind/bert-base-portuguese-cased'
        )
        
        # Definir entidades e ações conhecidas
        self.entidades_conhecidas = {
            'responsaveis': set(),  # Será preenchido pelo AgenteValidador
            'projetos': set(),
            'quadros': set(),
            'colunas': set()
        }
        
        logger.info("AgenteAnalista inicializado com sucesso!")

    def extrair_entidades(self, texto: str) -> dict:
        """
        Extrai entidades do texto usando spaCy e classificação.
        
        Args:
            texto (str): Texto processado pelo AgentePre
            
        Returns:
            dict: Entidades extraídas
        """
        logger.info("Extraindo entidades do texto...")
        
        # Processar texto com spaCy
        doc = self.nlp(texto)
        
        # Extrair entidades nomeadas
        entidades = {
            'pessoas': [],
            'datas': [],
            'projetos': [],
            'quadros': [],
            'colunas': []
        }
        
        for ent in doc.ents:
            if ent.label_ in ['PER']:  # Pessoas
                entidades['pessoas'].append(ent.text)
            elif ent.label_ in ['DATE', 'TIME']:  # Datas
                entidades['datas'].append(ent.text)
            
        # Extrair entidades específicas do Monday.com
        for token in doc:
            if token.text.lower() in self.entidades_conhecidas['projetos']:
                entidades['projetos'].append(token.text)
            elif token.text.lower() in self.entidades_conhecidas['quadros']:
                entidades['quadros'].append(token.text)
            elif token.text.lower() in self.entidades_conhecidas['colunas']:
                entidades['colunas'].append(token.text)
        
        logger.info("Entidades extraídas com sucesso!")
        return entidades

    def identificar_acoes(self, texto: str) -> list:
        """
        Identifica ações no texto usando classificação de intenções.
        
        Args:
            texto (str): Texto processado
            
        Returns:
            list: Lista de ações identificadas
        """
        logger.info("Identificando ações no texto...")
        
        # Classificar intenções
        resultado = self.classificador(texto)
        
        # Mapear resultados para ações específicas
        acoes = []
        for pred in resultado:
            if pred['score'] > 0.7:  # Limiar de confiança
                acao = {
                    'tipo': pred['label'],
                    'confianca': pred['score']
                }
                acoes.append(acao)
        
        logger.info("Ações identificadas com sucesso!")
        return acoes

    def analisar_intencoes(self, texto_processado):
        """Analisa o texto processado para identificar intenções e ações."""
        logger.info("Analisando intenções do texto...")
        
        # Extração de entidades com spaCy
        doc = self.nlp(texto_processado)
        entidades = {
            'pessoas': [ent.text for ent in doc.ents if ent.label_ == 'PER'],
            'datas': [ent.text for ent in doc.ents if ent.label_ == 'DATE'],
            'projetos': [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        }
        
        # Identificação de ações com BERT
        logger.info("Identificando ações no texto...")
        inputs = self.tokenizer(
            texto_processado,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Obter a predição
        predicoes = torch.argmax(outputs.logits, dim=-1).item()
        
        # Mapear para ações
        acoes = [
            "criar_tarefa",
            "atualizar_tarefa",
            "mover_tarefa",
            "comentar_tarefa"
        ]
        
        # Análise de prioridade
        prioridades = {
            'alta': ['urgente', 'imediato', 'prioridade alta'],
            'media': ['importante', 'necessário', 'prioridade média'],
            'baixa': ['pode esperar', 'não urgente', 'prioridade baixa']
        }
        
        prioridade = 'media'
        for nivel, palavras in prioridades.items():
            if any(palavra in texto_processado.lower() for palavra in palavras):
                prioridade = nivel
                break
        
        logger.info("Ações identificadas com sucesso!")
        logger.info("Análise de intenções concluída!")
        
        return {
            'entidades_validas': entidades,
            'acao': acoes[predicoes],
            'prioridade': prioridade,
            'texto_processado': texto_processado
        }
