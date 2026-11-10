from pathlib import Path
import json, uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from app.retrieval import ingest_pdf,retrieve
app=FastAPI(title="Multimodal RAG Visual Intelligence",version="0.1.0")
DATA=Path("data"); DATA.mkdir(exist_ok=True); INDEX=DATA/"index.json"
def load(): return json.loads(INDEX.read_text()) if INDEX.exists() else []
def save(rows): INDEX.write_text(json.dumps(rows,indent=2))
class Query(BaseModel): question:str=Field(min_length=1); top_k:int=Field(default=5,ge=1,le=20)
@app.get("/health")
def health(): return {"status":"ok","indexed_pages":len(load())}
@app.post("/ingest")
async def ingest(file:UploadFile=File(...)):
    if not file.filename.lower().endswith(".pdf"): raise HTTPException(400,"Only PDF files are supported")
    name=f"{uuid.uuid4().hex}.pdf"; path=DATA/name; path.write_bytes(await file.read())
    try: rows=ingest_pdf(path,DATA/name.replace(".pdf",""))
    except Exception as exc: path.unlink(missing_ok=True); raise HTTPException(400,f"Could not parse PDF: {exc}") from exc
    index=load(); index.extend(rows); save(index)
    return {"document":name,"pages_added":len(rows),"pages":rows}
@app.post("/query")
def query(req:Query):
    hits=retrieve(req.question,load(),req.top_k)
    return {"question":req.question,"results":hits,"note":"Lexical baseline retrieval. Page images are returned as visual evidence; no vision model has interpreted them yet."}
