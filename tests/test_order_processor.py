import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
from pyspark.sql.functions import col
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from business.order_processor import OrderProcessor
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
            StructField("forma_pagamento", StringType(), True),
            StructField("valor_pagamento", DoubleType(), True),
            StructField("status", BooleanType(), False),
            StructField("data_processamento", TimestampType(), True),
            StructField("avaliacao_fraude", StructType([
                StructField("fraude", BooleanType(), False),
                StructField("score", DoubleType(), True)
            ]), True)
        ])
        
        data = [
            ("PED001", "CARTAO_CREDITO", 100.0, False, datetime(2025, 1, 1), {"fraude": False, "score": 0.10}),
            ("PED002", "PIX", 200.0, True, datetime(2025, 1, 2), {"fraude": False, "score": 0.20}),
            ("PED003", "BOLETO", 150.0, False, datetime(2025, 1, 3), {"fraude": True, "score": 0.90})
        ]
        
        return spark.createDataFrame(data, schema)
    
    @pytest.fixture(scope="class")
    def sample_pedidos_data(self, spark):
        """Fixture para criar dados de teste de pedidos"""
        schema = StructType([
            StructField("ID_PEDIDO", StringType(), False),
            StructField("PRODUTO", StringType(), True),
            StructField("VALOR_UNITARIO", DoubleType(), True),
            StructField("QUANTIDADE", DoubleType(), True),
            StructField("DATA_CRIACAO", TimestampType(), True),
            StructField("UF", StringType(), True),
            StructField("ID_CLIENTE", StringType(), True)
        ])
        
        data = [
            ("PED001", "NOTEBOOK", 100.0, 1.0, datetime(2025, 1, 1), "SP", "CLI001"),
            ("PED002", "MOUSE", 50.0, 2.0, datetime(2025, 1, 2), "RJ", "CLI002"),
            ("PED003", "TECLADO", 75.0, 2.0, datetime(2025, 1, 3), "MG", "CLI003")
        ]
        
        return spark.createDataFrame(data, schema)
    
    def test_process_orders_report(self, processor, sample_pagamentos_data, sample_pedidos_data):
        """Testa o processamento do relatório de pedidos"""
        # Executar processamento
        result = processor.process_orders_report(sample_pagamentos_data, sample_pedidos_data)
        
        # Verificar se o resultado não está vazio
        assert result.count() > 0
        
        # Verificar se contém apenas pedidos com status=False e fraude=False
        # Apenas PED001 deve aparecer no resultado (status=False AND fraude=False)
        assert result.count() == 1
        
        # Verificar se as colunas estão presentes
        expected_columns = ["id_pedido", "estado", "forma_pagamento", "valor_total", "data_pedido"]
        actual_columns = result.columns
        
        for col_name in expected_columns:
            assert col_name in actual_columns
        
        # Verificar o conteúdo específico
        row = result.collect()[0]
        assert row["id_pedido"] == "PED001"
        assert row["estado"] == "SP"
        assert row["forma_pagamento"] == "CARTAO_CREDITO"
        assert row["valor_total"] == 100.0
