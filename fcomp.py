import xml.etree.ElementTree as ET
import sys

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




class Operation:
    def __init__(self, name: str, attributes: list):
        self.name: str = name
        self.attributes = attributes



operations = [Operation(name, [attribute for attribute in attributes]) for name, attributes in OPERATION_DECLARATIONS.items()]
print(operations)
# TODO add syntax check

# line structure: operation attr1, attr2, attr3...
with open(infile) as f:
    user_input = f.readlines()

    tree = ET.parse(outfile)
    root = tree.getroot()

    # TODO specify main function
    body = root.find("function").find("body")

    for line in user_input:
        print(line)
        line = line.split(" ")
        operation = line[0]
        if operation.strip() == "":
            continue

        attributes = [e.strip() for e in line[1:]]

        print(operation)
        print(attributes)

        required_attributes = OPERATION_DECLARATIONS[operation]
        print(required_attributes)

        values = {}

        for i, e in enumerate(required_attributes):
            try:
                values.update({required_attributes[i]["name"]: attributes[i]})
            except IndexError:
                values.update({required_attributes[i]["name"]: required_attributes[i]["default"]})

        print(values)

        body.append(ET.Element(operation, values))

    tree.write(outfile)


        
