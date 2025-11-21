import xml.etree.ElementTree as ET

def xml_to_dict(element):
    # Converts XML element and its children to a dictionary
    node = {}
    # Add attributes (optional, remove if you do not want attributes)
    #if element.attrib:
    #    node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Add children elements
    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag in node:
            if not isinstance(node[child.tag], list):
                node[child.tag] = [node[child.tag]]
            node[child.tag].append(child_dict)
        else:
            node[child.tag] = child_dict
    # Add text if present and not just whitespace
    text = (element.text or '').strip()
    if text:
        if node:
            node['#text'] = text
        else:
            return text
    return node

def dict_to_yaml(d, indent=0):
    # Serialize the dictionary to a YAML formatted string
    yaml_str = ""
    if isinstance(d, dict):
        for k, v in d.items():
            pre = "  " * indent
            if isinstance(v, (dict, list)):
                yaml_str += f"{pre}{k}:\n{dict_to_yaml(v, indent+1)}"
            else:
                yaml_str += f"{pre}{k}: {v}\n"
    elif isinstance(d, list):
        for item in d:
            pre = "  " * indent
            if isinstance(item, (dict, list)):
                yaml_str += f"{pre}-\n{dict_to_yaml(item, indent+1)}"
            else:
                yaml_str += f"{pre}- {item}\n"
    else:
        pre = "  " * indent
        yaml_str += f"{pre}{d}\n"
    return yaml_str

def convert_xml_file_to_yaml_file(xml_path, yaml_path):
    # Parses XML and writes YAML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    data_dict = {root.tag: xml_to_dict(root)}
    yaml_content = dict_to_yaml(data_dict)
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

# Example usage:
convert_xml_file_to_yaml_file('pom.xml', 'utilities/output.yml')