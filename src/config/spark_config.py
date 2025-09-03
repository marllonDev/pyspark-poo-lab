from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SparkConfig:
    """Classe de configuração para o Spark"""
    
    app_name: str = "RelatorioPedidos"
    master: str = "local[*]"
    spark_configs: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.spark_configs is None:
            self.spark_configs = {
                "spark.sql.adaptive.enabled": "true",
                "spark.sql.adaptive.coalescePartitions.enabled": "true",
                "spark.sql.adaptive.skewJoin.enabled": "true"
            }
