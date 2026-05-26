class ComparerTool:

    def compare(
        self,
        retrieved_docs
    ):

        comparisons = []

        for index, item in enumerate(
            retrieved_docs,
            start=1
        ):

            doc = item["document"]

            comparisons.append(
                f"""
Document {index}:

{doc.page_content[:300]}
"""
            )

        return "\n".join(comparisons)