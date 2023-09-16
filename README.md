# API Status VPS

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://choosealicense.com/licenses/gpl-3.0/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](https://choosealicense.com/licenses/gpl-3.0/)

Este sistema foi desenvolvido por Sérgio Moreira Costa
Contato: WhatsApp +55 48 92000-4273

## Descrição

Este é um exemplo de uma API Flask que fornece informações sobre o sistema, processos gerenciados pelo PM2 e contêineres Docker em execução. Ele retorna um JSON com essas informações quando você acessa a rota `/api`.

## Principais Funções

- Fornecer informações sobre o sistema, incluindo uso de CPU e memória.
- Listar processos gerenciados pelo PM2.
- Listar contêineres Docker em execução.

## Modelo de Curl de Exemplo

Aqui está um exemplo de como você pode acessar a API usando o `curl`:

```bash
curl -u seu_usuario:sua_senha -X GET http://seu-servidor:porta/api
Substitua seu_usuario e sua_senha pelo seu nome de usuário e senha definidos para autenticação básica, e seu-servidor e porta pelo endereço e porta onde a API está hospedada.

Como Instalar
Para instalar as dependências do projeto, você pode usar o arquivo requirements.txt. Certifique-se de ter o Python e o pip instalados e execute o seguinte comando no diretório do projeto:

bash
Copy code
pip install -r requirements.txt
Como Executar na VPS
Para executar a aplicação na sua VPS, siga estas etapas:

Certifique-se de que o arquivo app.py esteja corretamente configurado com as rotas e a lógica do seu projeto.

Ative seu ambiente virtual (se você estiver usando um).

Execute a aplicação usando o Gunicorn ou qualquer servidor WSGI que você preferir. Por exemplo:

bash
Copy code
gunicorn -b 0.0.0.0:5000 app:app
Isso fará com que a aplicação esteja disponível na porta 5000 da sua VPS.

Agora, você pode acessar a API a partir do seu cliente, usando o modelo de comando curl fornecido anteriormente.
```
