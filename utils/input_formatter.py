import xml.etree.ElementTree as ET
import json


def preprocess_xml_or_json(input_data: str) -> dict:
    if input_data.startswith("<"):
        return convert_xml_to_dict(input_data)
    else:
        return json.loads(input_data)


def convert_xml_to_dict(xml_string) -> dict:
    xml = ET.fromstring(xml_string)
    return xml_to_dict(xml)


def xml_to_dict(xml) -> dict:
    result = {}
    for node in xml:
        if node.tag in result:
            if type(result[node.tag]) is list:
                result[node.tag].append(xml_to_dict(node))
            else:
                result[node.tag] = [result[node.tag], xml_to_dict(node)]
        else:
            result[node.tag] = xml_to_dict(node) if node else node.text
    return result
