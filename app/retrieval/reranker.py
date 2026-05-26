class Reranker:

    def rerank(self, retrieved_docs):

        # Remove duplicates
        unique_docs = []

        seen_contents = set()

        for item in retrieved_docs:

            content = item["document"].page_content

            if content not in seen_contents:

                seen_contents.add(content)

                unique_docs.append(item)

        # Sort results
        reranked_docs = sorted(
            unique_docs,
            key=lambda x: x["score"]
        )

        return reranked_docs[:4]