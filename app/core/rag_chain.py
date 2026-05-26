from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage


class RAGChain:

    def __init__(self, llm, memory):

        self.llm = llm

        self.memory = memory

    def generate_response(
        self,
        query,
        retrieved_docs
    ):

        compressed_contexts = []

        for item in retrieved_docs:

            content = item["document"].page_content

            compressed_content = content[:1200]

            compressed_contexts.append(
                compressed_content
            )

        context = "\n\n".join(
            compressed_contexts
        )

        print("Context Length:", len(context))

        memory_variables = self.memory.load_memory()

        chat_history = memory_variables.get(
            "history",
            ""
        )

        prompt = f"""
You are AstraRAG-X, an advanced AI research assistant.

Provide detailed, clear, and well-structured answers
using the retrieved context.

Guidelines:
- Explain concepts thoroughly.
- Use multiple paragraphs when needed.
- Include technical insights if relevant.
- Keep answers natural and professional.
- Do not mention retrieval process,
  conversation history,
  or missing context unless absolutely necessary.

Retrieved Context:
{context}

User Question:
{query}
"""

        response = self.llm.invoke(
            prompt,
            config={
                "callbacks": [
                    StreamingStdOutCallbackHandler()
                ]
            }
        )

        self.memory.save_context(
            query,
            response.content
        )

        return response.content

    def stream_response(
        self,
        query,
        retrieved_docs
    ):

        compressed_contexts = []

        for item in retrieved_docs:

            content = item["document"].page_content

            compressed_content = content[:1200]

            compressed_contexts.append(
                compressed_content
            )

        context = "\n\n".join(
            compressed_contexts
        )

        memory_variables = self.memory.load_memory()

        chat_history = memory_variables.get(
            "history",
            ""
        )

        prompt = f"""
You are AstraRAG-X, an advanced AI research assistant.

Provide detailed, clear, and well-structured answers
using the retrieved context.

Guidelines:
- Explain concepts thoroughly.
- Use multiple paragraphs when needed.
- Include technical insights if relevant.
- Keep answers natural and professional.
- Do not mention retrieval process,
  conversation history,
  or missing context unless absolutely necessary.

Retrieved Context:
{context}

User Question:
{query}
"""

        full_response = ""

        for chunk in self.llm.stream(
            [HumanMessage(content=prompt)]
        ):

            if chunk.content:

                full_response += chunk.content

                yield chunk.content

        self.memory.save_context(
            query,
            full_response
        )
    