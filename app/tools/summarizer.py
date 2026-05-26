class SummarizerTool:

    def summarize(
        self,
        retrieved_docs
    ):

        summaries = []

        for item in retrieved_docs:

            doc = item["document"]

            content = doc.page_content[:300]

            summaries.append(content)

        combined_summary = "\n\n".join(
            summaries
        )

        return combined_summary