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
│   ├── data_io/           # Leitura e escrita de dados
│   ├── business/         # Lógica de negócio
│   ├── orchestration/    # Orquestração do pipeline
│   └── main.py          # Ponto de entrada
├── tests/                # Testes unitários
├── data/                 # Dados de entrada e saída
│   ├── input/            # Dados de entrada
│   │   ├── pagamentos/   # Arquivos JSON de pagamentos
│   │   └── pedidos/      # Arquivos CSV de pedidos
│   └── output/           # Dados de saída
├── venv/                 # Ambiente virtual
├── pyproject.toml        # Configuração do projeto
├── requirements.txt      # Dependências
└── README.md            # Documentação
```

## Pré-requisitos
- Python 3.8+
- PySpark 3.4.0+
- Pandas 1.5.0+
- Java 8+ (recomendado Java 17)

## Instalação
```bash
# 1. Criar o ambiente virtual (primeira vez)
python3 -m venv venv

# 2. Ativar o ambiente virtual
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt
```

## Execução
```bash
# Ativar o ambiente virtual (deve ter sido criado no passo de instalação)
source venv/bin/activate

# Executar o pipeline completo
python3 src/main.py
```

## Testes
```bash
# Ativar o ambiente virtual (deve ter sido criado no passo de instalação)
source venv/bin/activate

# Executar testes unitários
python3 -m pytest tests/test_order_processor.py -v
```

## Configuração
As configurações do Spark podem ser ajustadas em `src/config/spark_config.py`.

### Configurações Spark Ativas
- **Adaptive Query Execution**: Habilitado para otimização automática
- **Partition Coalescing**: Reduz automaticamente o número de partições quando benéfico
- **Skew Join**: Otimiza joins com dados desbalanceados
- **Modo de Execução**: Local com todos os cores disponíveis (`local[*]`)

## Estrutura dos Dados

> **📋 Nota**: Os datasets já estão incluídos no repositório em `data/input/`. Não é necessário baixá-los separadamente.

### Dataset de Pagamentos
- **Formato**: JSON comprimido (*.json.gz)
- **Caminho**: `data/input/pagamentos/`
- **Schema**: 
  - `id_pedido` (string): Identificador do pedido
  - `forma_pagamento` (string): Forma de pagamento utilizada
  - `valor_pagamento` (double): Valor do pagamento
  - `status` (boolean): Status do pagamento (true=aprovado, false=recusado)
  - `data_processamento` (string): Data de processamento do pagamento (formato ISO)
  - `avaliacao_fraude` (object): Objeto contendo:
    - `fraude` (boolean): Indicador de fraude (true=fraudulento, false=legítimo)
    - `score` (double): Score de risco de fraude

### Dataset de Pedidos
- **Formato**: CSV comprimido (*.csv.gz) com separador `;` (ponto e vírgula)
- **Caminho**: `data/input/pedidos/`
- **Schema**:
  - `ID_PEDIDO` (string): Identificador único do pedido
  - `PRODUTO` (string): Nome do produto
  - `VALOR_UNITARIO` (double): Valor unitário do produto
  - `QUANTIDADE` (long): Quantidade do produto
  - `DATA_CRIACAO` (timestamp): Data de criação do pedido (formato ISO: yyyy-MM-ddTHH:mm:ss)
  - `UF` (string): Estado onde foi realizado o pedido (código de 2 letras)
  - `ID_CLIENTE` (long): Identificador do cliente

## Saída
O relatório é gerado em formato Parquet no diretório `data/output/relatorio_pedidos/`:
- **Schema de Saída**:
  - `id_pedido` (string): Identificador do pedido
  - `estado` (string): Estado (UF) onde o pedido foi feito
  - `forma_pagamento` (string): Forma de pagamento
  - `valor_total` (double): Valor total do pedido (VALOR_UNITARIO × QUANTIDADE)
  - `data_pedido` (timestamp): Data do pedido

### Filtros Aplicados
- ✅ Pedidos com pagamentos recusados (`status = false`)
- ✅ Pedidos classificados como legítimos (`avaliacao_fraude.fraude = false`)
- ✅ Apenas pedidos do ano de 2025
- ✅ Ordenação: estado → forma_pagamento → data_pedido

## Status do Projeto

### ✅ Testes Realizados
- **Testes Unitários**: ✅ PASSOU - Todas as funcionalidades da classe `OrderProcessor` testadas (1 teste executado em ~5s)
- **Pipeline Completo**: ✅ PASSOU - Pipeline executado com sucesso nos dados reais 
- **Leitura de Dados**: ✅ PASSOU - Datasets de pagamentos (JSON.gz) e pedidos (CSV.gz) lidos corretamente
- **Estrutura de Dados**: ✅ PASSOU - Schema de entrada e saída validados

### 📊 Resultados da Última Execução
- **Data da Execução**: 30 de Agosto de 2025
- **Filtros aplicados**: Pagamentos recusados (`status=false`) e legítimos (`avaliacao_fraude.fraude=false`) do ano 2025
- **Processamento**: Join entre datasets, cálculo de valor total, ordenação por estado/forma_pagamento/data
- **Arquivo de saída**: `data/output/relatorio_pedidos/part-*.snappy.parquet` (~28KB)
- **Status**: ✅ Pipeline executado com sucesso
- **Formato de saída**: Parquet com compressão Snappy

### 🔧 Arquitetura Implementada
- ✅ **Orientação a Objetos**: Todas as classes implementadas
- ✅ **Injeção de Dependências**: Configurada no `main.py`
- ✅ **Configurações Centralizadas**: `SparkConfig`
- ✅ **Gerenciamento de Sessão**: `SparkSessionManager`
- ✅ **Separação de Responsabilidades**: Reader, Writer, Processor, Orchestrator
- ✅ **Logging**: Configurado em todas as classes
- ✅ **Tratamento de Erros**: Try/catch implementado
- ✅ **Empacotamento**: pyproject.toml, requirements.txt, MANIFEST.in

## Troubleshooting

### ⚠️ Problemas Comuns

1. **Erro de Ambiente Virtual**: 
   ```bash
   # Se o venv não existir ou estiver corrompido, recrie
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Paths ou Diretório de Execução**: 
   - Execute sempre a partir do diretório raiz do projeto (`pyspark-poo-lab/`)
   - Não execute de dentro de subpastas como `src/`

3. **Dependências ou Java**: 
   ```bash
   # Verificar Java (necessário para PySpark)
   java -version
   
   # Reinstalar dependências Python
   pip install -r requirements.txt
   ```

4. **Warnings do Spark**: 
   - Os warnings sobre "native-hadoop library" e "metadata directory" são normais e não afetam o funcionamento
   - O pipeline funciona corretamente mesmo com esses warnings

5. **Dados não encontrados**: 
   - Os datasets estão incluídos no repositório em `data/input/`
   - Verifique se os arquivos `.gz` estão presentes nas pastas `pagamentos/` e `pedidos/`

## Autor
Eduardo Castilho de Almeida Prado - RM: 358966 <br>
Marllon Zucolotto de Almeida - RM: 358117 <br>
Mateus Bonacina Zanguettin - RM: 358472 <br>
Tiago Bento Amado - RM: 359183


## Licença
Este projeto está sob a licença MIT.
