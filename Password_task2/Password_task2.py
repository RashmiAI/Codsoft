from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import ListProperty
import random
import string
from kivy.core.clipboard import Clipboard

# Set window size
Window.size = (400, 600)

class HoverButton(Button):
    def on_enter(self, *args):
        # Create bouncing animation sequence
        anim = (Animation(size_hint=(1.1, 0.9), duration=0.1) + 
                Animation(size_hint=(0.95, 1.05), duration=0.1) +
                Animation(size_hint=(1.02, 0.98), duration=0.1) +
                Animation(size_hint=(1, 1), duration=0.1))
        anim.start(self)

    def on_leave(self, *args):
        # Cancel any running animation and reset to normal size
        Animation.cancel_all(self)
        anim = Animation(size_hint=(1, 1), duration=0.1)
        anim.start(self)

KV = '''
#:import utils kivy.utils

<HoverButton>:
    size_hint: 1, 1
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]

<PasswordGenerator>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 1, 1  # Light blue-white background
        Rectangle:
            pos: self.pos
            size: self.size
    
    padding: dp(20)
    spacing: dp(15)

    Label:
        text: 'Password Generator'
        font_size: '42sp'
        size_hint_y: None
        height: dp(50)
        color: 0, 0, 0.3  # blue color
        bold: True
        font: 'Arial-BoldMT'

    Label:
        text: 'Choose a password length:'
        font_size: '20sp'
        size_hint_y: None
        height: dp(30)
        color: 0.1, 0, 0  # black color
        bold: True

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)
        spacing: dp(10)

        HoverButton:
            text: '4'
            on_press: root.set_password_length(4)
            background_color: (0, 0.5, 1, 1)  # Blue color for all number buttons
            color: 1, 1, 1, 1

        HoverButton:
            text: '6'
            on_press: root.set_password_length(6)
            background_color: (0, 0.5, 1, 1)
            color: 1, 1, 1, 1

        HoverButton:
            text: '8'
            on_press: root.set_password_length(8)
            background_color: (0, 0.5, 1, 1)
            color: 1, 1, 1, 1

        HoverButton:
            text: '10'
            on_press: root.set_password_length(10)
            background_color: (0, 0.5, 1, 1)
            color: 1, 1, 1, 1

        HoverButton:
            text: '12'
            on_press: root.set_password_length(12)
            background_color: (0, 0.5, 1, 1)
            color: 1, 1, 1, 1

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        CheckBox:
            id: uppercase_check
            active: False
            size_hint_x: None
            width: dp(40)
            color: 0, 0.5, 1, 1  # Blue color
        Label:
            text: 'Include Uppercase Letters'
            color: 0, 0, 0, 1  # Black color for better visibility
            text_size: self.size
            halign: 'left'
            valign: 'center'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        CheckBox:
            id: lowercase_check
            active: True
            size_hint_x: None
            width: dp(40)
            color: 0, 0.5, 1, 1  # Blue color
        Label:
            text: 'Include Lowercase Letters'
            color: 0, 0, 0, 1
            text_size: self.size
            halign: 'left'
            valign: 'center'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        CheckBox:
            id: numbers_check
            active: True
            size_hint_x: None
            width: dp(40)
            color: 0, 0.5, 1, 1  # Blue color
        Label:
            text: 'Include Numbers'
            color: 0, 0, 0, 1
            text_size: self.size
            halign: 'left'
            valign: 'center'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        CheckBox:
            id: special_check
            active: False
            size_hint_x: None
            width: dp(40)
            color: 0, 0.5, 1, 1  # Blue color
        Label:
            text: 'Include Special Characters'
            color: 0, 0, 0, 1
            text_size: self.size
            halign: 'left'
            valign: 'center'

    Widget:
        size_hint_y: None
        height: dp(20)

    HoverButton:
        text: 'Generate Password'
        size_hint_y: None
        height: dp(50)
        background_color: 1, 0, 0.1  # Red color
        color: 1, 1, 1, 1  # White text
        on_press: root.generate_password()

    TextInput:
        id: password_output
        readonly: True
        size_hint_y: None
        height: dp(50)
        background_color: 1, 1, 1, 1  # White background
        foreground_color: 0, 0.8, 0, 1  # Green text
        multiline: False
        font_size: '20sp'
        padding: [10, 10]

    HoverButton:
        text: 'Copy to Clipboard'
        size_hint_y: None
        height: dp(50)
        background_color: 0.5, 0, 1, 1  # Purple color
        color: 1, 1, 1, 1  # White text
        on_press: root.copy_to_clipboard()

    Widget:
        size_hint_y: 1  # Takes remaining space
'''

class PasswordGenerator(BoxLayout):
    password_length = 8  # Default password length

    def set_password_length(self, length):
        self.password_length = length

    def generate_password(self):
        # Create character pool based on selections
        chars = ''
        if self.ids.uppercase_check.active:
            chars += string.ascii_uppercase
        if self.ids.lowercase_check.active:
            chars += string.ascii_lowercase
        if self.ids.numbers_check.active:
            chars += string.digits
        if self.ids.special_check.active:
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'

        # Ensure at least one option is selected
        if not chars:
            self.ids.password_output.text = 'Select at least one option'
            return

        # Generate password with selected length
        password = ''.join(random.choice(chars) for _ in range(self.password_length))
        self.ids.password_output.text = password

    def copy_to_clipboard(self):
        if self.ids.password_output.text and self.ids.password_output.text != 'Select at least one option':
            Clipboard.copy(self.ids.password_output.text)

class PasswordGeneratorApp(App):
    def build(self):
        Builder.load_string(KV)
        return PasswordGenerator()

if __name__ == '__main__':
    PasswordGeneratorApp().run()