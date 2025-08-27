from pyspark.sql import SparkSession
from ..config.spark_config import SparkConfig

class SparkSessionManager:
    """Classe para gerenciar a sessão do Spark"""
    
    def __init__(self, config: SparkConfig):
        self.config = config
        self.spark = None
    
    def create_session(self) -> SparkSession:
        """Cria e configura a sessão do Spark"""
        builder = SparkSession.builder \
            .appName(self.config.app_name) \
            .master(self.config.master)
        
        # Aplicar configurações adicionais
        for key, value in self.config.spark_configs.items():
            builder = builder.config(key, value)
        
        self.spark = builder.getOrCreate()
        return self.spark
    
    def stop_session(self):
        """Para a sessão do Spark"""
        if self.spark:
            self.spark.stop()
