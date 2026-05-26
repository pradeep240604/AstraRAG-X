from aiohttp.web_routedef import route
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.ingestion.document_ingestor import DocumentIngestor
from app.chunking.text_chunker import TextChunker
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectorstore.faiss_store import VectorStoreManager

from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import Reranker

from app.llm.groq_client import GroqClient
from app.core.rag_chain import RAGChain

from app.memory.conversation_memory import MemoryManager
from app.agents.query_router import QueryRouter
from app.agents.corrective_agent import CorrectiveAgent
from app.tools.summarizer import SummarizerTool
from app.tools.comparer import ComparerTool
from app.agents.research_agent import ResearchAgent
from fastapi import UploadFile, File


app = FastAPI()

corrective_agent = CorrectiveAgent()

memory_manager = MemoryManager()


@app.get("/")
def home():

    return {
        "message": "AstraRAG Running"
    }

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)

    return {
        "message": (
            f"{file.filename} uploaded successfully"
        )
    }


@app.get("/ask")
def ask_question(query: str):

    router = QueryRouter()

    route = router.route(query)

    print("Selected Route:", route)
    if route == "direct":

        return {
            "query": query,
            "answer": (
                "Hello! I am AstraRAG-X, "
                "your AI research assistant."
            ),
            "sources": []
        }
    if route == "memory":

        chat_history = memory_manager.get_chat_history()

        return {
            "query": query,
            "answer": chat_history,
            "sources": []
        }

    # Load documents
    ingestor = DocumentIngestor("data")

    documents = ingestor.load_documents()

    # Chunking
    chunker = TextChunker()

    chunks = chunker.split_documents(documents)

    # Embeddings
    embedding_generator = EmbeddingGenerator()

    embedding_model = embedding_generator.get_embeddings()

    # Vector Store
    vector_store_manager = VectorStoreManager(
        embedding_model
    )

    vector_store = vector_store_manager.load_vector_store()

    if vector_store is None:

        vector_store = vector_store_manager.create_vector_store(
            chunks
        )

    # Hybrid Retrieval
    retriever = HybridRetriever(
        vector_store=vector_store,
        chunks=chunks
    )

    # Conversation-aware retrieval
    chat_history = memory_manager.get_chat_history()

    enhanced_query = f"""
Conversation History:
{chat_history}

Current Question:
{query}
"""

    retrieved_docs = retriever.retrieve(
        query=enhanced_query,
        k=4,
        score_threshold=100.0
    )

    # Reranking
    reranker = Reranker()

    retrieved_docs = reranker.rerank(
        retrieved_docs
    )

    # Empty retrieval protection
    if not retrieved_docs:

        return {
            "query": query,
            "answer": "No relevant information found in the documents.",
            "sources": []
        }
    

    #toolroutes
    if route == "summarize":

        summarizer = SummarizerTool()

        summary = summarizer.summarize(
            retrieved_docs
        )

        return {
            "query": query,
            "answer": summary,
            "sources": []
        }

    if route == "compare":

        comparer = ComparerTool()

        comparison = comparer.compare(
            retrieved_docs
        )

        return {
            "query": query,
            "answer": comparison,
            "sources": []
        }
    if route == "research":

        research_agent = ResearchAgent()

        research_context = (
            research_agent.build_research_context(
                retrieved_docs
            )
        )

        research_prompt = f"""
    You are an AI research assistant.

    Analyze the following research material
    and generate a structured research report.

    Include:
    - Overview
    - Key Concepts
    - Important Findings
    - Technical Insights
    - Conclusion

    Research Material:

    {research_context}
    """

        groq_client = GroqClient()

        llm = groq_client.get_llm()

        response = llm.invoke(
            research_prompt
        )

        return {
            "query": query,
            "answer": response.content,
            "sources": []
        }

    # LLM
    groq_client = GroqClient()

    llm = groq_client.get_llm()

    # RAG Chain
    rag_chain = RAGChain(
        llm,
        memory_manager
    )

    answer = rag_chain.generate_response(
        query,
        retrieved_docs
    )

    # Sources
    sources = []

    for item in retrieved_docs:

        doc = item["document"]

        score = item["score"]

        sources.append({
            "source_document": doc.metadata.get(
                "source_document",
                "Unknown"
            ),
            "page": doc.metadata.get(
                "page",
                "Unknown"
            ),
            "similarity_score": float(score),
            "content_preview": doc.page_content[:300]
        })

    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }

