from data.database import Database
from domain.logic import parse_decimal, calcular_custo_por_porcao

# Instanciar banco
db = Database()

# Criar uma receita
ok, msg = db.insert_receita("Bolo Simples", 10)  # rendimento = 10 porções
print(msg)

# Inserir ingredientes com preço e quantidade de pacote
ok_preco, preco = parse_decimal("6,50")  # aceita vírgula
ok_qtd, qtd = parse_decimal("1000")      # pacote de 1000 ml
if ok_preco and ok_qtd:
    ok, msg = db.insert_ingrediente("Leite", "ml", preco, qtd)
    print(msg)

ok_preco, preco = parse_decimal("7.00")
ok_qtd, qtd = parse_decimal("2000")      # pacote de 2000 g
if ok_preco and ok_qtd:
    ok, msg = db.insert_ingrediente("Açúcar", "g", preco, qtd)
    print(msg)

# Adicionar ingredientes à receita
db.add_ingrediente_na_receita(1, 1, 200)   # 200 ml de leite
db.add_ingrediente_na_receita(1, 2, 300)   # 300 g de açúcar

# Buscar dados crus
ok, receitas = db.list_receitas()
ok, ingredientes = db.list_ingredientes_da_receita(1)

# Calcular custo usando logic.py
if ok and receitas:
    receita_dict = {"rendimento": receitas[0]["rendimento"]}
    ok, resultado = calcular_custo_por_porcao(receita_dict, ingredientes)
    if ok:
        print("Custo total:", resultado["custo_total"])
        print("Custo por porcao:", resultado["custo_por_porcao"])
    else:
        print("Erro:", resultado)

db.close()
