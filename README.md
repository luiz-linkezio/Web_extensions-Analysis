# <div align="center">Vulnerabilidades em extensões web</div>

## 🎯 Objetivo

Este projeto visa explorar vulnerabilidades em extensões de navegador, com foco na análise de permissões e potenciais vetores de ataque.

##  📁️ Estrutura de Pastas
* **exploit_permissions**: Esta pasta contém scripts destinados à extração e análise dos arquivos `manifest.json` das extensões, com foco na identificação de possíveis vulnerabilidades.
    * `dump_manifest.py`: Script responsável pela extração dos arquivos `manifest.json` das extensões.
* **extensions**: Pasta que abriga extensões maliciosas para fins de teste de segurança.
* **server**: Contém um servidor que simula um servidor atacante, recebendo informações da vítima para análise.


## ⚙️ Exploit Permissions
O objetivo deste etapa é extrair (`dump`) os arquivos `manifest.json` de extensões para analisar, principalmente, os seguintes campos:  

- `permissions`  
- `host_permissions`  
- `content_scripts`
- `manifest_version`
- Outros campos relevantes identificados durante a análise  

### 🚀 Executando o `dump_manifest`

Para executar o script `dump_manifest` e extrair os arquivos `manifest.json` das extensões, siga os passos abaixo:

#### Pré-requisitos

Antes de executar o script, você precisará instalar as seguintes bibliotecas Python:

- **Selenium**: Para automação de navegador e interação com a página da Chrome Web Store.
- **Beautiful Soup (bs4)**: Para analisar o HTML e extrair informações das extensões.

#### Instalação

1. **Instale o Python**:  
   Certifique-se de ter o Python 3.x instalado em seu sistema. Você pode baixá-lo [aqui](https://www.python.org/downloads/).

2. **Clone o repositório**:
   ```bash
   git clone https://github.com/Dev-JoseRonaldo/web-extensions-vulnerabilities.git
   cd web-extensions-vulnerabilities/exploit_permissions
   ```

3. **Instale as dependências**:  
   ```bash
    pip install selenium beautifulsoup4
   ```

3. **Execute o Script**:  
   ```bash
    python dump_manifest.py
   ```
O script irá acessar a Chrome Web Store, extrair os IDs das extensões e baixar os arquivos manifest.json, incluindo os campos relevantes para análise. O resultado será salvo no arquivo `exploit_permissions/dump/extensions_info.json`

### 📝 TO-DO
- [x] Extrair dados do `manifest.json` do maior número possível de extensões.
- [x] Adicionar, no json de saída, a quantidade de usuários de cada extensão.
- [x] Criar arquivo de logs parao processo de extração dos dados.
- [ ] Analisar os campos `permissions`, `host_permissions` e `content_scripts` para avaliar possíveis vetores de ataque. 
- [ ] Identificar cenários em que combinações desses campos possam representar riscos à segurança.
- [ ] Criar provas de conceito para explorar esses cenários e obter estatísticas sobre as extensões mapeadas.

### 🛠️ Ferramentas
- [CRXviewer](https://crxviewer.com/): Esta ferramenta **permite analisar o código-fonte** das extensões informando seu ID ou URL. Será útil na etapa de identificação de cenários de ataque, especialmente na detecção de más práticas de desenvolvimento que, juntamente com os campos `permissions` e `host_permissions`, podem levar a vulnerabilidades e cenários de exploração.  