@app.get("/chat")
def chat(query: str):

    # Load documents
    ingestor = DocumentIngestor("data")

    documents = ingestor.load_documents()

    # Chunking
    chunker = TextChunker()

    chunks = chunker.split_documents(documents)

    # Embeddings
    embedding_generator = EmbeddingGenerator()

    embedding_model = embedding_generator.get_embeddings()

    # Vector Store
    vector_store_manager = VectorStoreManager(
        embedding_model
    )

    vector_store = vector_store_manager.load_vector_store()

    if vector_store is None:

        vector_store = vector_store_manager.create_vector_store(
            chunks
        )

    # Retrieval
    retriever = HybridRetriever(
        vector_store=vector_store,
        chunks=chunks
    )

    retrieved_docs = retriever.retrieve(
        query=query,
        k=4,
        score_threshold=100.0
    )

    reranker = Reranker()

    retrieved_docs = reranker.rerank(
        retrieved_docs
    )

    # LLM
    groq_client = GroqClient()

    llm = groq_client.get_llm()

    rag_chain = RAGChain(
        llm,
        memory_manager
    )

    answer = rag_chain.generate_response(
        query,
        retrieved_docs
    )

    # Sources
    sources = []

    for item in retrieved_docs:

        doc = item["document"]

        sources.append({

            "document": doc.metadata.get(
                "source_document",
                "Unknown"
            ),

            "page": doc.metadata.get(
                "page",
                "Unknown"
            ),

            "preview": doc.page_content[:250]
        })

    return {
        "answer": answer,
        "sources": sources
    }


@app.get("/stream")
def stream_answer(query: str):

    router = QueryRouter()

    route = router.route(query)

    print("Selected Route:", route)
    if route == "direct":

        return {
            "query": query,
            "answer": (
                "Hello! I am AstraRAG-X, "
                "your AI research assistant."
            ),
            "sources": []
        }
    if route == "memory":

        chat_history = memory_manager.get_chat_history()

        return {
            "query": query,
            "answer": chat_history,
            "sources": []
        }

    # Load documents
    ingestor = DocumentIngestor("data")

    documents = ingestor.load_documents()

    # Chunking
    chunker = TextChunker()

    chunks = chunker.split_documents(documents)

    # Embeddings
    embedding_generator = EmbeddingGenerator()

    embedding_model = embedding_generator.get_embeddings()

    # Vector Store
    vector_store_manager = VectorStoreManager(
        embedding_model
    )

    vector_store = vector_store_manager.load_vector_store()

    if vector_store is None:

        vector_store = vector_store_manager.create_vector_store(
            chunks
        )

    # Hybrid Retrieval
    retriever = HybridRetriever(
        vector_store=vector_store,
        chunks=chunks
    )

    # Conversation-aware retrieval
    follow_up_keywords = [
        "it",
        "this",
        "that",
        "they",
        "them",
        "he",
        "she"
    ]

    query_words = query.lower().split()

    is_follow_up = any(
        word in query_words
        for word in follow_up_keywords
    )

    if is_follow_up:

        chat_history = (
            memory_manager.get_chat_history()
        )

        enhanced_query = f"""
    Conversation History:
    {chat_history}

    Current Question:
    {query}
    """

    else:

        enhanced_query = query

    retrieved_docs = retriever.retrieve(
        query=enhanced_query,
        k=4,
        score_threshold=100.0
    )

    # Reranking
    reranker = Reranker()

    retrieved_docs = reranker.rerank(
        retrieved_docs
    )

    # Empty retrieval protection
    if not retrieved_docs:

        corrective_agent = CorrectiveAgent()

        rewritten_query = corrective_agent.rewrite_query(
            query
        )

        print("Rewritten Query:", rewritten_query)

        retrieved_docs = retriever.retrieve(
            query=rewritten_query,
            k=4,
            score_threshold=100.0
        )

        retrieved_docs = reranker.rerank(
            retrieved_docs
        )

        if not retrieved_docs:

            return {
                "query": query,
                "answer": (
                    "I could not find relevant "
                    "information in the documents."
                ),
                "sources": []
            }

    # LLM
    groq_client = GroqClient()

    llm = groq_client.get_llm()

    # RAG Chain
    rag_chain = RAGChain(
        llm,
        memory_manager
    )

    return StreamingResponse(
        rag_chain.stream_response(
            query,
            retrieved_docs
        ),
        media_type="text/plain"
    )


