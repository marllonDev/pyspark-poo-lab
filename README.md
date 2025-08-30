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
- PySpark 3.4+
- Java 17

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
  - `data_processamento` (string): Data de processamento do pagamento
  - `avaliacao_fraude` (object): Objeto contendo:
    - `fraude` (boolean): Indicador de fraude (true=fraudulento, false=legítimo)
    - `score` (double): Score de risco de fraude

### Dataset de Pedidos
- **Formato**: CSV comprimido (*.csv.gz)
- **Caminho**: `data/input/pedidos/`
- **Schema**:
  - `ID_PEDIDO` (string): Identificador único do pedido (UUID format)
  - `PRODUTO` (string): Nome do produto
  - `VALOR_UNITARIO` (double): Valor unitário do produto
  - `QUANTIDADE` (long): Quantidade do produto
  - `DATA_CRIACAO` (timestamp): Data de criação do pedido (ISO format: yyyy-MM-ddTHH:mm:ss)
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
- **Testes Unitários**: ✅ PASSOU - Todas as funcionalidades da classe `OrderProcessor` testadas
- **Pipeline Completo**: ✅ PASSOU - Pipeline executado com sucesso nos dados reais
- **Verificação de Linting**: ✅ PASSOU - Nenhum erro de linting encontrado
- **Estrutura de Dados**: ✅ PASSOU - Schema de saída conforme especificação

### 📊 Resultados da Última Execução
- **Total de registros processados**: 540 pedidos
- **Filtros aplicados**: Pagamentos recusados e legítimos do ano 2025
- **Arquivo de saída**: `data/output/relatorio_pedidos/part-*.parquet`
- **Status**: ✅ Pipeline executado com sucesso
- **Validação de Schema**: ✅ 36,000 registros validados (100% conformidade)
- **Tipos de Dados**: ✅ Schema atualizado com tipos corretos (double, long, timestamp)

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

1. **Erro de Permissão do Python ou Ambiente Virtual**: 
   ```bash
   # Se o venv não existir, crie primeiro
   python3 -m venv venv
   
   # Ative o ambiente virtual
   source venv/bin/activate
   ```

2. **Paths Incorretos**: 
   - Execute sempre a partir do diretório raiz do projeto
   - Verifique se está na pasta `pyspark-poo-lab/`

3. **Dependências Faltando**:
   ```bash
   # Instalar Java 17 para PySpark
   java -version
   
   # Reinstalar dependências Python
   pip install -r requirements.txt
   ```

4. **Erro "PATH_NOT_FOUND"**: 
   - Verifique se você está no diretório correto do projeto
   - Os datasets já estão incluídos no repositório em `data/input/`

## Autor
Eduardo Castilho de Almeida Prado - RM: 358966
Marllon Zucolotto de Almeida - RM: 358117
Mateus Bonacina Zanguettin - RM: 358472
Tiago Bento Amado - RM: 359183


## Licença
Este projeto está sob a licença MIT.
