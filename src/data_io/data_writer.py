from pyspark.sql import SparkSession, DataFrame
import logging

class DataWriter:
    """Classe para escrita de dados"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.logger = logging.getLogger(__name__)
    
    def write_parquet(self, df: DataFrame, path: str, mode: str = "overwrite"):
        """Escreve DataFrame em formato Parquet"""
        try:
            self.logger.info(f"Escrevendo relatório em: {path}")
            df.write \
                .mode(mode) \
                .parquet(path)
            self.logger.info("Relatório salvo com sucesso!")
        except Exception as e:
            self.logger.error(f"Erro ao escrever relatório: {str(e)}")
            raise
