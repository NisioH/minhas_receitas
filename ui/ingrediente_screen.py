from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout

from data.database import Database
from domain.logic import parse_decimal, validar_unidade

class IngredienteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40,
                             size_hint=(0.8, None), height=450,
                             pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.nome = MDTextField(hint_text="Nome do ingrediente")
        self.unidade = MDTextField(hint_text="Unidade (ml/g/und)")
        self.preco = MDTextField(hint_text="Preço do pacote (ex: 6,50)")
        self.qtd_pacote = MDTextField(hint_text="Quantidade do pacote (ex: 1000)")

        salvar_btn = MDRaisedButton(text="Salvar", pos_hint={"center_x": 0.5})
        salvar_btn.bind(on_release=self.salvar)

        voltar_btn = MDRaisedButton(text="Voltar ao Menu", pos_hint={"center_x": 0.5})
        voltar_btn.bind(on_release=lambda *args: setattr(self.manager, "current", "menu"))

        layout.add_widget(self.nome)
        layout.add_widget(self.unidade)
        layout.add_widget(self.preco)
        layout.add_widget(self.qtd_pacote)
        layout.add_widget(salvar_btn)
        layout.add_widget(voltar_btn)

        self.add_widget(layout)

    def salvar(self, *args):
        nome = self.nome.text.strip()
        unidade = self.unidade.text.strip()
        ok_preco, preco = parse_decimal(self.preco.text)
        ok_qtd, qtd = parse_decimal(self.qtd_pacote.text)

        if not nome or not unidade:
            toast(text="Preencha todos os campos!")
            return
        if not validar_unidade(unidade):
            toast(text="Unidade inválida (ml/g/und)")
            return
        if not ok_preco or not ok_qtd:
            toast(text="Preço ou quantidade inválidos")
            return

        ok, msg = self.db.insert_ingrediente(nome, unidade, preco, qtd)
        toast(msg)

        if ok:
            self.nome.text = ""
            self.unidade.text = ""
            self.preco.text = ""
            self.qtd_pacote.text = ""
