import logging
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from datetime import datetime
from config import Config

# Baixar recursos do NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

logger = logging.getLogger(__name__)

class AgentePre:
    def __init__(self):
        """Inicializa o AgentePre com as configurações necessárias."""
        logging.info("Inicializando AgentePre...")
        
        # Carregar modelo spaCy em português
        try:
            self.nlp = spacy.load('pt_core_news_lg')
            
            # Registrar extensão para data de processamento
            spacy.tokens.Doc.set_extension('date', default=datetime.now())
            logging.info("Modelo spaCy carregado com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao carregar modelo spaCy: {str(e)}")
            raise
        
        # Configurar recursos do NLTK
        self.stop_words = set(stopwords.words('portuguese'))
        self.lemmatizer = WordNetLemmatizer()
        
        logger.info("AgentePre inicializado com sucesso!")

    def processar_texto(self, texto: str) -> str:
        """Processa o texto bruto, removendo caracteres especiais e aplicando limpeza."""
        logger.info("Iniciando processamento do texto...")
        
        # 1. Remover caracteres especiais
        texto_limpo = re.sub(r'[^\w\s.,!?@#$%&*()\-_=+]', '', texto)
        
        # 2. Tokenização
        tokens = word_tokenize(texto_limpo, language='portuguese')
        
        # 3. Remover stopwords
        tokens_filtrados = [token for token in tokens if token.lower() not in self.stop_words]
        
        # 4. Lematização
        tokens_lematizados = [self.lemmatizer.lemmatize(token) for token in tokens_filtrados]
        
        # 5. Reconstituir texto
        texto_processado = ' '.join(tokens_lematizados)
        
        logger.info("Processamento do texto concluído!")
        return texto_processado

    def validar_texto(self, texto: str) -> bool:
        """
        Valida se o texto de entrada é válido para processamento.
        
        Args:
            texto (str): Texto de entrada
            
        Returns:
            bool: True se o texto é válido, False caso contrário
        """
        if not texto or not isinstance(texto, str):
            logger.error("Texto inválido: deve ser uma string não vazia")
            return False
            
        if len(texto.strip()) < 10:  # Mínimo de 10 caracteres
            logger.error("Texto muito curto para processamento")
            return False
            
        return True
