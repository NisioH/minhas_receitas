# Minhas Receitas 🍰

Sistema de gerenciamento de receitas desenvolvido em **Python** com **KivyMD** e **SQLite**.

## 📌 Funcionalidades
- Cadastro de **ingredientes** com preço e quantidade de pacote.
- Cadastro de **receitas** com rendimento.
- Associação de ingredientes às receitas.
- Cálculo automático de **custo total** e **custo por porção**.
- Tratamento de valores com vírgula (ex.: `2,50` → `2.50`).

## 🛠️ Tecnologias
- Python 3.x
- SQLite
- KivyMD

## 🚀 Como executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/NisioH/minhas_receitas

2. Entre na pasta do projeto:
    ```bash
    cd minhas-receitas

3. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt

5. Execute o projeto:
    ```bash
    python main.py

## 📂 Estrutura do Projeto
    
    minhas-receitas/
    ├── data/
    │   └── database.py        # Classe Database (CRUD)
    ├── domain/
    │   └── logic.py           # Regras de negócio (validações e cálculos)
    ├── ui/
    │   └── ...                # Telas KivyMD
    ├── test_db.py             # Testes de banco e lógica
    ├── README.md
    └── .gitignor

## 📖 Exemplos
- Inserir ingrediente:
     ```
        db.insert_ingrediente("Leite", "ml", 6.50, 1000)

- Calcular custo por porção:
    ```
        receita = {"rendimento": 10}
        ingredientes = [
            {"quantidade": 200, "preco_pacote": 6.50, "quantidade_pacote": 1000},
            {"quantidade": 300, "preco_pacote": 7.00, "quantidade_pacote": 2000}
        ]
        ok, resultado = calcular_custo_por_porcao(receita, ingredientes)
        print(resultado)
