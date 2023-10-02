#import xml.etree.ElementTree as ET
import sys

import lxml.etree as ET


OPERATION_DECLARATIONS = {
    "declare": [
        {
            "name": "name"
        },
        {
            "name": "type"
        },
        {
            "name": "array",
            "default": "False"
        },
        {
            "name": "size",
            "default": ""
        }
    ],
    "assign": [
        {
            "name": "variable"
        },
        {
            "name": "expression"
        }
    ],
    "output": [
        {
            "name": "expression"
        },
        {
            "name": "newline",
            "default": "True"
        }
    ],
    "input": [
        {
            "name": "variable"
        }
    ],
    "if": [
        {
            "name": "expression"
        }
    ],
    "then": [],
    "else": [],
    "fi": [],
    "for": [
        {
            "name": "variable"
        },
        {
            "name": "start"
        },
        {
            "name": "end"
        },
        {
            "name": "direction"
        },
        {
            "name": "step"
        }
    ],
    "endfor": [],
    "while": [
        {
            "name": "expression"
        }
    ],
    "endwhile": []
}

TEMPLATE = """<?xml version="1.0"?>
<flowgorithm fileversion="3.0">
    <attributes>
        <attribute name="name" value=""/>
        <attribute name="authors" value="paolo"/>
        <attribute name="about" value=""/>
        <attribute name="saved" value="2023-09-25 01:41:34 dop."/>
        <attribute name="created" value="cGFvbG87RklaTEk7MjAyMy0wOS0yNTswMTozNzo0MiBkb3AuOzI0MTc="/>
        <attribute name="edited" value="cGFvbG87RklaTEk7MjAyMy0wOS0yNTswMTo0MTozNCBkb3AuOzE7MjUyMQ=="/>
    </attributes>
    <function name="Main" type="None" variable="">
        <parameters/>
        <body>
        </body>
    </function>
</flowgorithm>
"""

infile = sys.argv[1]
outfile = sys.argv[2]



with open(outfile, "w") as f:
    f.write(TEMPLATE)


def parenthesis_split(sentence,separator=" ",lparen="(",rparen=")"):
    nb_brackets=0
    sentence = sentence.strip(separator) # get rid of leading/trailing seps

    l=[0]
    for i,c in enumerate(sentence):
        if c==lparen:
            nb_brackets+=1
        elif c==rparen:
            nb_brackets-=1
        elif c==separator and nb_brackets==0:
            l.append(i)
        # handle malformed string
        if nb_brackets<0:
            raise Exception("Syntax error")

    l.append(len(sentence))
    # handle missing closing parentheses
    if nb_brackets>0:
        raise Exception("Syntax error")


    return([sentence[i:j].strip(separator) for i,j in zip(l,l[1:])])


class Operation:
    def __init__(self, name: str, attributes: list):
        self.name: str = name
        self.attributes = attributes



operations = [Operation(name, [attribute for attribute in attributes]) for name, attributes in OPERATION_DECLARATIONS.items()]
# TODO add syntax check

# line structure: operation attr1, attr2, attr3...
with open(infile) as f:
    user_input = f.readlines()

    tree = ET.parse(outfile)
    root = tree.getroot()

    # TODO specify main function
    body = root.find("function").find("body")
    parent = body

    for line in user_input:
        line = parenthesis_split(line.strip())
         
        operation = line[0]
        if operation.strip() == "":
            continue

        attributes = [e.strip() for e in line[1:]] 

        required_attributes = OPERATION_DECLARATIONS[operation]

        values = {}

        # TODO temp solution for multi-tag operations

        for i, e in enumerate(required_attributes):
            try:
                values.update({required_attributes[i]["name"]: attributes[i]})
            except IndexError:
                values.update({required_attributes[i]["name"]: required_attributes[i]["default"]})
        
        # ops that should not be translated directly
        if operation not in ["fi", "else", "endfor", "endwhile"]:
            new_element = ET.Element(operation, values)
            parent.append(new_element)

        match operation:
            case "if":
                parent = new_element
                
            case "then":
                parent = new_element
                
            case "else":
                parent = parent.getparent()
                new_element = ET.Element("else")
                parent.append(new_element)
                parent = new_element
               
            case "fi":
                parent = parent.getparent().getparent()
                
            case "for":
                parent = new_element

            case "endfor":
                parent = parent.getparent()

            case "while":
                parent = new_element

            case "endwhile":
                parent = parent.getparent()

    tree.write(outfile)
