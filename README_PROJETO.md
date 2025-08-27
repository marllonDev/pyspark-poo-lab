# Projeto PySpark - Relatório de Pedidos com Pagamentos Recusados

## Descrição
Este projeto PySpark gera um relatório de pedidos de venda com pagamentos recusados e classificados como legítimos, para o ano de 2025.

## Funcionalidades
- Filtra pedidos com pagamentos recusados (`status=false`) e legítimos (`fraude=false`)
- Processa apenas pedidos do ano de 2025
- Ordena por estado, forma de pagamento e data
- Gera relatório em formato Parquet

## Estrutura do Projeto
```
pyspark-poo-lab/
├── src/                    # Código fonte
│   ├── config/            # Configurações
│   ├── session/           # Gerenciamento de sessão Spark
│   ├── io/               # Leitura e escrita de dados
│   ├── business/         # Lógica de negócio
│   ├── orchestration/    # Orquestração do pipeline
│   ├── main_project.py  # Ponto de entrada do projeto
│   └── main.py          # Ponto de entrada original
├── tests/                # Testes unitários
├── data/                 # Dados de entrada e saída
│   ├── input/
│   │   ├── pagamentos/   # Arquivos JSON.gz
│   │   └── pedidos/      # Arquivos CSV.gz
│   └── output/           # Relatório Parquet gerado
├── pyproject.toml        # Configuração do projeto
├── requirements.txt      # Dependências
├── MANIFEST.in          # Manifesto para distribuição
├── test_project_structure.py  # Script de validação
└── README_PROJETO.md    # Este arquivo
```

## Pré-requisitos
- Python 3.8+
- PySpark 3.4+
- Java 8+

## Instalação
```bash
pip install -r requirements.txt
```

## Obtenção dos Datasets

### 1. Dataset de Pagamentos
```bash
# Clonar repositório de pagamentos
git clone https://github.com/infobarbosa/dataset-json-pagamentos.git
# Copiar dados para a estrutura do projeto
cp -r dataset-json-pagamentos/data/pagamentos/* data/input/pagamentos/
```

### 2. Dataset de Pedidos
```bash
# Clonar repositório de pedidos
git clone https://github.com/infobarbosa/datasets-csv-pedidos.git
# Copiar dados para a estrutura do projeto
cp -r datasets-csv-pedidos/data/pedidos/* data/input/pedidos/
```

## Execução

### 1. Validação do Projeto
```bash
python test_project_structure.py
```

### 2. Execução dos Testes
```bash
pytest tests/ -v
```

### 3. Execução do Pipeline
```bash
python src/main_project.py
```

## Configuração
As configurações do Spark podem ser ajustadas em `src/config/spark_config.py`.

## Estrutura dos Dados

### Dataset de Pagamentos
- Formato: JSON
- Caminho: `data/input/pagamentos/`
- Schema: id_pedido, status, fraude, forma_pagamento, valor, data_pagamento

### Dataset de Pedidos
- Formato: CSV
- Caminho: `data/input/pedidos/`
- Schema: id_pedido, estado, forma_pagamento, valor_total, data_pedido

## Saída
O relatório é gerado em formato Parquet no diretório `data/output/relatorio_pedidos/`.

## Critérios Implementados

### ✅ Todos os 12 Critérios Específicos Atendidos:
1. **Schemas explícitos** - Definidos em `DataReader`
2. **Orientação a objetos** - Todas as classes implementadas
3. **Injeção de Dependências** - Implementada no `main_project.py`
4. **Configurações centralizadas** - Classe `SparkConfig`
5. **Sessão Spark gerenciada** - Classe `SparkSessionManager`
6. **Leitura e escrita de dados** - Classes `DataReader` e `DataWriter`
7. **Lógica de negócio** - Classe `OrderProcessor`
8. **Orquestração do pipeline** - Classe `PipelineOrchestrator`
9. **Logging configurado** - Implementado em todas as classes
10. **Tratamento de erros** - Try/catch em todas as operações
11. **Empacotamento da aplicação** - pyproject.toml, requirements.txt, MANIFEST.in
12. **Testes unitários** - Implementados para `OrderProcessor`

## Autor
Tiago - RM: [Seu RM]

## Licença
Este projeto está sob a licença MIT.
