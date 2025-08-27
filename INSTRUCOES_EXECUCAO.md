# 📋 Instruções de Execução - Projeto PySpark

## 🎯 Objetivo do Projeto
Gerar um relatório de pedidos de venda com pagamentos recusados (`status=false`) e classificados como legítimos (`fraude=false`), apenas para o ano de 2025, ordenado por estado, forma de pagamento e data.

## 🏗️ Estrutura Implementada

### ✅ Critérios Atendidos
- [x] **Schemas explícitos** - Definidos em `DataReader`
- [x] **Orientação a objetos** - Todas as classes implementadas
- [x] **Injeção de Dependências** - Implementada no `main_project.py`
- [x] **Configurações centralizadas** - Classe `SparkConfig`
- [x] **Sessão Spark gerenciada** - Classe `SparkSessionManager`
- [x] **Leitura e escrita de dados** - Classes `DataReader` e `DataWriter`
- [x] **Lógica de negócio** - Classe `OrderProcessor`
- [x] **Orquestração do pipeline** - Classe `PipelineOrchestrator`
- [x] **Logging configurado** - Implementado em todas as classes
- [x] **Tratamento de erros** - Try/catch em todas as operações
- [x] **Empacotamento da aplicação** - pyproject.toml, requirements.txt, MANIFEST.in
- [x] **Testes unitários** - Implementados para `OrderProcessor`

## 🚀 Passos para Execução

### 1. Preparação do Ambiente

#### 1.1 Verificar Python
```bash
python --version
# ou
python3 --version
```

#### 1.2 Criar ambiente virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 1.3 Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Obtenção dos Datasets

#### 2.1 Dataset de Pagamentos
```bash
# Clonar repositório
git clone https://github.com/infobarbosa/dataset-json-pagamentos.git

# Copiar dados para a estrutura do projeto
cp -r dataset-json-pagamentos/data/pagamentos/* data/input/pagamentos/
```

#### 2.2 Dataset de Pedidos
```bash
# Clonar repositório
git clone https://github.com/infobarbosa/datasets-csv-pedidos.git

# Copiar dados para a estrutura do projeto
cp -r datasets-csv-pedidos/data/pedidos/* data/input/pedidos/
```

### 3. Validação do Projeto

#### 3.1 Executar script de validação
```bash
python test_project_structure.py
```

Este script irá verificar:
- ✅ Estrutura de diretórios
- ✅ Arquivos de código fonte
- ✅ Arquivos de configuração
- ✅ Dados de entrada

### 4. Execução dos Testes

#### 4.1 Executar testes unitários
```bash
pytest tests/ -v
```

#### 4.2 Verificar cobertura (opcional)
```bash
pytest tests/ --cov=src --cov-report=html
```

### 5. Execução do Pipeline

#### 5.1 Executar aplicação principal
```bash
python src/main_project.py
```

#### 5.2 Verificar logs
A aplicação irá mostrar logs detalhados de cada etapa:
- Configuração do Spark
- Leitura dos dados
- Processamento
- Escrita do resultado

### 6. Verificação dos Resultados

#### 6.1 Verificar arquivo de saída
```bash
ls data/output/relatorio_pedidos/
```

#### 6.2 Visualizar dados (opcional)
```python
from pyspark.sql import SparkSession

# Criar sessão Spark
spark = SparkSession.builder.appName('Verificacao').getOrCreate()

# Ler resultado
df = spark.read.parquet('data/output/relatorio_pedidos')

# Mostrar dados
df.show(10)
df.printSchema()

# Contar registros
print(f"Total de registros: {df.count()}")

# Verificar filtros
df.filter("estado = 'SP'").show(5)
```

## 📊 Estrutura dos Dados

### Dataset de Pagamentos (JSON)
- **Caminho**: `data/input/pagamentos/*.json.gz`
- **Schema**:
  - `id_pedido` (String)
  - `status` (Boolean)
  - `fraude` (Boolean)
  - `forma_pagamento` (String)
  - `valor` (Double)
  - `data_pagamento` (Timestamp)

