class ResearchAgent:

    def build_research_context(
        self,
        retrieved_docs
    ):

        research_sections = []

        for index, item in enumerate(
            retrieved_docs,
            start=1
        ):

            doc = item["document"]

            source = doc.metadata.get(
                "source_document",
                "Unknown"
            )

            content = doc.page_content[:500]

            section = f"""
Research Source {index}

Document:
{source}

Content:
{content}
"""

            research_sections.append(
                section
            )

        return "\n\n".join(
            research_sections
        )