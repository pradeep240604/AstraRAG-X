from langchain.memory import ConversationBufferMemory


class MemoryManager:

    def __init__(self):

        self.memory = ConversationBufferMemory(
            return_messages=True
        )

    def save_context(
        self,
        question,
        answer
    ):

        self.memory.save_context(
            {"input": question},
            {"output": answer}
        )

    def load_memory(self):

        return self.memory.load_memory_variables(
            {}
        )
    def get_chat_history(self):

        memory_variables = self.memory.load_memory_variables(
            {}
        )

        return memory_variables.get(
            "history",
            ""
        )