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
            StructField("status", BooleanType(), False),
            StructField("fraude", BooleanType(), False),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor", DoubleType(), True),
            StructField("data_pagamento", TimestampType(), True)
        ])
    
    def get_pedidos_schema(self) -> StructType:
        """Define o schema para o dataset de pedidos"""
        return StructType([
            StructField("id_pedido", StringType(), False),
            StructField("estado", StringType(), True),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor_total", DoubleType(), True),
            StructField("data_pedido", TimestampType(), True)
        ])
    
    def read_pagamentos(self, path: str) -> DataFrame:
        """Lê o dataset de pagamentos"""
        try:
            self.logger.info(f"Lendo dataset de pagamentos de: {path}")
            return self.spark.read \
                .option("multiline", "true") \
                .option("mode", "PERMISSIVE") \
                .schema(self.get_pagamentos_schema()) \
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
                .schema(self.get_pedidos_schema()) \
                .csv(path)
        except Exception as e:
            self.logger.error(f"Erro ao ler pedidos: {str(e)}")
            raise
