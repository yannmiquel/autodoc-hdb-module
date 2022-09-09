# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:46:36 2022

@author: Yann Miquel
"""

import xml.etree.ElementTree as ET
import collections

def get_description(root:ET.Element):
    """Get the columns description in the semantics"""
    desc = {}
    for parent in root.findall('.//measure/.'):
        for elem in parent.findall(".//descriptions/."):
            desc[parent.get("id")] = elem.get("defaultDescription")
    for parent in root.findall(".//attribute/."):
        for elem in parent.findall(".//descriptions/."):
            desc[parent.get("id")] = elem.get("defaultDescription")
    for parent in root.findall(".//calculatedAttribute/."):
        for elem in parent.findall(".//descriptions/."):
            desc[parent.get("id")] = elem.get("defaultDescription")
    return desc


def get_elements_in_nodes(root:ET.Element):
    """Get for each column created in the nodes the formula and the datatype."""
    elements = collections.defaultdict(dict)
    for node in root.findall('.//calculationView'):
        node_name = node.get("id")
        for parent in node.findall('.//calculatedViewAttribute/.'):
            elements[parent.get("id")]["formule"] = parent.find(".//formula").text
            elements[parent.get("id")]["node_definition"] = node_name
            if parent.get("datatype") in ["DECIMAL"]:
                datatype = (str(parent.get("datatype"))
                            +"("
                            +str(parent.get("length"))
                            +","
                            +str(parent.get("scale"))+")")
            elif parent.get("datatype")=="NVARCHAR":
                datatype = (str(parent.get("datatype"))
                    +"("+str(parent.get("length"))+")")
            else:
                datatype = parent.get("datatype")
            elements[parent.get("id")]["datatype"] = datatype
    return elements

def get_elements_in_final(root:ET.Element):
    """Get for each column created in the final node the formula and the datatype."""
    elements = collections.defaultdict(dict)
    for node in root.findall('.//logicalModel'):
        for att in node.findall(".//calculatedAttribute"):
            elements[att.get("id")]["formule"] = att.find("keyCalculation").find("formula").text
            if att.find("keyCalculation").get("datatype") in ["DECIMAL"]:
                datatype = (str(att.find("keyCalculation").get("datatype"))
                    +"("
                    +str(att.find("keyCalculation").get("length"))
                    +","
                    +str(att.find("keyCalculation").get("scale"))+')')
            elif att.find("keyCalculation").get("datatype") == "NVARCHAR":
                datatype = (str(att.find("keyCalculation").get("datatype"))
                    +"("+str(att.find("keyCalculation").get("length"))+")")
            else:
                datatype = att.find("keyCalculation").get("datatype")
            elements[att.get("id")]["datatype"] = datatype
            elements[att.get("id")]["node_definition"] = "Final node"
        for parent in node.findall('.//measure/.'):
            for elem in parent.findall(".//formula/."):
                elements[parent.get("id")]["formule"] = elem.text
                if parent.get("datatype") in ["DECIMAL"]:
                    datatype = (str(parent.get("datatype"))
                                +"("
                                +str(parent.get("length"))
                                +","
                                +str(parent.get("scale"))+')')
                elif parent.get("datatype") == "NVARCHAR":
                    datatype = (str(parent.get("datatype"))
                        +"("+str(parent.get("length"))+")")
                else:
                    datatype = parent.get("datatype")
                elements[parent.get("id")]["datatype"] = datatype
                elements[parent.get("id")]["node_definition"] = "Final node"
    return elements

def get_elements(root:ET.Element):
    """Concat the elements from all nodes and add the CV name"""
    cv_name = root.get("id")
    elements = collections.defaultdict(dict)
    # Dans les nodes individuels
    elements_in_nodes = get_elements_in_nodes(root)
    # Dans le node final
    elements_in_final = get_elements_in_final(root)
    elements = elements_in_nodes|elements_in_final
    return elements, cv_name

def generate_markdown(elements:dict, cv_name:str, desc:dict, lang="FR"):
    """Generate the markdown"""
    markdown = f"## Calculation view: {cv_name}\n\n"
    match lang:
        case "FR":
            column_name = "Nom du champ "
            no_semantics = "Champs absents de la sémantique"
            dtype = "Type de champ "
            where = "Node de définition "
        case "EN":
            column_name = "Name of the column"
            no_semantics = "Column missing in the semantics"
            dtype = "Datatype"
            where = "Node of definition"
    for champ in sorted(elements.keys()):
        if desc.get(champ):
            markdown += f"""### {desc.get(champ)}\n\n"""
            markdown += f"""* {column_name}: `{champ}`\n\n"""
            markdown += f"""* {dtype}: {elements.get(champ).get("datatype")}\n\n"""
            markdown += f"""* {where}: {elements.get(champ).get("node_definition")}\n\n"""
            markdown += f"""```sql\n{elements.get(champ).get("formule")}\n```"""
            markdown += """\n\n"""

    markdown += f"### {no_semantics}\n\n "
    for champ in sorted(elements.keys()):
        if not desc.get(champ):
            markdown += f"""* {column_name}: `{champ}`\n\n"""
            markdown += f"""* {dtype}: {elements.get(champ).get("datatype")}\n\n"""
            markdown += f"""* {where}: {elements.get(champ).get("node_definition")}\n\n"""
            markdown += f"""```sql\n{elements.get(champ).get("formule")}\n```"""
            markdown += """\n\n"""
    return markdown

def cv_to_markdown(file, lang="FR"):
    """ read the file and return the markdown for this file"""
    tree = ET.parse(file)
    root = tree.getroot()
    elem, cv_name = get_elements(root)
    if not elem:
        return ""
    markdown = generate_markdown(elem,
                                 cv_name,
                                 get_description(root),
                                 lang=lang)
    return markdown
