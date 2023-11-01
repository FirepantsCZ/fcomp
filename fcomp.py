#import xml.etree.ElementTree as ET
import sys

import lxml.etree as ET

TYPES = [
    "Integer",
    "Real",
    "String",
    "Boolean"
]

BOOLEANS = [
    "True",
    "False"
]

OPERATION_DECLARATIONS = {
    "declare": [
        {
            "name": "name"
        },
        {
            "name": "type",
            "enum": TYPES
        },
        {
            "name": "array",
            "default": "False",
            "enum": BOOLEANS
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
            "default": "True",
            "enum": BOOLEANS
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
            "name": "direction",
            "default": "inc",
            "enum": ["inc", "dec"]
        },
        {
            "name": "step",
            "default": "1"
        }
    ],
    "endfor": [],
    "while": [
        {
            "name": "expression"
        }
    ],
    "endwhile": [],
    "function": [
        {
            "name": "name"
        },
        {
            "name": "type",
            "default": "None",
            "enum": TYPES + ["None"]
        },
        {
            "name": "variable",
            "default": ""
        }
    ],
    "parameter": [
        {
            "name": "name"
        },
        {
            "name": "type"
        },
        {
            "name": "array",
            "default": "False",
            "enum": BOOLEANS
        }
    ],
    "end": [],
    "call":[
        {
            "name": "expression"
        }
    ]
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


def parenthesis_split(test_str):
    test_str=test_str.replace("(","*(")
    test_str=test_str.replace(")",")*")
    x=test_str.split("*")
    res=[]
    for i in x:
        if i.startswith("(") and i.endswith(")"):
            res.append(i[1:-1])
        else:
            if i != "":
                res.append(i)
    return res


class Operation:
    def __init__(self, name: str, attributes: list):
        self.name: str = name
        self.attributes = attributes



operations = [Operation(name, [attribute for attribute in attributes]) for name, attributes in OPERATION_DECLARATIONS.items()]
# TODO add syntax check

# line structure: operation attr1, attr2, attr3...
with open(infile) as f:
    # TODO declare multiple vars inline
    user_input = f.readlines()
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(outfile,parser)
    root = tree.getroot()

    # TODO specify main function
    main_body = root.find("function").find("body")
    parent = main_body

    tokens = []
    operations = []
    token_number = 0
    line_number = 0
    while line_number <= len(user_input)-1:

        #TODO implement escapig characters
        line = user_input[line_number]
        #token = line.split()


        group = line.strip("\n").split(";")
        for operation in group:
            if operation != "" and not operation.startswith("//"):
                operations.append(operation.strip())

        #tokens = parenthesis_split(line.strip())
        line_number += 1

    for operation in operations:
        #l = parenthesis_split()
        print(operation)
        operation = parenthesis_split(operation)
        instruction = operation[0]
        attributes = [val.strip() for val in "".join(operation[1:]).split(",")]
        print(operation)
        print(instruction)
        print(attributes)
        token = operation[0]

        required_attributes = OPERATION_DECLARATIONS[instruction]

        values = {}

        # TODO temp solution for multi-tag operations

        for i, currentAttribute in enumerate(required_attributes):
            try:
                values.update({currentAttribute["name"]: attributes[i]})
            except IndexError:
                values.update({currentAttribute["name"]: currentAttribute["default"]})

            # if the attribute has enum field, check it
            if "enum" in currentAttribute and values[currentAttribute["name"]] not in currentAttribute["enum"]:
                raise ValueError(f"error on line {line_number}: attribute {currentAttribute['name']} can't have the value {values[currentAttribute['name']]}")
        
        # ops that should not be translated directly
        if instruction not in ["fi", "else", "parameter", "function", "end", "}", ";"]:
            new_element = ET.Element(instruction, values)
            parent.append(new_element)

        match instruction:
            case ";":

                continue

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

            case "end":
                if parent.getparent().tag == "function":
                    parent = main_body

                else:
                    parent = parent.getparent()

            case "while":
                parent = new_element

            case "function":
                new_element = ET.Element(instruction, values)
                new_element.append(ET.Element("parameters"))

                new_body = ET.Element("body")
                new_element.append(new_body)

                root.append(new_element)
                parent = new_body

            case "parameter":
               parent.getparent().xpath("parameters")[0].append(ET.Element(instruction, values))

        token_number += 1

    
    tree.write(outfile, pretty_print=True)
