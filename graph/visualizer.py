import os

def visualize_graph_png(graph, output_dir=".", filename="graph.png"):
    """
    Visualizes the given graph and saves it as PNG file.

    Args:
        graph: The graph to visualize.
        output_dir (str): Directory to save the output file.
        filename (str): Name of the output PNG file.
    """
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the full path for the output file
    path = os.path.join(output_dir, filename)
    
    # Generate and save the Mermaid_Diagram
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open(path, "wb") as f:
        f.write(png_bytes)
    print(f"Graph saved to {path}")

def visualize_graph_terminal(graph):
    """
    Visualizes the given graph in the terminal.

    Args:
        graph: The graph to visualize.
    """
    print(graph.get_graph().draw_ascii())
    