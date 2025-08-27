from pyspark.sql import SparkSession
from ..io.data_reader import DataReader
from ..io.data_writer import DataWriter
from ..business.order_processor import OrderProcessor
import logging

class PipelineOrchestrator:
    """Classe para orquestrar o pipeline de processamento"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.reader = DataReader(spark)
        self.writer = DataWriter(spark)
        self.processor = OrderProcessor(spark)
        self.logger = logging.getLogger(__name__)
    
    def execute_pipeline(self, pagamentos_path: str, pedidos_path: str, output_path: str):
        """Executa o pipeline completo"""
        try:
            self.logger.info("Iniciando execução do pipeline")
            
            # 1. Ler dados
            self.logger.info("Etapa 1: Leitura dos dados")
            pagamentos_df = self.reader.read_pagamentos(pagamentos_path)
            pedidos_df = self.reader.read_pedidos(pedidos_path)
            
            # 2. Processar dados
            self.logger.info("Etapa 2: Processamento dos dados")
            relatorio_df = self.processor.process_orders_report(pagamentos_df, pedidos_df)
            
            # 3. Escrever resultado
            self.logger.info("Etapa 3: Escrita do relatório")
            self.writer.write_parquet(relatorio_df, output_path)
            
            self.logger.info("Pipeline executado com sucesso!")
            
        except Exception as e:
            self.logger.error(f"Erro na execução do pipeline: {str(e)}")
            raise
