from kivy.app import App
from kivy.uix.label import Label

from interfaces.inicial import Inicial

class CluedoApp(App):
    def build(self):
        return Inicial()


CluedoApp().run()