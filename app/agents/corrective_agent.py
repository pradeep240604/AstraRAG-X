class CorrectiveAgent:

    def rewrite_query(
        self,
        query: str
    ):

        query = query.lower()

        replacements = {
            "it": "retrieval augmented generation",
            "this": "retrieval augmented generation",
            "rag": "retrieval augmented generation"
        }

        words = query.split()

        rewritten_words = []

        for word in words:

            rewritten_words.append(
                replacements.get(word, word)
            )

        rewritten_query = " ".join(
            rewritten_words
        )

        return rewritten_query