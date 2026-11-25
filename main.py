from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# Тёмная тема
Window.clearcolor = get_color_from_hex('#1a1a2e')

class CalcButton(Button):
    """Красивая круглая кнопка с закруглёнными углами"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # прозрачный фон
        self.font_size = dp(24)
        self.bold = True
        self.color = get_color_from_hex('#ffffff')
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self._bg_color = get_color_from_hex('#2d2d44')

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])

    def on_press(self):
        self._bg_color = get_color_from_hex('#4a4a6a')
        self.update_canvas()

    def on_release(self):
        self._bg_color = get_color_from_hex('#2d2d44')
        self.update_canvas()


class CalculatorApp(App):
    def build(self):
        self.title = "Кот-Калькулятор 🐱"
        self.expression = ""

        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        # --- Дисплей ---
        display_box = BoxLayout(size_hint_y=0.25, padding=dp(10))
        with display_box.canvas.before:
            Color(*get_color_from_hex('#16213e'))
            self.display_bg = RoundedRectangle(pos=display_box.pos, size=display_box.size, radius=[dp(25)])
        display_box.bind(pos=self._update_display_bg, size=self._update_display_bg)

        self.display = Label(
            text="0",
            font_size=dp(42),
            bold=True,
            color=get_color_from_hex('#e94560'),
            halign='right',
            valign='middle',
            size_hint=(1, 1)
        )
        self.display.bind(size=self.display.setter('text_size'))
        display_box.add_widget(self.display)
        root.add_widget(display_box)

        # --- Кот-талисман (маленький) ---
        kot = Label(
            text="🐱",
            font_size=dp(28),
            size_hint_y=0.08,
            color=get_color_from_hex('#e94560')
        )
        root.add_widget(kot)

        # --- Сетка кнопок ---
        grid = GridLayout(cols=4, spacing=dp(8), size_hint_y=0.67)

        buttons = [
            ('C', '#e94560'), ('⌫', '#e94560'), ('%', '#533483'), ('÷', '#533483'),
            ('7', '#2d2d44'), ('8', '#2d2d44'), ('9', '#2d2d44'), ('×', '#533483'),
            ('4', '#2d2d44'), ('5', '#2d2d44'), ('6', '#2d2d44'), ('−', '#533483'),
            ('1', '#2d2d44'), ('2', '#2d2d44'), ('3', '#2d2d44'), ('+', '#533483'),
            ('0', '#2d2d44'), ('.', '#2d2d44'), ('=', '#0f9b0f'), ('', '#1a1a2e'),
        ]

        for text, color in buttons:
            if text == '':
                # Пустая ячейка-заглушка
                empty = BoxLayout()
                grid.add_widget(empty)
                continue
            btn = CalcButton(text=text)
            btn._bg_color = get_color_from_hex(color)
            btn.update_canvas()
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)

        root.add_widget(grid)
        return root

    def _update_display_bg(self, instance, value):
        self.display_bg.pos = instance.pos
        self.display_bg.size = instance.size

    def on_button_press(self, instance):
        text = instance.text

        if text == 'C':
            self.expression = ""
            self.display.text = "0"
        elif text == '⌫':
            self.expression = self.expression[:-1]
            self.display.text = self.expression if self.expression else "0"
        elif text == '=':
            try:
                # Заменяем красивые символы на математические
                expr = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                result = eval(expr)
                # Убираем .0 у целых чисел
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.display.text = str(result)
                self.expression = str(result)
            except Exception:
                self.display.text = "Ошибка 😾"
                self.expression = ""
        else:
            self.expression += text
            self.display.text = self.expression


if __name__ == '__main__':
    CalculatorApp().run()