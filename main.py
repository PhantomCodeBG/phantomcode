from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import random
import string

class PhantomObfuscator:
    def generate_phantom_name(self):
        prefixes = ['_', '__', 'p', 'ph', 'gh']
        length = random.randint(3, 8)
        return random.choice(prefixes) + ''.join(random.choices(string.ascii_letters, k=length))

    def encode_to_az(self, data_bytes):
        result = []
        for b in data_bytes:
            first = (b // 16) + 65
            second = (b % 16) + 65
            result.append(chr(first) + chr(second))
        return ''.join(result)

    def simple_obfuscate(self, code):
        encoded = self.encode_to_az(code.encode("utf-8"))

        d = self.generate_phantom_name()
        r = self.generate_phantom_name()
        i = self.generate_phantom_name()
        c = self.generate_phantom_name()
        v = self.generate_phantom_name()

        return f'''-- PhantomCode
local function {d}(s)
    local {r}={{}}
    local {i}=1
    while {i}<=#s do
        local {c}=s:sub({i},{i}+1)
        local {v}=({c}:byte(1)-65)*16+({c}:byte(2)-65)
        {r}[#{r}+1]=string.char({v})
        {i}={i}+2
    end
    return table.concat({r})
end
load({d}("{encoded}"))()
'''

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.input = TextInput(
            text="print('Hello Phantom')",
            size_hint=(1, 0.8)
        )

        self.output = TextInput(
            readonly=True,
            size_hint=(1, 0.8)
        )

        btn = Button(
            text="ОБФУСЦИРОВАТЬ",
            size_hint=(1, 0.2)
        )
        btn.bind(on_press=self.run_obf)

        layout.add_widget(self.input)
        layout.add_widget(btn)
        layout.add_widget(self.output)

        return layout

    def run_obf(self, instance):
        code = self.input.text
        obf = PhantomObfuscator()
        result = obf.simple_obfuscate(code)
        self.output.text = result

if __name__ == "__main__":
    MainApp().run()