from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

from ui.ingrediente_screen import IngredienteScreen
from ui.receita_screen import ReceitaScreen
from ui.vinculo_screen import VinculoScreen
from ui.custo_screen import CustoScreen


class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40)
        layout.size_hint = (0.8, None)
        layout.height = 400
        layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        btn_ing = MDRaisedButton(text="Cadastro de Ingredientes", pos_hint={"center_x": 0.5})
        btn_ing.bind(on_release=lambda *args: setattr(self.manager, "current", "ingredientes"))

        btn_rec = MDRaisedButton(text="Cadastro de Receitas", pos_hint={"center_x": 0.5})
        btn_rec.bind(on_release=lambda *args: setattr(self.manager, "current", "receitas"))

        btn_vinc = MDRaisedButton(text="Vincular Ingredientes", pos_hint={"center_x": 0.5})
        btn_vinc.bind(on_release=lambda *args: setattr(self.manager, "current", "vinculo"))

        btn_custo = MDRaisedButton(text="Calcular Custo", pos_hint={"center_x": 0.5})
        btn_custo.bind(on_release=lambda *args: setattr(self.manager, "current", "custo"))

        layout.add_widget(btn_ing)
        layout.add_widget(btn_rec)
        layout.add_widget(btn_vinc)
        layout.add_widget(btn_custo)

        self.add_widget(layout)
    
    def toogle_theme(self):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"


class ReceitasApp(MDApp):
    def build(self):
        sm = MDScreenManager()

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(IngredienteScreen(name="ingredientes"))
        sm.add_widget(ReceitaScreen(name="receitas"))
        sm.add_widget(VinculoScreen(name="vinculo"))
        sm.add_widget(CustoScreen(name="custo"))

        sm.current = "menu"

        return sm


if __name__ == "__main__":
    ReceitasApp().run()
