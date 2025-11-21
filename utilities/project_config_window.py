from textual.app import App, ComposeResult
from textual.widgets import Tree

def read_indent_yaml(filepath):
    # Extremely basic YAML (subset) parser:
    # Understands only dicts/lists with indentation; no quotes, values, etc.
    with open(filepath) as f:
        lines = [line.rstrip('\n') for line in f if line.strip() != ""]
    result = {}
    stack = [(result, -1)]
    for line in lines:
        indent = len(line) - len(line.lstrip(' '))
        content = line.strip()
        node = content.rstrip(':')
        d = None if not content.endswith(':') else {}
        # Find proper parent for current indent
        while indent <= stack[-1][1]:
            stack.pop()
        cur_dict, _ = stack[-1]
        if isinstance(cur_dict, dict):
            if d is not None:
                cur_dict[node] = d
                stack.append((d, indent))
            else:
                cur_dict.setdefault('_files', []).append(node)
        elif isinstance(cur_dict, list):
            if d is not None:
                entry = {node: d}
                cur_dict.append(entry)
                stack.append((d, indent))
            else:
                cur_dict.append(node)
    # Move any '_files' lists to direct lists in parent dicts
    def cleanup(obj):
        if isinstance(obj, dict):
            for k in list(obj.keys()):
                if k == "_files":
                    continue
                obj[k] = cleanup(obj[k])
            if "_files" in obj:
                if len(obj) == 1:
                    return obj["_files"]
        return obj
    return cleanup(result)

def build_tree_widget(parent, subtree):
    if isinstance(subtree, dict):
        for k, v in subtree.items():
            node = parent.add(k)
            build_tree_widget(node, v)
    elif isinstance(subtree, list):
        for item in subtree:
            if isinstance(item, dict):
                build_tree_widget(parent, item)
            else:
                parent.add_leaf(item)
    else:
        parent.add_leaf(str(subtree))

class YamlDirTreeApp(App):
    def compose(self) -> ComposeResult:
        structure = read_indent_yaml("pom.yml")
        # Get the root key (e.g., "root")
        root_key = next(iter(structure))
        tree = Tree(root_key)
        build_tree_widget(tree.root, structure[root_key])
        yield tree

if __name__ == "__main__":
    YamlDirTreeApp().run()