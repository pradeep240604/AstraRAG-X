from app.graph.workflow import app_graph


queries = [
    "research retrieval augmented generation",
    "summarize transformers",
    "compare rag and transformers",
    "what is faiss"
]


for query in queries:

    result = app_graph.invoke(
        {
            "query": query
        }
    )

    print("\n")
    print("QUERY:", query)
    print("RESULT:", result)