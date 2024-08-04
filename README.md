# Dog API Server

Este projeto é um servidor REST que permite a interação com uma API de terceiros para gerenciar raças de cães e favoritos de imagens de cães. A API é construída usando Flask e oferece suporte a operações básicas para adicionar, listar e gerenciar informações sobre raças e imagens favoritas.

## Estrutura do Projeto

O projeto é dividido em três partes principais:

1. **Servidor REST API**: Implementado em Flask, fornece endpoints para gerenciar raças de cães e favoritos.
2. **Cliente Web**: Aplicação simples em Python que se comunica com a API REST para listar e adicionar favoritos.
3. **Cliente Mobile**: Aplicação móvel em Kivy que permite aos usuários interagir com a API REST para adicionar e visualizar favoritos.

## Requisitos

- Python 3.7 ou superior
- Flask
- Requests
- Protobuf
- dicttoxml
- Kivy (para o cliente móvel)

## Configuração

### Servidor REST

1. Servidor
Função: Serve como o backend da aplicação, fornecendo uma API RESTful para gerenciar raças de cachorros e imagens favoritas.

Endpoints Principais:

/breeds:
GET: Obtém a lista de raças de cachorros da API externa (dog.ceo).
POST: Adiciona uma nova raça ao banco de dados simulado.
/breeds/{breed_id}:
GET: Obtém detalhes de uma raça específica.
PUT: Atualiza informações de uma raça específica.
DELETE: Remove uma raça específica do banco de dados.
/favorites:
POST: Adiciona uma nova imagem aos favoritos.
GET: Obtém a lista de imagens favoritas.

### Cliente Web
Função: Interface web para visualizar e adicionar favoritos.

Tecnologias Usadas:

Flask: Framework para criar a aplicação web.
HTML: Para a estrutura da página web.
Funcionalidades:

Adicionar Favorito: Permite que os usuários adicionem URLs de imagens aos favoritos.
Visualizar Favoritos: Exibe uma lista de URLs de imagens favoritas como links clicáveis.

### Cliente Móvel (Kivy)
Função: Aplicação móvel para gerenciar e visualizar favoritos.

Tecnologias Usadas:

Kivy: Framework para criar a interface gráfica móvel.
Funcionalidades:

Adicionar Favorito: Permite que os usuários adicionem URLs de imagens aos favoritos.
Atualizar Lista de Favoritos: Exibe a lista de favoritos como URLs.

### Instalação e Execução

Servidor Flask:

Instale as dependências e execute o servidor Flask para fornecer a API.
Cliente Web:

Instale as dependências e execute a aplicação Flask para servir a interface web.
Cliente Móvel:

Instale as dependências e execute a aplicação Kivy para gerenciar favoritos.

## Documento de especifiações

openapi.yaml
