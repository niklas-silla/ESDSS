"""
ESDSS Web UI — FastAPI backend
Start with: uvicorn server:app --reload --port 8000

Extra dependencies (if not yet installed):
    pip install fastapi uvicorn python-multipart
"""
import asyncio
import json
import uuid
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

# Suppress noisy third-party loggers before importing workflow modules
logging.getLogger("docling").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("faiss").setLevel(logging.WARNING)

from dotenv import load_dotenv
load_dotenv()

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title="ESDSS Web API")

DATA_DIR = Path("data")
MANUSCRIPTS_DIR = DATA_DIR / "manuscripts"
MANUSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# One thread-pool worker for blocking LangGraph work
_executor = ThreadPoolExecutor(max_workers=2)

# job_id → {"queue": asyncio.Queue, "loop": running event-loop}
_jobs: dict = {}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_serializable(obj):
    """Recursively convert types that are not JSON-safe to JSON-safe equivalents."""
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, dict):
        return {
            k: ("vectorstore_created" if k == "vectorstore" else _make_serializable(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_make_serializable(i) for i in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    # Fallback: try json round-trip, then str()
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return str(obj)


def _run_workflow(job_id: str, manuscript_path: str, artifacts_folder: str) -> None:
    """Synchronous LangGraph runner — lives in a thread-pool worker."""
    loop  = _jobs[job_id]["loop"]
    queue = _jobs[job_id]["queue"]

    def emit(event: dict) -> None:
        asyncio.run_coroutine_threadsafe(queue.put(event), loop)

    try:
        from graph.graphbuilder import build_graph
        from graph.state import create_initial_state

        graph         = build_graph()
        initial_state = create_initial_state(manuscript_path, artifacts_folder)

        # Accumulate all state updates so we can persist AgentState.json at the end.
        # With stream_mode="updates" each chunk contains only the changed fields,
        # so last-write-wins merging gives us the correct final state for every field.
        accumulated = dict(initial_state)

        emit({"type": "started"})

        for chunk in graph.stream(initial_state, stream_mode="updates"):
            for node_name, state_update in chunk.items():
                # LangGraph can emit None for internal routing nodes — skip them
                if not state_update:
                    continue

                # Merge update into accumulated state (last write wins)
                for key, value in state_update.items():
                    accumulated[key] = value

                emit({
                    "type": "node_update",
                    "node": node_name,
                    "data": _make_serializable(state_update),
                })

        # ── Save AgentState.json (mirrors what main.py does after graph.invoke) ──
        # finished_logged is a set — JSON requires a list
        accumulated["finished_logged"] = list(accumulated.get("finished_logged", set()))
        # vectorstore object is not serialisable — replace with a placeholder string
        method_data = accumulated.get("method_agent", {}).get("data", {})
        if method_data.get("vectorstore") and not isinstance(method_data["vectorstore"], str):
            method_data["vectorstore"] = "vectorstore was created"

        json_path = Path(artifacts_folder) / "AgentState.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(_make_serializable(accumulated), f, ensure_ascii=False, indent=4)

        emit({"type": "complete"})

    except Exception as exc:
        emit({"type": "error", "message": str(exc)})


# ── API routes ─────────────────────────────────────────────────────────────────

@app.post("/api/upload")
async def upload_manuscript(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    dest = MANUSCRIPTS_DIR / file.filename
    dest.write_bytes(await file.read())

    m_id             = Path(file.filename).stem
    artifacts_folder = DATA_DIR / m_id
    artifacts_folder.mkdir(parents=True, exist_ok=True)

    job_id = str(uuid.uuid4())
    loop   = asyncio.get_running_loop()
    _jobs[job_id] = {"queue": asyncio.Queue(), "loop": loop}

    loop.run_in_executor(_executor, _run_workflow, job_id, str(dest), str(artifacts_folder))

    return {"job_id": job_id, "filename": file.filename, "m_id": m_id}


@app.get("/api/stream/{job_id}")
async def stream_progress(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found.")

    queue = _jobs[job_id]["queue"]

    async def _gen():
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=60.0)
                yield f"data: {json.dumps(event)}\n\n"
                if event["type"] in ("complete", "error"):
                    break
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"   # keep the connection alive

    return StreamingResponse(
        _gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/manuscripts")
async def list_manuscripts():
    """Return all previously processed manuscripts (folders with AgentState.json), newest first."""
    results = []
    if DATA_DIR.exists():
        for folder in sorted(DATA_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if not folder.is_dir():
                continue
            state_file = folder / "AgentState.json"
            if not state_file.exists():
                continue
            try:
                with open(state_file, encoding="utf-8") as f:
                    state = json.load(f)
                results.append({
                    "m_id":          folder.name,
                    "deskreject":    state.get("deskreject"),
                    "original_path": state.get("original_manuscript_path", ""),
                })
            except Exception:
                results.append({"m_id": folder.name, "deskreject": None, "original_path": ""})
    return results


@app.get("/api/manuscripts/{m_id:path}")
async def get_manuscript_state(m_id: str):
    """Return the full AgentState.json for a processed manuscript."""
    # Guard against path traversal
    folder = (DATA_DIR / m_id).resolve()
    if not str(folder).startswith(str(DATA_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid manuscript id.")
    state_file = folder / "AgentState.json"
    if not state_file.exists():
        raise HTTPException(status_code=404, detail="Manuscript not found.")
    with open(state_file, encoding="utf-8") as f:
        return json.load(f)


# ── Static file mounts — must be registered after API routes ──────────────────
app.mount("/data", StaticFiles(directory="data"), name="data_files")
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
