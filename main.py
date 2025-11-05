from graph.graphbuilder import build_graph
from graph.visualizer import visualize_graph_png, visualize_graph_terminal
from graph.state import create_initial_state
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    
    graph = build_graph()
    app = graph.compile()

    visualize_graph_png(graph=app)
    # visualize_graph_terminal(graph=app) # dont work with bigger graphs

    # Create initial state
    state = create_initial_state(
        manuscript_path="data/manuscripts/ELMA-D-24-00001-High-Quality development and Resilience of Cross-border E-commerce Enterprises.pdf"
    )
    
    # Invoke the app with the initial state
    result = app.invoke(state)
    print(result)