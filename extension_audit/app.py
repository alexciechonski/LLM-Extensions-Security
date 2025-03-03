import streamlit as st
import json
import sys
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

def json_to_tree(json_data, root_name="payload"):
    """Convert a JSON object into a tree structure and return the root TreeNode."""
    
    root = TreeNode(root_name)

    def build_tree(node, data):
        """Recursive function to populate the tree."""
        if isinstance(data, dict):
            for key, value in data.items():
                child_node = TreeNode(key)
                node.add_child(child_node)
                build_tree(child_node, value)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                list_item_node = TreeNode(f"idx{index + 1}") # Numbered nodes for lists
                node.add_child(list_item_node)
                build_tree(list_item_node, item)
        else:
            node.value = data  # Store the primitive value

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

    def add_node(node_id, node):
        """Add a node to the visualization only if it doesn't already exist."""
        node_label = f"{node.name}: {node.value}" if node.value else node.name
        if node.name.startswith("idx") and not node.value:
            font_color = "darkgray" 
        else:
            font_color = "black"
        if node_id not in node_ids:
            nodes.append(
                Node(
                id=node_id,
                    label=node_label,
                    size=25,
                    color="white",
                    shape='box', 
                    font={"color":font_color},
                    borderWidth=2,
                    borderRadius=0 
                    )
                )
            node_ids.add(node_id)

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
            add_node(node_id, node)  # Add current node
            
            if parent_id:
                add_edge(parent_id, node_id)  # Connect to parent
            
            for child in node.children:  # Iterate through children
                queue.append((node_id, child))  # Enqueue child with parent ID

    bfs(root)  # Start BFS traversal

    return nodes, edges

def display_results(fp, tp):
    st.title("Payload Visualizer")

    config = Config(
        width=1000, 
        height=1000, 
        directed=True, 
        physics=True,  # Enable physics but tune settings
        hierarchical=True,
    )

    try:
        json_obj_1 = fp
        json_obj_2 = tp
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")
        
    col1, col2 = st.columns(2)

    st.header("Payload Tree")
    with col1:
        root = json_to_tree(fp)
        nodes, edges = traverse(root)
        agraph(nodes=nodes, 
        edges=edges, 
        config=config)

    with col2:
        root = json_to_tree(tp)
        nodes, edges = traverse(root)
        agraph(nodes=nodes, 
        edges=edges, 
        config=config)

    st.header("Raw Payload")
    with col1:
        st.header("First Parties")
        st.write(json_obj_1)

    with col2:
        st.header("Third Parties")
        st.write(json_obj_2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_data = json.loads(sys.argv[1])  # Decode JSON from argument
        fp, tp = json_data.get("fp", {}), json_data.get("tp", {})
    else:
        fp, tp = {}, {}
    display_results(fp, tp)
