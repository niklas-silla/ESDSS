import logging
logging.getLogger("docling").setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('faiss').setLevel(logging.WARNING)

from graph.graphbuilder import build_graph
from graph.visualizer import visualize_graph_png
from graph.state import create_initial_state
from pathlib import Path
import csv
import time
from tqdm import tqdm
import json
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    print("========== WORKFLOW STARTED ==========")
    start = time.time() # starting time
    # build main graph
    graph = build_graph()
    visualize_graph_png(graph = graph, filename = "main_graph.png")

    manuscript_folder = Path("data/all_manuscripts")
    all_manuscripts = list(manuscript_folder.glob("*.pdf"))
    # create CSV 
    csv_file = Path("data/results.csv")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["m_id", "deskreject", "final_report", "scopefit_score", "method_score", "innovation_score", "format_score", "quality_score"])  # column headings

    for manuscript_path in tqdm(all_manuscripts):

        # extract manuscript id from filename
        filename = manuscript_path.stem
        parts = filename.split("-")
        m_id = "-".join(parts[:4])

        # create artifact folder 
        artifacts_folder = Path(f"data/{m_id}")
        artifacts_folder.mkdir(parents=True, exist_ok=True)

        # create initial state
        state = create_initial_state(
            original_manuscript_path=str(manuscript_path),
            artifacts_folder=str(artifacts_folder)
        )

        # invoke graph with initial state
        result = graph.invoke(state)
        result["success_logged"] = list(result["success_logged"]) # json suports not "set" only "list"
        result["method_agent"]["data"]["vectorstore"] = None

        json_file = artifacts_folder / "AgentState.json"
        with open(json_file, "w", encoding ="utf-8") as f:
            json.dump(result, f, indent=4)

        # add row in csv file
        print(result)
        with open(csv_file, mode="a", newline="", encoding="utf-8") as f:    # mode a = append
            writer = csv.writer(f)
            writer.writerow([m_id, 
                             result["deskreject"], 
                             result["final_report"], 
                             result["scopefit_agent"]["data"]["score"],
                             result["method_agent"]["data"]["score"], 
                             result["innovation_agent"]["data"]["score"], 
                             result["format_agent"]["data"]["score"], 
                             result["quality_agent"]["data"]["score"], 
                             ])

    print("========== WORKFLOW FINISHED ==========")
    end = time.time()
    runtime = end - start
    hours, rest = divmod(runtime, 3600)
    minutes, seconds = divmod(rest, 60)
    print(f"Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")