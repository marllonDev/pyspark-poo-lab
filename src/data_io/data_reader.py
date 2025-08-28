from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
import logging

class DataReader:
    """Classe para leitura de dados"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.logger = logging.getLogger(__name__)
    
    def get_pagamentos_schema(self) -> StructType:
        """Define o schema para o dataset de pagamentos"""
        return StructType([
            StructField("id_pedido", StringType(), False),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor_pagamento", DoubleType(), True),
            StructField("status", BooleanType(), False),
            StructField("data_processamento", StringType(), True),
            StructField("avaliacao_fraude", StructType([
                StructField("fraude", BooleanType(), False),
                StructField("score", DoubleType(), True)
            ]), True)
        ])
    
    def get_pedidos_schema(self) -> StructType:
        """Define o schema para o dataset de pedidos"""
        return StructType([
            StructField("ID_PEDIDO", StringType(), False),
            StructField("PRODUTO", StringType(), True),
            StructField("VALOR_UNITARIO", StringType(), True),
            StructField("QUANTIDADE", StringType(), True),
            StructField("DATA_CRIACAO", StringType(), True),
            StructField("UF", StringType(), True),
            StructField("ID_CLIENTE", StringType(), True)
        ])
    
    def read_pagamentos(self, path: str) -> DataFrame:
        """Lê o dataset de pagamentos"""
        try:
            self.logger.info(f"Lendo dataset de pagamentos de: {path}")
            return self.spark.read \
                .option("compression", "gzip") \
                .json(path)
        except Exception as e:
            self.logger.error(f"Erro ao ler pagamentos: {str(e)}")
            raise
    
    def read_pedidos(self, path: str) -> DataFrame:
        """Lê o dataset de pedidos"""
        try:
            self.logger.info(f"Lendo dataset de pedidos de: {path}")
            return self.spark.read \
                .option("header", "true") \
                .option("inferSchema", "false") \
                .option("compression", "gzip") \
                .option("sep", ";") \
                .csv(path)
        except Exception as e:
            self.logger.error(f"Erro ao ler pedidos: {str(e)}")
            raise
