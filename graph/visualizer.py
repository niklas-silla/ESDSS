import os
from pathlib import Path

def visualize_graph_png(graph, filename):
    """
    Visualizes the given graph and saves it as PNG file.

    Args:
        graph: The graph to visualize.
        filename (str): Name of the output PNG file.
    """

    # Ensure output directory exists
    output_dir = Path("graph_draws")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define the full path for the output file
    path = output_dir / filename
    
    # Generate and save the Mermaid_Diagram
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open(path, "wb") as f:
        f.write(png_bytes)
    print(f"💾 {filename} saved.")
