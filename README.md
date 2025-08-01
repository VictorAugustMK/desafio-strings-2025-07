# 📝 Projeto FastAPI para Quebra de Linhas em Arquivos .txt

API para processar arquivos .txt, quebrando linhas respeitando largura máxima e parágrafos.

## 🏗️ Tecnologias
- FastAPI
- Python 3.10+
- Uvicorn
- Docker & Docker Compose
- Pydantic
- Pytest

## 📁 Estrutura
O projeto está organizado em módulos:

- `app/` – código fonte da aplicação
- `app/services` – lógica de processamento de texto
- `app/config.py` – configurações e variáveis de ambiente
- `app/models.py` – schemas Pydantic para requisições
- `tests/ – testes` unitários e de integração

## ⚙️ Configuração
1. Clone o repositório:
```bash
git clone https://github.com/VictorAugustMK/desafio-strings-2025-07.git  
cd desafio-strings-2025-07
```
2. Crie o arquivo .env (exemplo):
```bash
INPUT_PATH=./input  
OUTPUT_PATH=./output
```
3. Inicie o projeto com Docker:
```bash
docker compose up --build
```
4. Acesse:
- API: http://localhost:8001
- Docs Swagger: http://localhost:8001/docs
  
## 🚀 Como usar a API
Endpoint: POST /upload/
Envie um ou mais arquivos .txt para processar a quebra de linhas.

Parâmetros:

`files (opcional)`: arquivo(s) .txt

`width (opcional)`: largura máxima da linha (padrão 40)
Exemplo curl:
```
curl -X POST http://localhost:8000/upload/ \  
  -F "files=seuarquivo.txt" \  
  -F "width=40"
```
Ou via Postman
```
{
  "path": "",
  "width": 0
}
```
`OBS: Se nunhum dos parâmetro for preenchido será feito a leitura de todos os arquivos .txt dentro da pasta com padrão 40 caracteres por linha.`
Os arquivos processados são salvos na pasta output/ com o nome original acrescido de _break.txt.

## 🧪 Testes
Rodar localmente com:
```bash
pytest  
```
- Rodar dentro do container Docker de testes:
```bash
docker compose -f docker-compose.test.yml up --build
```
Testes cobrem processamento de arquivos, múltiplos parágrafos, arquivos vazios, inexistentes, e validação da saída.
