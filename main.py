import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
from datetime import datetime

Window.softinput_mode = "below_target"

KV_INTERFACE = """
<TaxiCalculator>:
    orientation: 'vertical'
    padding: 15
    spacing: 12
    canvas.before:
        Color:
            rgba: 0.03, 0.03, 0.03, 1
        Rectangle:
            pos: self.pos
            size: self.size

    TextInput:
        id: input_origen
        hint_text: "ORIGEN"
        multiline: False
        size_hint_y: None
        height: 120
        font_size: 45
        background_color: (0.2, 0.2, 0.2, 1)
        foreground_color: (1, 1, 1, 1)
        input_type: 'text'

    TextInput:
        id: input_destino
        hint_text: "DESTINO"
        multiline: False
        size_hint_y: None
        height: 120
        font_size: 45
        background_color: (0.2, 0.2, 0.2, 1)
        foreground_color: (1, 1, 1, 1)
        input_type: 'text'

    BoxLayout:
        size_hint_y: None
        height: 110
        spacing: 15
        Spinner:
            id: selector_tarifa
            text: "T1 (Predet.)"
            values: ["T1 (Predet.)", "T2 (Promo)"]
            font_size: 40
            background_color: (0.6, 0.4, 0.2, 1)
        Spinner:
            id: selector_unidad
            text: "KM"
            values: ["KM", "Cuadras"]
            font_size: 40
            background_color: (0.6, 0.4, 0.2, 1)

    BoxLayout:
        size_hint_y: None
        height: 140
        spacing: 10
        Button:
            text: "CALCULAR"
            font_size: 42
            bold: True
            background_color: (0, 0.7, 0, 1)
            on_press: root.calcular_y_reportar()
        Button:
            text: "CONVERTIR T"
            font_size: 38
            bold: True
            background_color: (0.8, 0.5, 0, 1)
            on_press: root.convertir_tarifa()
        Button:
            text: "GPS"
            size_hint_x: 0.5
            font_size: 38
            background_color: (0.2, 0.4, 0.7, 1)
            on_press: root.abrir_mapa()

    TextInput:
        id: input_distancia
        hint_text: "DISTANCIA"
        input_filter: 'float'
        font_size: 55
        size_hint_y: None
        height: 110
        input_type: 'number'
        halign: 'center'

    RelativeLayout:
        Label:
            markup: True
            text: root.reporte_final
            font_size: root.tamanio_letra_dinamico
            halign: 'center'
            valign: 'top'
            text_size: self.width * 0.85, None
            pos_hint: {'center_x': 0.5, 'top': 1}
        
        Button:
            text: "LIMPIAR"
            size_hint_y: None
            height: 120
            pos_hint: {'center_x': 0.5, 'y': 0}
            background_color: (0.7, 0, 0, 1)
            font_size: 35
            bold: True
            on_press: root.limpiar_todo()
"""

TARIFAS = {
    "T1 (Predet.)": {"bajada": 2752.00, "ficha": 116.00},
    "T2 (Promo)": {"bajada": 2148.00, "ficha": 101.00}
}

class TaxiCalculator(BoxLayout):
    reporte_final = StringProperty("ESPERANDO DATOS...")
    tamanio_letra_dinamico = NumericProperty(45)

    def limpiar_todo(self):
        self.ids.input_origen.text = ""
        self.ids.input_destino.text = ""
        self.ids.input_distancia.text = ""
        self.tamanio_letra_dinamico = 45
        self.reporte_final = "LISTO"

    def abrir_mapa(self):
        o = self.ids.input_origen.text.replace(" ", "+")
        d = self.ids.input_destino.text.replace(" ", "+")
        if o and d:
            url = f"https://www.google.com/maps/dir/{o}+Rosario/{d}+Rosario/"
            webbrowser.open(url)

    def calcular_y_reportar(self):
        try:
            self.tamanio_letra_dinamico = 38 
            val = float(self.ids.input_distancia.text)
            dist_m = val * 130 if self.ids.selector_unidad.text == "Cuadras" else val * 1000
            t_data = TARIFAS[self.ids.selector_tarifa.text]
            fichas = int(dist_m / 100)
            total = t_data["bajada"] + (fichas * t_data["ficha"])
            cabify45 = total * 0.55
            ahora = datetime.now().strftime("%H:%M")

            self.reporte_final = f"""[b]TICKET {self.ids.selector_tarifa.text.split(' ')[0]}[/b]
{ahora} hs | {val} {self.ids.selector_unidad.text}
[color=555555]--------------------------[/color]
[b]TOTAL: [color=00FF00]${total:,.2f}[/color][/b]
[color=555555]--------------------------[/color]
Bajada: ${t_data['bajada']:.0f} | Ficha: ${t_data['ficha']:.0f}
O: {self.ids.input_origen.text}
D: {self.ids.input_destino.text}
[color=555555]--------------------------[/color]
[b]CABI 45%: [color=00FFFF]${cabify45:,.2f}[/color][/b]"""
        except:
            self.reporte_final = "⚠️ ERROR"

    def convertir_tarifa(self):
        try:
            self.tamanio_letra_dinamico = 36
            val = float(self.ids.input_distancia.text)
            dist_m = val * 130 if self.ids.selector_unidad.text == "Cuadras" else val * 1000
            fichas = int(dist_m / 100)
            res = {nombre: data["bajada"] + (fichas * data["ficha"]) for nombre, data in TARIFAS.items()}

            self.reporte_final = f"""[b][color=FFCC00]COMPARATIVA DE TARIFAS[/color][/b]
Distancia: {val} {self.ids.selector_unidad.text}
[color=555555]--------------------------[/color]
[b]T1 (Predet): [color=00FF00]${res['T1 (Predet.)']:,.2f}[/color][/b]
[b]T2 (Promo):  [color=00FF00]${res['T2 (Promo)']:,.2f}[/color][/b]
[color=555555]--------------------------[/color]
Diferencia: ${abs(res['T1 (Predet.)']-res['T2 (Promo)']):,.2f}"""
        except:
            self.reporte_final = "⚠️ Ingrese distancia"

class TaxiApp(App):
    def build(self):
        Builder.load_string(KV_INTERFACE)
        return TaxiCalculator()

if __name__ == '__main__':
    TaxiApp().run()