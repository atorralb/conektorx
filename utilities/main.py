from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Select, Static

import xml.etree.ElementTree as ET

# Parse XML


class SelectApp(App):

    def compose(self) -> ComposeResult:
        # Load and parse pom.xml
        tree = ET.parse("pom.xml")
        root = tree.getroot()

  # Handle namespaces if any
        ns = {'m': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
        

        def nodetag(elem):
            # Helper to strip namespace from a tag
            return elem.tag.split('}')[-1]

        with Vertical():
            for child in root:
                tag = nodetag(child)
                options = []
                # Add direct child tags (skip empty text nodes etc.)
                for sub in child:
                    subtag = nodetag(sub)
                    options.append((subtag, subtag))
                # Optionally add attributes as options
                for attr_key, attr_val in child.attrib.items():
                    options.append((f"[attr] {attr_key}={attr_val}", attr_key))
                # If child has text and no children
                if not list(child) and (child.text and child.text.strip()):
                    options.append((f"[text] {child.text.strip()}", f"text:{child.text.strip()}"))

                yield Static(f"Node: {tag}")
                if options:
                    yield Select(options, id=f"select-{tag}")
                else:
                    yield Static("No sub-nodes")
# @on(Select.Changed)
    #def select_changed(self, event: Select.Changed) -> None:
     #   self.title = str(event.value)


if __name__ == "__main__":
    app = SelectApp()
    app.run()
