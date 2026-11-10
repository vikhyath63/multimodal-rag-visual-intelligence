import re
from pathlib import Path
from typing import Any

def terms(s:str)->set[str]: return {x.lower() for x in re.findall(r"\w+",s) if len(x)>2}
def retrieve(query:str,pages:list[dict[str,Any]],limit:int=5)->list[dict[str,Any]]:
    q=terms(query)
    ranked=[]
    for page in pages:
        p=terms(page.get("text",""))
        score=len(q & p)/max(1,len(q))
        if score>0: ranked.append({**page,"score":round(score,3)})
    return sorted(ranked,key=lambda x:x["score"],reverse=True)[:limit]

def ingest_pdf(path:Path,out_dir:Path)->list[dict]:
    import fitz
    out_dir.mkdir(parents=True,exist_ok=True)
    doc=fitz.open(path); pages=[]
    for i,page in enumerate(doc):
        image_path=out_dir/f"page-{i+1}.png"
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(image_path)
        pages.append({"page":i+1,"text":page.get_text("text"),"image_path":str(image_path)})
    return pages
