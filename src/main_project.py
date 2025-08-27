from config.spark_config import SparkConfig
from session.spark_session_manager import SparkSessionManager
from orchestration.pipeline_orchestrator import PipelineOrchestrator
import logging

def main():
    """Função principal - Aggregation Root"""
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Iniciando aplicação")
        
        # 1. Criar configuração
        config = SparkConfig()
        
        # 2. Criar e configurar sessão Spark
        session_manager = SparkSessionManager(config)
        spark = session_manager.create_session()
        
        # 3. Criar orquestrador
        orchestrator = PipelineOrchestrator(spark)
        
        # 4. Definir caminhos dos dados
        pagamentos_path = "data/input/pagamentos/*.json.gz"
        pedidos_path = "data/input/pedidos/*.csv.gz"
        output_path = "data/output/relatorio_pedidos"
        
        # 5. Executar pipeline
        orchestrator.execute_pipeline(pagamentos_path, pedidos_path, output_path)
        
        logger.info("Aplicação executada com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro na execução da aplicação: {str(e)}")
        raise
    
    finally:
        # 6. Parar sessão Spark
        if 'session_manager' in locals():
            session_manager.stop_session()

if __name__ == "__main__":
    main()
