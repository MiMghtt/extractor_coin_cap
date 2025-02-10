# CoinCap API 2.0
**v2.0.1**

CoinCap é uma ferramenta útil para precificação em tempo real e atividade de mercado para mais de 1.000 criptomoedas. Ao coletar dados de câmbio de milhares de mercados, somos capazes de oferecer dados transparentes e precisos sobre preço e disponibilidade de ativos.

## Desenho da Pipeline

Abaixo estão as etapas principais da pipeline utilizada no projeto, incluindo as fontes de dados e ferramentas utilizadas.
![CoinCap](https://github.com/user-attachments/assets/3e643c0c-4ce4-4372-a8d3-348b46d84611)

### 1. **Extração de Dados com Python**

A linguagem Python foi utilizada para a extração dos dados, utilizando as seguintes bibliotecas:
- **Requisição de dados**: Utilizando bibliotecas como `requests` para fazer chamadas à API do CoinCap.
- **Configuração do GCP**: Para interagir com o Google Cloud Storage, foi utilizada a biblioteca `gcsf`.
- **Manipulação de Dados**: Para tratar e manipular os dados obtidos, foi utilizada a biblioteca `pandas`.

### 2. **Google Cloud Storage (GCS)**

Os dados brutos extraídos são armazenados em um **bucket no Google Cloud Storage** para posterior processamento e análise.

### 3. **Google BigQuery**

O **Google BigQuery** foi utilizado para o tratamento e transformação dos dados brutos em um formato mais adequado para análise. Os dados processados são armazenados em tabelas no BigQuery para uso futuro.

---

## Scripts de Tratamento de Dados

Abaixo estão os scripts SQL utilizados para o tratamento e transformação das tabelas.

### 1. **Script de Tratamento da Tabela de Ativos**

Este script realiza o tratamento dos dados brutos da tabela de ativos, incluindo conversões de tipos de dados e filtragem.

```sql
CREATE OR REPLACE TABLE `stoked-aloe-450217-a2.tratados.ativos_tratados_resultado` AS
SELECT
  id,
  CAST(rank AS INT64) AS rank, 
  symbol, 
  name, 
  CAST(supply AS FLOAT64) AS supply,
  CAST(maxSupply AS FLOAT64) AS maxSupply, 
  CAST(marketCapUsd AS FLOAT64) AS marketCapUsd, 
  CAST(volumeUsd24Hr AS FLOAT64) AS volumeUsd24Hr, 
  CAST(priceUsd AS FLOAT64) AS priceUsd, 
  CAST(changePercent24Hr AS FLOAT64) AS changePercent24Hr, 
  CAST(vwap24Hr AS FLOAT64) AS vwap24Hr, 
  CURRENT_TIMESTAMP() AS processed_at 
FROM
  `stoked-aloe-450217-a2.tratados.ativos_tratados` 
WHERE
  id IS NOT NULL 
  AND marketCapUsd IS NOT NULL
  AND priceUsd IS NOT NULL 
  AND supply IS NOT NULL
  AND rank IS NOT NULL 
ORDER BY
  rank;
```

### 2. **Script de Tratamento da Tabela de Conversão**
```
CREATE OR REPLACE TABLE `stoked-aloe-450217-a2.tratados.conversao_tratados` AS
SELECT
  id, 
  symbol, 
  currencySymbol,
  CAST(rateUsd AS FLOAT64) AS rateUsd, 
  type, 
  CURRENT_TIMESTAMP() AS processed_at
FROM
  `stoked-aloe-450217-a2.brutos.conversao` 
WHERE
  id IS NOT NULL 
  AND rateUsd IS NOT NULL
  AND type IS NOT NULL 
ORDER BY
  symbol;
```
### 3. **Script de Tratamento da Tabela de Historicos**
```
CREATE OR REPLACE TABLE `stoked-aloe-450217-a2.tratados.historico_tratados` AS
WITH raw_data AS (
  SELECT
    data 
  FROM
    `stoked-aloe-450217-a2.brutos.historico` 
)

SELECT
  DATE(data.date) AS date, 
  data.id,
  CAST(data.priceUsd AS FLOAT64) AS priceUsd,
  TIMESTAMP_MILLIS(data.time) AS time, 
  CURRENT_TIMESTAMP() AS processed_at
FROM
  raw_data 
WHERE
  data.date IS NOT NULL
  AND data.id IS NOT NULL 
  AND data.priceUsd IS NOT NULL
  AND data.time IS NOT NULL 
ORDER BY
  time;
```

## Visualizações no Power BI
As visualizações dos dados foram criadas através de um dashboard no Power BI, que oferece uma visão interativa e gráfica dos dados processados, facilitando a análise de informações como preços, volumes de negociação e capitalização de mercado.

![image](https://github.com/user-attachments/assets/5fc3a111-4ed3-492c-a2f3-10ce515a2f2c)
(Acesse o arquivo desse BI nesse link: https://drive.google.com/file/d/1DF0OOvTK8K2DDpQr0hA8YfURozDYTs0R/view?usp=sharing)

## Tecnologias Utilizadas
- Python: Para a extração e manipulação dos dados.
- Google Cloud Storage: Para armazenamento dos dados brutos.
- Google BigQuery: Para processamento e análise dos dados.
- Power BI: Para visualizações interativas e análise dos dados.



