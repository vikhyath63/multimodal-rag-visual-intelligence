from app.retrieval import retrieve
def test_retrieves_matching_page():
    hits=retrieve("revenue growth", [{"page":1,"text":"Revenue growth improved","image_path":"p1.png"},{"page":2,"text":"Hiring plan","image_path":"p2.png"}])
    assert hits[0]["page"]==1
