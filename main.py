from graph.builder import build_graph
from graph.visualizer import visualize_graph_png, visualize_graph_terminal

if __name__ == "__main__":
    graph = build_graph()
    app = graph.compile()

    # visualize_graph_png(graph=app)
    visualize_graph_terminal(graph=app)

    result = app.invoke({})
    print(result)