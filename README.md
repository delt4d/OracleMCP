# MCP Sankhya Community Search Server

Servidor MCP (Model Context Protocol) em Python 3 que permite a modelos de IA pesquisar e ler tópicos na **Comunidade Sankhya** — discussões onde desenvolvedores resolvem problemas técnicos, personalizações e erros do sistema.

---

## Estrutura do Projeto

```
mcp-sankhya/
├── mcp_server.py           # Ponto de entrada: inicializa o servidor e registra as tools
├── requirements.txt        # Dependências do projeto (inclui pytest para testes)
├── .gitignore
│
├── src/                    # Módulos de negócio (testáveis isoladamente)
│   ├── __init__.py
│   ├── comunidade_sankhya.py   # Pesquisa de tópicos via Selenium + BeautifulSoup
│   └── leitor_paginas.py       # Leitura e limpeza de conteúdo de posts
│
├── tests/                  # Testes unitários
│   ├── __init__.py
│   ├── test_comunidade_sankhya.py
│   └── test_leitor_paginas.py
│
├── config/                 # Configurações de ambiente (ex.: .env, claude_desktop_config)
└── docs/                   # Documentação complementar
```

---

## Pré-requisitos

- Python 3.10+
- Microsoft Edge instalado (para o Selenium headless na busca)
- Microsoft Edge WebDriver compatível com a versão do Edge instalada

---

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd mcp-sankhya

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## Executar o Servidor MCP

```bash
# Modo padrão (stdio — integração com Claude Desktop)
python mcp_server.py

# Modo rede (HTTP/SSE)
fastmcp run mcp_server.py --transport sse
```

---

## Testar Módulos Individualmente

Cada módulo pode ser executado diretamente para validação manual:

```bash
# Pesquisar tópicos na comunidade
python -m src.comunidade_sankhya "nota fiscal"

# Ler e limpar conteúdo de um post
python -m src.leitor_paginas "https://community.sankhya.com.br/wms/post/slug-do-post"
```

---

## Executar os Testes

```bash
pytest tests/ -v
```

---

## Ferramentas MCP Disponíveis

| Ferramenta | Descrição |
|---|---|
| `pesquisar_comunidade` | Pesquisa tópicos/discussões por termo. Retorna título, URL e resumo dos resultados. |
| `acessar_postagem_comunidade` | Acessa um post específico e retorna o conteúdo limpo (sem menus/rodapés). Restrito a `community.sankhya.com.br`. |
| `obter_respostas` | Busca respostas/replies de um post por ID, com paginação (`limit` e `after`). |

---

## Configuração no Claude Desktop

Adicione ao seu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sankhya-community": {
      "command": "python",
      "args": ["C:/caminho/para/mcp-sankhya/mcp_server.py"]
    }
  }
}
```

---

## Rotas da Comunidade Sankhya

| Destino | URL |
|---|---|
| Home | `https://community.sankhya.com.br/` |
| Pesquisa | `https://community.sankhya.com.br/search?query={TERMO}&type=posts&expanded=posts` |
| Post | `https://community.sankhya.com.br/wms/post/{SLUG}` |