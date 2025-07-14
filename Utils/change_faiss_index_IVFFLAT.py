from langchain.vectorstores import faiss
import faiss
import math
def change_faiss_index_IVFFLAT(db):
    vectors = db.index.reconstruct_n(0, db.index.ntotal)
    dim = vectors.shape[1]
    quantizer = faiss.IndexFlatIP(dim)
    nlist = max(1,int(math.sqrt(vectors.shape[0])))
    index = faiss.IndexIVFFlat(quantizer, dim, nlist)
    index.train(vectors)
    index.add(vectors)
    db.index = index
    return db