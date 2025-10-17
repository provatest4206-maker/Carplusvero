# main.py - CarPlus Manager (Kivy)
# NOTE: This file is based on the user's provided code and intended for building.
import os, sqlite3, json, traceback
from datetime import datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

DB_PATH = os.path.join(os.path.expanduser("~"), "carplus.db")
Window.clearcolor = (0.99,0.98,0.995,1)

def ensure_db_and_columns():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute(\"\"\"CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, qty REAL DEFAULT 0, unit_price REAL DEFAULT 0, threshold REAL DEFAULT 0)\"\"\")
    c.execute(\"\"\"CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, client TEXT, address TEXT, datetime TEXT, service TEXT, price REAL DEFAULT 0, consumption TEXT DEFAULT '')\"\"\")
    conn.commit(); conn.close()

class Dashboard(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=8, spacing=8)
        root.add_widget(Label(text='CarPlus Manager', font_size='22sp'))
        root.add_widget(Button(text='Vai a Inventario', size_hint_y=None, height=44, on_release=lambda *a: self.manager.current='inventory'))
        self.add_widget(root)

class Inventory(Screen):
    def on_pre_enter(self):
        self.clear_widgets(); self.add_widget(Label(text='Inventory'))

class Appointments(Screen):
    def on_pre_enter(self):
        self.clear_widgets(); self.add_widget(Label(text='Appointments'))

class Stats(Screen):
    def on_pre_enter(self):
        self.clear_widgets(); self.add_widget(Label(text='Stats'))

class Backup(Screen):
    def on_pre_enter(self):
        self.clear_widgets(); self.add_widget(Label(text='Backup'))

class RootManager(ScreenManager):
    pass

class CarPlusApp(App):
    def build(self):
        ensure_db_and_columns()
        rm = RootManager(transition=SlideTransition(duration=0.18))
        rm.add_widget(Dashboard(name='dashboard'))
        rm.add_widget(Inventory(name='inventory'))
        rm.add_widget(Appointments(name='appointments'))
        rm.add_widget(Stats(name='stats'))
        rm.add_widget(Backup(name='backup'))
        rm.current = 'dashboard'
        return rm

if __name__ == '__main__':
    try:
        CarPlusApp().run()
    except Exception as e:
        print('Run error:', e)