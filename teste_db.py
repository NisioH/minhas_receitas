from data.database import Database
from domain.logic import parse_decimal, calcular_custo_por_porcao

db = Database()

ok, msg = db.insert_receita("Bolo Simples", 10) 
print(msg)

ok_preco, preco = parse_decimal("6,50")  
ok_qtd, qtd = parse_decimal("1000")     
if ok_preco and ok_qtd:
    ok, msg = db.insert_ingrediente("Leite", "ml", preco, qtd)
    print(msg)

ok_preco, preco = parse_decimal("7.00")
ok_qtd, qtd = parse_decimal("2000")      
if ok_preco and ok_qtd:
    ok, msg = db.insert_ingrediente("Açúcar", "g", preco, qtd)
    print(msg)

db.add_ingrediente_na_receita(1, 1, 200)   
db.add_ingrediente_na_receita(1, 2, 300)  

ok, receitas = db.list_receitas()
ok, ingredientes = db.list_ingredientes_da_receita(1)

if ok and receitas:
    receita_dict = {"rendimento": receitas[0]["rendimento"]}
    ok, resultado = calcular_custo_por_porcao(receita_dict, ingredientes)
    if ok:
        print("Custo total:", resultado["custo_total"])
        print("Custo por porcao:", resultado["custo_por_porcao"])
    else:
        print("Erro:", resultado)

db.close()
