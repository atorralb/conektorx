#class_name : input
from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static
from textual.containers import Vertical
import xml.etree.ElementTree as ET

class InputForm(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Field 1:")
        self.field1 = Input(placeholder="Enter value 1")
        yield self.field1

        yield Static("Field 2:")
        self.field2 = Input(placeholder="Enter value 2")
        yield self.field2

        yield Static("Field 3:")
        self.field3 = Input(placeholder="Enter value 3")
        yield self.field3

        self.save_btn = Button("Save", id="save")
        yield self.save_btn

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            data = {
                "field1": self.field1.value,
                "field2": self.field2.value,
                "field3": self.field3.value
            }
            self.save_to_xml(data)

    def save_to_xml(self, data):
        root = ET.Element("inputs")
        for key, value in data.items():
            child = ET.SubElement(root, key)
            child.text = value
        tree = ET.ElementTree(root)
        tree.write("input_data.xml", encoding="utf-8", xml_declaration=True)

class MyApp(App):
    CSS_PATH = None

    def compose(self):
        yield InputForm()

if __name__ == "__main__":
    app = MyApp()
    app.run()
