import json
from typing import List, Dict, Union
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
from collections import deque

class TreeNode:
    def __init__(self, value, children=None) -> None:
        self.val = value if isinstance(value, list) else [value]
        self.children = children if children else []

    def add_value(self, new):
        self.val.append(new)

    def add_child(self, child):
        self.children.append(child)

def json_parser(json_data):
    """
    Parses JSON data into a TreeNode structure following the given rules.
    """
    root = TreeNode([], [])

    def build_tree(node, data):
        for key, val in data.items():
            if isinstance(val, dict):
                # Create an intermediate node for the nested dictionary
                intermediate = TreeNode([key], [])
                node.add_child(intermediate)
                working_node = TreeNode([],[])
                intermediate.add_child(working_node)
                build_tree(working_node, val) 
            elif isinstance(val, list):
                intermediate = TreeNode([key], [])
                node.add_child(intermediate)
                for element in val:
                    if isinstance(element, dict):
                        dict_obj = [', '.join([f"{key}: {val}" for key, val in element.items()])]   
                        intermediate.add_child(TreeNode(dict_obj, []))
                    else:                   
                        intermediate.add_child(TreeNode([element], []))
            else:
                node.add_value(f"{key}: {val}")
    build_tree(root, json_data)
    return root

def process_table_text(val):
    if len(val) == 1:
        return str(val[0])
    return '\n'.join(val)

def get_graph(root):
    nodes, edges = [], []
    id = 0
    if not root:
        return
    
    queue = deque([(None, root)])  # Queue contains (parent_id, node) tuples

    while queue:
        parent_id, node = queue.popleft()
        nodes.append(Node(id, label=process_table_text(node.val), shape='box'))
        edges.append(Edge(parent_id, id))

        for child in node.children:
            queue.append([id, child])
        id += 1

    config = Config(
            width=750,
            height=950,
            directed=True, 
            physics=True, 
            hierarchical=False,
            # **kwargs
            )
    return agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
    


# Streamlit App
st.title("JSON Graph Visualizer")

# JSON Input
json_data = {
    "name": "John Doe",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zipcode": {
            "place": "Poland",
            "miasto": "WWA"
        }
    },
    "contacts": [
        {"type": "email", "value": "john@example.com"},
        {"type": "phone", "value": "+123456789"}
    ],
    "list": [1, 2, 3, 4, 5, {'element_six': 'six'}]
}

graph = json_parser(json_data)
get_graph(graph)