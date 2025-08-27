#!/usr/bin/env python3
"""
Script para validar a estrutura do projeto PySpark
"""

import os
import sys
from pathlib import Path

def check_project_structure():
    """Verifica se a estrutura do projeto está correta"""
    
    print("🔍 Validando estrutura do projeto PySpark...")
    
    # Estrutura esperada
    expected_structure = {
        "src": {
            "config": ["__init__.py", "spark_config.py"],
            "session": ["__init__.py", "spark_session_manager.py"],
            "io": ["__init__.py", "data_reader.py", "data_writer.py"],
            "business": ["__init__.py", "order_processor.py"],
            "orchestration": ["__init__.py", "pipeline_orchestrator.py"],
            "__init__.py": None,
            "main_project.py": None
        },
        "tests": {
            "__init__.py": None,
            "test_order_processor.py": None
        },
        "data": {
            "input": {
                "pagamentos": None,
                "pedidos": None
            },
            "output": None
        },
        "pyproject.toml": None,
        "requirements.txt": None,
        "MANIFEST.in": None
    }
    
    def check_directory(base_path, structure, level=0):
        """Verifica recursivamente a estrutura de diretórios"""
        indent = "  " * level
        
        for item, sub_structure in structure.items():
            item_path = base_path / item
            
            if not item_path.exists():
                print(f"❌ {indent}Arquivo/Diretório não encontrado: {item}")
                return False
            
            if sub_structure is None:
                # É um arquivo
                print(f"✅ {indent}Arquivo: {item}")
            else:
                # É um diretório
                print(f"📁 {indent}Diretório: {item}")
                if not check_directory(item_path, sub_structure, level + 1):
                    return False
                
                # Verificar se os arquivos esperados estão no diretório
                for expected_file in sub_structure:
                    file_path = item_path / expected_file
                    if not file_path.exists():
                        print(f"❌ {indent}  Arquivo não encontrado: {expected_file}")
                        return False
                    print(f"✅ {indent}  Arquivo: {expected_file}")
        
        return True
    
    # Verificar estrutura
    base_path = Path(".")
    if check_directory(base_path, expected_structure):
        print("\n🎉 Estrutura do projeto está correta!")
        return True
    else:
        print("\n❌ Estrutura do projeto tem problemas!")
        return False

def check_data_files():
    """Verifica se os arquivos de dados estão presentes"""
    
    print("\n📊 Verificando arquivos de dados...")
    
    # Verificar pagamentos
    pagamentos_path = Path("data/input/pagamentos")
    if pagamentos_path.exists():
        pagamentos_files = list(pagamentos_path.glob("*.json.gz"))
        print(f"✅ Arquivos de pagamentos encontrados: {len(pagamentos_files)}")
        
        # Verificar se há dados de 2025
        pagamentos_2025 = [f for f in pagamentos_files if "2025" in f.name]
        print(f"✅ Arquivos de pagamentos 2025: {len(pagamentos_2025)}")
    else:
        print("❌ Diretório de pagamentos não encontrado")
        return False
    
    # Verificar pedidos
    pedidos_path = Path("data/input/pedidos")
    if pedidos_path.exists():
        pedidos_files = list(pedidos_path.glob("*.csv.gz"))
        print(f"✅ Arquivos de pedidos encontrados: {len(pedidos_files)}")
        
        # Verificar se há dados de 2025
        pedidos_2025 = [f for f in pedidos_files if "2025" in f.name]
        print(f"✅ Arquivos de pedidos 2025: {len(pedidos_2025)}")
    else:
        print("❌ Diretório de pedidos não encontrado")
        return False
    
    return True

def main():
    """Função principal"""
    
    print("=" * 60)
    print("🚀 VALIDAÇÃO DO PROJETO PYSPARK")
    print("=" * 60)
    
    # Verificar estrutura
    structure_ok = check_project_structure()
    
    # Verificar dados
    data_ok = check_data_files()
    
    print("\n" + "=" * 60)
    if structure_ok and data_ok:
        print("🎉 PROJETO PRONTO PARA EXECUÇÃO!")
        print("\n📋 Próximos passos:")
        print("1. Instalar dependências: pip install -r requirements.txt")
        print("2. Executar testes: pytest tests/")
        print("3. Executar pipeline: python src/main_project.py")
    else:
        print("❌ PROJETO TEM PROBLEMAS!")
        print("Verifique os erros acima e corrija antes de continuar.")
    print("=" * 60)

if __name__ == "__main__":
    main()
