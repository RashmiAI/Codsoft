import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle

# Define the KV string for custom widgets with hover effects
Builder.load_string('''
<HoverButton>:
    canvas.before:
        PushMatrix
        Scale:
            origin: self.center
            x: self.scale
            y: self.scale
    canvas.after:
        PopMatrix
    background_color: self.normal_color if not self.hovered else self.hover_color
    
<AnimatedLabel>:
    canvas.before:
        PushMatrix
        Scale:
            origin: self.center
            x: self.scale
            y: self.scale
    canvas.after:
        PopMatrix
''')

class HoverButton(Button):
    scale = NumericProperty(1)
    hovered = BooleanProperty(False)
    normal_color = get_color_from_hex('#F10000')  # green
    hover_color = get_color_from_hex('#6F236F')  # purple 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self._on_mouse_pos)
        self.background_normal = ''
        self.background_color = self.normal_color

    def _on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        rel_pos = self.to_widget(*pos)
        inside = self.collide_point(*rel_pos)
        
        if inside != self.hovered:
            self.hovered = inside
            if inside:
                Animation(scale=1.1, duration=0.1, transition='out_bounce').start(self)
            else:
                Animation(scale=1.0, duration=0.1).start(self)

class AnimatedLabel(Label):
    scale = NumericProperty(1)

