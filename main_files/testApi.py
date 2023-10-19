import requests
import xml.etree.ElementTree as ET
from main_files.errorCalls import returnResponse


def get_domains():
    with open("domains.txt") as f:
        return [line.strip() for line in f]


def make_api_call(domain, years, api_key):
    url = f"https://www.namesilo.com/apibatch/registerDomainDrop?version=1&type=xml&key={api_key}&domain={domain}&years={years}&private=1"
    response = requests.get(url).content.decode('utf-8')
    root = ET.fromstring(response)
    tree = ET.ElementTree(root)
    return tree


def read_xml_file(parse_tree):
    tree = ET.parse(parse_tree)
    root = tree.getroot()

    for child in root:
        for grandchild in child:
            if grandchild.tag == "code":
                return int(grandchild.text)


def print_detail_xml():
    tree = ET.parse('response.xml')
    root = tree.getroot()
    for child in root:
        for grandchild in child:
            if grandchild.tag == "detail":
                print(grandchild.text)


def final_response(years, api_key):
    domains = get_domains()

    for domain in domains:
        while True:
            tree = make_api_call(domain, years, api_key)
            response_code = read_xml_file(tree)
            response_statement = returnResponse(response_code)
            if response_statement in [210, 254, 261, 264, 265]:
                print_detail_xml()
            elif response_statement == 300:
                print_detail_xml()
                break
            elif response_statement == 301:
                print_detail_xml()
                break
            elif response_statement == 302:
                print_detail_xml()
                break
            else:
                print(response_statement)
        print("\n\nJumping to next Domain...IF EXITS!...\n\n")
