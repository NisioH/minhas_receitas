from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout

from data.database import Database
from domain.logic import parse_decimal, validar_unidade

class IngredienteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        # Layout vertical centralizado
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40)
        layout.size_hint = (0.8, None)
        layout.height = 400
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Campos
        self.nome = MDTextField(hint_text="Nome do ingrediente")
        self.unidade = MDTextField(hint_text="Unidade (ml/g/und)")
        self.preco = MDTextField(hint_text="Preço do pacote (ex: 6,50)")
        self.qtd_pacote = MDTextField(hint_text="Quantidade do pacote (ex: 1000)")

        # Botão
        salvar_btn = MDRaisedButton(text="Salvar", pos_hint={"center_x": 0.5})
        salvar_btn.bind(on_release=self.salvar)

        # Adiciona widgets ao layout
        layout.add_widget(self.nome)
        layout.add_widget(self.unidade)
        layout.add_widget(self.preco)
        layout.add_widget(self.qtd_pacote)
        layout.add_widget(salvar_btn)

        # Adiciona layout à tela
        self.add_widget(layout)

    def salvar(self, *args):
        nome = self.nome.text.strip()
        unidade = self.unidade.text.strip()

        ok_preco, preco = parse_decimal(self.preco.text)
        ok_qtd, qtd = parse_decimal(self.qtd_pacote.text)

        if not nome or not unidade:
            Snackbar(text="Preencha todos os campos!").open()
            return

        if not validar_unidade(unidade):
            Snackbar(text="Unidade inválida (use ml, g ou und)").open()
            return

        if not ok_preco or not ok_qtd:
            Snackbar(text="Preço ou quantidade inválidos").open()
            return

        ok, msg = self.db.insert_ingrediente(nome, unidade, preco, qtd)
        Snackbar(text=msg).open()


class ReceitasApp(MDApp):
    def build(self):
        return IngredienteScreen()

ReceitasApp().run()
