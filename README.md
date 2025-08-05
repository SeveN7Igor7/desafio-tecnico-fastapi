# API de Formulários Dinâmicos

Sistema de formulários dinâmicos desenvolvido com FastAPI, SQLAlchemy e PostgreSQL, permitindo que usuários criem e gerenciem formulários com perguntas personalizadas.

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construção de APIs
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI para aplicações Python

## Funcionalidades

### CRUD Completo
- **Formulários**: Criar, listar, obter, atualizar e deletar formulários
- **Perguntas**: Criar, listar, obter, atualizar e deletar perguntas
- **Opções de Respostas**: Gerenciar opções de resposta para perguntas

### Recursos Avançados
- **Filtros**: Filtrar perguntas por tipo, obrigatoriedade, formulário, etc.
- **Ordenação**: Ordenar resultados por diferentes campos (id, título, ordem)
- **Paginação**: Navegação eficiente através de grandes conjuntos de dados
- **Validação**: Validação automática de dados de entrada
- **Documentação**: Documentação automática da API com Swagger/OpenAPI

## Estrutura do Projeto

```
formularios_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação principal
│   ├── database/
│   │   └── database.py         # Configuração do banco de dados
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # Modelos SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Schemas Pydantic
│   └── routers/
│       ├── __init__.py
│       ├── formularios.py      # Endpoints de formulários
│       ├── perguntas.py        # Endpoints de perguntas
│       └── opcoes_respostas.py # Endpoints de opções de resposta
├── venv/                       # Ambiente virtual Python
├── .env                        # Variáveis de ambiente (não versionado)
├── .env.example               # Exemplo de variáveis de ambiente
├── requirements.txt           # Dependências do projeto
└── README.md                  # Este arquivo
```

## Instalação e Configuração

Para executar este projeto, você precisará ter o Python e o PostgreSQL instalados em seu sistema. Siga os passos abaixo para configurar o ambiente.

### Pré-requisitos

