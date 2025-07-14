def RerankRRF(result_list,k=60):
    scores_result = {}
    id_to_doc = {}
    for rank,doc in enumerate(result_list,1):#返回的是1,doc
        score = 1 / (rank + k)
        doc_id = f"{doc.metadata['source']}@{doc.metadata['id']}"
        if doc_id in scores_result:
            scores_result[doc_id] = score + scores_result[doc_id]
        else:
            scores_result[doc_id] = score
        id_to_doc[doc_id] = doc
    rerank_doc = sorted(scores_result.items(), key=lambda x: x[1], reverse=True)
    return [id_to_doc[doc_id] for doc_id,_ in rerank_doc]


