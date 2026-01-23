from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel

from data.database import Database
from domain.logic import calcular_custo_por_porcao

class CustoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=40,
            size_hint=(0.9, None),
            height=420,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # Seleção de receita
        self.receita_btn = MDRaisedButton(text="Selecionar Receita", pos_hint={"center_x": 0.5})
        self.receita_selecionada = None

        ok_rec, receitas = self.db.list_receitas()
        if not ok_rec:
            receitas = []

        receita_items = [
            {"viewclass": "OneLineListItem", "text": r["nome"], "on_release": lambda x=r: self.set_receita(x)}
            for r in receitas
        ]
        self.menu_receita = MDDropdownMenu(caller=self.receita_btn, items=receita_items, width_mult=4)
        self.receita_btn.bind(on_release=lambda *args: self.menu_receita.open())

        # Botão calcular
        calcular_btn = MDRaisedButton(text="Calcular custo", pos_hint={"center_x": 0.5})
        calcular_btn.bind(on_release=self.calcular)

        # Labels de resultado
        self.result_total = MDLabel(text="Custo total: -", halign="center")
        self.result_porcao = MDLabel(text="Custo por porção: -", halign="center")

        # Voltar ao menu
        voltar_btn = MDRaisedButton(text="Voltar ao Menu", pos_hint={"center_x": 0.5})
        voltar_btn.bind(on_release=lambda *args: setattr(self.manager, "current", "menu"))

        # Montagem
        layout.add_widget(self.receita_btn)
        layout.add_widget(calcular_btn)
        layout.add_widget(self.result_total)
        layout.add_widget(self.result_porcao)
        layout.add_widget(voltar_btn)

        self.add_widget(layout)

    def set_receita(self, receita):
        self.receita_selecionada = receita
        self.receita_btn.text = f"Receita: {receita['nome']}"
        self.menu_receita.dismiss()

    def calcular(self, *args):
        if not self.receita_selecionada:
            toast(text="Selecione uma receita!")
            return

        ok_ing, ingredientes = self.db.list_ingredientes_da_receita(self.receita_selecionada["id"])
        if not ok_ing or not ingredientes:
            toast(text="Nenhum ingrediente vinculado à receita!")
            return

        receita_info = {"rendimento": self.receita_selecionada["rendimento"]}
        ok_calc, resultado = calcular_custo_por_porcao(receita_info, ingredientes)

        if ok_calc:
            self.result_total.text = f"Custo total: R$ {resultado['custo_total']:.2f}"
            self.result_porcao.text = f"Custo por porção: R$ {resultado['custo_por_porcao']:.2f}"
        else:
            toast(text=resultado)
