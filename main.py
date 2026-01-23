from kivymd.app import MDApp
from ui.ingrediente_screen import IngredienteScreen


class ReceitasApp(MDApp):
    def build(self):
        return IngredienteScreen()

if __name__ == "__main__":
    ReceitasApp().run()