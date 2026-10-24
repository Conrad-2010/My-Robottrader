# POWERED BY LIMO EDGE - OWNER: GONSTE - ANDROID EDITION
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import threading, time, requests, json, os

# --- BOT LOGIC WITHOUT PANDAS (for Android) ---
def get_ema(prices, period):
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return ema

class LimoEdgeApp(App):
    def build(self):
        self.title = "LIMO EDGE - GONSTE"
        self.bot_running = False
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='[b][color=00ffff]⚡ LIMO EDGE ⚡[/color][/b]', markup=True, font_size=22, size_hint_y=None, height=40))
        layout.add_widget(Label(text='OWNER: GONSTE | $10 SURVIVOR', color=[1,1,1,1], font_size=12, size_hint_y=None, height=20))
        
        # Inputs
        self.login = TextInput(hint_text='MT5 Login ID e.g 123456', multiline=False, size_hint_y=None, height=40)
        self.password = TextInput(hint_text='MT5 Password', password=True, multiline=False, size_hint_y=None, height=40)
        self.server = TextInput(hint_text='MT5 Server e.g Exness-MT5Real', multiline=False, size_hint_y=None, height=40)
        self.symbol = TextInput(text='EURUSD', hint_text='Symbol EURUSD or XAUUSD', multiline=False, size_hint_y=None, height=40)
        self.profit = TextInput(text='0.15', hint_text='Close Profit $ 0.15 for $10', multiline=False, size_hint_y=None, height=40)
        
        for w in [self.login, self.password, self.server, self.symbol, self.profit]:
            layout.add_widget(w)
        
        self.status = Label(text='STATUS: WAITING', color=[0,1,0,1], size_hint_y=None, height=30)
        layout.add_widget(self.status)
        
        self.btn = Button(text='SAVE & START BOT', background_color=[0,0.8,1,1], size_hint_y=None, height=50, bold=True)
        self.btn.bind(on_press=self.start_bot_thread)
        layout.add_widget(self.btn)
        
        layout.add_widget(Label(text='Keep app open. Don\'t close screen.\nPowered by Limo Edge', color=[0.5,0.5,0.5,1], font_size=10))
        
        # Load saved
        if os.path.exists("config.json"):
            try:
                with open("config.json","r") as f:
                    d=json.load(f)
                    self.login.text=str(d.get("login",""))
                    self.server.text=str(d.get("server",""))
                    self.symbol.text=str(d.get("symbol","EURUSD"))
                    self.profit.text=str(d.get("profit","0.15"))
            except: pass
        return layout

    def start_bot_thread(self, instance):
        # Save config
        config = {
            "login": self.login.text,
            "password": self.password.text,
            "server": self.server.text,
            "symbol": self.symbol.text,
            "profit": self.profit.text
        }
        with open("config.json","w") as f:
            json.dump(config,f)
        
        if not self.bot_running:
            self.bot_running = True
            self.btn.text = "BOT RUNNING... CLICK TO STOP"
            self.status.text = "BOT STARTED - SCANNING EMA 50/200"
            threading.Thread(target=self.bot_loop, daemon=True).start()
        else:
            self.bot_running = False
            self.btn.text = "SAVE & START BOT"
            self.status.text = "BOT STOPPED"

    def bot_loop(self):
        # NOTE: This is DEMO logic using MetaApi Cloud
        # For real trading you need to connect MetaApi Token
        # I will give you real MetaApi code after you tell me your broker
        while self.bot_running:
            try:
                # Here we will put real MetaApi trading code
                # For now showing scanning status
                Clock.schedule_once(lambda dt: setattr(self.status, 'text', f"SCANNING {self.symbol.text} EMA 50/200..."), 0)
                time.sleep(5)
                Clock.schedule_once(lambda dt: setattr(self.status, 'text', f"WAITING FOR CROSS ON {self.symbol.text}"), 0)
                time.sleep(5)
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.status, 'text', f"ERROR: {e}"), 0)
                time.sleep(5)

LimoEdgeApp().run()
