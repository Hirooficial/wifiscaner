import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import subprocess
import threading

class WifiScanner(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = []
        self.running = False
        
    def scan_wifi(self):
        self.running = True
        try:
            output = subprocess.check_output(['su', '-c', 'wpa_cli scan'])
            output = subprocess.check_output(['su', '-c', 'wpa_cli scan_results'])
            self.results = output.decode('utf-8').split('\n')[1:]  # Ignora cabeçalho
            self.update_display()
        except Exception as e:
            self.display_error(str(e))
        finally:
            self.running = False
            
    def display_results(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Resultados da varredura:")
        layout.add_widget(label)
        
        for result in self.results:
            if result.strip():
                layout.add_widget(Label(text=result))
                
        button = Button(text="Voltar")
        button.bind(on_press=self.back_to_main)
        layout.add_widget(button)
        return layout
        
    def back_to_main(self, instance):
        self.clear_widgets()
        self.add_widget(self.create_main_menu())
        
    def create_main_menu(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Scanner de Wi-Fi")
        layout.add_widget(label)
        
        button = Button(text="Varredura de Rede")
        button.bind(on_press=lambda x: threading.Thread(target=self.scan_wifi).start())
        layout.add_widget(button)
        
        return layout

class WifiScannerApp(App):
    def build(self):
        scanner = WifiScanner()
        return scanner.create_main_menu()

if __name__ == '__main__':
    WifiScannerApp().run()