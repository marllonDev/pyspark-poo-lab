from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, year, to_timestamp
from pyspark.sql.types import DoubleType
import logging

class OrderProcessor:
    """Classe de lógica de negócio para processamento de pedidos"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.logger = logging.getLogger(__name__)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def process_orders_report(self, pagamentos_df: DataFrame, pedidos_df: DataFrame) -> DataFrame:
        """Processa os dados para gerar o relatório de pedidos"""
        try:
            self.logger.info("Iniciando processamento do relatório de pedidos")
            
            # 1. Filtrar pagamentos recusados e legítimos
            self.logger.info("Filtrando pagamentos recusados e legítimos")
            pagamentos_filtrados = pagamentos_df.filter(
                (col("status") == False) & (col("avaliacao_fraude.fraude") == False)
            )
            
            # 2. Filtrar pedidos de 2025
            self.logger.info("Filtrando pedidos de 2025")
            pedidos_2025 = pedidos_df.filter(
                year(to_timestamp(col("DATA_CRIACAO"), "yyyy-MM-dd'T'HH:mm:ss")) == 2025
            )
            
            # 3. Calcular valor total do pedido
            self.logger.info("Calculando valor total dos pedidos")
            pedidos_com_valor = pedidos_2025.withColumn(
                "valor_total", 
                col("VALOR_UNITARIO").cast(DoubleType()) * col("QUANTIDADE").cast(DoubleType())
            )
            
            # 4. Fazer join entre pedidos e pagamentos
            self.logger.info("Realizando join entre pedidos e pagamentos")
            relatorio = pedidos_com_valor.join(
                pagamentos_filtrados,
                pedidos_com_valor.ID_PEDIDO == pagamentos_filtrados.id_pedido,
                "inner"
            )
            
            # 5. Selecionar apenas as colunas necessárias
            self.logger.info("Selecionando colunas do relatório")
            relatorio_final = relatorio.select(
                pedidos_com_valor.ID_PEDIDO.alias("id_pedido"),
                pedidos_com_valor.UF.alias("estado"),
                pagamentos_filtrados.forma_pagamento,
                pedidos_com_valor.valor_total,
                to_timestamp(pedidos_com_valor.DATA_CRIACAO, "yyyy-MM-dd'T'HH:mm:ss").alias("data_pedido")
            )
            
            # 6. Ordenar por estado, forma de pagamento e data
            self.logger.info("Ordenando relatório")
            relatorio_ordenado = relatorio_final.orderBy(
                col("estado"),
                col("forma_pagamento"),
                col("data_pedido")
            )
            
            self.logger.info("Processamento concluído com sucesso!")
            return relatorio_ordenado
            
        except Exception as e:
            self.logger.error(f"Erro durante o processamento: {str(e)}")
            raise
