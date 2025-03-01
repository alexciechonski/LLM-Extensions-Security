import json
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from collections import deque

class TreeNode:
    """Class representing a node in the JSON tree."""
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child_node):
        """Add a child to the current node."""
        self.children.append(child_node)

def json_to_tree(json_data, root_name="root"):
    """Convert a JSON object into a tree structure and return the root TreeNode."""
    
    # Create root node
    root = TreeNode(root_name)

    def build_tree(node, data):
        """Recursive function to populate the tree."""
        if isinstance(data, dict):
            for key, value in data.items():
                child_node = TreeNode(key)
                node.add_child(child_node)
                build_tree(child_node, value)  # Recur for nested structures
        elif isinstance(data, list):
            for i, item in enumerate(data):
                child_node = TreeNode(f"Item {i}")
                node.add_child(child_node)
                build_tree(child_node, item)
        else:
            # Leaf node with actual value
            node.value = data

    build_tree(root, json_data)
    return root  # Return the root TreeNode

def traverse(root):
    """Convert a TreeNode structure into nodes and edges for visualization in Streamlit AGraph."""
    nodes = []
    edges = []
    node_ids = set()  # Track existing nodes to prevent duplicates

    def generate_unique_id(parent_id, node_name):
        """Generate a unique ID using the parent ID as a prefix."""
        return f"{parent_id}_{node_name}" if parent_id else node_name

    def add_node(node_id, node_label):
        """Add a node to the visualization only if it doesn't already exist."""
        if node_id not in node_ids:
            nodes.append(Node(id=node_id, label=node_label, size=25, color="lightblue", shape='square'))
            node_ids.add(node_id)  # Mark this ID as used

    def add_edge(parent_id, child_id):
        """Add an edge from parent to child."""
        edges.append(Edge(source=parent_id, target=child_id))

    def bfs(root):
        """Perform BFS traversal to populate nodes and edges."""
        if not root:
            return
        
        queue = deque([(None, root)])  # Queue contains (parent_id, node) tuples
        
        while queue:
            parent_id, node = queue.popleft()  # Dequeue a node
            node_id = generate_unique_id(parent_id, node.name)  # Unique ID for node
            add_node(node_id, node.name)  # Add current node
            
            if parent_id:
                add_edge(parent_id, node_id)  # Connect to parent
            
            for child in node.children:  # Iterate through children
                queue.append((node_id, child))  # Enqueue child with parent ID

    bfs(root)  # Start BFS traversal

    return nodes, edges


# Example usage
if __name__ == "__main__":
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
        ]
    }

    root = json_to_tree(json_data)

    # Generate nodes and edges for visualization
    nodes, edges = traverse(root)

    # Streamlit UI
    st.title("JSON Tree Visualization with AGraph")

    # Render the graph
    config = Config(
                width=1000, 
                height=1000, 
                directed=True, 
                physics=True, 
                hierarchical=True
            )
    agraph(nodes=nodes, 
        edges=edges, 
        config=config)
