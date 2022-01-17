from dataclasses import dataclass
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest

from weakness import weakness


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2
        self.tem_data = []
        self.on_start()

        self.display_data1 = (
            Label(text='Input name of tem: ', font_size='5sp'))
        self.add_widget(self.display_data1)

        self.display_data2 = (
            Label(text='Input name of tem: ', font_size='5sp'))
        self.add_widget(self.display_data2)

        self.inputName = TextInput(multiline=False, size_hint=(0.5, 0.4))
        self.inputName.bind(on_text_validate=self.on_enter)
        self.add_widget(self.inputName)

        self.inputName2 = TextInput(multiline=False, size_hint=(0.5, 0.4))
        self.inputName2.bind(on_text_validate=self.on_enter2)
        self.add_widget(self.inputName2)

    def on_start(self, *args):
        req = UrlRequest(
            'https://temtem-api.mael.tech/api/temtems', self.got_json)

    def got_json(self, req, result):
        self.tem_data = [*result]
        # print(self.tem_data[0])

    def on_enter(self, instance):
        temName = self.inputName.text
        multiplicator = self.search_tem(temName)
        multiplicator = [e.split("-") for e in multiplicator]
        self.display_data1.text = temName.title() + "\n\nEffective:\n"
        for e in multiplicator:
            if int(e[0][0]) == 4:
                self.display_data1.text += e[0] + ' ' + e[1] + "\n"
        for e in multiplicator:
            if int(e[0][0]) == 2:
                self.display_data1.text += e[0] + ' ' + e[1] + "\n"
        self.display_data1.text += "\nNot effective:\n"
        for e in multiplicator:
            try:
                if int(e[0][2]) == 5:
                    self.display_data1.text += e[0] + ' ' + e[1] + "\n"
            except:
                pass
        for e in multiplicator:
            try:
                if int(e[0][2]) == 2:
                    self.display_data1.text += e[0] + ' ' + e[1] + "\n"
            except:
                pass

        self.inputName.text = ""

    def on_enter2(self, instance):
        temName = self.inputName2.text
        multiplicator = self.search_tem(temName)
        multiplicator = [e.split("-") for e in multiplicator]
        self.display_data2.text = temName.title() + "\n\nEffective:\n"
        for e in multiplicator:
            if int(e[0][0]) == 4:
                self.display_data2.text += e[0] + ' ' + e[1] + "\n"
        for e in multiplicator:
            if int(e[0][0]) == 2:
                self.display_data2.text += e[0] + ' ' + e[1] + "\n"
        self.display_data2.text += "\nNot effective:\n"
        for e in multiplicator:
            try:
                if int(e[0][2]) == 5:
                    self.display_data2.text += e[0] + ' ' + e[1] + "\n"
            except:
                pass
        for e in multiplicator:
            try:
                if int(e[0][2]) == 2:
                    self.display_data2.text += e[0] + ' ' + e[1] + "\n"
            except:
                pass

        self.inputName2.text = ""

    def search_tem(self, temName):
        search_temtem = temName
        output = []
        for i in range(164):
            if search_temtem.lower() == self.tem_data[i]['name'].lower():
                output_multiplicator = {'neutral': 1, 'wind': 1, 'earth': 1, 'water': 1, 'fire': 1,
                                        'nature': 1, 'electric': 1, 'mental': 1, 'digital': 1, 'melee': 1, 'crystal': 1, 'toxic': 1, }
                temtem_name = self.tem_data[i]['name']
                print('Name: ' + temtem_name)
                temtem_type = self.tem_data[i]['types']
                print('Types: ', end='')
                print(temtem_type)

                for att_type in temtem_type:
                    for def_type in weakness:
                        if att_type.lower() == def_type['type']:
                            for attack in def_type['weaknesses']:
                                output_multiplicator[attack] *= def_type['weaknesses'][attack]
                # print(output_multiplicator)
                print()
                for multp in output_multiplicator:
                    multiplicator = output_multiplicator[multp]
                    if multiplicator == 4 or multiplicator == 2:
                        output.append(str(multiplicator) +
                                      'x-' + multp.title())
                    if multiplicator == 0.5 or multiplicator == 0.25:
                        output.append(str(multiplicator) +
                                      'x-' + multp.title())
        return output


class TestApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    TestApp().run()
