import json
from typing import List, Dict, Union
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node_id, text, data=None):
        """Adds a node to the graph."""
        if data is None:
            data = {}
        node = {"id": node_id, "text": text, "data": data}
        self.nodes.append(node)
        return node_id

    def add_edge(self, from_id, to_id):
        """Adds an edge to the graph."""
        self.edges.append({"from": from_id, "to": to_id})


class ParserState:
    def __init__(self):
        self.graph = Graph()


def traverse_json(data, parent_id=None, graph=None):
    """Recursively traverse JSON and build a graph."""
    if isinstance(data, dict):
        for key, value in data.items():
            node_id = f"{parent_id}.{key}" if parent_id else key
            graph.add_node(node_id, key)
            if parent_id:
                graph.add_edge(parent_id, node_id)
            traverse_json(value, node_id, graph)

    elif isinstance(data, list):
        for item in data:
            node_id = f"{parent_id}" if parent_id else "list_item"
            graph.add_node(node_id, "list_item")
            if parent_id:
                graph.add_edge(parent_id, node_id)
            traverse_json(item, node_id, graph)

    else:
        graph.add_node(parent_id, str(data), {"value": data})


def json_parser(json_str):
    """Main function to parse JSON into a graph."""
    try:
        data = json.loads(json_str)
        states = ParserState()

        # Start traversal
        traverse_json(data, parent_id="root", graph=states.graph)

        return states.graph.__dict__

    except Exception as e:
        print("Error parsing JSON:", e)
        return {"nodes": [], "edges": []}


def add_node(node, graph_nodes):
    graph_nodes.append(
        Node(
            id=node['id'],
            label=node['text'],
            size=25,
            color="lightblue",
            shape="box",
            font={"color": "black"},
            borderWidth=2,
            borderRadius=0
        )
    )


def add_edge(edge, graph_edges):
    graph_edges.append(Edge(source=edge.get('from'), target=edge.get('to')))


def get_graph(json_graph):
    """Builds the graph using agraph and Streamlit."""
    nodes_lst, edges_lst = json_graph.get("nodes", []), json_graph.get("edges", [])
    graph_nodes, graph_edges = [], []

    for node in nodes_lst:
        add_node(node, graph_nodes)

    for edge in edges_lst:
        add_edge(edge, graph_edges)

    config = Config(
        width=750,
        height=950,
        directed=True,
        physics=True,
        hierarchical=False,
    )
    
    return agraph(nodes=graph_nodes, edges=graph_edges, config=config)


# Streamlit App
st.title("JSON Graph Visualizer")

# JSON Input
json_data = {
    "name": "John Doe",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zipcode": "10001"
    },
    "contacts": [
        {"type": "email", "value": "john@example.com"},
        {"type": "phone", "value": "+123456789"}
    ],
    "list":[1,2,3,4,5,{'element_six': 'six'}]
}

if st.button("Generate Graph"):
    graph = json_parser(json_data)
    get_graph(graph)
