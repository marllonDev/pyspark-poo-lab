import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
from pyspark.sql.functions import col
from src.business.order_processor import OrderProcessor
from datetime import datetime

class TestOrderProcessor:
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Fixture para criar sessão Spark para testes"""
        return SparkSession.builder \
            .appName("TestOrderProcessor") \
            .master("local[1]") \
            .getOrCreate()
    
    @pytest.fixture(scope="class")
    def processor(self, spark):
        """Fixture para criar instância do OrderProcessor"""
        return OrderProcessor(spark)
    
    @pytest.fixture(scope="class")
    def sample_pagamentos_data(self, spark):
        """Fixture para criar dados de teste de pagamentos"""
        schema = StructType([
            StructField("id_pedido", StringType(), False),
            StructField("status", BooleanType(), False),
            StructField("fraude", BooleanType(), False),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor", DoubleType(), True),
            StructField("data_pagamento", TimestampType(), True)
        ])
        
        data = [
            ("PED001", False, False, "cartao", 100.0, datetime(2025, 1, 1)),
            ("PED002", True, False, "pix", 200.0, datetime(2025, 1, 2)),
            ("PED003", False, True, "boleto", 150.0, datetime(2025, 1, 3))
        ]
        
        return spark.createDataFrame(data, schema)
    
    @pytest.fixture(scope="class")
    def sample_pedidos_data(self, spark):
        """Fixture para criar dados de teste de pedidos"""
        schema = StructType([
            StructField("id_pedido", StringType(), False),
            StructField("estado", StringType(), True),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor_total", DoubleType(), True),
            StructField("data_pedido", TimestampType(), True)
        ])
        
        data = [
            ("PED001", "SP", "cartao", 100.0, datetime(2025, 1, 1)),
            ("PED002", "RJ", "pix", 200.0, datetime(2025, 1, 2)),
            ("PED003", "MG", "boleto", 150.0, datetime(2025, 1, 3))
        ]
        
        return spark.createDataFrame(data, schema)
    
    def test_process_orders_report(self, processor, sample_pagamentos_data, sample_pedidos_data):
        """Testa o processamento do relatório de pedidos"""
        # Executar processamento
        result = processor.process_orders_report(sample_pagamentos_data, sample_pedidos_data)
        
        # Verificar se o resultado não está vazio
        assert result.count() > 0
        
        # Verificar se contém apenas pedidos com status=False e fraude=False
        filtered_result = result.join(
            sample_pagamentos_data.filter((col("status") == False) & (col("fraude") == False)),
            "id_pedido"
        )
        
        assert result.count() == filtered_result.count()
        
        # Verificar se as colunas estão presentes
        expected_columns = ["id_pedido", "estado", "forma_pagamento", "valor_total", "data_pedido"]
        actual_columns = result.columns
        
        for col_name in expected_columns:
            assert col_name in actual_columns