### Dataset de Pedidos (CSV)
- **Caminho**: `data/input/pedidos/*.csv.gz`
- **Schema**:
  - `id_pedido` (String)
  - `estado` (String)
  - `forma_pagamento` (String)
  - `valor_total` (Double)
  - `data_pedido` (Timestamp)

### Relatório de Saída (Parquet)
- **Caminho**: `data/output/relatorio_pedidos/`
- **Colunas**:
  - `id_pedido`
  - `estado`
  - `forma_pagamento`
  - `valor_total`
  - `data_pedido`

## 🔧 Configurações

### Spark Config
As configurações do Spark podem ser ajustadas em `src/config/spark_config.py`:

```python
@dataclass
class SparkConfig:
    app_name: str = "RelatorioPedidos"
    master: str = "local[*]"
    spark_configs: Dict[str, Any] = None
```

### Logging
O logging está configurado para mostrar:
- Timestamps
- Níveis de log (INFO, ERROR)
- Mensagens detalhadas de cada etapa

## 🐛 Solução de Problemas

### Erro de Memória
```python
# Ajustar em spark_config.py
spark_configs = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.driver.memory": "2g",
    "spark.executor.memory": "2g"
}
```

### Erro de Schema
- Verificar se os schemas em `DataReader` estão corretos
- Validar formato dos dados de entrada
- Usar `mode="PERMISSIVE"` para leitura tolerante

### Erro de Dependências
```bash
# Reinstalar dependências
pip uninstall pyspark pandas pytest
pip install -r requirements.txt
```

## 📈 Monitoramento

### Logs de Execução
A aplicação gera logs detalhados:
```
2025-08-27 20:30:15 - INFO - Iniciando aplicação
2025-08-27 20:30:16 - INFO - Lendo dataset de pagamentos
2025-08-27 20:30:17 - INFO - Lendo dataset de pedidos
2025-08-27 20:30:18 - INFO - Processando dados
2025-08-27 20:30:19 - INFO - Escrevendo relatório
2025-08-27 20:30:20 - INFO - Pipeline executado com sucesso!
```

### Métricas de Performance
- Tempo de execução por etapa
- Número de registros processados
- Uso de memória

## 📝 Evidências para Entrega

### Screenshots Necessários
1. **Estrutura do projeto** - `tree /F` ou `ls -la`
2. **Execução do script de validação** - `python test_project_structure.py`
3. **Resultado dos testes** - `pytest tests/ -v`
4. **Execução do pipeline** - `python src/main_project.py`
5. **Arquivo de saída** - `ls data/output/relatorio_pedidos/`
6. **Código fonte das classes principais** (máximo 20 linhas cada)

### Dicas para Screenshots
- Use fonte legível (12pt ou maior)
- Capture apenas as partes relevantes
- Inclua timestamps nos logs
- Mostre a estrutura completa de diretórios
- Verifique se os dados de saída estão corretos

## 🎯 Checklist Final

### Antes da Entrega
- [ ] Todos os testes passando
- [ ] Pipeline executando sem erros
- [ ] Arquivo de saída gerado corretamente
- [ ] Logs mostrando todas as etapas
- [ ] Screenshots das evidências capturados
- [ ] Repositório no GitHub criado
- [ ] Documentação completa

### Critérios de Avaliação
- [ ] Schemas explícitos ✅
- [ ] Orientação a objetos ✅
- [ ] Injeção de dependências ✅
- [ ] Configurações centralizadas ✅
- [ ] Sessão Spark gerenciada ✅
- [ ] Leitura e escrita de dados ✅
- [ ] Lógica de negócio ✅
- [ ] Orquestração do pipeline ✅
- [ ] Logging configurado ✅
- [ ] Tratamento de erros ✅
- [ ] Empacotamento da aplicação ✅
- [ ] Testes unitários ✅

## 📞 Suporte
Para dúvidas sobre o escopo e execução:
- Email: profmarcelo.barbosa@fiap.com.br
- Repositório de referência: https://github.com/infobarbosa/pyspark-poo

---

**🎉 Projeto implementado com sucesso seguindo todos os critérios especificados!**
