class QueryRouter:

    def route(
        self,
        query: str
    ):

        query = query.lower()

        # Greeting queries
        greetings = [
            "hi",
            "hello",
            "hey"
        ]

        if any(
            greeting in query
            for greeting in greetings
        ):

            return "direct"

        # Memory-related queries
        memory_keywords = [
            "previous",
            "before",
            "earlier",
            "history"
        ]

        if any(
            keyword in query
            for keyword in memory_keywords
        ):

            return "memory"
        summary_keywords = [
            "summarize",
            "summary"
        ]

        if any(
            keyword in query
            for keyword in summary_keywords
        ):
            return "summarize"
        comparison_keywords = [
            "compare",
            "difference"
        ]

        if any(
            keyword in query
            for keyword in comparison_keywords
        ):

            return "compare"
        
        
        research_keywords = [
            "research",
            "analyze",
            "study"
        ]

        if any(
            keyword in query
            for keyword in research_keywords
        ):

            return "research"

        # Default route
        return "retrieval"