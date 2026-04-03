# 🚀 Pipeline ETL: Automação de Marketing Imobiliário

Este projeto foi desenvolvido como parte do desafio prático da **Santander Dev Week 2026**. O objetivo é demonstrar um fluxo completo de **ETL (Extração, Transformação e Carregamento)** utilizando Python.

O sistema conecta-se a uma API real de gestão de imóveis, processa os dados brutos e gera mensagens personalizadas de marketing para cada registro.

## 🛠️ Tecnologias Utilizadas
* **Python 3.13**
* **Bibliotecas:** `requests`, `csv`, `python-dotenv`.
* **Segurança:** Implementação de `TLS 1.2 Adapter` e `SECLEVEL=1` para comunicação segura com a API.

## 🔄 O Fluxo ETL

### 1. Extract (Extração)
* Consumo de dados via API REST com autenticação dinâmica.
* Paginação automática para suporte a grandes volumes de dados.

### 2. Transform (Transformação)
* **Limpeza:** Padronização de valores e formatos de data.
* **Inteligência:** Geração de propostas de marketing personalizadas unindo bairro, tipo de imóvel e valor.

### 3. Load (Carregamento)
* Exportação dos dados para formato **CSV**.
* *Nota: O arquivo de saída (CSV) foi omitido deste repositório para preservar o sigilo dos dados da API real consultada.*

## 🛡️ Segurança
* O projeto utiliza variáveis de ambiente (`.env`) para proteger credenciais sensíveis, seguindo as melhores práticas de proteção de dados.
