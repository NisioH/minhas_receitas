import sqlite3

DB_NAME = "minhas_receitas.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ingredientes (
            id_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_ingrediente TEXT NOT NULL,
            unidade_ingrediente TEXT NOT NULL CHECK(unidade_ingrediente IN ('ml','g','und')),
            preco_pacote REAL NOT NULL,
            quantidade_pacote REAL NOT NULL CHECK(quantidade_pacote > 0)
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Receitas (
            id_receita INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_receita TEXT NOT NULL,
            rendimento INTEGER NOT NULL CHECK(rendimento > 0)
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Receita_Ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_receita INTEGER NOT NULL,
            id_ingrediente INTEGER NOT NULL,
            quantidade REAL NOT NULL CHECK(quantidade >= 0),
            FOREIGN KEY(id_receita) REFERENCES Receitas(id_receita) ON DELETE CASCADE,
            FOREIGN KEY(id_ingrediente) REFERENCES Ingredientes(id_ingrediente)
        );
        """)

        self.conn.commit()

    def insert_ingrediente(self, nome, unidade, preco_pacote, quantidade_pacote):
        try:
            self.cursor.execute("""
                INSERT INTO Ingredientes (nome_ingrediente, unidade_ingrediente, preco_pacote, quantidade_pacote)
                VALUES (?, ?, ?, ?)
            """, (nome, unidade, preco_pacote, quantidade_pacote))
            self.conn.commit()
            return True, "Ingrediente inserido com sucesso!"
        except Exception as e:
            return False, f"Erro ao inserir: {e}"

    def list_ingredientes(self):
        try:
            self.cursor.execute("SELECT * FROM Ingredientes")
            rows = self.cursor.fetchall()
            ingredientes = [
                {
                    "id": r[0],
                    "nome": r[1],
                    "unidade": r[2],
                    "preco_pacote": r[3],
                    "quantidade_pacote": r[4]
                }
                for r in rows
            ]
            return True, ingredientes
        except Exception as e:
            return False, f"Erro ao listar: {e}"

    def update_ingrediente(self, id_ingrediente, nome, unidade, preco_pacote, quantidade_pacote):
        try:
            self.cursor.execute("""
                UPDATE Ingredientes
                SET nome_ingrediente = ?, unidade_ingrediente = ?, preco_pacote = ?, quantidade_pacote = ?
                WHERE id_ingrediente = ?
            """, (nome, unidade, preco_pacote, quantidade_pacote, id_ingrediente))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False, "Ingrediente não encontrado."
            return True, "Ingrediente atualizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar ingrediente: {e}"

    def delete_ingrediente(self, id_ingrediente):
        try:
            self.cursor.execute("DELETE FROM Ingredientes WHERE id_ingrediente = ?", (id_ingrediente,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False, "Ingrediente não encontrado."
            return True, "Ingrediente excluído com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir ingrediente: {e}"

    def insert_receita(self, nome, rendimento):
        try:
            self.cursor.execute("""
                INSERT INTO Receitas (nome_receita, rendimento)
                VALUES (?, ?)
            """, (nome, rendimento))
            self.conn.commit()
            return True, "Receita inserida com sucesso!"
        except Exception as e:
            return False, f"Erro ao inserir receita: {e}"

    def list_receitas(self):
        try:
            self.cursor.execute("SELECT * FROM Receitas")
            rows = self.cursor.fetchall()
            receitas = [
                {
                    "id": r[0],
                    "nome": r[1],
                    "rendimento": r[2]
                }
                for r in rows
            ]
            return True, receitas
        except Exception as e:
            return False, f"Erro ao listar receitas: {e}"

    def update_receita(self, id_receita, nome, rendimento):
        try:
            self.cursor.execute("""
                UPDATE Receitas
                SET nome_receita = ?, rendimento = ?
                WHERE id_receita = ?
            """, (nome, rendimento, id_receita))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False, "Receita não encontrada."
            return True, "Receita atualizada com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar receita: {e}"

    def delete_receita(self, id_receita):
        try:
            self.cursor.execute("DELETE FROM Receitas WHERE id_receita = ?", (id_receita,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False, "Receita não encontrada."
            return True, "Receita excluída com sucesso!"
        except Exception as e:
            return False, f"Erro ao excluir receita: {e}"

    def add_ingrediente_na_receita(self, id_receita, id_ingrediente, quantidade):
        try:
            self.cursor.execute("""
                INSERT INTO Receita_Ingredientes (id_receita, id_ingrediente, quantidade)
                VALUES (?, ?, ?)
            """, (id_receita, id_ingrediente, quantidade))
            self.conn.commit()
            return True, "Ingrediente adicionado à receita!"
        except Exception as e:
            return False, f"Erro ao adicionar ingrediente na receita: {e}"

    def list_ingredientes_da_receita(self, id_receita):
        try:
            self.cursor.execute("""
                SELECT i.id_ingrediente, i.nome_ingrediente, ri.quantidade,
                       i.unidade_ingrediente, i.preco_pacote, i.quantidade_pacote
                FROM Receita_Ingredientes ri
                JOIN Ingredientes i ON ri.id_ingrediente = i.id_ingrediente
                WHERE ri.id_receita = ?
            """, (id_receita,))
            rows = self.cursor.fetchall()
            ingredientes = [
                {
                    "id": r[0],
                    "nome": r[1],
                    "quantidade": r[2],
                    "unidade": r[3],
                    "preco_pacote": r[4],
                    "quantidade_pacote": r[5]
                }
                for r in rows
            ]
            return True, ingredientes
        except Exception as e:
            return False, f"Erro ao listar ingredientes da receita: {e}"

    def delete_ingrediente_da_receita(self, id_receita, id_ingrediente):
        try:
            self.cursor.execute("""
                DELETE FROM Receita_Ingredientes
                WHERE id_receita = ? AND id_ingrediente = ?
            """, (id_receita, id_ingrediente))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False, "Ingrediente não encontrado na receita."
            return True, "Ingrediente removido da receita!"
        except Exception as e:
            return False, f"Erro ao remover ingrediente da receita: {e}"

    def close(self):
        self.conn.close()