class RockPaperScissors(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add gradient-like background
        with self.canvas.before:
            # First gradient color
            Color(rgba=get_color_from_hex('#A8DADC'))  # Light cyan
            self.bg1 = Rectangle(pos=self.pos, size=self.size)
            # Second gradient color
            Color(rgba=get_color_from_hex('#457B9D'))  # Blue-gray
            self.bg2 = Rectangle(pos=self.pos, size=(self.size[0], self.size[1] * 0.5))
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.player_score = 0
        self.computer_score = 0
        self.buttons = {}
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Header layout for title and reset button
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.2,
            spacing=10
        )
        
        self.title = AnimatedLabel(
            text='Rock Paper Scissors',
            font_size='48sp',
            color=get_color_from_hex('#1D3557'),  # Dark navy blue
            bold=True,
            size_hint_x=0.8
        )
        self.animate_title()
        
        # Reset button in header
        reset_button = HoverButton(
            text='Reset',
            size_hint=(0.2, 0.8),
            pos_hint={'center_y': 0.5},
            font_size='18sp',
            bold=True,
            background_color=get_color_from_hex('#EF476F')  # Bright red
        )   
        reset_button.bind(on_release=self.reset_game)
        
        header_layout.add_widget(self.title)
        header_layout.add_widget(reset_button)
        main_layout.add_widget(header_layout)
        
        keyboard_instructions = AnimatedLabel(
            text='Press R for Rock, P for Paper, S for Scissors',
            font_size='16sp',
            size_hint_y=0.1,
            color=get_color_from_hex('#000000')  # White
        )
        main_layout.add_widget(keyboard_instructions)
        
        self.score_label = AnimatedLabel(
            text='Player: 0 - Computer: 0',
            font_size='24sp',
            size_hint_y=0.1,
            color=get_color_from_hex('#08782a')  # Off-white
        )
        main_layout.add_widget(self.score_label)
        
        self.result_label = AnimatedLabel(
            text='Choose your move!',
            font_size='20sp',
            size_hint_y=0.2,
            color=get_color_from_hex('#FFFFFF')  # White
        )
        main_layout.add_widget(self.result_label)
        
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint_y=0.3,
            padding=[20, 10]
        )
        
        choices = [('Rock', 'R'), ('Paper', 'P'), ('Scissors', 'S')]
        for choice, key in choices:
            btn = HoverButton(
                text=f'{choice} ({key})',
                font_size='20sp',
                bold=True
            )
            btn.bind(on_release=lambda x, c=choice: self.make_choice(c))
            self.buttons[key.lower()] = btn
            button_layout.add_widget(btn)
        
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
        
        self.animate_entrance()

    def _update_rect(self, instance, value):
        self.bg1.pos = instance.pos
        self.bg1.size = instance.size
        self.bg2.pos = instance.pos
        self.bg2.size = (instance.size[0], instance.size[1] * 0.5)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1].lower()
        if key in ['r', 'p', 's']:
            choice_map = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}
            choice = choice_map[key]
            btn = self.buttons[key]
            Animation(scale=0.9, duration=0.1).start(btn)
            Clock.schedule_once(lambda dt: Animation(scale=1, duration=0.1).start(btn), 0.1)
            self.make_choice(choice)
        elif key == 'enter':
            if hasattr(self, 'popup') and self.popup:
                self.popup.dismiss()
                self.reset_game()
        elif key == 'escape':
            self.reset_game()
        return True

    def animate_entrance(self):
        for child in self.children:
            child.pos_hint = {'center_x': 0.5, 'center_y': 1.5}
            anim = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, 
                           duration=0.5,
                           transition='out_bounce')
            anim.start(child)

    def animate_title(self):
        anim = Animation(scale=1.1, duration=1) + Animation(scale=1, duration=1)
        anim.repeat = True
        anim.start(self.title)

    def make_choice(self, player_choice):
        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices)
        result = self.get_winner(player_choice, computer_choice)
        
        self.result_label.opacity = 0
        self.result_label.scale = 0.5
        
        if result == 'win':
            self.player_score += 1
            result_text = f'You chose {player_choice}, Computer chose {computer_choice}.\nYou win!'
            self.result_label.color = get_color_from_hex('#08782a')  # Vivid green
        elif result == 'lose':
            self.computer_score += 1
            result_text = f'You chose {player_choice}, Computer chose {computer_choice}.\nComputer wins!'
            self.result_label.color = get_color_from_hex('#f50505')  # Bright red
        else:
            result_text = f'You chose {player_choice}, Computer chose {computer_choice}.\nIt\'s a tie!'
            self.result_label.color = get_color_from_hex('#fafaf5')  # Soft yellow
        
        self.result_label.text = result_text
        anim = Animation(opacity=1, scale=1, duration=0.3, transition='out_bounce')
        anim.start(self.result_label)
        
        self.score_label.text = f'Player: {self.player_score} - Computer: {self.computer_score}'
        score_anim = Animation(scale=1.2, duration=0.1) + Animation(scale=1, duration=0.1)
        score_anim.start(self.score_label)
        
        if self.player_score == 5 or self.computer_score == 5:
            Clock.schedule_once(lambda dt: self.game_over(), 0.5)
    
    def get_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return 'tie'
        winning_combinations = {
            'Rock': 'Scissors',
            'Paper': 'Rock',
            'Scissors': 'Paper'
        }
        return 'win' if winning_combinations[player_choice] == computer_choice else 'lose'
    
    def game_over(self):
        winner = 'Player' if self.player_score == 5 else 'Computer'
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        message = AnimatedLabel(
            text=f'{winner} wins the game!',
            font_size='24sp',
            color=get_color_from_hex('#FFFFFF'),
            bold=True
        )
        
        restart_button = HoverButton(
            text='Play Again',
            size_hint=(1, 0.5),
            font_size='20sp',
            bold=True
        )
        
        content.add_widget(message)
        content.add_widget(restart_button)
        
        self.popup = Popup(
            title='Game Over',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            title_color=get_color_from_hex('#FFFFFF'),
            title_size='24sp',
            separator_color=get_color_from_hex('#2A9D8F'),  # Teal
            background_color=get_color_from_hex('#457B9D')  # Blue-gray
        )
        
        self.popup.opacity = 0
        self.popup.scale = 0.5
        
        def show_popup(dt):
            self.popup.open()
            anim = Animation(opacity=1, scale=1, duration=0.3, transition='out_bounce')
            anim.start(self.popup)
        
        def restart_game(instance):
            anim = Animation(opacity=0, scale=0.5, duration=0.2)
            anim.bind(on_complete=lambda *args: self.popup.dismiss())
            anim.start(self.popup)
            self.reset_game()
        
        restart_button.bind(on_release=restart_game)
        Clock.schedule_once(show_popup, 0.1)

    def reset_game(self, *args):
        self.player_score = 0
        self.computer_score = 0
        self.score_label.text = 'Player: 0'
        self.score_label.text1 = 'Computer: 0'
        self.result_label.text = 'Choose your move!'
        self.result_label.color = get_color_from_hex('#FFFFFF')
        self.result_label.color = get_color_from_hex('#000000')
        self.animate_entrance()

class RockPaperScissorsApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#A8DADC')  # Light cyan
        return RockPaperScissors()

if __name__ == '__main__':
    RockPaperScissorsApp().run()
