from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem

from data.database import Database
from domain.logic import parse_decimal

class IngredienteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40)
        layout.size_hint = (0.8, None)
        layout.height = 450
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.nome = MDTextField(hint_text="Nome do ingrediente")
        self.preco = MDTextField(hint_text="Preço do pacote (ex: 6,50)")
        self.qtd_pacote = MDTextField(hint_text="Quantidade do pacote (ex: 1000)")

        self.unidade_btn = MDFlatButton(text="Selecionar unidade", pos_hint={"center_x": 0.5})
        self.unidade_selecionada = None

        menu_items = [
            {"viewclass": "OneLineListItem", "text": "ml", "on_release": lambda x="ml": self.set_unidade(x)},
            {"viewclass": "OneLineListItem", "text": "g", "on_release": lambda x="g": self.set_unidade(x)},
            {"viewclass": "OneLineListItem", "text": "und", "on_release": lambda x="und": self.set_unidade(x)},
        ]

        self.menu = MDDropdownMenu(caller=self.unidade_btn, items=menu_items, width_mult=3)
        self.unidade_btn.bind(on_release=lambda *args: self.menu.open())

        salvar_btn = MDRaisedButton(text="Salvar", pos_hint={"center_x": 0.5})
        salvar_btn.bind(on_release=self.salvar)

        layout.add_widget(self.nome)
        layout.add_widget(self.unidade_btn)
        layout.add_widget(self.preco)
        layout.add_widget(self.qtd_pacote)
        layout.add_widget(salvar_btn)

        self.add_widget(layout)

    def set_unidade(self, unidade):
        self.unidade_selecionada = unidade
        self.unidade_btn.text = f"Unidade: {unidade}"
        self.menu.dismiss()

    def salvar(self, *args):
        nome = self.nome.text.strip()
        unidade = self.unidade_selecionada

        ok_preco, preco = parse_decimal(self.preco.text)
        ok_qtd, qtd = parse_decimal(self.qtd_pacote.text)

        if not nome or not unidade:
            Snackbar(text="Preencha todos os campos!").open()
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
