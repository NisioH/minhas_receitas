from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout

from data.database import Database
from domain.logic import parse_decimal

class ReceitaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40,
                             size_hint=(0.8, None), height=300,
                             pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.nome = MDTextField(hint_text="Nome da receita")
        self.rendimento = MDTextField(hint_text="Rendimento (número de porções)", input_filter="int")

        salvar_btn = MDRaisedButton(text="Salvar", pos_hint={"center_x": 0.5})
        salvar_btn.bind(on_release=self.salvar)

        voltar_btn = MDRaisedButton(text="Voltar ao Menu", pos_hint={"center_x": 0.5})
        voltar_btn.bind(on_release=lambda *args: setattr(self.manager, "current", "menu"))

        layout.add_widget(self.nome)
        layout.add_widget(self.rendimento)
        layout.add_widget(salvar_btn)
        layout.add_widget(voltar_btn)

        self.add_widget(layout)

    def salvar(self, *args):
        nome = self.nome.text.strip()
        rendimento_texto = self.rendimento.text.strip()

        if not nome or not rendimento_texto:
            Snackbar(text="Preencha todos os campos!").open()
            return

        ok_rend, rendimento = parse_decimal(rendimento_texto)
        if not ok_rend or rendimento <= 0:
            Snackbar(text="Rendimento inválido").open()
            return

        ok, msg = self.db.insert_receita(nome, int(rendimento))
        Snackbar(text=msg).open()
