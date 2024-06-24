import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def format_xml(input_file, output_file):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Prettify and write to the output file
        pretty_xml_as_string = prettify(root)
        
        with open(output_file, "w") as f:
            f.write(pretty_xml_as_string)
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")

def check_and_fix_xml(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        fixed_lines = []
        for line in lines:
            # Add any necessary line-by-line fixes here
            fixed_lines.append(line)

        with open(input_file, 'w', encoding='utf-8') as file:
            file.writelines(fixed_lines)

    except Exception as e:
        print(f"Error reading or fixing XML file: {e}")

if __name__ == "__main__":
    input_file = 'data_zoom.xml'  # 入力ファイルのパス
    output_file = 'data_zoom.xml'  # 出力ファイルのパス

    # Check and fix the XML file before parsing
    check_and_fix_xml(input_file)
    format_xml(input_file, output_file)
