from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty

# Set window properties
Window.size = (320, 500)
Window.minimum_width = 100
Window.minimum_height = 100

KV = '''
<CalculatorView>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.98, 0.98, 0.98, 1  # Light gray background
        Rectangle:
            pos: self.pos
            size: self.size

    # Title bar
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        spacing: '8dp'
        padding: '8dp'
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Button:
            size_hint_x: None
            width: '40dp'
            text: '≡'
            background_color: 0, 0, 0, 0
            color: 0.2, 0.2, 0.2, 1

        Label:
            text: 'Standard'
            color: 0.2, 0.2, 0.2, 1
            text_size: self.size
            halign: 'left'
            valign: 'center'
            bold: True

        Button:
            size_hint_x: None
            width: '40dp'
            text: '⟲'
            background_color: 0, 0, 0, 0
            color: 0.2, 0.2, 0.2, 1

    # Display
    BoxLayout:
        size_hint_y: None
        height: '120dp'
        padding: '16dp'
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: root.display_text
            font_size: '48sp'
            color: 0, 0, 0, 1
            text_size: self.size
            halign: 'right'
            valign: 'center'
            bold: True

    # Memory buttons
    GridLayout:
        size_hint_y: None
        height: '40dp'
        cols: 6
        padding: '1dp'
        spacing: '1dp'

        Button:
            text: 'MC'
            background_color: 0.98, 0.98, 0.98, 1
            color: 0.3, 0.3, 0.3, 1
            background_normal: ''
        Button:
            text: 'MR'
            background_color: 0.98, 0.98, 0.98, 1
            color: 0.3, 0.3, 0.3, 1
            background_normal: ''
        Button:
            text: 'M+'
            background_color: 0.98, 0.98, 0.98, 1
            color: 0.3, 0.3, 0.3, 1
            background_normal: ''
        Button:
            text: 'M-'
            background_color: 0.98, 0.98, 0.98, 1
            color: 0.3, 0.3, 0.3, 1
            background_normal: ''
        Button:
            text: 'MS'
            background_color: 0.98, 0.98, 0.98, 1
            color: 0.3, 0.3, 0.3, 1
            background_normal: ''
        Button:
            text: 'M▾'
            background_color: 0.98, 0.98, 0.98, 1
            color: 0.3, 0.3, 0.3, 1
            background_normal: ''

    # Calculator buttons
    GridLayout:
        cols: 4
        padding: '1dp'
        spacing: '1dp'

        Button:
            text: '%'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_operation_press('%')
        Button:
            text: 'CE'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_clear_press()
        Button:
            text: 'C'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_clear_press()
        Button:
            text: '⌫'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''

        Button:
            text: '¹/x'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
        Button:
            text: 'x²'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
        Button:
            text: '√x'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
        Button:
            text: '÷'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_operation_press('÷')

        Button:
            text: '7'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(7)
        Button:
            text: '8'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(8)
        Button:
            text: '9'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(9)
        Button:
            text: '×'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_operation_press('×')

        Button:
            text: '4'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(4)
        Button:
            text: '5'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(5)
        Button:
            text: '6'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(6)
        Button:
            text: '-'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_operation_press('-')

        Button:
            text: '1'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(1)
        Button:
            text: '2'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(2)
        Button:
            text: '3'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(3)
        Button:
            text: '+'
            background_color: 0.96, 0.96, 0.96, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_operation_press('+')

        Button:
            text: '+/-'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
        Button:
            text: '0'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
            on_press: root.on_number_press(0)
        Button:
            text: '.'
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            background_normal: ''
        Button:
            text: '='
            background_color: 0.98, 0.45, 0, 1  # Orange color for equals button
            color: 1, 1, 1, 1
            background_normal: ''
            on_press: root.on_equals_press()
'''
class CalculatorLogic:
    def __init__(self):
        self.current_number = '0'
        self.previous_number = None
        self.operation = None
        self.reset_next = False
        
    def add_number(self, number):
        if self.reset_next:
            self.current_number = str(number)
            self.reset_next = False
        else:
            if self.current_number == '0':
                self.current_number = str(number)
            else:
                self.current_number += str(number)
        return self.current_number
        
    def add_operation(self, operation):
        if self.previous_number is None:
            self.previous_number = float(self.current_number)
        else:
            self.calculate()
        self.operation = operation
        self.reset_next = True
        return self.current_number
        
    def calculate(self):
        if self.previous_number is None or self.operation is None:
            return self.current_number
            
        current = float(self.current_number)
        
        if self.operation == '+':
            result = self.previous_number + current
        elif self.operation == '-':
            result = self.previous_number - current
        elif self.operation == '×':
            result = self.previous_number * current
        elif self.operation == '÷':
            if current == 0:
                return 'Error'
            result = self.previous_number / current
            
        self.current_number = str(result)
        self.previous_number = None
        self.operation = None
        return self.current_number
        
    def clear(self):
        self.current_number = '0'
        self.previous_number = None
        self.operation = None
        self.reset_next = False

class CalculatorView(BoxLayout):
    display_text = StringProperty('0')
    memory_visible = BooleanProperty(False)
    history_visible = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calc_logic = CalculatorLogic()
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        # Keyboard mapping
        self.key_mapping = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
            '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'numpad0': 0, 'numpad1': 1, 'numpad2': 2, 'numpad3': 3, 'numpad4': 4,
            'numpad5': 5, 'numpad6': 6, 'numpad7': 7, 'numpad8': 8, 'numpad9': 9,
            'numpadadd': '+', 'numpadsubtract': '-', 
            'numpadmultiply': '×', 'numpaddivide': '÷',
            'plus': '+', 'minus': '-', 'asterisk': '×', 'slash': '÷',
            'enter': '=', 'numpadenter': '=',
            'escape': 'C', 'delete': 'CE',
            'backspace': '⌫', 'period': '.',
            'numpadperiod': '.'
        }
        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key_name = keycode[1]
        if key_name in self.key_mapping:
            mapped_key = self.key_mapping[key_name]
            if isinstance(mapped_key, int):
                self.on_number_press(mapped_key)
            elif mapped_key in ['+', '-', '×', '÷']:
                self.on_operation_press(mapped_key)
            elif mapped_key == '=':
                self.on_equals_press()
            elif mapped_key in ['C', 'CE']:
                self.on_clear_press()
            elif mapped_key == '⌫':
                self.on_backspace_press()
            elif mapped_key == '.':
                self.on_decimal_press()
        return True
        
    def on_number_press(self, number):
        result = self.calc_logic.add_number(number)
        self.update_display(result)
        
    def on_operation_press(self, operation):
        result = self.calc_logic.add_operation(operation)
        self.update_display(result)
        
    def on_equals_press(self):
        result = self.calc_logic.calculate()
        self.update_display(result)
        
    def on_clear_press(self):
        self.calc_logic.clear()
        self.display_text = '0'
        
    def on_backspace_press(self):
        if len(self.calc_logic.current_number) > 1:
            self.calc_logic.current_number = self.calc_logic.current_number[:-1]
        else:
            self.calc_logic.current_number = '0'
        self.update_display(self.calc_logic.current_number)
        
    def on_decimal_press(self):
        if '.' not in self.calc_logic.current_number:
            self.calc_logic.current_number += '.'
            self.update_display(self.calc_logic.current_number)
        
    def update_display(self, value):
        self.display_text = str(value)

class CalculatorApp(App):
    def build(self):
        Builder.load_string(KV)
        return CalculatorView()

if __name__ == '__main__':
    CalculatorApp().run()
