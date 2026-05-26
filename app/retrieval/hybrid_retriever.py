from rank_bm25 import BM25Okapi


class HybridRetriever:

    def __init__(self, vector_store, chunks):

        self.vector_store = vector_store

        self.chunks = chunks

        self.chunk_texts = [
            chunk.page_content
            for chunk in chunks
        ]

        tokenized_chunks = [
            text.split()
            for text in self.chunk_texts
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def retrieve(
        self,
        query: str,
        k: int = 4,
        score_threshold: float = 1.0
    ):

        # Vector Search
        vector_results = self.vector_store.similarity_search_with_score(
            query,
            k=k
        )

        # BM25 Search
        tokenized_query = query.split()

        bm25_scores = self.bm25.get_scores(
            tokenized_query
        )

        # Get top BM25 results
        bm25_top_indices = sorted(
            range(len(bm25_scores)),
            key=lambda i: bm25_scores[i],
            reverse=True
        )[:k]

        hybrid_results = []

        # Add vector results
        for doc, score in vector_results:
            print(score)

            if score <= score_threshold:

                hybrid_results.append({
                    "document": doc,
                    "score": float(score),
                    "retrieval_type": "vector"
                })

        # Add BM25 results
        for idx in bm25_top_indices:

            hybrid_results.append({
                "document": self.chunks[idx],
                "score": float(bm25_scores[idx]),
                "retrieval_type": "bm25"
            })

        return hybrid_results