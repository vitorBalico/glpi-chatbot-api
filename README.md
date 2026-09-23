# GLPI Chatbot API

API em Python/FastAPI para integrar um chatbot ao GLPI e automatizar a abertura de chamados.

O projeto recebe os dados de um fluxo conversacional por HTTP, traduz as opções selecionadas em configurações do GLPI e registra o chamado pela API REST. No cenário de uso apresentado, o chatbot é construído no Landbot para atendimento pelo WhatsApp.

> **Escopo desta versão:** demonstração de integração e automação. Os mapas de categorias, entidades e localizações dependem de cada instalação do GLPI. Esta versão não deve ser exposta diretamente à internet sem as medidas descritas em Segurança e limitações.

## O problema e a solução

A proposta é transformar respostas de um chatbot em chamados estruturados, evitando o preenchimento manual repetido de categoria, entidade, urgência e localização no sistema de atendimento.

```text
Pessoa -> Chatbot / webhook -> API FastAPI -> API REST do GLPI -> Chamado
```

O repositório contém a API intermediária. O fluxo do chatbot, a conta do provedor e a instalação do GLPI são componentes externos e não estão incluídos.

## Funcionalidades implementadas

- Recebimento de solicitações por duas rotas HTTP.
- Consulta da existência de um requerente no GLPI.
- Roteamento por oito áreas, com categorias e subcategorias quando aplicáveis.
- Preenchimento de entidade, localização e urgência.
- Geração automática do título a partir da categoria e da subcategoria.
- Registro de chamados com tipo fixo **Requisição**.
- Leitura de credenciais por variáveis de ambiente.

A consulta de requerentes verifica um cadastro; ela **não autentica a identidade de quem está usando o chatbot**.

## Tecnologias

Python, FastAPI, Pydantic, Requests, python-dotenv e Uvicorn; integração com a API REST do GLPI e com um webhook do chatbot.

## Estrutura principal

```text
.
|-- main.py                  # Rotas, modelos e mapas de roteamento
|-- glpi.py                  # Integração com a API REST do GLPI
|-- listar_entidades.py      # Diagnóstico manual
|-- listar_grupos.py         # Diagnóstico manual
|-- listar_ids.py            # Diagnóstico manual
|-- teste_glpi.py            # Diagnóstico manual de conexão
|-- teste_usuario.py         # Diagnóstico manual de cadastro
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- README.md
```

Os scripts de diagnóstico não são uma suíte automatizada de testes. Eles podem consultar o GLPI e imprimir informações quando executados/importados; utilize somente credenciais de homologação e revise suas saídas.

## Configuração local para desenvolvimento

Use uma versão de Python compatível com as dependências fixadas no `requirements.txt`. Valide a instalação em ambiente limpo; copiar uma `venv` de outra máquina não substitui sua recriação.

No PowerShell, dentro da pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Edite o `.env` local com a URL e os tokens de **homologação**. Não publique este arquivo.

| Variável | Finalidade |
|---|---|
| `GLPI_URL` | URL base da API REST do GLPI, sem barra final. |
| `APP_TOKEN` | Token da aplicação autorizada no GLPI. |
| `USER_TOKEN` | Token de uma conta de integração com permissões mínimas necessárias. |

Ajuste os mapas em `main.py` para a instalação de testes: os números enviados pelo chatbot não são necessariamente os IDs reais do GLPI.

Os nomes das unidades nesta cópia são demonstrativos. Os IDs de categorias e entidades ainda dependem da instalação usada como referência. Não substitua a configuração da API de produção por estes mapas de portfólio.

Inicie o servidor apenas na interface local:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`. O modo `--reload` é para desenvolvimento.

## Contrato HTTP

### `POST /validar-usuario`

Exemplo fictício:

```json
{
  "requerente": "usuario.exemplo"
}
```

A resposta informa `valido`, `mensagem` e `usuario_id`. Na implementação atual, a busca aceita login, e-mail ou nome completo; não deve ser apresentada como autenticação ou como busca exclusiva por login.

### `POST /criar-chamado`

Exemplo fictício, a ser adaptado aos mapas de homologação:

```json
{
  "formulario": "1",
  "urgencia": "3",
  "categoria": "1",
  "subcategoria": "1",
  "localizacao": "21",
  "requerente": "usuario.exemplo",
  "descricao": "Solicitacao ficticia para demonstracao da integracao.",
  "teamviewer": null
}
```

`subcategoria` é necessária quando a categoria escolhida possui subcategorias. `localizacao` é obrigatória nesta versão. `teamviewer` é opcional. O campo opcional `titulo`, embora aceito pelo modelo, não substitui o título gerado automaticamente. O tipo do chamado é fixo em Requisição; não há seleção de tipo na rota atual.

Uma resposta de sucesso contém `mensagem` e `resultado` com a resposta do GLPI. Área, urgência, categoria ou subcategoria inválidas geram erro HTTP 400; campos obrigatórios ausentes são rejeitados pelo modelo da API.

## Segurança e limitações

Antes de uma implantação acessível externamente, é necessário:

- Autenticar e autorizar o chamador da API, ou documentar e validar uma camada externa que cumpra essa função. As duas rotas não possuem essa proteção no código atual.
- Configurar certificados confiáveis e remover `verify=False`; estabelecer timeouts nas chamadas HTTP.
- Rejeitar entradas vazias; revisar a busca de requerentes e eliminar correspondências parciais/ambíguas de localização.
- Manter logs sem tokens e sem dados completos de chamados/usuários; revisar as saídas dos scripts de diagnóstico e diferenciar falhas de comunicação de cadastros não encontrados.
- Implementar paginação, testes automatizados e tratamento consistente das falhas do GLPI.

Não inclua senhas, tokens, dados pessoais, `.env`, `venv`, backups, logs ou ZIPs da pasta de trabalho no repositório. Para portfólio, utilize dados fictícios, configurações demonstrativas e autorização de divulgação do trabalho.

## Demonstração sugerida

Uma gravação curta com dados fictícios pode mostrar: preenchimento do chatbot, envio ao webhook e chamado resultante em um GLPI de homologação. Não inclua tokens, endereços internos nem informações reais de pessoas.

Não foram incluídas métricas de economia de tempo, disponibilidade ou volume de chamados, pois elas precisam ser medidas antes de divulgadas.
