from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class DangerousWritingApp(App):
    def build(self):
        self.idle_threshold = 5  # 5 seconds before text deletion
        self.dim_threshold = 2   # 2 seconds before the screen dims red
        self.idle_event = None
        self.dim_event = None

        # Main layout
        self.layout = BoxLayout(orientation='vertical')

        # Main text editor
        self.text_input = TextInput(multiline=True, font_size=20)
        self.text_input.bind(text=self.reset_timer_and_update_word_count)
        self.layout.add_widget(self.text_input)

        # Word count label
        self.word_count_label = Label(text="Words: 0", size_hint=(1, 0.1))
        self.layout.add_widget(self.word_count_label)

        # Notification label
        self.notification_label = Label(text="", color=(1, 0, 0, 1), size_hint=(1, 0.1))
        self.layout.add_widget(self.notification_label)

        # Start the idle and dim timers
        self.reset_timer_and_update_word_count()

        return self.layout

    def reset_timer_and_update_word_count(self, *args):
        if self.idle_event:
            self.idle_event.cancel()
        if self.dim_event:
            self.dim_event.cancel()

        self.idle_event = Clock.schedule_once(self.clear_text, self.idle_threshold)
        self.dim_event = Clock.schedule_once(self.apply_red_dim, self.dim_threshold)
        self.clear_red_dim()
        self.update_word_count()
        self.notification_label.text = ""

    def clear_text(self, *args):
        self.text_input.text = ""
        self.notification_label.text = "Text deleted due to idling!"
        self.clear_red_dim()

    def apply_red_dim(self, *args):
        Window.clearcolor = get_color_from_hex("#FF6666")  # Light red background

    def clear_red_dim(self):
        Window.clearcolor = get_color_from_hex("#FFFFFF")  # Reset to white background

    def update_word_count(self):
        text = self.text_input.text
        word_count = len(text.split())
        self.word_count_label.text = f"Words: {word_count}"

if __name__ == "__main__":
    DangerousWritingApp().run()
