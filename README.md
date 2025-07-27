# 📑 Language / Idioma

- [English](#english)
- [Português](#português)

---

# English

[⬆️ Back to top](#language--idioma)

# Analysis of insecure configurations in Chrome Web Store extensions: Impact on user security and privacy

This repository contains the artifacts and scripts used for security risk analysis of Chrome Web Store extensions. The project aims to identify and analyze extensions that request potentially dangerous permissions but do not effectively use them in their code, representing a security risk for users. The analysis was conducted through automated collection of extension manifests, analysis of requested versus used permissions, and identification of insecure usage patterns.

**Paper Abstract:** Browser extensions, popular for enhancing functionality, pose risks to user privacy and security. This study analyzes insecure configurations in Chrome Web Store extensions, assessing their functional justification. Auditing 287 extensions revealed that many employ excessive permissions or unnecessary access to sensitive data without clear justification, exposing avoidable vulnerabilities. Findings show that risky practices persist even in widely used tools, highlighting flaws in app stores' verification processes. The research provides empirical evidence of these issues and advocates for stricter policies for developers, platforms, and regulators to balance functionality and security in the ecosystem.

## README.md Structure

This repository is organized as follows:

- **`scripts/`**: Contains all Python scripts used for data collection, processing, and analysis
  - `dump_manifest.py`: Main script for collecting extension manifests from Chrome Web Store using Selenium automation
  - `filter_data.py`: Interactive filtering of extensions based on specific criteria (downloads, permissions, etc.)
  - `merge_data.py`: Consolidation of data collected from different categories into unified datasets
  - `permissions_usage.py`: Analysis of permission usage in extension JavaScript code through static analysis
  - `permissions_usage_stats.py`: Generation of comprehensive permission usage statistics and reports
  - `permissions_percent_usage.py`: Calculation of permission usage percentages and ratios
  - `permissions_per_manifest_version.py`: Analysis of permissions by manifest version to identify trends

- **`data/`**: Stores all collected and processed data
  - `raw_json_manifests/`: Raw manifests organized by category (productivity, lifestyle, etc.)
  - `merged_extensions.json`: Consolidated dataset of all extensions (24MB, comprehensive dataset)
  - `filtered_extensions.json`: Extensions filtered by specific criteria (528KB, 15,402 extensions)
  - `filtered_extensions_insecure.json`: Extensions identified as potentially insecure (160KB, 5,834 extensions)
  - `permission_analysis_report.json`: Permission analysis report with usage statistics (21KB, 863 lines)
  - `permissions_usage_report.json`: Detailed permission usage report (51KB, 1,910 lines)

- **`logs/`**: Script execution logs organized by functionality
  - `dump/`: Data collection logs with timestamps and execution details
  - `merge_data/`: Data consolidation process logs with merge statistics

- **`requirements.txt`**: Python dependencies with specific versions for reproducibility
- **`.gitignore`**: Git ignore file for managing repository contents

## Considered Badges

The considered badges are: **Available and Functional**.

**Justification for Available Badge (SeloD):**
- Code and data are available in a stable GitHub repository
- README.md meets all minimum requirements
- Repository is publicly accessible and well-organized

**Justification for Functional Badge (SeloF):**
- Complete list of dependencies with specific versions provided
- Detailed environment description and execution instructions
- Minimum execution example included
- All scripts can be executed and demonstrate functionality

## Basic Information

### Hardware Requirements
- **RAM**: Minimum 4GB, recommended 8GB or higher (for processing large datasets)
- **Storage**: Minimum 10GB of free space (for extension downloads and analysis)
- **CPU**: Multi-core processor recommended for parallel processing (Intel i5/AMD Ryzen 5 or better)
- **Network**: Stable internet connection for Chrome Web Store access

### Software Requirements
- **Operating System**: Linux (tested on Arch Linux), macOS, or Windows
- **Python**: Version 3.8 or higher
- **Browser**: Google Chrome (for Selenium execution)
- **ChromeDriver**: Compatible with the installed Chrome version

### Execution Environment
- **Shell**: Bash (Linux/macOS) or PowerShell (Windows)
- **Package Manager**: pip (Python Package Installer)
- **Version Control**: Git (optional, for repository cloning)

## Dependencies

### Main Python Dependencies (with versions)
- **requests==2.32.3**: For HTTP requests to Chrome Web Store and extension downloads
- **selenium==4.29.0**: For web automation and data collection from Chrome Web Store
- **beautifulsoup4==4.13.3**: For HTML parsing and extraction of extension information
- **websocket-client==1.8.0**: For WebSocket communication during browser automation
- **cryptography==44.0.2**: For cryptographic operations and secure communications
- **argcomplete==3.5.3**: For command-line argument completion
- **attrs==25.1.0**: For advanced class definitions and data structures
- **psutil==7.0.0**: For system resource monitoring during execution

### System Dependencies
- **Google Chrome**: Browser for Selenium execution (version 91.0+)
- **ChromeDriver**: Driver for Chrome automation (compatible version)
- **zipfile**: Standard Python module for ZIP file manipulation

### Third-Party Resources
- **Chrome Web Store**: Primary source of extension data
- **Google Chrome Extension API**: For downloading CRX files
- **Chrome Web Store Categories**: Extension categorization

### Resource Access Process
1. **Chrome Web Store**: Public access via automated web navigation
2. **Extension Downloads**: Uses Google's public API for downloading CRX files
3. **Code Analysis**: Local processing of downloaded files without external dependencies
4. **Data Storage**: Local file system storage with automatic cleanup

## Installation

### 1. Repository Clone
```bash
git clone https://github.com/your-username/Web_extensions-Analysis.git
cd Web_extensions-Analysis
```

### 2. Python Environment Setup
```bash
# Virtual environment creation (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Verify Python version
python --version  # Should be 3.8 or higher

# Upgrade pip
pip install --upgrade pip

# Dependencies installation
pip install -r requirements.txt
```

### 3. Chrome and ChromeDriver Setup
```bash
# Chrome installation (Ubuntu/Debian)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable

# Chrome installation (Arch Linux)
sudo pacman -S google-chrome

# Chrome installation (macOS)
brew install --cask google-chrome

# ChromeDriver installation
# Download the version compatible with your Chrome at: https://chromedriver.chromium.org/
# Add to PATH or specify the path in the script
# Example for Linux:
wget https://chromedriver.storage.googleapis.com/[VERSION]/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

### 4. Installation Verification
```bash
# Python and dependencies test
python -c "import selenium, requests, bs4, websocket; print('All dependencies installed successfully!')"

# Chrome test
google-chrome --version

# ChromeDriver test
chromedriver --version

# Verify repository structure
ls -la scripts/ data/ logs/
```

### 5. Environment Validation
```bash
# Test connectivity to Chrome Web Store
python -c "
import requests
try:
    response = requests.get('https://chrome.google.com/webstore/category/extensions', timeout=10)
    print(f'Chrome Web Store connectivity: {response.status_code}')
except Exception as e:
    print(f'Connectivity error: {e}')
"
```

## Minimum Test

### Objective
Verify that the environment is properly configured and that basic scripts work.

### Step by Step

1. **Environment Preparation**
```bash
cd Web_extensions-Analysis
source venv/bin/activate  # or activate your virtual environment
```

2. **Connectivity Test**
```bash
python -c "
import requests
response = requests.get('https://chrome.google.com/webstore/category/extensions')
print(f'Status: {response.status_code}')
print('Connectivity OK!' if response.status_code == 200 else 'Connectivity error')
"
```

3. **Existing Data Analysis Test**
```bash
# Test with existing data files
python scripts/permissions_percent_usage.py
```

4. **Results Verification**
```bash
ls -la data/
echo "Data files found:"
ls data/*.json | wc -l
echo "Log files found:"
ls logs/*/ | wc -l
```

5. **Basic Functionality Test**
```bash
# Test data filtering functionality
python scripts/filter_data.py --help 2>/dev/null || echo "Filter script available"
```

### Expected Result
- Connectivity status: 200
- Script execution without errors
- Presence of JSON files in the `data/` folder
- Log files in appropriate directories
- All dependencies properly installed

### Estimated Time
- **Preparation**: 5 minutes
- **Execution**: 2-3 minutes
- **Total**: 8-10 minutes

### Troubleshooting
- If Chrome connectivity fails, check internet connection and firewall settings
- If dependencies fail to install, ensure Python version is 3.8+
- If ChromeDriver issues occur, verify version compatibility with Chrome

## Experiments

### Claim #1: Extension Data Collection

**Objective**: Demonstrate the capability of automated collection of extension manifests from Chrome Web Store.

#### Configuration
- **File**: `scripts/dump_manifest.py`
- **Parameters**: Extension categories defined in the script
- **Limit**: Maximum 1568 extensions per category

#### Execution Commands
```bash
# Complete collection execution
python scripts/dump_manifest.py

# Execution with detailed logging
python scripts/dump_manifest.py 2>&1 | tee logs/collection_$(date +%Y%m%d_%H%M%S).log
```

#### Configuration Details (from code)
- **Headless Mode**: Enabled by default
- **Timeout**: 10 seconds for page loading
- **Delay**: 2 seconds between requests
- **Logging**: Timestamped logs to logs/dump/ directory

#### Expected Result
- JSON files in `data/raw_json_manifests/` organized by category
- Detailed logs in `logs/dump/` with timestamps
- Extension manifests with metadata

### Claim #2: Permission Usage Analysis

**Objective**: Identify extensions that request permissions but do not use them in the code.

#### Configuration
- **File**: `scripts/permissions_usage.py`
- **Input**: `data/filtered_extensions.json`
- **Output**: `permissions_usage_report.json`
- **Analysis Type**: Static code analysis of JavaScript files

#### Execution Commands
```bash
# Complete permission usage analysis
python scripts/permissions_usage.py
```

#### Configuration Details (from code)
- **Download Directory**: `extensions_crx/`
- **Search Patterns**: chrome.permissions, chrome.tabs, chrome.storage
- **Automatic Cleanup**: Removal of temporary files after analysis
- **Error Handling**: Skip failed downloads and continue processing

#### Expected Result
- JSON report with permission usage analysis
- Statistics of requested vs. used permissions
- Identification of potentially insecure extensions

### Claim #3: Insecure Extensions Identification

**Objective**: Filter and categorize extensions with insecure permission usage patterns.

#### Configuration
- **File**: `scripts/filter_data.py`
- **Input**: `data/merged_extensions.json`
- **Output**: Filtered extensions based on user criteria
- **Mode**: Interactive filtering process

#### Execution Commands
```bash
# Interactive filtering
python scripts/filter_data.py
```

#### Configuration Details (from code)
- **Filter Options**: Downloads count, specific fields
- **Interactive Mode**: User-guided filtering process
- **Field Selection**: Dynamic field discovery from data

#### Expected Result
- Filtered list of extensions based on specified criteria
- Statistics of distribution by category
- Report of extensions matching filter conditions

### Claim #4: Statistical Reports Generation

**Objective**: Produce statistical reports on permission usage patterns.

#### Configuration
- **Files**: `scripts/permissions_usage_stats.py`, `scripts/permissions_percent_usage.py`, `scripts/permissions_per_manifest_version.py`
- **Input**: Permission usage data from previous analyses
- **Output**: Statistical reports in JSON format

#### Execution Commands
```bash
# Statistics generation
python scripts/permissions_usage_stats.py

# Analysis by manifest version
python scripts/permissions_per_manifest_version.py

# Percentage analysis
python scripts/permissions_percent_usage.py
```

#### Expected Result
- Statistical reports with permission usage data
- Analysis of trends and patterns
- Risk assessment metrics based on permission usage

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

# Português

[⬆️ Voltar ao topo](#language--idioma)

# Análise de configurações inseguras em extensões da Chrome Web Store: Impacto na segurança e privacidade do usuário

Este repositório contém os artefatos e scripts utilizados para a análise de riscos de segurança em extensões da Chrome Web Store. O objetivo do projeto é identificar e analisar extensões que solicitam permissões potencialmente perigosas, mas não as utilizam efetivamente em seu código, representando um risco para os usuários. A análise foi realizada por meio da coleta automatizada de manifestos, análise das permissões solicitadas versus utilizadas e identificação de padrões inseguros.

**Resumo do artigo:** Extensões de navegador, populares por ampliar funcionalidades, trazem riscos à privacidade e segurança dos usuários. Este estudo analisa configurações inseguras em extensões da Chrome Web Store, avaliando sua justificativa funcional. A auditoria de 287 extensões revelou que muitas utilizam permissões excessivas ou acesso desnecessário a dados sensíveis sem justificativa clara, expondo vulnerabilidades evitáveis. Os resultados mostram que práticas arriscadas persistem mesmo em ferramentas amplamente utilizadas, evidenciando falhas nos processos de verificação das lojas de aplicativos. A pesquisa fornece evidências empíricas desses problemas e defende políticas mais rigorosas para desenvolvedores, plataformas e reguladores, visando equilibrar funcionalidade e segurança no ecossistema.

## Estrutura do README.md

Este repositório está organizado da seguinte forma:

- **`scripts/`**: Contém todos os scripts Python utilizados para coleta, processamento e análise dos dados
  - `dump_manifest.py`: Script principal para coleta de manifestos de extensões usando Selenium
  - `filter_data.py`: Filtragem interativa de extensões por critérios (downloads, permissões, etc.)
  - `merge_data.py`: Consolidação dos dados coletados em diferentes categorias
  - `permissions_usage.py`: Análise do uso de permissões no código JavaScript das extensões
  - `permissions_usage_stats.py`: Geração de estatísticas de uso de permissões
  - `permissions_percent_usage.py`: Cálculo de percentuais de uso de permissões
  - `permissions_per_manifest_version.py`: Análise de permissões por versão do manifesto

- **`data/`**: Armazena todos os dados coletados e processados
  - `raw_json_manifests/`: Manifestos brutos organizados por categoria
  - `merged_extensions.json`: Dataset consolidado de todas as extensões
  - `filtered_extensions.json`: Extensões filtradas por critérios específicos
  - `filtered_extensions_insecure.json`: Extensões identificadas como potencialmente inseguras
  - `permission_analysis_report.json`: Relatório de análise de permissões
  - `permissions_usage_report.json`: Relatório detalhado de uso de permissões

- **`logs/`**: Logs de execução dos scripts
  - `dump/`: Logs da coleta de dados
  - `merge_data/`: Logs do processo de consolidação

- **`requirements.txt`**: Dependências Python com versões específicas
- **`.gitignore`**: Arquivo para ignorar arquivos no Git

## Selos Considerados

Os selos considerados são: **Disponível e Funcional**.

**Justificativa para o selo Disponível (SeloD):**
- Código e dados disponíveis em repositório estável
- README.md atende aos requisitos mínimos
- Repositório público e bem organizado

**Justificativa para o selo Funcional (SeloF):**
- Lista completa de dependências com versões
- Descrição detalhada do ambiente e instruções de execução
- Exemplo mínimo de execução incluído
- Todos os scripts podem ser executados e demonstram funcionalidade

## Informações Básicas

### Requisitos de Hardware
- **RAM**: Mínimo 4GB, recomendado 8GB ou mais
- **Armazenamento**: Mínimo 10GB de espaço livre
- **CPU**: Processador multi-core recomendado
- **Rede**: Conexão estável com a internet

### Requisitos de Software
- **Sistema Operacional**: Linux (testado em Arch Linux), macOS ou Windows
- **Python**: Versão 3.8 ou superior
- **Navegador**: Google Chrome
- **ChromeDriver**: Compatível com a versão do Chrome instalada

### Ambiente de Execução
- **Shell**: Bash (Linux/macOS) ou PowerShell (Windows)
- **Gerenciador de Pacotes**: pip
- **Controle de Versão**: Git (opcional)

## Dependências

### Principais dependências Python (com versões)
- **requests==2.32.3**: Requisições HTTP
- **selenium==4.29.0**: Automação web e coleta de dados
- **beautifulsoup4==4.13.3**: Parsing de HTML
- **websocket-client==1.8.0**: Comunicação WebSocket
- **cryptography==44.0.2**: Operações criptográficas
- **argcomplete==3.5.3**: Autocompletar argumentos de linha de comando
- **attrs==25.1.0**: Estruturas de dados avançadas
- **psutil==7.0.0**: Monitoramento de recursos do sistema

### Dependências do Sistema
- **Google Chrome**: Navegador para execução do Selenium
- **ChromeDriver**: Driver para automação do Chrome
- **zipfile**: Módulo padrão do Python para arquivos ZIP

### Recursos de Terceiros
- **Chrome Web Store**: Fonte principal dos dados
- **API de Extensões do Chrome**: Para download de arquivos CRX
- **Categorias da Chrome Web Store**: Categorização das extensões

### Processo de Acesso a Recursos
1. **Chrome Web Store**: Acesso público via automação web
2. **Download de Extensões**: Utiliza API pública do Google
3. **Análise de Código**: Processamento local dos arquivos baixados
4. **Armazenamento de Dados**: Armazenamento local com limpeza automática

## Instalação

### 1. Clonar o Repositório
```bash
git clone https://github.com/your-username/Web_extensions-Analysis.git
cd Web_extensions-Analysis
```

### 2. Configuração do Ambiente Python
```bash
# Criação de ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Verifique a versão do Python
python --version  # Deve ser 3.8 ou superior

# Atualize o pip
pip install --upgrade pip

# Instale as dependências
pip install -r requirements.txt
```

### 3. Instalação do Chrome e ChromeDriver
```bash
# Instalação do Chrome (Ubuntu/Debian)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable

# Instalação do Chrome (Arch Linux)
sudo pacman -S google-chrome

# Instalação do Chrome (macOS)
brew install --cask google-chrome

# Instalação do ChromeDriver
# Baixe a versão compatível com seu Chrome em: https://chromedriver.chromium.org/
# Adicione ao PATH ou especifique o caminho no script
# Exemplo para Linux:
wget https://chromedriver.storage.googleapis.com/[VERSAO]/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

### 4. Verificação da Instalação
```bash
# Teste do Python e dependências
python -c "import selenium, requests, bs4, websocket; print('Todas as dependências instaladas com sucesso!')"

# Teste do Chrome
google-chrome --version

# Teste do ChromeDriver
chromedriver --version

# Verifique a estrutura do repositório
ls -la scripts/ data/ logs/
```

### 5. Validação do Ambiente
```bash
# Teste de conectividade com a Chrome Web Store
python -c "
import requests
try:
    response = requests.get('https://chrome.google.com/webstore/category/extensions', timeout=10)
    print(f'Conectividade com a Chrome Web Store: {response.status_code}')
except Exception as e:
    print(f'Erro de conectividade: {e}')
"
```

## Teste Mínimo

### Objetivo
Verificar se o ambiente está configurado corretamente e se os scripts básicos funcionam.

### Passo a Passo

1. **Preparação do Ambiente**
```bash
cd Web_extensions-Analysis
source venv/bin/activate  # ou ative seu ambiente virtual
```

2. **Teste de Conectividade**
```bash
python -c "
import requests
response = requests.get('https://chrome.google.com/webstore/category/extensions')
print(f'Status: {response.status_code}')
print('Conectividade OK!' if response.status_code == 200 else 'Erro de conectividade')
"
```

3. **Teste de Análise de Dados Existentes**
```bash
# Teste com arquivos de dados existentes
python scripts/permissions_percent_usage.py
```

4. **Verificação de Resultados**
```bash
ls -la data/
echo "Arquivos de dados encontrados:"
ls data/*.json | wc -l
echo "Arquivos de log encontrados:"
ls logs/*/ | wc -l
```

5. **Teste de Funcionalidade Básica**
```bash
# Teste da funcionalidade de filtragem de dados
python scripts/filter_data.py --help 2>/dev/null || echo "Script de filtro disponível"
```

### Resultado Esperado
- Status de conectividade: 200
- Execução dos scripts sem erros
- Presença de arquivos JSON na pasta `data/`
- Arquivos de log nos diretórios apropriados
- Todas as dependências instaladas corretamente

## Experimentos

### Reivindicação #1: Coleta de Dados de Extensões

**Objetivo**: Demonstrar a capacidade de coleta automatizada de manifestos de extensões da Chrome Web Store.

#### Configuração
- **Arquivo**: `scripts/dump_manifest.py`
- **Categorias**: 19 categorias definidas no script (productivity, lifestyle, make_chrome_yours)
- **Limite**: Máximo de 1568 extensões por categoria (conforme definido no código)

#### Comandos de Execução
```bash
# Execução completa da coleta
git clone https://github.com/your-username/Web_extensions-Analysis.git
cd Web_extensions-Analysis
python scripts/dump_manifest.py

# Execução com log detalhado
python scripts/dump_manifest.py 2>&1 | tee logs/collection_$(date +%Y%m%d_%H%M%S).log
```

#### Detalhes de Configuração (do código)
- **Modo Headless**: Ativado por padrão
- **Timeout**: 10 segundos para carregamento de página
- **Delay**: 2 segundos entre requisições
- **Logs**: Logs com timestamp em logs/dump/

#### Resultado Esperado
- Arquivos JSON em `data/raw_json_manifests/` organizados por categoria
- Logs detalhados em `logs/dump/` com timestamps
- Manifestos de extensões com metadados

### Reivindicação #2: Análise de Uso de Permissões

**Objetivo**: Identificar extensões que solicitam permissões mas não as utilizam no código JavaScript.

#### Configuração
- **Arquivo**: `scripts/permissions_usage.py`
- **Entrada**: `data/filtered_extensions.json`
- **Saída**: `permissions_usage_report.json`
- **Tipo de Análise**: Análise estática de código JavaScript

#### Comandos de Execução
```bash
# Análise completa de uso de permissões
python scripts/permissions_usage.py
```

#### Detalhes de Configuração (do código)
- **Diretório de Download**: `extensions_crx/`
- **Padrões de Busca**: chrome.permissions, chrome.tabs, chrome.storage
- **Limpeza Automática**: Remoção de arquivos temporários após análise
- **Tratamento de Erros**: Ignora downloads com falha e continua o processamento

#### Resultado Esperado
- Relatório JSON com análise de uso de permissões
- Estatísticas de permissões solicitadas vs. utilizadas
- Identificação de extensões potencialmente inseguras

### Reivindicação #3: Identificação de Extensões Inseguras

**Objetivo**: Filtrar e categorizar extensões com padrões inseguros de uso de permissões.

#### Configuração
- **Arquivo**: `scripts/filter_data.py`
- **Entrada**: `data/merged_extensions.json`
- **Saída**: Extensões filtradas conforme critérios do usuário
- **Modo**: Processo de filtragem interativo

#### Comandos de Execução
```bash
# Filtragem interativa
python scripts/filter_data.py
```

#### Detalhes de Configuração (do código)
- **Opções de Filtro**: Número de downloads, campos específicos
- **Modo Interativo**: Processo guiado pelo usuário
- **Seleção de Campos**: Descoberta dinâmica dos campos a partir dos dados

#### Resultado Esperado
- Lista filtrada de extensões conforme critérios especificados
- Estatísticas de distribuição por categoria
- Relatório de extensões que atendem aos filtros

### Reivindicação #4: Geração de Relatórios Estatísticos

**Objetivo**: Produzir relatórios estatísticos sobre padrões de uso de permissões.

#### Configuração
- **Arquivos**: `scripts/permissions_usage_stats.py`, `scripts/permissions_percent_usage.py`, `scripts/permissions_per_manifest_version.py`
- **Entrada**: Dados de uso de permissões de análises anteriores
- **Saída**: Relatórios estatísticos em formato JSON

#### Comandos de Execução
```bash
# Geração de estatísticas
python scripts/permissions_usage_stats.py

# Análise por versão do manifesto
python scripts/permissions_per_manifest_version.py

# Análise percentual
python scripts/permissions_percent_usage.py
```

#### Resultado Esperado
- Relatórios estatísticos com dados de uso de permissões
- Análise de tendências e padrões
- Métricas de risco baseadas no uso de permissões

## LICENÇA

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License
Copyright (c) 2025 [Seu Nome]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
``` 