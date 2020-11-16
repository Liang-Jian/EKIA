
import xml.etree.ElementTree as etree
import json


class JSONConnector:
    def __init__(self,filepath):
        self.data = dict()
        with open(filepath,mode='r',encoding='utf-8') as f:
            self.data = json.load(f)
    @property
    def parsed_data(self):
        return self.data


class XMLConnect:
    def __init__(self,filepath):
        self.tree = etree.parse(filepath)
    @property
    def parsed_data(self):
        return self.tree

class VMConnect:
    def __init__(self,filepath):
        self.data  = ""
        with open(filepath,mode='r',encoding='utf-8') as f:
            self.data  = f.read()
    @property
    def parsed_data(self):
        return self.data
def connection_factory(filepath):
    if filepath.endswith('.json'):
        connector = JSONConnector
    elif filepath.endswith('.xml'):
        connector = XMLConnect
    elif filepath.endswith('.vm'):
        connector = VMConnect
    else :
        raise("unSupported file style")
    return connector(filepath)

def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as e:
        print(e)
    return  factory


# def main():
#     # sqlite_factory = connect_to('data/persqn.sq3')
#     print()
#     xml_factory = connect_to('data/person.xml')
#     xml_data = xml_factory.parsed_data
#     print(xml_data)
#
#
#     json_factory = connect_to('data/dount.json')
#     json_data = json_factory.parsed_data
#     print('found {}'.format(json_data))
#     for donut in json_data:
#         print("name {}".format(donut['name']))


