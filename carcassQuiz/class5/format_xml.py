import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def format_xml(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Prettify and write to the output file
    pretty_xml_as_string = prettify(root)
    
    with open(output_file, "w") as f:
        f.write(pretty_xml_as_string)

if __name__ == "__main__":
    input_file = 'data_zoom.xml'  # 入力ファイルのパス
    output_file = 'formatted_data_zoom.xml'  # 出力ファイルのパス
    format_xml(input_file, output_file)
