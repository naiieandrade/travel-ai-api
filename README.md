# Travel AI API

API inteligente para criação e validação de roteiros de viagem.

## Objetivo

Este projeto foi desenvolvido para a disciplina de Construção de APIs para Inteligência Artificial.

A API disponibiliza três serviços:

1. Classificação de perfil de viagem
2. Geração de roteiro personalizado
3. Validação de viabilidade do roteiro

## Equipe

- [x] Camila Melo
- [x] Naiara Andrade 


## Tecnologias

- FastAPI
- Pydantic
- Uvicorn
- Pytest
- API Key
- Docker
- Ollama

## Como executar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload
```

Acesse a documentação:

```text
http://localhost:8000/docs
```

## Autenticação

Todos os endpoints principais exigem o header:

```text
X-API-Key: travel-api-key
```

## Executar com Docker

```bash
docker build -t travel-ai-api .
docker run -p 8000:8000 --env-file .env travel-ai-api
```

## Executar testes

```bash
pytest
```

## Endpoints

### 1. Classificar perfil

```http
POST /api/v1/travel-profile/classify
```

Exemplo:

```json
{
  "preferencias": ["trilhas", "cachoeiras", "rapel"],
  "ritmo": "intenso",
  "orcamento": "medio",
  "companhia": "amigos"
}
```

### 2. Gerar roteiro

```http
POST /api/v1/itinerary/generate
```

Exemplo:

```json
{
  "destino": "Chapada dos Veadeiros",
  "dias": 4,
  "perfil": "aventura",
  "orcamento": "medio",
  "preferencias": ["trilhas", "cachoeiras", "gastronomia local"],
  "ritmo": "intenso"
}
```

### 3. Validar roteiro

```http
POST /api/v1/itinerary/validate
```

Exemplo:

```json
{
  "destino": "Rio de Janeiro",
  "dias": 1,
  "perfil": "relaxamento",
  "ritmo": "leve",
  "atividades": [
    "Trilha Pedra da Gávea",
    "Cristo Redentor",
    "Pão de Açúcar",
    "Museu do Amanhã"
  ]
}
```

## Boas práticas implementadas

- Versionamento de API com `/api/v1`
- Validação de entrada com Pydantic
- Tratamento de erros HTTP
- Logs de execução
- Segurança via API Key
- Documentação automática com Swagger
- Testes automatizados
- Dockerfile para execução em outro computador