- **Python 3.11 ou superior**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 12 ou superior**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads/)
- **Postman (Opcional)**: [Download Postman](https://www.postman.com/downloads/)

### Passo a Passo Detalhado

#### 1. Clone o repositório

Abra seu terminal (ou PowerShell no Windows) e execute o comando:

```bash
git clone <url-do-repositorio>
cd formularios_api
```

#### 2. Crie e ative o ambiente virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto. Isso evita conflitos com outras instalações Python em seu sistema.

**No Linux/macOS:**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

**No Windows (Prompt de Comando ou PowerShell):**

```cmd
python -m venv venv
```

Para ativar o ambiente virtual no Windows:

**No Prompt de Comando:**
```cmd
venv\Scripts\activate.bat
```

**No PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

Após a ativação, você verá `(venv)` no início da linha de comando, indicando que o ambiente virtual está ativo.

#### 3. Instale as dependências do projeto

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

#### 4. Configure o PostgreSQL

You precisará de uma instância do PostgreSQL rodando e um banco de dados configurado para o projeto.

##### Instalação do PostgreSQL

- **No Ubuntu/Debian:**
  Abra o terminal e execute:
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ```

- **No Windows:**
  Baixe o instalador do PostgreSQL no [site oficial](https://www.postgresql.org/download/windows/). Siga as instruções do instalador. Durante a instalação, você será solicitado a definir uma senha para o usuário `postgres`. Lembre-se dessa senha.

##### Configuração do Banco de Dados e Usuário

Vamos criar um usuário e um banco de dados específicos para a aplicação. Por padrão, o PostgreSQL cria um usuário `postgres` com privilégios de superusuário.

**No Linux/macOS:**

```bash
# Inicie o serviço PostgreSQL (se não estiver rodando)
sudo systemctl start postgresql
sudo systemctl enable postgresql # Para iniciar automaticamente no boot

# Acesse o terminal do PostgreSQL como usuário postgres
sudo -u postgres psql

# Dentro do psql, execute os seguintes comandos:
CREATE USER usuario WITH PASSWORD 'senha';
CREATE DATABASE formularios_db OWNER usuario;
GRANT ALL PRIVILEGES ON DATABASE formularios_db TO usuario;
\q # Para sair do psql
```

**No Windows:**

1. Abra o **SQL Shell (psql)** que foi instalado com o PostgreSQL. Ele pedirá as seguintes informações:
   - Server: `localhost` (ou o IP do seu servidor PostgreSQL)
   - Database: `postgres` (o banco de dados padrão)
   - Port: `5432` (a porta padrão)
   - Username: `postgres`
   - Password: Digite a senha que você definiu para o usuário `postgres` durante a instalação.

2. Uma vez conectado ao `psql`, execute os seguintes comandos para criar o usuário e o banco de dados:

   ```sql
   CREATE USER usuario WITH PASSWORD 'senha';
   CREATE DATABASE formularios_db OWNER usuario;
   GRANT ALL PRIVILEGES ON DATABASE formularios_db TO usuario;
   \q -- Para sair do psql
   ```

   **Importante**: O `usuario` e `senha` aqui são apenas exemplos. Você pode usar outros nomes, mas certifique-se de que eles correspondam às configurações no arquivo `.env`.

#### 5. Configure as variáveis de ambiente

O projeto utiliza um arquivo `.env` para gerenciar as variáveis de ambiente, como as credenciais do banco de dados. Você encontrará um arquivo de exemplo chamado `.env.example`.

1. Copie o arquivo `.env.example` para `.env`:

   **No Linux/macOS:**
   ```bash
   cp .env.example .env
   ```

   **No Windows (Prompt de Comando ou PowerShell):**
   ```cmd
   copy .env.example .env
   ```

2. Edite o arquivo `.env` com suas configurações. Certifique-se de que o `DATABASE_URL` corresponda ao usuário e senha que você criou no PostgreSQL.

   ```env
   # Configurações do Banco de Dados PostgreSQL
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/formularios_db

   # Configurações da Aplicação
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

#### 6. Execute a aplicação

Com o ambiente virtual ativo e as variáveis de ambiente configuradas, você pode iniciar a API:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- O parâmetro `--reload` fará com que o servidor reinicie automaticamente ao detectar mudanças no código.
- O parâmetro `--host 0.0.0.0` permite que a aplicação seja acessível de outras máquinas na mesma rede (útil para testes).

A aplicação estará disponível em: `http://localhost:8000`

### Verificação da Instalação

Após iniciar a aplicação, acesse os seguintes endpoints em seu navegador para verificar se tudo está funcionando corretamente:

- **API Root**: `http://localhost:8000/`
- **Health Check**: `http://localhost:8000/health`
- **Documentação Interativa (Swagger UI)**: `http://localhost:8000/docs`
- **Documentação Alternativa (ReDoc)**: `http://localhost:8000/redoc`


## Documentação da API

### Endpoints Principais

#### Formulários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/formularios/` | Criar novo formulário |
| GET | `/formularios/` | Listar todos os formulários |
| GET | `/formularios/{id}` | Obter formulário específico |
| PUT | `/formularios/{id}` | Atualizar formulário |
| DELETE | `/formularios/{id}` | Deletar formulário |

#### Perguntas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/perguntas/` | Criar nova pergunta |
| GET | `/perguntas/` | Listar perguntas com filtros |
| GET | `/perguntas/paginated` | Listar perguntas com paginação detalhada |
| GET | `/perguntas/{id}` | Obter pergunta específica |
| PUT | `/perguntas/{id}` | Atualizar pergunta |
| DELETE | `/perguntas/{id}` | Deletar pergunta |
| GET | `/perguntas/formulario/{formulario_id}` | Listar perguntas de um formulário |

#### Opções de Respostas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/opcoes-respostas/` | Criar nova opção de resposta |
| GET | `/opcoes-respostas/pergunta/{pergunta_id}` | Listar opções de uma pergunta |
| GET | `/opcoes-respostas/{id}` | Obter opção específica |
| PUT | `/opcoes-respostas/{id}` | Atualizar opção |
| DELETE | `/opcoes-respostas/{id}` | Deletar opção |

### Filtros e Parâmetros

#### Filtros para Perguntas
- `formulario_id`: Filtrar por ID do formulário
- `tipo_pergunta`: Filtrar por tipo de pergunta
- `obrigatoria`: Filtrar por obrigatoriedade (true/false)
- `sub_pergunta`: Filtrar por sub-pergunta (true/false)

#### Ordenação
- `order_by`: Campo para ordenação (id, titulo, ordem)
- `order_direction`: Direção da ordenação (asc, desc)

#### Paginação
- `page`: Número da página (padrão: 1)
- `size`: Tamanho da página (padrão: 10, máximo: 100)

### Tipos de Pergunta Suportados

- `Sim_Não`: Pergunta de sim ou não
- `multipla_escolha`: Múltipla escolha
- `unica_escolha`: Escolha única
- `texto_livre`: Texto livre
- `Inteiro`: Número inteiro
- `Numero com duas casa decimais`: Número decimal


## Exemplos de Uso

Você pode testar os endpoints da API usando ferramentas como `curl` (disponível no Linux/macOS e no PowerShell do Windows) ou o **Postman** (recomendado para uma interface mais amigável). A interface interativa do Swagger UI (`http://localhost:8000/docs`) também é uma ótima opção.

### Usando o Postman

Para usar o Postman, siga estes passos:

1.  Abra o Postman.
2.  Crie uma nova requisição clicando em `+` ou `New > HTTP Request`.
3.  Selecione o método HTTP (GET, POST, PUT, DELETE).
4.  Insira a URL do endpoint (ex: `http://localhost:8000/formularios/`).
5.  Para requisições `POST` ou `PUT`, selecione a aba `Body`, escolha `raw` e `JSON` no dropdown. Insira o JSON da requisição.
6.  Clique em `Send` para enviar a requisição.

#### 1. Criar um Formulário (POST)

- **Método**: `POST`
- **URL**: `http://localhost:8000/formularios/`
- **Headers**: `Content-Type: application/json`
- **Body (raw, JSON)**:

```json
{
  "titulo": "Pesquisa de Satisfação",
  "descricao": "Formulário para avaliar a satisfação do cliente",
  "ordem": 1
}
```

**Resposta de Exemplo (Status 201 Created):**
```json
{
  "id": 1,
  "titulo": "Pesquisa de Satisfação",
  "descricao": "Formulário para avaliar a satisfação do cliente",
  "ordem": 1,
  "perguntas": []
}
```

#### 2. Criar uma Pergunta (POST)

- **Método**: `POST`
- **URL**: `http://localhost:8000/perguntas/`
- **Headers**: `Content-Type: application/json`
- **Body (raw, JSON)**:

```json
{
  "titulo": "Qual é o seu nome?",
  "codigo": "NOME",
  "orientacao_resposta": "Digite seu nome completo",
  "ordem": 1,
  "obrigatoria": true,
  "sub_pergunta": false,
  "tipo_pergunta": "texto_livre",
  "id_formulario": 1
}
```

**Resposta de Exemplo (Status 201 Created):**
```json
{
  "id": 1,
  "titulo": "Qual é o seu nome?",
  "codigo": "NOME",
  "orientacao_resposta": "Digite seu nome completo",
  "ordem": 1,
  "obrigatoria": true,
  "sub_pergunta": false,
  "tipo_pergunta": "texto_livre",
  "id_formulario": 1,
  "opcoes_respostas": []
}
```

#### 3. Listar Perguntas com Filtros (GET)

- **Método**: `GET`
- **URL**: `http://localhost:8000/perguntas/?formulario_id=1&obrigatoria=true&order_by=ordem&order_direction=asc&page=1&size=10`

**Resposta de Exemplo (Status 200 OK):**
```json
[
  {
    "titulo": "Qual é o seu nome?",
    "codigo": "NOME",
    "orientacao_resposta": "Digite seu nome completo",
    "ordem": 1,
    "obrigatoria": true,
    "sub_pergunta": false,
    "tipo_pergunta": "texto_livre",
    "id": 1,
    "id_formulario": 1
  }
]
```

#### 4. Criar Opção de Resposta (POST)

- **Método**: `POST`
- **URL**: `http://localhost:8000/opcoes-respostas/`
- **Headers**: `Content-Type: application/json`
- **Body (raw, JSON)**:

```json
{
  "resposta": "Muito Satisfeito",
  "ordem": 1,
  "resposta_aberta": false,
  "id_pergunta": 2
}
```

**Resposta de Exemplo (Status 201 Created):**
```json
{
  "id": 1,
  "resposta": "Muito Satisfeito",
  "ordem": 1,
  "resposta_aberta": false,
  "id_pergunta": 2
}
```

#### 5. Obter Formulário Completo (GET)

- **Método**: `GET`
- **URL**: `http://localhost:8000/formularios/1`

**Resposta de Exemplo (Status 200 OK):**
```json
{
  "id": 1,
  "titulo": "Pesquisa de Satisfação",
  "descricao": "Formulário para avaliar a satisfação do cliente",
  "ordem": 1,
  "perguntas": [
    {
      "id": 1,
      "titulo": "Qual é o seu nome?",
      "codigo": "NOME",
      "orientacao_resposta": "Digite seu nome completo",
      "ordem": 1,
      "obrigatoria": true,
      "sub_pergunta": false,
      "tipo_pergunta": "texto_livre",
      "id_formulario": 1,
      "opcoes_respostas": []
    }
  ]
}
```

### Usando cURL (Alternativa)

Os exemplos abaixo são equivalentes aos do Postman e podem ser executados diretamente no terminal.

#### 1. Criar um Formulário

```bash
curl -X POST "http://localhost:8000/formularios/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Pesquisa de Satisfação",
    "descricao": "Formulário para avaliar a satisfação do cliente",
    "ordem": 1
  }'
```

#### 2. Criar uma Pergunta

```bash
curl -X POST "http://localhost:8000/perguntas/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Qual é o seu nome?",
    "codigo": "NOME",
    "orientacao_resposta": "Digite seu nome completo",
    "ordem": 1,
    "obrigatoria": true,
    "sub_pergunta": false,
    "tipo_pergunta": "texto_livre",
    "id_formulario": 1
  }'
```

#### 3. Listar Perguntas com Filtros

```bash
curl -X GET "http://localhost:8000/perguntas/?formulario_id=1&obrigatoria=true&order_by=ordem&order_direction=asc&page=1&size=10"
```

#### 4. Criar Opção de Resposta

```bash
curl -X POST "http://localhost:8000/opcoes-respostas/" \
  -H "Content-Type: application/json" \
  -d '{
    "resposta": "Muito Satisfeito",
    "ordem": 1,
    "resposta_aberta": false,
    "id_pergunta": 2
  }'
```

#### 5. Obter Formulário Completo

```bash
curl -X GET "http://localhost:8000/formularios/1"
```

## Estrutura do Banco de Dados

### Tabelas

#### `formulario`
- `id` (INTEGER, PK): Identificador único do formulário.
- `titulo` (VARCHAR): Título do formulário.
- `descricao` (VARCHAR): Descrição detalhada do formulário.
- `ordem` (INTEGER): Ordem de exibição do formulário.

#### `pergunta`
- `id` (INTEGER, PK): Identificador único da pergunta.
- `id_formulario` (INTEGER, FK): Chave estrangeira que referencia o `id` do formulário ao qual a pergunta pertence.
- `titulo` (VARCHAR): Título da pergunta.
- `codigo` (VARCHAR): Código identificador da pergunta (opcional).
- `orientacao_resposta` (VARCHAR): Orientação ou instrução para a resposta da pergunta.
- `ordem` (INTEGER): Ordem de exibição da pergunta dentro do formulário.
- `obrigatoria` (BOOLEAN): Indica se a resposta a esta pergunta é obrigatória (True/False).
- `sub_pergunta` (BOOLEAN): Indica se esta é uma sub-pergunta (True/False).
- `tipo_pergunta` (ENUM): Tipo de resposta esperada para a pergunta (ex: 'Sim_Não', 'texto_livre').

#### `opcoes_respostas`
- `id` (INTEGER, PK): Identificador único da opção de resposta.
- `id_pergunta` (INTEGER, FK): Chave estrangeira que referencia o `id` da pergunta à qual esta opção pertence.
- `resposta` (VARCHAR): Texto da opção de resposta.
- `ordem` (INTEGER): Ordem de exibição da opção de resposta.
- `resposta_aberta` (BOOLEAN): Indica se esta opção permite uma resposta aberta (texto livre) além da seleção.

#### `opcoes_resposta_pergunta`
- `id` (INTEGER, PK): Identificador único da relação.
- `id_opcao_resposta` (INTEGER, FK): Chave estrangeira que referencia o `id` da opção de resposta.
- `id_pergunta` (INTEGER, FK): Chave estrangeira que referencia o `id` da pergunta.

### Relacionamentos

- **Formulário para Pergunta (1:N)**: Um formulário pode conter várias perguntas.
- **Pergunta para Opções de Respostas (1:N)**: Uma pergunta pode ter várias opções de resposta (para tipos como múltipla escolha).
- **Opções de Respostas para Pergunta (N:M)**: Existe uma tabela de junção (`opcoes_resposta_pergunta`) para gerenciar a relação entre perguntas e suas opções de resposta, permitindo flexibilidade em cenários mais complexos.

## Troubleshooting (Resolução de Problemas Comuns)

Se você encontrar algum problema ao configurar ou executar o projeto, consulte as soluções abaixo:

### 1. Erro de Conexão com o Banco de Dados (`sqlalchemy.exc.OperationalError`)

Este erro geralmente indica que a aplicação não conseguiu se conectar ao PostgreSQL.

**Mensagem de Erro Comum:**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost", port 5432 failed
```

**Soluções:**
- **Verifique se o serviço PostgreSQL está rodando:**
  - **Linux/macOS:** `sudo systemctl status postgresql`
  - **Windows:** Abra o "Gerenciador de Serviços" (Services) e procure por "postgresql". Certifique-se de que o status seja "Em execução" (Running).
- **Verifique as credenciais no arquivo `.env`:** Certifique-se de que o usuário, senha, host e porta estão corretos.
- **Teste a conexão manualmente:**
  - **Linux/macOS:** `psql -h localhost -U usuario -d formularios_db`
  - **Windows:** Use o SQL Shell (psql) para testar a conexão.

### 2. Erro de Importação de Módulos (`ModuleNotFoundError`)

**Mensagem de Erro Comum:**
```
ModuleNotFoundError: No module named 'app'
```

**Soluções:**
- **Certifique-se de estar no diretório raiz do projeto:** O comando `python -m uvicorn app.main:app` deve ser executado a partir do diretório `formularios_api/`.
- **Ative o ambiente virtual:**
  - **Linux/macOS:** `source venv/bin/activate`
  - **Windows (Prompt de Comando):** `venv\Scripts\activate.bat`
  - **Windows (PowerShell):** `. \venv\Scripts\Activate.ps1`
- **Reinstale as dependências:** `pip install -r requirements.txt`

### 3. Erro de Validação de Dados (`422 Unprocessable Entity`)

Este erro ocorre quando os dados enviados para a API não estão no formato esperado.

**Soluções:**
- **Verifique se todos os campos obrigatórios estão sendo enviados.**
- **Confirme se os tipos de dados estão corretos** (ex: números como inteiros, booleanos como true/false).
- **Consulte a documentação interativa** em `http://localhost:8000/docs` para ver o schema esperado para cada endpoint.

### 4. Porta já em uso (`OSError: [Errno 98] Address already in use`)

**Soluções:**
- **Mate o processo que está usando a porta:**
  - **Linux/macOS:** `sudo lsof -t -i tcp:8000 | xargs kill -9`
  - **Windows:** Use o Gerenciador de Tarefas para encerrar processos Python ou execute `netstat -ano | findstr :8000` para encontrar o PID e depois `taskkill /PID <PID> /F`
- **Use uma porta diferente:** `python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload`

### 5. Problemas com Ambiente Virtual no Windows PowerShell

Se você receber um erro relacionado à política de execução no PowerShell:

```
cannot be loaded because running scripts is disabled on this system
```

**Solução:**
Execute o PowerShell como Administrador e execute o comando:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 6. Erro de Instalação de Dependências (`pip install` falha)

**Soluções:**
- **Atualize o pip:** `python -m pip install --upgrade pip`
- **Use um mirror diferente:** `pip install -r requirements.txt -i https://pypi.org/simple/`
- **Instale as dependências uma por uma** para identificar qual está causando o problema.

### Logs e Debug

Para visualizar logs detalhados e identificar problemas, execute a aplicação com:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## Desenvolvimento

### Executando em Modo de Desenvolvimento

```bash
# Com reload automático (recomendado para desenvolvimento)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Com logs detalhados para debug
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Testando a API

A maneira mais fácil de testar a API é usando a documentação interativa:

1. **Swagger UI**: Acesse `http://localhost:8000/docs`
   - Interface interativa onde você pode testar todos os endpoints diretamente no navegador.
   - Mostra os schemas de entrada e saída para cada endpoint.
   - Permite executar requisições e ver as respostas em tempo real.

2. **ReDoc**: Acesse `http://localhost:8000/redoc`
   - Documentação alternativa com um layout mais limpo.
   - Ideal para leitura e compreensão da API.

### Adicionando Novas Funcionalidades

Se você quiser estender a API:

1. **Novos Modelos**: Adicione em `app/models/models.py`
2. **Novos Schemas**: Adicione em `app/schemas/schemas.py`
3. **Novos Endpoints**: Crie um novo arquivo em `app/routers/` e registre no `app/main.py`

## Comandos Úteis

### Comandos de Banco de Dados

```bash
# Conectar ao banco de dados
psql -h localhost -U usuario -d formularios_db

# Listar todas as tabelas
\dt

# Descrever uma tabela específica
\d formulario

# Sair do psql
\q
```

### Comandos Python

```bash
# Verificar versão do Python
python --version

# Listar pacotes instalados no ambiente virtual
pip list

# Gerar arquivo requirements.txt atualizado
pip freeze > requirements.txt

# Verificar se há atualizações para os pacotes
pip list --outdated
```

## Estrutura de Dados de Exemplo

Para ajudar no entendimento, aqui está um exemplo de como os dados se relacionam:

```json
{
  "formulario": {
    "id": 1,
    "titulo": "Pesquisa de Satisfação do Cliente",
    "descricao": "Avaliação da experiência do cliente com nossos serviços",
    "ordem": 1,
    "perguntas": [
      {
        "id": 1,
        "titulo": "Como você avalia nosso atendimento?",
        "codigo": "ATENDIMENTO",
        "orientacao_resposta": "Selecione uma das opções abaixo",
        "ordem": 1,
        "obrigatoria": true,
        "sub_pergunta": false,
        "tipo_pergunta": "unica_escolha",
        "opcoes_respostas": [
          {
            "id": 1,
            "resposta": "Excelente",
            "ordem": 1,
            "resposta_aberta": false
          },
          {
            "id": 2,
            "resposta": "Bom",
            "ordem": 2,
            "resposta_aberta": false
          },
          {
            "id": 3,
            "resposta": "Regular",
            "ordem": 3,
            "resposta_aberta": false
          },
          {
            "id": 4,
            "resposta": "Ruim",
            "ordem": 4,
            "resposta_aberta": false
          }
        ]
      },
      {
        "id": 2,
        "titulo": "Deixe seus comentários adicionais",
        "codigo": "COMENTARIOS",
        "orientacao_resposta": "Campo opcional para comentários livres",
        "ordem": 2,
        "obrigatoria": false,
        "sub_pergunta": false,
        "tipo_pergunta": "texto_livre",
        "opcoes_respostas": []
      }
    ]
  }
}
```

## Licença

Este projeto foi desenvolvido como parte de um desafio técnico para demonstração de habilidades em desenvolvimento backend com FastAPI, SQLAlchemy e PostgreSQL.


