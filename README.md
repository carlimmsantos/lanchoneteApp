# LanchoneteApp

Bem-vindo ao **LanchoneteApp**, um aplicativo para gerenciar pedidos e o funcionamento de uma lanchonete. Este projeto foi desenvolvido para facilitar o controle de pedidos, cardápio e pagamentos.

## Funcionalidades

- **Gerenciamento de Cardápio**: Adicione, edite ou remova itens do cardápio.
- **Registro de Pedidos**: Crie e acompanhe pedidos em tempo real.
- **Controle de Pagamentos**: Registre pagamentos e calcule o total de cada pedido.
- **Relatórios**: Gere relatórios de vendas e desempenho.

## Tecnologias Utilizadas

- **Frontend**: Flet  
- **Backend**: Django Ninja  
- **Banco de Dados**: SQLite  
- **Linguagem**: Python  
- **Gerenciador de Dependências**: `pip`

## Como Executar o Projeto

1. Clone este repositório:
    ```bash
    git clone https://github.com/carlimmsantos/lanchoneteApp.git
    ```
2. Acesse o diretório do projeto:
    ```bash
    cd lanchoneteApp
    ```
3. Instale as dependências listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
4. Acesse a pasta do backend:
    ```bash
    cd backend
    ```
5. Aplique as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```
6. Inicie o servidor:
    ```bash
    python manage.py runserver
    ```

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
    ```bash
    git checkout -b minha-feature
    ```
3. Faça commit das suas alterações:
    ```bash
    git commit -m "Adiciona nova funcionalidade"
    ```
4. Envie para o repositório remoto:
    ```bash
    git push origin minha-feature
    ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---
**Desenvolvido por Carlos Freitas e Pedro Santana**