from typing import TypedDict

from langgraph.graph import StateGraph


class GraphState(TypedDict):

    query: str

    route: str

    retrieved_docs: list

    answer: str


def router_node(state):

    query = state["query"].lower()

    if "research" in query:

        return {
            "route": "research"
        }

    if (
        "summary" in query
        or
        "summarize" in query
    ):

        return {
            "route": "summarize"
        }
    if "compare" in query:

        return {
            "route": "compare"
        }

    return {
        "route": "default"
    }


def research_node(state):

    query = state["query"]
    answer = (
        f"Research workflow executed for: {query}"
    )
    return {
        "answer": answer
    }


def summarize_node(state):
    query = state["query"]
    answer = (
        f"Summarization workflow executed for: {query}"
    )

    return {
        "answer": answer
    }


def default_node(state):
    query = state["query"]
    answer = (
        f"RAG workflow executed for: {query}"
    )


    return {
        "answer": answer
    }

def compare_node(state):

    query = state["query"]

    answer = (
        f"Comparison workflow executed for: {query}"
    )

    return {
        "answer": answer
    }



workflow = StateGraph(
    GraphState
)

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "research",
    research_node
)

workflow.add_node(
    "summarize",
    summarize_node
)

workflow.add_node(
    "default",
    default_node
)

workflow.add_node(
    "compare",
    compare_node
)



def route_decision(state):

    route = state["route"]

    if route == "research":

        return "research"

    if route == "summarize":

        return "summarize"

    if route == "compare":

        return "compare"

    return "default"


workflow.set_entry_point(
    "router"
)

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "research": "research",
        "summarize": "summarize",
        "compare": "compare",
        "default": "default"
    }
)

workflow.set_finish_point(
    "research"
)

workflow.set_finish_point(
    "summarize"
)

workflow.set_finish_point(
    "default"
)

workflow.set_finish_point(
    "compare"
)


app_graph = workflow.compile()
