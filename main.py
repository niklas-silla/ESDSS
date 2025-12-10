import logging
logging.getLogger("docling").setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('faiss').setLevel(logging.WARNING)
from dotenv import load_dotenv
load_dotenv()

from graph.graphbuilder import build_graph
from graph.visualizer import visualize_graph_png
from graph.state import create_initial_state
from evaluation_csv_builder import create_evaluation_csv, prepare_csv_row, save_row_in_csv
from pathlib import Path
from datetime import datetime
import time
from tqdm import tqdm
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

# for progress tracking
PROGRESS_FILE = "data/processing_progress.json"
MANUSCRIPT_FOLDER = Path("data/all_manuscripts")

# for evaluation
CSV_FILE = Path("data/results.csv")

def extract_sort_id(path: Path) -> int:
    parts = path.stem.split("-")
    if len(parts) >= 4:
        return int(parts[3])   # 00003 → 3
    return 99999999 # fallback -> last processed


def process_single_manuscript(args):
    """
    Processing single manuscript.
    This function runs in a separate process.
    """
    manuscript_path, index = args
    # graph must be recreated in each process
    graph = build_graph()
    # extract manuscript id from filename
    parts = manuscript_path.stem.split("-")
    m_id = "-".join(parts[:4])

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
        start_graph = time.perf_counter()
        result_state = graph.invoke(state)
        end_graph = time.perf_counter()

        # preprocess result_state for saving
        result_state["total_duration"] = end_graph - start_graph
        result_state["finished_logged"] = list(result_state["finished_logged"]) # json suports not "set" only "list"
        result_state["method_agent"]["data"]["vectorstore"] = "vectorstore was created"

        # save AgentState in JSON file
        json_file = artifacts_folder / "AgentState.json"
        with open(json_file, "w", encoding ="utf-8") as f:
            json.dump(result_state, f, ensure_ascii=False, indent=4)

        # prepare CSV-row
        csv_row = prepare_csv_row(m_id, result_state)

        print(f"=== WORKFLOW {index} FINISHED ===")
        return {"status": "success", "m_id": m_id, "csv_row": csv_row}
    
    except Exception as e:
        return {"status": "error", "m_id": m_id, "error": str(e)}



def main():
    print("========== PROCESSING STARTED ==========")
    start = datetime.now() # starting time

    # build main graph
    graph = build_graph()
    #visualize_graph_png(graph = graph, filename = "main_graph.png")

    all_manuscripts = sorted(
        MANUSCRIPT_FOLDER.glob("*.pdf"),
        key=extract_sort_id # sort order function as key -> no ()
    )

    # create CSV if it doesn't exists
    if not CSV_FILE.exists():
        create_evaluation_csv(CSV_FILE)
        
    # load progress file or create empty set if file is empty
    try:
        with open(PROGRESS_FILE, 'r') as f:
            progress_data = json.load(f)
            processed = set(progress_data.get("processed", []))
            failed = set(progress_data.get("failed", []))
        print(f"Bereits verarbeitet: {len(processed)} Dateien")
    except Exception as e:
        processed = set()
        failed = set()

    # filter allready processed manuscripts
    manuscripts_to_process = []
    for index, manuscript_path in enumerate(all_manuscripts, start=1):
        # extract manuscript id from filename
        parts = manuscript_path.stem.split("-")
        m_id = "-".join(parts[:4])
        
        if m_id in processed:
            print(f"Skip (already processed): {m_id}")
            continue
        
        manuscripts_to_process.append((manuscript_path, index))
    
    print(f"To process: {len(manuscripts_to_process)} files")
    
    if not manuscripts_to_process:
        print("No new files to process.")
        return

    # Parallel processing
    max_workers = min(os.cpu_count(), 1)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit alle Tasks
        futures = {executor.submit(process_single_manuscript, args): args 
                  for args in manuscripts_to_process}

        # Process results as soon as they are ready
        for future in tqdm(as_completed(futures), total=len(manuscripts_to_process), 
                          desc="Processed Manuscripts"):
            result = future.result()
            m_id = result["m_id"]
            if result["status"] == "success":
                csv_row = result["csv_row"]
                
                # Write in CSV (thread-safe through sequential writing)
                save_row_in_csv(CSV_FILE, csv_row)
                
                # mark as processed
                processed.add(m_id)

            else:
                error = result["error"]
                # markt as failed
                failed.add(f"{m_id}: {error}")
                print(f"💥 Error at {m_id}: {error}")
            
            # write in progress file
            with open(PROGRESS_FILE, 'w') as f:
                    json.dump({'processed': list(processed), 'failed': list(failed)}, f, indent=2) # indent for better readability



    print("========== PROCESSING FINISHED ==========")
    runtime = datetime.now() - start
    print(f"Runtime: {str(runtime).split('.')[0]}")


if __name__ == "__main__":
    main()