class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 4, score_threshold: float = 1.0):
        results = self.vector_store.similarity_search_with_score(query,k=k)
        filtered_results = []
        for doc, score in results:
            if score <= score_threshold:
                filtered_results.append({
                    "document": doc,
                "score": score
            })
        # Retrieve relevant documents based on the query
        return filtered_results
    