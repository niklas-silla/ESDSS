import logging
logging.getLogger("docling").setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('faiss').setLevel(logging.WARNING)
from dotenv import load_dotenv
load_dotenv()

from graph.graphbuilder import build_graph
from graph.visualizer import visualize_graph_png
from graph.state import create_initial_state
from pathlib import Path
import csv
from datetime import datetime
from tqdm import tqdm
import json

# for progress tracking
PROGRESS_FILE = "data/processing_progress.json"
MANUSCRIPT_FOLDER = Path("data/all_manuscripts")

def extract_sort_id(path: Path) -> int:
    parts = path.stem.split("-")
    if len(parts) >= 4:
        return int(parts[3])   # 00003 → 3
    return 99999999 # fallback -> last processed


def main():
    print("========== PROCESSING STARTED ==========")
    start = datetime.now() # starting time
    # build main graph
    graph = build_graph()
    visualize_graph_png(graph = graph, filename = "main_graph.png")

    all_manuscripts = sorted(
        MANUSCRIPT_FOLDER.glob("*.pdf"),
        key=extract_sort_id # sort order function as key -> no ()
    )
    # create CSV 
    csv_file = Path("data/results.csv")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["m_id", "deskreject", "final_report", "scopefit_score", "method_score", "innovation_score", "format_score", "quality_score"])  # column headings

    # load progress file or create empty set if file is empty
    try:
        with open(PROGRESS_FILE, 'r') as f:
            processed = set(json.load(f).get('processed', []))
        print(f"Bereits verarbeitet: {len(processed)} Dateien")
    except Exception as e:
        processed = set()

    for index, manuscript_path in enumerate(tqdm(all_manuscripts), start=1):
        # extract manuscript id from filename
        parts = manuscript_path.stem.split("-")
        m_id = "-".join(parts[:4])

        if m_id in processed:
            print(f"Überspringe (bereits verarbeitet): {m_id}")
            continue

        print(f"=== WORKFLOW {index} STARTED ===")
        print(f"m_id: {m_id}")

        try:
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

            # save AgentState in JSON file
            json_file = artifacts_folder / "AgentState.json"
            with open(json_file, "w", encoding ="utf-8") as f:
                json.dump(result, f, indent=4)

            # add row in csv file
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
            
            # mark as processed
            processed.add(m_id)
            with open(PROGRESS_FILE, 'w') as f:
                json.dump({
                    'processed': list(processed),
                }, f, indent=2) # indent for better readability
            print(f"=== WORKFLOW {index} FINISHED ===")
        
        except Exception as e:
            print(f"=== WORKFLOW {index} STOPPED ===")
            print(e)


    print("========== PROCESSING FINISHED ==========")
    runtime = datetime.now() - start
    print(f"Runtime: {str(runtime).split('.')[0]}")


if __name__ == "__main__":
    main()