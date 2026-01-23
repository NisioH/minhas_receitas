from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem

from data.database import Database
from domain.logic import parse_decimal

class VinculoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40,
                             size_hint=(0.9, None), height=400,
                             pos_hint={"center_x": 0.5, "center_y": 0.5})

        # Seleção de receita
        self.receita_btn = MDRaisedButton(text="Selecionar Receita", pos_hint={"center_x": 0.5})
        self.receita_selecionada = None
        receitas = self.db.list_receitas()[1]
        receita_items = [
            {"viewclass": "OneLineListItem", "text": r["nome"], "on_release": lambda x=r: self.set_receita(x)}
            for r in receitas
        ]
        self.menu_receita = MDDropdownMenu(caller=self.receita_btn, items=receita_items, width_mult=4)
        self.receita_btn.bind(on_release=lambda *args: self.menu_receita.open())

        # Seleção de ingrediente
        self.ingrediente_btn = MDRaisedButton(text="Selecionar Ingrediente", pos_hint={"center_x": 0.5})
        self.ingrediente_selecionado = None
        ingredientes = self.db.list_ingredientes()[1]
        ingrediente_items = [
            {"viewclass": "OneLineListItem", "text": i["nome"], "on_release": lambda x=i: self.set_ingrediente(x)}
            for i in ingredientes
        ]
        self.menu_ingrediente = MDDropdownMenu(caller=self.ingrediente_btn, items=ingrediente_items, width_mult=4)
        self.ingrediente_btn.bind(on_release=lambda *args: self.menu_ingrediente.open())

        self.qtd_usada = MDTextField(hint_text="Quantidade usada", input_filter="float")

        salvar_btn = MDRaisedButton(text="Adicionar", pos_hint={"center_x": 0.5})
        salvar_btn.bind(on_release=self.salvar)

        voltar_btn = MDRaisedButton(text="Voltar ao Menu", pos_hint={"center_x": 0.5})
        voltar_btn.bind(on_release=lambda *args: setattr(self.manager, "current", "menu"))

        layout.add_widget(self.receita_btn)
        layout.add_widget(self.ingrediente_btn)
        layout.add_widget(self.qtd_usada)
        layout.add_widget(salvar_btn)
        layout.add_widget(voltar_btn)

        self.add_widget(layout)

    def set_receita(self, receita):
        self.receita_selecionada = receita
        self.receita_btn.text = f"Receita: {receita['nome']}"
        self.menu_receita.dismiss()

    def set_ingrediente(self, ingrediente):
        self.ingrediente_selecionado = ingrediente
        self.ingrediente_btn.text = f"Ingrediente: {ingrediente['nome']}"
        self.menu_ingrediente.dismiss()

    def salvar(self, *args):
        if not self.receita_selecionada or not self.ingrediente_selecionado:
            toast(text="Selecione receita e ingrediente!")
            return

        ok_qtd, qtd = parse_decimal(self.qtd_usada.text)
        if not ok_qtd or qtd <= 0:
            toast(text="Quantidade inválida!")
            return

        ok, msg = self.db.add_ingrediente_na_receita(
            self.receita_selecionada["id"],
            self.ingrediente_selecionado["id"],
            qtd
        )
        toast(text=msg).open()
